#!/usr/bin/env python3
import json
import sys
from pathlib import Path

VALID_VERDICTS = {"PASS", "WARN", "BLOCK"}
VALID_SEVERITIES = {"INFO", "WARN", "BLOCK"}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_result(data: dict) -> None:
    if data.get("schema_version") != "1.0": fail("schema_version must be 1.0")
    verdict = data.get("verdict")
    if verdict not in VALID_VERDICTS: fail("invalid verdict")
    if not isinstance(data.get("summary"), str) or not data["summary"].strip(): fail("summary is required")
    findings = data.get("findings")
    if not isinstance(findings, list): fail("findings must be an array")
    for finding in findings:
        if finding.get("severity") not in VALID_SEVERITIES: fail("invalid finding severity")
        if not finding.get("message"): fail("finding message is required")
        location = finding.get("location")
        if not isinstance(location, dict) or not location.get("path"): fail("finding location.path is required")
    severities = {f["severity"] for f in findings}
    if verdict == "PASS" and ("WARN" in severities or "BLOCK" in severities): fail("PASS cannot contain WARN/BLOCK findings")
    if verdict == "WARN" and "BLOCK" in severities: fail("WARN cannot contain BLOCK findings")
    if verdict == "BLOCK" and "BLOCK" not in severities: fail("BLOCK requires a BLOCK finding")
    reviewer = data.get("reviewer")
    if not isinstance(reviewer, dict) or not reviewer.get("adapter") or not reviewer.get("model"): fail("reviewer adapter/model are required")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_ai_review_contract.py RESULT.json", file=sys.stderr); return 2
    try:
        validate_result(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"AI review contract invalid: {exc}", file=sys.stderr); return 1
    print("AI review contract valid"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
