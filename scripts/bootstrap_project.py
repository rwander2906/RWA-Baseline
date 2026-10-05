"""Bootstrap a new project from the RWA Baseline using only the Python standard library."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

BASELINE_VERSION = "1.1.0"

COMMON_FILES = {
    ".rwa-baseline.yml": """baseline:
  version: "{version}"
  adopted: "YYYY-MM-DD"

profile:
  language: "{profile}"

quality:
  coverage_minimum: 80
  complexity_maximum: 12
  warnings_allowed: 0

exceptions: []
""",
    "CHANGELOG.md": """# Changelog

## Unreleased
""",
    "docs/ARCHITECTURE.md": """# Architecture

Describe system context, major components, data flows, persistence, external dependencies and relevant deployment/runtime boundaries.
""",
    "docs/PROJECT_GUIDELINES.md": """# Project Guidelines

This project follows RWA Baseline {version}.

Document only project-specific additions or justified deviations here. General engineering rules belong to RWA-Baseline.\n\n## Human Maintainability\n\nThis project must remain understandable, buildable, testable, operable and maintainable by a competent developer without prior project history and without an AI service. Critical project knowledge must live in the repository and reproducible processes, not only in chats or prompts.\n""",
}

PROFILE_FILES = {
    "python": {
        ".github/dependabot.yml": """version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
""",
        "requirements-dev.txt": "coverage\nruff\nradon\n",
        "tests/test_smoke.py": '''"""Initial bootstrap smoke test."""

import unittest


class SmokeTest(unittest.TestCase):
    def test_bootstrap(self) -> None:
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()
''',
        ".github/workflows/ci.yml": """name: CI

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main, staging]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install -r requirements-dev.txt
      - run: ruff check .
      - run: radon cc . --min C --show-complexity --total-average
      - run: python -m compileall -q .
      - run: coverage run -m unittest discover -s tests -v
      - run: coverage report --fail-under=80
""",
    },
    "node": {
        ".github/dependabot.yml": """version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
""",
        "package.json": """{
  "name": "{project_slug}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test",
    "test:coverage": "node --experimental-test-coverage --test --test-coverage-lines=80",
    "lint": "eslint . --max-warnings=0"
  },
  "devDependencies": {
    "eslint": "10.10.0"
  }
}
""",
        "eslint.config.js": """export default [
  {
    files: ["**/*.js"],
    rules: {
      "no-unused-vars": "error",
      "no-undef": "error",
      "complexity": ["error", 12],
      "no-empty": "error"
    }
  }
];
""",
        "test/smoke.test.js": """import test from "node:test";
import assert from "node:assert/strict";

test("project bootstrap smoke test", () => {
  assert.equal(1 + 1, 2);
});
""",
        ".github/workflows/ci.yml": """name: CI

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main, staging]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: "22"
          cache: npm
          cache-dependency-path: package-lock.json
      - run: npm ci --ignore-scripts --no-audit --no-fund
      - run: npm audit --audit-level=high
      - run: npm run lint
      - run: npm run test:coverage
""",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a project skeleton from RWA Baseline.")
    parser.add_argument("target", type=Path, help="Target project directory")
    parser.add_argument("--profile", choices=sorted(PROFILE_FILES), required=True)
    parser.add_argument("--name", help="Project display name; defaults to target directory name")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument(
        "--github-repo",
        help="Optional owner/repo. If supplied with --configure-github, repository settings are applied through gh.",
    )
    parser.add_argument(
        "--configure-github",
        action="store_true",
        help="Configure supported GitHub repository settings using the gh CLI.",
    )
    return parser.parse_args()


def project_slug(name: str) -> str:
    return "-".join(name.lower().replace("_", "-").split())


def load_baseline_template(relative_path: str) -> str:
    root = Path(__file__).resolve().parents[1]
    path = root / relative_path
    return path.read_text(encoding="utf-8")


def generated_files(args: argparse.Namespace) -> dict[str, str]:
    name = args.name or args.target.name
    slug = project_slug(name)

    files = {
        "README.md": f"""# {name}

Project initialized from RWA Baseline {BASELINE_VERSION}.

## Development

- work starts with a GitHub Issue
- work branches are created from `staging`
- pull requests target `staging`
- promotion from `staging` to `main` requires explicit approval
- see `.rwa-baseline.yml` for the adopted baseline version
""",
        ".github/pull_request_template.md": load_baseline_template(".github/pull_request_template.md"),
        ".github/ISSUE_TEMPLATE/bug.yml": load_baseline_template(".github/ISSUE_TEMPLATE/bug.yml"),
        ".github/ISSUE_TEMPLATE/feature.yml": load_baseline_template(".github/ISSUE_TEMPLATE/feature.yml"),
        ".github/workflows/promotion-gate.yml": load_baseline_template(
            ".github/workflows/promotion-gate.yml"
        ),
        ".github/workflows/dependabot-issue-tracker.yml": load_baseline_template(
            ".github/workflows/dependabot-issue-tracker.yml"
        ),
        ".github/workflows/preserve-staging.yml": load_baseline_template(
            ".github/workflows/preserve-staging.yml"
        ),
    }

    values = {
        "version": BASELINE_VERSION,
        "profile": args.profile,
        "project_slug": slug,
    }

    def render(template: str) -> str:
        rendered = template
        for key, value in values.items():
            rendered = rendered.replace("{" + key + "}", value)
        return rendered

    for path, template in COMMON_FILES.items():
        files[path] = render(template)
    for path, template in PROFILE_FILES[args.profile].items():
        files[path] = render(template)

    return files


def ensure_safe_target(target: Path, files: dict[str, str]) -> None:
    conflicts = [str(target / relative) for relative in files if (target / relative).exists()]
    if conflicts:
        joined = "\n  - ".join(conflicts)
        raise RuntimeError(
            "Bootstrap would overwrite existing files. Aborting. Conflicts:\n  - " + joined
        )


def write_files(target: Path, files: dict[str, str], dry_run: bool) -> None:
    ensure_safe_target(target, files)
    for relative, content in sorted(files.items()):
        destination = target / relative
        print(f"{'WOULD CREATE' if dry_run else 'CREATE'} {destination}")
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def finalize_profile(target: Path, profile: str, dry_run: bool) -> None:
    if profile != "node":
        return

    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError(
            "Node profile requires npm to generate package-lock.json reproducibly."
        )

    command = [
        npm,
        "install",
        "--package-lock-only",
        "--ignore-scripts",
        "--no-audit",
        "--no-fund",
    ]
    print(("WOULD RUN " if dry_run else "RUN ") + " ".join(command))
    if not dry_run:
        subprocess.run(command, cwd=target, check=True)


def configure_github(repo: str, dry_run: bool) -> None:
    gh = shutil.which("gh")
    if gh is None:
        raise RuntimeError("GitHub configuration requested, but gh CLI is not installed.")

    commands = [
        [gh, "repo", "edit", repo, "--delete-branch-on-merge"],
        [gh, "api", f"repos/{repo}", "--method", "PATCH", "-f", "allow_auto_merge=true"],
    ]

    for command in commands:
        print(("WOULD RUN " if dry_run else "RUN ") + " ".join(command))
        if not dry_run:
            subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    files = generated_files(args)

    try:
        write_files(args.target, files, args.dry_run)
        finalize_profile(args.target, args.profile, args.dry_run)
        if args.configure_github:
            if not args.github_repo:
                raise RuntimeError("--configure-github requires --github-repo owner/repo")
            configure_github(args.github_repo, args.dry_run)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Bootstrap completed." if not args.dry_run else "Dry-run completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
