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
"""Render human-readable docs from the JSON Schemas.

Generates a Markdown field reference per schema version, with a table
for each `schema/<version>/*.schema.json` record schema. This includes
both ProvenanceRecord and TrainingProvenanceRecord. It does not render
SHACL shapes, cross-link to the prose spec, or produce HTML output.

Usage:
    uv run python tools/render-docs.py

Output is written to `spec/<version>/generated-field-reference.md` for
each published schema version. Generated files are not intended to be
committed until the project decides how generated output should be
handled (see the "Notes for contributors" section of SETUP.md).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schema"
SPEC_DIR = REPO_ROOT / "spec"

# Find published schema version directories that should have docs generated.
def find_version_dirs(base: Path) -> list[Path]:
    """Return published version directories under `base` (e.g. schema/0.0.1)."""
    if not base.is_dir():
        return []
    return sorted(
        p for p in base.iterdir()
        if p.is_dir() and not p.is_symlink() and p.name[0].isdigit()
    )


# Build a Markdown field-reference table from a JSON Schema dictionary.
def render_field_table(schema: dict) -> str:
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    conditional_required = set()
    for keyword in ("then", "else"):
        branch = schema.get(keyword)
        if isinstance(branch, dict):
            conditional_required.update(branch.get("required", []))

    lines = [
        f"## {schema.get('title', 'Schema Reference')}",
        "",
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]

    for field_name, field_def in properties.items():
        field_type = field_def.get("type", field_def.get("format", "—"))
        if field_name in required:
            is_required = "Yes"
        elif field_name in conditional_required:
            is_required = "Conditional (see description)"
        else:
            is_required = "No"
        description = field_def.get("description", "").replace("\n", " ")
        lines.append(f"| `{field_name}` | {field_type} | {is_required} | {description} |")

    return "\n".join(lines) + "\n"


# Render generated documentation for one schema version and return the output path.
def render_version(version_dir: Path) -> Path | None:
    schema_files = sorted(
        version_dir.glob("*.schema.json"),
        key=lambda path: (path.name != "sourcelume.schema.json", path.name),
    )
    if not schema_files:
        return None

    sections = [
        f"# Apache Sourcelume Field Reference ({version_dir.name})",
        "",
        "> Generated from the JSON Schemas. Do not edit by hand — edit the",
        "> schemas and re-run `tools/render-docs.py` instead.",
        "",
    ]
    for schema_file in schema_files:
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        sections.append(render_field_table(schema))
    doc = "\n".join(sections)

    output_dir = SPEC_DIR / version_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "generated-field-reference.md"
    output_path.write_text(doc, encoding="utf-8")
    return output_path


# Generate documentation for all available schema versions and return an exit code.
def main() -> int:
    version_dirs = find_version_dirs(SCHEMA_DIR)

    if not version_dirs:
        print("No schema versions found under schema/.")
        return 0

    for version_dir in version_dirs:
        output_path = render_version(version_dir)
        if output_path:
            print(f"Wrote {output_path}")
        else:
            print(f"Skipped {version_dir}: no *.schema.json files found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
