"""Tests for the RWA project bootstrap tool."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_project.py"
SPEC = importlib.util.spec_from_file_location("bootstrap_project", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class BootstrapProjectTests(unittest.TestCase):
    def test_python_profile_generates_expected_baseline_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "demo"
            args = SimpleNamespace(target=target, name="Demo", profile="python")
            files = MODULE.generated_files(args)

            self.assertIn(".rwa-baseline.yml", files)
            self.assertIn(".github/workflows/ci.yml", files)
            self.assertIn(".github/workflows/preserve-staging.yml", files)
            self.assertIn("requirements-dev.txt", files)
            self.assertIn('language: "python"', files[".rwa-baseline.yml"])

    def test_node_profile_generates_package_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "My App"
            args = SimpleNamespace(target=target, name="My App", profile="node")
            files = MODULE.generated_files(args)

            self.assertIn("package.json", files)
            self.assertIn(".github/workflows/preserve-staging.yml", files)
            self.assertIn('"name": "my-app"', files["package.json"])

    def test_existing_file_blocks_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            existing = target / "README.md"
            existing.write_text("keep me", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                MODULE.ensure_safe_target(target, {"README.md": "replacement"})

    def test_write_files_creates_nested_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            MODULE.write_files(target, {"docs/ARCHITECTURE.md": "ok"}, dry_run=False)
            self.assertEqual((target / "docs/ARCHITECTURE.md").read_text(encoding="utf-8"), "ok")


if __name__ == "__main__":
    unittest.main()
