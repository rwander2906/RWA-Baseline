# Compliance Check

The compliance checker evaluates a project against machine-readable RWA Baseline rules.

## Local use

```bash
python scripts/check_project_compliance.py /path/to/project
```

For machine-readable output:

```bash
python scripts/check_project_compliance.py /path/to/project --json
```

Exit code is non-zero when at least one non-excepted error rule fails.

## Exceptions

A rule can be explicitly excepted in `.rwa-baseline.yml`:

```yaml
exceptions:
  - rule: "quality.coverage.minimum"
    value: 60
    reason: "Legacy measured baseline."
    issue: "#123"
```

The checker reports that rule as `EXCEPT` rather than silently passing it.

## Rule catalog

`rules/baseline-1.0.json` is the machine-readable catalog for Baseline 1.0. Stable rule IDs allow projects to carry exceptions across wording/documentation changes.

The first catalog checks project declaration, documentation, GitHub templates/workflows, promotion gate, coverage/complexity gates, least-privilege CI permissions and obvious tracked secret files.

## CI integration

Projects may copy the compliance checker into their CI or invoke the Baseline repository tooling as part of a bootstrap/update workflow. A future version can package this as a reusable GitHub Action.
