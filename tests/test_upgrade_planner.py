"""Tests for baseline upgrade planner."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "plan_baseline_upgrade.py"
SPEC = importlib.util.spec_from_file_location("plan_baseline_upgrade", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class UpgradePlannerTests(unittest.TestCase):
    def test_reads_baseline_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / ".rwa-baseline.yml"
            config.write_text(
                'baseline:\n  version: "0.1.0"\n  adopted: "2026-10-03"\n',
                encoding="utf-8",
            )
            self.assertEqual(MODULE.read_baseline_version(config), "0.1.0")

    def test_selects_only_versions_in_upgrade_range(self) -> None:
        migrations = [
            {"version": "0.2.0", "_version": MODULE.Version.parse("0.2.0"), "changes": []},
            {
                "version": "1.0.0",
                "_version": MODULE.Version.parse("1.0.0"),
                "changes": [
                    {
                        "id": "test.rule",
                        "summary": "summary",
                        "checklist": "do the thing",
                    }
                ],
            },
            {"version": "1.1.0", "_version": MODULE.Version.parse("1.1.0"), "changes": []},
        ]
        plan = MODULE.build_plan("0.2.0", "1.0.0", migrations, [])
        self.assertEqual(plan["migration_versions"], ["1.0.0"])
        self.assertEqual(plan["changes"][0]["id"], "test.rule")

    def test_existing_exceptions_are_preserved_for_review(self) -> None:
        exceptions = [{"rule": "quality.coverage.minimum", "reason": "legacy"}]
        plan = MODULE.build_plan("1.0.0", "1.0.0", [], exceptions)
        self.assertEqual(plan["exceptions_to_review"], exceptions)

    def test_markdown_contains_checklist_and_exception(self) -> None:
        plan = {
            "from": "0.1.0",
            "to": "1.0.0",
            "migration_versions": ["1.0.0"],
            "changes": [
                {
                    "version": "1.0.0",
                    "id": "workflow.issue-lifecycle",
                    "summary": "summary",
                    "checklist": "Align workflow.",
                }
            ],
            "exceptions_to_review": [
                {"rule": "quality.coverage.minimum", "reason": "legacy", "issue": "#12"}
            ],
        }
        rendered = MODULE.render_markdown(plan)
        self.assertIn("workflow.issue-lifecycle", rendered)
        self.assertIn("quality.coverage.minimum", rendered)
        self.assertIn("#12", rendered)


if __name__ == "__main__":
    unittest.main()
