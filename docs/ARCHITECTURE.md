# Architecture

RWA-Baseline is a policy and tooling repository rather than an application runtime.

## Components

- `docs/`: normative engineering guidance
- `profiles/`: stack-specific additions
- `rules/`: machine-readable compliance rules
- `scripts/`: bootstrap, validation and compliance tooling
- `templates/`: reusable GitHub/project templates
- `checklists/`: operational adoption and review checklists
- `.github/`: the repository's own active workflow and collaboration templates

## Data flow

Projects adopt a concrete Baseline version in `.rwa-baseline.yml`. The compliance checker reads the machine-readable rule catalog plus project files and produces pass/fail/excepted findings. Bootstrap tooling creates a compliant starting structure for new projects.

## State

The repository has no application runtime state. Versioned files are the source of truth.
