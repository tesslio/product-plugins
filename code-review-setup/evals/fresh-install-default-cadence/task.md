# Add Tessl Code Review to this repository

## Problem Description

This repository has one existing GitHub Actions workflow, `.github/workflows/ci.yml`,
which runs the test suite. The team wants automated pull-request review added
alongside it, using the supported Tessl Code Review Action, `tesslio/code-review`.

The team has already decided how they want it to behave, so no questions need to
be asked:

- Reviews should run once when a pull request becomes ready for review, and again
  whenever someone requests a fresh round by commenting on the pull request.
  Pushing new commits should not start a review on its own.
- Findings must not block merging. The review is advisory information.
- The reviewer should use the standard review profile with no custom lens
  selection.

Follow this repository's existing conventions for workflow file naming and for
pinning third-party actions. The Tessl API token is supplied to the workflow as a
repository secret named `TESSL_TOKEN`.

The team is adopting release `v1.4.0` of the Action, whose commit SHA is
`7c2f9a1e4b8d63057e9a1c4b8d63f0572a9e1c4b`. Pin that full SHA, and name the
release in your summary. Do not pin a tag, a branch, `main`, or `canary`, and do
not leave a placeholder in the file.

## Output Specification

Produce the following files:

- The Code Review caller workflow under `.github/workflows/`, invoking
  `tesslio/code-review` and nothing else. Do not copy or reimplement any review,
  checkout, CLI-setup, or review-publication logic into the workflow.
- `summary.md` at the root of the workspace, documenting the cadence and blocking
  contract that was installed, the repository secret the workflow needs, the
  permissions it grants and why, and how to update or remove the setup later.

Leave `.github/workflows/ci.yml` unchanged.
