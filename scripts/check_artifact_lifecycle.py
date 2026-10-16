"""Enforce explicit justification and short retention for Actions artifacts."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

UPLOAD = re.compile(r"\buses:\s*['\"]?actions/upload-artifact@[^\s'\"]+", re.I)
RETENTION = re.compile(r"^\s*retention-days:\s*(\d+)\s*(?:#.*)?$", re.M)
JUSTIFICATION = re.compile(r"^\s*#\s*artifact-lifecycle:\s*(cross-job|diagnostic)\s*$", re.M | re.I)


def inspect_workflow(text: str, filename: str) -> list[str]:
    """Review each upload step and demand documented, bounded storage."""
    findings = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not UPLOAD.search(line):
            continue
        # A marker must be within this step, not an unrelated workflow comment.
        start = index
        while start > 0 and not re.match(r"^\\s*-\\s*(?:name:|uses:)\\s*", lines[start]):
            start -= 1
        end = index + 1
        while end < len(lines) and not re.match(r"^\\s*-\\s*(?:name:|uses:)\\s*", lines[end]):
            end += 1
        # Include only contiguous comments immediately above this step.
        comment_start = start
        while comment_start > 0 and lines[comment_start - 1].lstrip().startswith("#"):
            comment_start -= 1
        chunk = "\n".join(lines[comment_start:end])
        context = f"{filename}:{index + 1}"
        if not JUSTIFICATION.search(chunk):
            findings.append(f"{context}: missing # artifact-lifecycle: cross-job|diagnostic")
        retention = RETENTION.findall(chunk)
        if not retention or int(retention[-1]) > 3:
            findings.append(f"{context}: retention-days must be explicitly set to 1..3")
    return findings


def check(root: Path) -> list[str]:
    folder = root / ".github" / "workflows"
    if not folder.is_dir():
        return []
    findings = []
    for path in sorted(list(folder.glob("*.yml")) + list(folder.glob("*.yaml"))):
        findings.extend(inspect_workflow(path.read_text(encoding="utf-8"), str(path.relative_to(root))))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    findings = check(args.repository)
    for finding in findings:
        print("ERROR:", finding)
    if findings:
        return 1
    print("Actions artifact lifecycle check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
