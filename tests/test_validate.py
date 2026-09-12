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

            # Load the context from the local file
            context_path = REPO_ROOT / "context" / "0.0.1" / "sourcelume.jsonld"
            context = json.loads(context_path.read_text())

            # Create a minimal valid ProvenanceRecord with inline context
            valid_record = {
                "@context": context["@context"],
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

            # This should return True for a valid record
            result = validate.validate_example(example_path, validator, shapes_path)
            self.assertTrue(result)

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


if __name__ == "__main__":
    unittest.main()