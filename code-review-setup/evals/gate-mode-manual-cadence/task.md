# Add a blocking Tessl Code Review gate, invoked on request only

## Problem Description

A platform team wants Tessl Code Review installed in this repository using the
supported Action, `tesslio/code-review-action`. Their release process is deliberate and
they do not want review runs firing on pull-request activity.

Their decisions, already made:

- Nothing runs automatically. A review happens only when someone asks for it, by
  commenting on the pull request or by dispatching the workflow manually with a
  pull-request number.
- Findings block the merge. A review that approves the changes should pass the
  check. A review that requests changes should fail it.
- The standard review profile, with no custom lens selection.

The Tessl API token is supplied to the workflow as a repository secret named
`TESSL_TOKEN`.

The team is adopting release `v1.5.0` of the Action, whose commit SHA is
`3a914f7c2b8e5d061a934f7c2b8e5d061a934f7c`. Pin that full SHA. Do not pin a tag,
a branch, `main`, or `canary`, and do not leave a placeholder in the file.

## Output Specification

Produce the following files:

- The Code Review caller workflow under `.github/workflows/`, invoking
  `tesslio/code-review-action` and nothing else. Do not copy or reimplement any review,
  checkout, CLI-setup, or review-publication logic into the workflow.
- `summary.md` at the root of the workspace, documenting the contract that was
  installed, every configuration step a repository administrator still has to
  perform by hand, and what this team has to do to clear a blocked pull request
  on the cadence they chose.
