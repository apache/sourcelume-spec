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
"""Render human-readable docs from the JSON Schema.

This is a starting skeleton. It currently generates a single Markdown
field-reference table per published schema version, from
`schema/<version>/sourcelume.schema.json`. It does not yet render SHACL
shapes, cross-link to the prose spec, or produce HTML output — see
SETUP.md for the intended scope.

Usage:
    uv run python tools/render-docs.py

Output is written to `spec/<version>/generated-field-reference.md` for
each published schema version. Generated files are not intended to be
committed until the project decides how generated output should be
handled (see the "Notes for contributors" section of SETUP.md).
Note: gitIgnores spec/*/generated-field-reference.md entry exists.
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

    lines = [
        f"# {schema.get('title', 'Schema Reference')}",
        "",
        "> Generated from the JSON Schema. Do not edit by hand — edit the",
        "> schema and re-run `tools/render-docs.py` instead.",
        "",
        "| Field | Type | Required | Description |",
        "|-------|------|----------|-------------|",
    ]

    for field_name, field_def in properties.items():
        field_type = field_def.get("type", field_def.get("format", "—"))
        is_required = "Yes" if field_name in required else "No"
        description = field_def.get("description", "").replace("\n", " ")
        lines.append(f"| `{field_name}` | {field_type} | {is_required} | {description} |")

    return "\n".join(lines) + "\n"


# Render generated documentation for one schema version and return the output path.
def render_version(version_dir: Path) -> Path | None:
    schema_files = list(version_dir.glob("*.schema.json"))
    if not schema_files:
        return None

    schema = json.loads(schema_files[0].read_text())
    doc = render_field_table(schema)

    output_dir = SPEC_DIR / version_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "generated-field-reference.md"
    output_path.write_text(doc)
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
            print(f"Skipped {version_dir}: no *.schema.json file found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
