"""Check a project against machine-readable RWA Baseline rules."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    rule: str
    severity: str
    status: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check project compliance with RWA Baseline.")
    parser.add_argument("target", type=Path, nargs="?", default=Path("."))
    parser.add_argument(
        "--rules",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "rules" / "baseline-1.0.json",
    )
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def parse_exception_ids(config_path: Path) -> set[str]:
    if not config_path.is_file():
        return set()

    text = read_text(config_path)
    return set(
        match.group(1)
        for match in re.finditer(r"^\s*-\s*rule:\s*["']?([^"'\s#]+)", text, re.MULTILINE)
    )


def matching_files(root: Path, pattern: str) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and fnmatch.fnmatch(path.relative_to(root).as_posix(), pattern))


def evaluate_rule(root: Path, rule: dict[str, Any]) -> tuple[bool, str]:
    check = rule["check"]

    if check == "file_exists":
        path = root / rule["path"]
        return path.is_file(), f"required file: {rule['path']}"

    if check == "glob_exists":
        files = matching_files(root, rule["path"])
        return bool(files), f"expected at least one file matching {rule['path']}"

    if check == "file_contains_all":
        path = root / rule["path"]
        text = read_text(path)
        missing = [token for token in rule["tokens"] if token not in text]
        return path.is_file() and not missing, (
            f"{rule['path']} missing tokens: {', '.join(missing)}" if missing else f"validated {rule['path']}"
        )

    if check == "glob_contains_any":
        files = matching_files(root, rule["path"])
        for path in files:
            text = read_text(path)
            if any(token in text for token in rule["tokens"]):
                return True, f"matched in {path.relative_to(root)}"
        return False, f"none of {rule['tokens']} found in files matching {rule['path']}"

    if check == "glob_contains_all":
        files = matching_files(root, rule["path"])
        if not files:
            return False, f"no files matching {rule['path']}"
        for path in files:
            text = read_text(path)
            if all(token in text for token in rule["tokens"]):
                return True, f"matched in {path.relative_to(root)}"
        return False, f"no file matching {rule['path']} contains all required tokens"

    if check == "glob_each_contains_all":
        files = matching_files(root, rule["path"])
        if not files:
            return False, f"no files matching {rule['path']}"
        failures = []
        for path in files:
            text = read_text(path)
            missing = [token for token in rule["tokens"] if token not in text]
            if missing:
                failures.append(f"{path.relative_to(root)} missing {', '.join(missing)}")
        return not failures, "; ".join(failures) if failures else f"validated {len(files)} file(s)"

    if check == "forbidden_globs":
        matches: list[str] = []
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            name = path.name
            for pattern in rule["paths"]:
                if fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(name, pattern):
                    if relative.endswith(".example") or relative.endswith(".example.env"):
                        continue
                    matches.append(relative)
        return not matches, f"forbidden files: {', '.join(sorted(set(matches)))}" if matches else "no forbidden secret files found"

    if check == "any_file_contains":
        for relative in rule["paths"]:
            path = root / relative
            if not path.is_file():
                continue
            text = read_text(path)
            if any(token in text for token in rule["tokens"]):
                return True, f"matched in {relative}"
        return False, f"none of {rule['paths']} references the baseline"

    raise ValueError(f"Unsupported check type: {check}")


def run_check(root: Path, rules_path: Path) -> list[Finding]:
    catalog = json.loads(rules_path.read_text(encoding="utf-8"))
    exceptions = parse_exception_ids(root / ".rwa-baseline.yml")
    findings: list[Finding] = []

    for rule in catalog["rules"]:
        rule_id = rule["id"]
        if rule_id in exceptions:
            findings.append(
                Finding(rule_id, rule["severity"], "excepted", "documented exception in .rwa-baseline.yml")
            )
            continue

        passed, message = evaluate_rule(root, rule)
        findings.append(
            Finding(rule_id, rule["severity"], "pass" if passed else "fail", message)
        )

    return findings


def main() -> int:
    args = parse_args()
    root = args.target.resolve()
    findings = run_check(root, args.rules)

    failed_errors = [f for f in findings if f.status == "fail" and f.severity == "error"]

    if args.json_output:
        print(json.dumps({"target": str(root), "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        for finding in findings:
            marker = {"pass": "PASS", "fail": "FAIL", "excepted": "EXCEPT"}[finding.status]
            print(f"{marker:6} {finding.rule}: {finding.message}")
        print()
        print(f"{len(findings)} rules checked; {len(failed_errors)} blocking failure(s).")

    return 1 if failed_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
