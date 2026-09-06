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


def load_validator() -> Draft202012Validator:
    schema = json.loads((SCHEMA_DIR / "sourcelume.schema.json").read_text())
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)


def validate_example(example: Path, validator: Draft202012Validator, shapes_path: Path) -> bool:
    doc = json.loads(example.read_text())

    schema_errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if schema_errors:
        print(f"FAIL {example.name}: JSON Schema errors:")
        for err in schema_errors:
            print(f"  - {list(err.path)}: {err.message}")
        return False

    data_graph = Graph()
    data_graph.parse(str(example), format="json-ld")

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
        return 1

    validator = load_validator()
    shapes_path = SCHEMA_DIR / "sourcelume.shacl.ttl"

    ok = all(
        [validate_example(example, validator, shapes_path) for example in examples]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
