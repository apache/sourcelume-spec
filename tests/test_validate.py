#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pyshacl import validate as shacl_validate
from rdflib import RDF, Graph, URIRef

# Add tools directory to path so we can import validate
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate  # noqa: E402


class ValidateToolTests(unittest.TestCase):
    def test_load_validator_returns_validator(self) -> None:
        """Test that load_validator successfully creates a validator."""
        validator = validate.load_validator()
        self.assertIsNotNone(validator)

    def test_validate_example_with_valid_record(self) -> None:
        """Test that a valid ProvenanceRecord passes validation."""
        with tempfile.TemporaryDirectory() as tmp:
            example_path = Path(tmp) / "valid.jsonld"

            # Create a minimal valid ProvenanceRecord with the canonical context IRI
            valid_record = {
                "@context": validate.CANONICAL_CONTEXT_IRI,
                "id": "https://example.org/records/test",
                "type": "ProvenanceRecord",
                "identifier": "https://example.org/datasets/test",
                "name": "Test Dataset",
                "license": "https://creativecommons.org/publicdomain/zero/1.0/",
                "creator": [
                    {
                        "type": "schema:Organization",
                        "name": "Test Org",
                        "role": "originator"
                    }
                ],
                "created": "2024-01-01T00:00:00Z",
                "added": "2024-01-01T00:00:00Z",
                "contentCreated": "2024-01-01T00:00:00Z",
                "origin": "https://example.org/source",
                "custodyChain": [
                    {
                        "agent": "https://example.org/agents/test-org",
                        "action": "created",
                        "startTime": "2024-01-01T00:00:00Z"
                    }
                ]
            }

            example_path.write_text(json.dumps(valid_record, indent=2), encoding="utf-8")

            validator = validate.load_validator()
            shapes_path = validate.SCHEMA_DIR / "sourcelume.shacl.ttl"

            # The expanded graph must carry the ProvenanceRecord type, otherwise the
            # SHACL shapes have no focus node and the run below would pass vacuously.
            context = json.loads((REPO_ROOT / "context" / "0.0.1" / "sourcelume.jsonld").read_text())["@context"]
            graph = Graph()
            graph.parse(data=json.dumps({**valid_record, "@context": context}), format="json-ld")
            expected = URIRef("https://sourcelume.apache.org/ns#ProvenanceRecord")
            self.assertIn((URIRef(valid_record["id"]), RDF.type, expected), graph)

            # This should return True for a valid record
            result = validate.validate_example(example_path, validator, shapes_path)
            self.assertTrue(result)

    def test_missing_context_is_required(self) -> None:
        """A record without @context fails: other processors cannot expand it."""
        record = self._record_with_content_period("2024-01-01T00:00:00Z", None)
        del record["@context"]
        errors = list(validate.load_validator().iter_errors(record))
        self.assertEqual([e.message for e in errors], ["'@context' is a required property"])

    def test_schema_pins_the_canonical_context_iri(self) -> None:
        """The schema's @context const and the validator's constant must agree."""
        schema = validate.load_validator().schema
        self.assertEqual(schema["properties"]["@context"]["const"], validate.CANONICAL_CONTEXT_IRI)

    def test_inline_context_is_rejected(self) -> None:
        """An inline @context object is not accepted, only the canonical IRI."""
        validator = validate.load_validator()
        context = json.loads((REPO_ROOT / "context" / "0.0.1" / "sourcelume.jsonld").read_text())
        record = {"@context": context["@context"], "id": "https://example.org/records/test", "type": "ProvenanceRecord"}
        errors = [e for e in validator.iter_errors(record) if list(e.path) == ["@context"]]
        self.assertEqual(len(errors), 1)

    def test_foreign_context_iri_is_rejected(self) -> None:
        """A context IRI on another host is rejected, even if the path looks the same."""
        validator = validate.load_validator()
        record = {
            "@context": "https://example.org/context/0.0.1/sourcelume.jsonld",
            "id": "https://example.org/records/test",
            "type": "ProvenanceRecord",
        }
        errors = [e for e in validator.iter_errors(record) if list(e.path) == ["@context"]]
        self.assertEqual(len(errors), 1)

    def _record_with_content_period(self, start: str, end: str | None) -> dict:
        record = {
            "@context": validate.CANONICAL_CONTEXT_IRI,
            "id": "https://example.org/records/test",
            "type": "ProvenanceRecord",
            "identifier": "https://example.org/datasets/test",
            "name": "Test Dataset",
            "license": "https://creativecommons.org/publicdomain/zero/1.0/",
            "creator": [{"type": "schema:Organization", "name": "Test Org", "role": "originator"}],
            "created": "2024-01-01T00:00:00Z",
            "added": "2024-01-01T00:00:00Z",
            "contentCreated": start,
            "origin": "https://example.org/source",
            "custodyChain": [
                {
                    "agent": "https://example.org/agents/test-org",
                    "action": "created",
                    "startTime": "2024-01-01T00:00:00Z",
                }
            ],
        }
        if end is not None:
            record["contentCreatedEnd"] = end
        return record

    def _validate_record(self, record: dict) -> bool:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.jsonld"
            path.write_text(json.dumps(record), encoding="utf-8")
            return validate.validate_example(
                path, validate.load_validator(), validate.SCHEMA_DIR / "sourcelume.shacl.ttl"
            )

    def test_content_created_period_is_accepted(self) -> None:
        record = self._record_with_content_period("1850-01-01T00:00:00Z", "1900-12-31T00:00:00Z")
        self.assertTrue(self._validate_record(record))

    def test_content_created_end_is_optional(self) -> None:
        record = self._record_with_content_period("1850-01-01T00:00:00Z", None)
        self.assertTrue(self._validate_record(record))

    def test_content_created_end_before_start_is_rejected(self) -> None:
        record = self._record_with_content_period("1900-12-31T00:00:00Z", "1850-01-01T00:00:00Z")
        self.assertFalse(self._validate_record(record))

    def test_content_created_end_must_be_a_date_time(self) -> None:
        record = self._record_with_content_period("1850-01-01T00:00:00Z", "not a date")
        self.assertFalse(self._validate_record(record))

    def test_validate_example_with_invalid_json_schema(self) -> None:
        """Test that an invalid record fails JSON Schema validation."""
        with tempfile.TemporaryDirectory() as tmp:
            example_path = Path(tmp) / "invalid.jsonld"

            # Missing required fields
            invalid_record = {
                "@context": "https://sourcelume.apache.org/context/0.0.1/sourcelume.jsonld",
                "id": "https://example.org/records/test",
                "type": "ProvenanceRecord"
                # Missing: identifier, name, license, creator, dates, origin, custodyChain
            }

            example_path.write_text(json.dumps(invalid_record, indent=2), encoding="utf-8")

            validator = validate.load_validator()
            shapes_path = validate.SCHEMA_DIR / "sourcelume.shacl.ttl"

            # This should return False for an invalid record
            result = validate.validate_example(example_path, validator, shapes_path)
            self.assertFalse(result)


