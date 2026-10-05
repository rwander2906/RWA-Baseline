# Dependabot Issue Tracking

RWA Baseline 1.1 requires Dependabot findings to remain visible in the normal issue backlog.

## Rule

Every newly opened Dependabot pull request receives exactly one linked GitHub issue.

The pull request documents the concrete dependency change and its CI result. The issue documents the finding, review status and lifecycle in the project's regular backlog.

## Workflow

`.github/workflows/dependabot-issue-tracker.yml` uses `pull_request_target` for `opened` and `reopened` events.

Security constraints:
- the workflow runs only when the PR author is `dependabot[bot]`
- no pull-request code is checked out or executed
- the token receives only `contents: read`, `issues: write` and `pull-requests: write`
- a stable marker in the issue body prevents duplicate tracking issues
- reopening a Dependabot PR reuses and, if necessary, reopens the existing tracking issue

## Lifecycle

1. Dependabot opens a PR.
2. The workflow creates a tracking issue.
3. The PR gets a comment linking to the issue.
4. Review, CI and remediation happen in the PR.
5. The tracking issue remains part of the normal issue lifecycle and is closed when the dependency finding is resolved or explicitly rejected.

This applies to regular dependency updates as well as security-related Dependabot pull requests.
