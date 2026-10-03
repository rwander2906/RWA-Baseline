"""Validate structural invariants of the RWA Baseline repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    ".rwa-baseline.yml",
    ".rwa-baseline.example.yml",
    "docs/BASELINE_ADOPTION.md",
    "docs/DEFINITION_OF_DONE.md",
    "docs/DEVELOPMENT_WORKFLOW.md",
    "docs/DOCUMENTATION.md",
    "docs/ENGINEERING_GUIDELINES.md",
    "docs/LOGGING_SECURITY.md",
    "docs/MIGRATION_1_0.md",
    "docs/RELEASES.md",
    "docs/REPOSITORY_SETTINGS.md",
    "docs/TESTING_AND_QUALITY.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/workflows/promotion-gate.yml",
    ".github/workflows/ci.yml",
]

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors = 0

    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            fail(f"required file missing: {relative_path}")
            errors += 1

    version_path = ROOT / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not VERSION_RE.fullmatch(version):
            fail(f"VERSION is not semantic-version compatible: {version!r}")
            errors += 1

        readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").is_file() else ""
        self_config = (ROOT / ".rwa-baseline.yml").read_text(encoding="utf-8") if (ROOT / ".rwa-baseline.yml").is_file() else ""

        if version not in readme:
            fail(f"README.md does not mention current VERSION {version}")
            errors += 1
        if f"## {version} " not in changelog and f"## {version}\n" not in changelog:
            fail(f"CHANGELOG.md has no release heading for VERSION {version}")
            errors += 1
        if f'version: "{version}"' not in self_config:
            fail(f".rwa-baseline.yml does not adopt VERSION {version}")
            errors += 1

    workflow = ROOT / ".github/workflows/promotion-gate.yml"
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        if "promotion-approved" not in text or "github.base_ref == 'main'" not in text:
            fail("promotion gate does not enforce promotion-approved for main")
            errors += 1

    pr_template = ROOT / ".github/pull_request_template.md"
    if pr_template.is_file():
        text = pr_template.read_text(encoding="utf-8")
        for expected in ("Refs #", "promotion-approved", "Coverage/Ratchet", "Dependency-/Security"):
            if expected not in text:
                fail(f"PR template missing expected marker: {expected}")
                errors += 1

    if errors:
        print(f"Baseline validation failed with {errors} error(s).", file=sys.stderr)
        return 1

    print("RWA Baseline structural validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
