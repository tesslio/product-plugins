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

You do not have a published release SHA for the Action available in this
environment. Where the pinned revision belongs, write the literal placeholder
`<full-commit-sha>` and call it out in your summary as the one thing a human has
to replace before the workflow can run.

## Output Specification

Produce the following files:

- The Code Review caller workflow under `.github/workflows/`, invoking
  `tesslio/code-review` and nothing else. Do not copy or reimplement any review,
  checkout, CLI-setup, or review-publication logic into the workflow.
- `summary.md` at the root of the workspace, documenting the cadence and blocking
  contract that was installed, the repository secret the workflow needs, the
  permissions it grants and why, and how to update or remove the setup later.

Leave `.github/workflows/ci.yml` unchanged.