class TrainingProvenanceRecordTests(unittest.TestCase):
    """TrainingProvenanceRecord is checked by the JSON Schema and by the SHACL shapes, which must agree."""

    CONTEXT = json.loads((REPO_ROOT / "context" / "0.0.1" / "sourcelume.jsonld").read_text())["@context"]

    def _record(self, **overrides) -> dict:
        record = {
            "@context": validate.CANONICAL_CONTEXT_IRI,
            "id": "https://example.org/records/test-model-training",
            "type": "TrainingProvenanceRecord",
            "identifier": "https://example.org/models/test",
            "name": "Test Model",
            "version": "1",
            "creator": [{"type": "schema:Organization", "name": "Test Org", "role": "originator"}],
            "created": "2024-01-01T00:00:00Z",
            "disclosure": "complete",
            "trainingData": [
                {
                    "dataset": "https://example.org/records/test-dataset",
                    "phase": "pretraining",
                    "tokens": 1000,
                    "share": 0.5,
                }
            ],
            "note": "Test record.",
        }
        record.update(overrides)
        return record

    def _schema_accepts(self, record: dict) -> bool:
        return validate.load_validator("TrainingProvenanceRecord").is_valid(record)

    def _shacl_accepts(self, record: dict) -> bool:
        graph = Graph()
        graph.parse(data=json.dumps({**record, "@context": self.CONTEXT}), format="json-ld")
        expected = URIRef("https://sourcelume.apache.org/ns#TrainingProvenanceRecord")
        self.assertIn((URIRef(record["id"]), RDF.type, expected), graph)
        conforms, _, _ = shacl_validate(
            graph,
            shacl_graph=str(validate.SCHEMA_DIR / "sourcelume.shacl.ttl"),
            shacl_graph_format="turtle",
            inference="none",
        )
        return conforms

    def assertAccepted(self, record: dict) -> None:
        self.assertTrue(self._schema_accepts(record), "JSON Schema rejected the record")
        self.assertTrue(self._shacl_accepts(record), "SHACL rejected the record")

    def assertRejectedByBoth(self, record: dict) -> None:
        self.assertFalse(self._schema_accepts(record), "JSON Schema accepted the record")
        self.assertFalse(self._shacl_accepts(record), "SHACL accepted the record")

    def test_valid_record_is_accepted(self) -> None:
        self.assertAccepted(self._record())

    def test_entry_needs_only_a_dataset(self) -> None:
        self.assertAccepted(self._record(trainingData=[{"dataset": "https://example.org/records/test-dataset"}]))

    def test_every_phase_is_accepted(self) -> None:
        for phase in ("pretraining", "fine-tuning", "alignment", "evaluation"):
            with self.subTest(phase=phase):
                self.assertAccepted(self._record(trainingData=[{"dataset": "https://example.org/d", "phase": phase}]))

    def test_unknown_phase_is_rejected(self) -> None:
        self.assertRejectedByBoth(self._record(trainingData=[{"dataset": "https://example.org/d", "phase": "sft"}]))

    def test_entry_without_dataset_is_rejected(self) -> None:
        self.assertRejectedByBoth(self._record(trainingData=[{"phase": "pretraining"}]))

    def test_share_is_a_fraction(self) -> None:
        for share in (0, 0.25, 1):
            with self.subTest(share=share):
                self.assertAccepted(self._record(trainingData=[{"dataset": "https://example.org/d", "share": share}]))
        for share in (-0.1, 1.5):
            with self.subTest(share=share):
                self.assertRejectedByBoth(
                    self._record(trainingData=[{"dataset": "https://example.org/d", "share": share}])
                )

    def test_negative_tokens_are_rejected(self) -> None:
        self.assertRejectedByBoth(self._record(trainingData=[{"dataset": "https://example.org/d", "tokens": -1}]))

    def test_disclosure_is_required_and_closed(self) -> None:
        record = self._record()
        del record["disclosure"]
        self.assertRejectedByBoth(record)
        self.assertRejectedByBoth(self._record(disclosure="mostly"))

    def test_listed_training_data_is_required_unless_undisclosed(self) -> None:
        for disclosure in ("complete", "partial"):
            record = self._record(disclosure=disclosure)
            del record["trainingData"]
            with self.subTest(disclosure=disclosure):
                self.assertRejectedByBoth(record)

        record = self._record(disclosure="undisclosed")
        del record["trainingData"]
        self.assertAccepted(record)

    def test_creator_is_required(self) -> None:
        record = self._record()
        del record["creator"]
        self.assertRejectedByBoth(record)

    def test_dataset_record_is_not_accepted_as_training_record(self) -> None:
        """The two record types have separate schemas; neither accepts the other's type."""
        self.assertFalse(validate.load_validator().is_valid(self._record()))

    def test_schema_files_match_their_record_type(self) -> None:
        for record_type in validate.SCHEMA_FILES:
            with self.subTest(record_type=record_type):
                schema = validate.load_validator(record_type).schema
                self.assertEqual(schema["properties"]["type"]["const"], record_type)

    def test_main_validates_each_record_against_its_own_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "training.jsonld").write_text(json.dumps(self._record()), encoding="utf-8")
            with mock.patch.object(validate, "EXAMPLES_DIR", Path(tmp)):
                self.assertEqual(validate.main(), 0)

    def test_main_rejects_an_unknown_record_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "unknown.jsonld").write_text(json.dumps(self._record(type="SomethingElse")), encoding="utf-8")
            with mock.patch.object(validate, "EXAMPLES_DIR", Path(tmp)):
                self.assertEqual(validate.main(), 1)


if __name__ == "__main__":
    unittest.main()