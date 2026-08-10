# Add a blocking Tessl Code Review gate, invoked on request only

## Problem Description

A platform team wants Tessl Code Review installed in this repository using the
supported Action, `tesslio/code-review`. Their release process is deliberate and
they do not want review runs firing on pull-request activity.

Their decisions, already made:

- Nothing runs automatically. A review happens only when someone asks for it, by
  commenting on the pull request or by dispatching the workflow manually with a
  pull-request number.
- Findings block the merge. A converged review should approve and pass the check.
  A non-converged review should request changes and fail the check.
- The standard review profile, with no custom lens selection.

The Tessl API token is supplied to the workflow as a repository secret named
`TESSL_TOKEN`.

You do not have a published release SHA for the Action available in this
environment. Where the pinned revision belongs, write the literal placeholder
`<full-commit-sha>`.

## Output Specification

Produce the following files:

- The Code Review caller workflow under `.github/workflows/`, invoking
  `tesslio/code-review` and nothing else. Do not copy or reimplement any review,
  checkout, CLI-setup, or review-publication logic into the workflow.
- `summary.md` at the root of the workspace, documenting the contract that was
  installed, every configuration step a repository administrator still has to
  perform by hand, and anything about this combination of choices that will not
  behave the way the team expects.
