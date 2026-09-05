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
"""Validate Sourcelume specification assets.

This is a starting skeleton. It currently checks that the versioned
schema, context, and SHACL files for each published version are present
and syntactically valid (valid JSON / valid Turtle). It does not yet
validate examples against the schema/SHACL, or check cross-version
consistency — see SETUP.md for the full intended scope.

Usage:
    uv run python tools/validate.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION_DIR_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTEXT_DIR = REPO_ROOT / "context"
SCHEMA_DIR = REPO_ROOT / "schema"
EXAMPLES_DIR = REPO_ROOT / "examples"

# Convert a filesystem path to a repository-relative string when possible.
def display_path(path: Path) -> str:
    """Return `path` relative to the repository root when possible."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# Check that a required path exists and is a regular file.
def require_file(path: Path) -> list[str]:
    """Return an error if `path` is not a regular file."""
    if not path.is_file():
        return [f"{display_path(path)}: missing required file"]
    return []


# Find all published version directories whose names match the expected SemVer format.
def find_version_dirs(base: Path) -> list[Path]:
    """Return published SemVer-like version directories under `base`."""
    if not base.is_dir():
        return []
    return sorted(
        p for p in base.iterdir()
        if p.is_dir() and not p.is_symlink() and VERSION_DIR_PATTERN.fullmatch(p.name)
    )


# Validate that a file can be read and parsed as JSON.
def check_json_file(path: Path) -> list[str]:
    errors = []
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{display_path(path)}: invalid JSON ({exc})")
    except OSError as exc:
        errors.append(f"{display_path(path)}: could not read file ({exc})")
    return errors


# Validate that a Turtle file can be read and parsed with rdflib.
def check_turtle_file(path: Path) -> list[str]:
    errors = []
    try:
        import rdflib
    except ImportError as exc:
        errors.append(f"{display_path(path)}: cannot validate Turtle because rdflib is not installed ({exc})")
        return errors

    try:
        rdflib.Graph().parse(str(path), format="turtle")
    except OSError as exc:
        errors.append(f"{display_path(path)}: could not read file ({exc})")
    except Exception as exc:  # noqa: BLE001 - report any parse failure
        errors.append(f"{display_path(path)}: invalid Turtle ({exc})")
    return errors


# Validate required schema, context, and SHACL assets for each published version.
def validate_schema_and_context() -> list[str]:
    errors: list[str] = []

    context_version_dirs = find_version_dirs(CONTEXT_DIR)
    schema_version_dirs = find_version_dirs(SCHEMA_DIR)

    context_versions = {version_dir.name for version_dir in context_version_dirs}
    schema_versions = {version_dir.name for version_dir in schema_version_dirs}

    for version in sorted(context_versions - schema_versions):
        errors.append(
            f"{display_path(SCHEMA_DIR / version)}: missing schema directory for context version {version}"
        )

    for version in sorted(schema_versions - context_versions):
        errors.append(
            f"{display_path(CONTEXT_DIR / version)}: missing context directory for schema version {version}"
        )

    for version_dir in context_version_dirs:
        context_file = version_dir / "sourcelume.jsonld"

        errors.extend(require_file(context_file))
        if context_file.is_file():
            errors.extend(check_json_file(context_file))

    for version_dir in schema_version_dirs:
        schema_file = version_dir / "sourcelume.schema.json"
        shacl_file = version_dir / "sourcelume.shacl.ttl"

        errors.extend(require_file(schema_file))
        errors.extend(require_file(shacl_file))

        if schema_file.is_file():
            errors.extend(check_json_file(schema_file))
        if shacl_file.is_file():
            errors.extend(check_turtle_file(shacl_file))

    return errors


# Validate example JSON-LD files when an examples directory is present.
def validate_examples() -> list[str]:
    errors: list[str] = []
    if not EXAMPLES_DIR.is_dir():
        return errors

    for example_file in EXAMPLES_DIR.rglob("*.jsonld"):
        if example_file.is_file() and not example_file.is_symlink():
            errors.extend(check_json_file(example_file))

    # TODO: validate each example against the corresponding version's
    # schema (jsonschema) and SHACL shapes (pyshacl), once example files
    # and a real data model exist.

    return errors


# Run all validation checks and return a process exit code.
def main() -> int:
    errors = validate_schema_and_context() + validate_examples()

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Validation passed (skeleton checks only; see TODOs in this file).")
    return 0


if __name__ == "__main__":
    sys.exit(main())