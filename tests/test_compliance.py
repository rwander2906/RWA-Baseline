"""Tests for project compliance checker."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_project_compliance.py"
SPEC = importlib.util.spec_from_file_location("check_project_compliance", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ComplianceTests(unittest.TestCase):
    def test_exception_ids_are_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / ".rwa-baseline.yml"
            path.write_text(
                'exceptions:\n  - rule: "quality.coverage.minimum"\n    reason: "legacy"\n',
                encoding="utf-8",
            )
            self.assertEqual(
                MODULE.parse_exception_ids(path),
                {"quality.coverage.minimum"},
            )

    def test_file_exists_rule(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("ok", encoding="utf-8")
            passed, _ = MODULE.evaluate_rule(
                root,
                {"check": "file_exists", "path": "README.md"},
            )
            self.assertTrue(passed)

    def test_forbidden_secret_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".env").write_text("TOKEN=secret", encoding="utf-8")
            passed, message = MODULE.evaluate_rule(
                root,
                {"check": "forbidden_globs", "paths": [".env", "*.pem"]},
            )
            self.assertFalse(passed)
            self.assertIn(".env", message)

    def test_documented_exception_is_not_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".rwa-baseline.yml").write_text(
                'exceptions:\n  - rule: "docs.readme"\n    reason: "test"\n',
                encoding="utf-8",
            )
            rules = root / "rules.json"
            rules.write_text(
                json.dumps(
                    {
                        "rules": [
                            {
                                "id": "docs.readme",
                                "description": "README",
                                "severity": "error",
                                "check": "file_exists",
                                "path": "README.md",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            findings = MODULE.run_check(root, rules)
            self.assertEqual(findings[0].status, "excepted")


if __name__ == "__main__":
    unittest.main()
