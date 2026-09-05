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

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_PATH = REPO_ROOT / "tools" / "validate.py"


def load_validate_module():
    spec = importlib.util.spec_from_file_location("validate", VALIDATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {VALIDATE_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate = load_validate_module()


class ValidateToolTests(unittest.TestCase):
    def test_find_version_dirs_returns_only_semver_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)

            (base / "0.0.1").mkdir()
            (base / "1.2.3").mkdir()
            (base / "latest").mkdir()
            (base / "1-draft").mkdir()
            (base / "2026-old").mkdir()
            (base / "not-a-version").mkdir()

            version_dirs = validate.find_version_dirs(base)

            self.assertEqual(
                [path.name for path in version_dirs],
                ["0.0.1", "1.2.3"],
            )

    def test_find_version_dirs_returns_empty_for_missing_base(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"

            self.assertEqual(validate.find_version_dirs(missing), [])

    def test_check_json_file_accepts_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "valid.jsonld"
            path.write_text(json.dumps({"@context": {}, "id": "example"}), encoding="utf-8")

            self.assertEqual(validate.check_json_file(path), [])

    def test_check_json_file_reports_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.jsonld"
            path.write_text("{ invalid json", encoding="utf-8")

            errors = validate.check_json_file(path)

            self.assertEqual(len(errors), 1)
            self.assertIn("invalid JSON", errors[0])

    def test_require_file_accepts_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "asset.json"
            path.write_text("{}", encoding="utf-8")

            self.assertEqual(validate.require_file(path), [])

    def test_require_file_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.json"

            errors = validate.require_file(path)

            self.assertEqual(len(errors), 1)
            self.assertIn("missing required file", errors[0])


if __name__ == "__main__":
    unittest.main()