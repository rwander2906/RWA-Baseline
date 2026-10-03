# Baseline Upgrade Planner

The upgrade planner turns the version declared by a project into a concrete migration/refactoring checklist.

## Usage

```bash
python scripts/plan_baseline_upgrade.py /path/to/project --to 1.0.0
```

JSON output:

```bash
python scripts/plan_baseline_upgrade.py /path/to/project --to 1.0.0 --json
```

Write a Markdown plan:

```bash
python scripts/plan_baseline_upgrade.py /path/to/project \
  --to 1.0.0 \
  --output BASELINE-UPGRADE.md
```

## Migration manifests

Machine-readable migration manifests live in `migrations/<version>.json`.

The planner:
1. reads the project's current version from `.rwa-baseline.yml`,
2. selects all migration manifests newer than the current version and not newer than the target,
3. combines their checklist items,
4. carries existing exceptions into a mandatory re-review section,
5. emits Markdown or JSON.

This avoids reconstructing upgrade work from prose changelogs alone. The human-readable `CHANGELOG.md` remains the release narrative; the migration manifests are the machine-readable counterpart.
