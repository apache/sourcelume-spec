#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Validates every examples/*.jsonld record against the JSON Schema and SHACL
shapes for a spec version. Run via `uv run python tools/validate.py`."""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from pyshacl import validate as shacl_validate
from rdflib import Graph

SPEC_VERSION = "0.0.1"
BASE = Path(__file__).resolve().parent.parent
SCHEMA_DIR = BASE / "schema" / SPEC_VERSION
EXAMPLES_DIR = BASE / "examples"
CANONICAL_CONTEXT_IRI = "https://sourcelume.apache.org/context/0.0.1/sourcelume.jsonld"
CONTEXT_FILE = BASE / "context" / SPEC_VERSION / "sourcelume.jsonld"
# One JSON Schema per record type; the SHACL shapes for all types share one file.
SCHEMA_FILES = {
    "ProvenanceRecord": "sourcelume.schema.json",
    "TrainingProvenanceRecord": "sourcelume-training.schema.json",
}


def load_validator(record_type: str = "ProvenanceRecord") -> Draft202012Validator:
    schema = json.loads((SCHEMA_DIR / SCHEMA_FILES[record_type]).read_text())
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)


def validate_example(example: Path, validator: Draft202012Validator, shapes_path: Path) -> bool:
    doc = json.loads(example.read_text())

    schema_errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if schema_errors:
        print(f"FAIL {example.name}: JSON Schema errors:")
        for err in schema_errors:
            print(f"  - {list(err.path)}: {err.message}")
        return False

    # The canonical context IRI is resolved from the bundled copy, never fetched.
    # The schema has already guaranteed that @context is exactly that IRI.
    context = json.loads(CONTEXT_FILE.read_text())["@context"]
    data_graph = Graph()
    data_graph.parse(data=json.dumps({**doc, "@context": context}), format="json-ld")

    conforms, _, results_text = shacl_validate(
        data_graph,
        shacl_graph=str(shapes_path),
        shacl_graph_format="turtle",
        inference="none",
    )
    if not conforms:
        print(f"FAIL {example.name}: SHACL errors:\n{results_text}")
        return False

    print(f"PASS {example.name}")
    return True


def main() -> int:
    examples = sorted(EXAMPLES_DIR.glob("*.jsonld"))
    if not examples:
        print(f"No *.jsonld files found under {EXAMPLES_DIR} — nothing to validate.", file=sys.stderr)
        return 0

    validators = {record_type: load_validator(record_type) for record_type in SCHEMA_FILES}
    shapes_path = SCHEMA_DIR / "sourcelume.shacl.ttl"

    results = []
    for example in examples:
        record_type = json.loads(example.read_text()).get("type")
        if record_type not in validators:
            print(f"FAIL {example.name}: unknown record type {record_type!r}")
            results.append(False)
            continue
        results.append(validate_example(example, validators[record_type], shapes_path))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
