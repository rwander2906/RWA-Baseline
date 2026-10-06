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
            self.assertIn(".python-version", files)
            self.assertEqual(files[".python-version"], "3.12
")
            self.assertIn(".env.example", files)
            self.assertIn("coverage==", files["requirements-dev.txt"])
            self.assertNotIn("coverage
", files["requirements-dev.txt"])
            self.assertIn('language: "python"', files[".rwa-baseline.yml"])
            self.assertIn("radon cc . --min C", files[".github/workflows/ci.yml"])
            self.assertIn("ruff check .", files[".github/workflows/ci.yml"])
            for heading in ("## Purpose", "## Prerequisites", "## Installation", "## Configuration", "## Start", "## Tests", "## Build", "## Architecture"):
                self.assertIn(heading, files["README.md"])
            self.assertIn("docs/TESTING_AND_QUALITY.md", files)
            self.assertIn("docs/USER_DOCUMENTATION.md", files)
            self.assertIn("docs/user/README.md", files)
            self.assertIn("docs/user/screenshots/.gitkeep", files)
            self.assertIn(".github/workflows/release-documentation-gate.yml", files)
            self.assertIn("scripts/check_user_documentation.py", files)
            self.assertIn("Verhalten vor Kennzahl", files["docs/TESTING_AND_QUALITY.md"])
            self.assertIn("Legacy-Adoption und Ratchet", files["docs/TESTING_AND_QUALITY.md"])
            self.assertIn("docs/adr/README.md", files)
            self.assertIn("docs/adr/0000-template.md", files)
            self.assertIn("## Components and Responsibilities", files["docs/ARCHITECTURE.md"])

    def test_python_desktop_profile_generates_release_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "Desktop App"
            args = SimpleNamespace(target=target, name="Desktop App", profile="python-desktop")
            files = MODULE.generated_files(args)

            self.assertIn("desktop.spec", files)
            self.assertIn("VERSION", files)
            self.assertIn("requirements-build.txt", files)
            self.assertIn("pyinstaller==", files["requirements-build.txt"])
            self.assertIn(".github/workflows/windows-desktop-release.yml", files)
            self.assertIn("windows-latest", files[".github/workflows/windows-desktop-release.yml"])
            self.assertIn("Smoke test executable", files[".github/workflows/windows-desktop-release.yml"])
            self.assertIn("docs/WINDOWS_DESKTOP_RELEASE.md", files)
            self.assertIn("docs/user", files[".github/workflows/windows-desktop-release.yml"])

    def test_node_profile_generates_package_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "My App"
            args = SimpleNamespace(target=target, name="My App", profile="node")
            files = MODULE.generated_files(args)

            self.assertIn("package.json", files)
            self.assertIn(".nvmrc", files)
            self.assertEqual(files[".nvmrc"], "22
")
            self.assertIn(".env.example", files)
            self.assertIn(".github/workflows/preserve-staging.yml", files)
            self.assertIn('"name": "my-app"', files["package.json"])
            self.assertIn('"complexity": ["error", 12]', files["eslint.config.js"])
            self.assertIn('"no-empty": "error"', files["eslint.config.js"])
            self.assertIn("test:coverage", files["package.json"])
            self.assertIn("npm run test:coverage", files[".github/workflows/ci.yml"])

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
