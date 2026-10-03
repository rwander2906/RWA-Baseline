"""Build an upgrade/refactoring plan from an adopted RWA Baseline version."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(order=True, frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "Version":
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-[0-9A-Za-z.-]+)?", value.strip())
        if not match:
            raise ValueError(f"Unsupported semantic version: {value}")
        return cls(*(int(part) for part in match.groups()))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan an RWA Baseline upgrade.")
    parser.add_argument("target", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--to", required=True, help="Target baseline version, e.g. 1.0.0")
    parser.add_argument(
        "--migrations",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "migrations",
    )
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--output", type=Path, help="Optional file for Markdown/JSON output")
    return parser.parse_args()


def read_baseline_version(config_path: Path) -> str:
    if not config_path.is_file():
        raise RuntimeError(f"Missing baseline declaration: {config_path}")

    text = config_path.read_text(encoding="utf-8")
    match = re.search(r"^\s*version:\s*["']?([0-9A-Za-z.-]+)", text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"No baseline.version found in {config_path}")
    return match.group(1)


def read_exceptions(config_path: Path) -> list[dict[str, str]]:
    if not config_path.is_file():
        return []

    exceptions: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        rule_match = re.match(r"-\s*rule:\s*["']?([^"']+)", line)
        if rule_match:
            if current:
                exceptions.append(current)
            current = {"rule": rule_match.group(1).strip()}
            continue

        if current is None:
            continue

        field_match = re.match(r"(value|reason|issue):\s*["']?(.*?)["']?$", line)
        if field_match:
            current[field_match.group(1)] = field_match.group(2).strip()

    if current:
        exceptions.append(current)

    return exceptions


def load_migrations(directory: Path) -> list[dict[str, Any]]:
    migrations = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = str(path)
        data["_version"] = Version.parse(data["version"])
        migrations.append(data)
    return sorted(migrations, key=lambda item: item["_version"])


def build_plan(
    current_version: str,
    target_version: str,
    migrations: list[dict[str, Any]],
    exceptions: list[dict[str, str]],
) -> dict[str, Any]:
    current = Version.parse(current_version)
    target = Version.parse(target_version)

    if target < current:
        raise RuntimeError(f"Target {target} is older than current baseline {current}.")

    selected = [
        migration
        for migration in migrations
        if current < migration["_version"] <= target
    ]

    changes = []
    for migration in selected:
        for change in migration.get("changes", []):
            changes.append(
                {
                    "version": migration["version"],
                    "id": change["id"],
                    "summary": change["summary"],
                    "checklist": change["checklist"],
                }
            )

    return {
        "from": current_version,
        "to": target_version,
        "migration_versions": [migration["version"] for migration in selected],
        "changes": changes,
        "exceptions_to_review": exceptions,
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# RWA Baseline Upgrade {plan['from']} → {plan['to']}",
        "",
    ]

    if plan["changes"]:
        lines.extend(["## Required review / migration", ""])
        for change in plan["changes"]:
            lines.append(
                f"- [ ] **{change['id']}** ({change['version']}): {change['checklist']}"
            )
            lines.append(f"  - {change['summary']}")
    else:
        lines.extend(["No migration changes are required for this version range.", ""])

    lines.extend(["", "## Existing exceptions to re-evaluate", ""])
    if plan["exceptions_to_review"]:
        for exception in plan["exceptions_to_review"]:
            detail = exception.get("reason", "no reason recorded")
            issue = exception.get("issue")
            suffix = f" ({issue})" if issue else ""
            lines.append(f"- [ ] **{exception['rule']}**: {detail}{suffix}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Completion",
            "",
            f"- [ ] Compliance check passes for Baseline {plan['to']}",
            f"- [ ] .rwa-baseline.yml updated to {plan['to']}",
            "- [ ] remaining exceptions are explicitly justified",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    config_path = args.target.resolve() / ".rwa-baseline.yml"

    try:
        current_version = read_baseline_version(config_path)
        exceptions = read_exceptions(config_path)
        migrations = load_migrations(args.migrations)
        plan = build_plan(current_version, args.to, migrations, exceptions)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(plan, indent=2) if args.json_output else render_markdown(plan)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
        print(f"Wrote upgrade plan to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
