# Migration Manifests

Each stable Baseline version that creates adoption work may add `migrations/<version>.json`.

A manifest contains:
- target version,
- human-readable title,
- stable change IDs,
- concise summary,
- concrete checklist instruction.

The manifests are append-only historical records. Corrections that change required migration work should normally be introduced in a later Baseline version rather than silently rewriting already adopted history.
