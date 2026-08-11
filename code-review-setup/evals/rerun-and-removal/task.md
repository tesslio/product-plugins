# Confirm the Code Review setup, and write down how to undo it

## Problem Description

This repository already runs Tessl Code Review. A new maintainer has taken over
the repository and wants two things.

First, confirm the setup matches what the team wants, and change it if it does
not. Their intent, unchanged since it was installed:

- A review on every push to a pull-request branch, with the in-flight review
  superseded when a newer commit lands.
- Findings block the merge.
- The standard review profile, with no custom lens selection.
- Pinned to release `v1.3.0` of the Action, whose commit SHA is
  `8d4a1e7b3c9f5026d8a4e1b7c3f950268d4a1e7b`. They are not adopting a newer
  release in this pass.

Second, they want the removal procedure written down before they need it. The
gate is enforced today by a required status check on the protected branch.

## Output Specification

- `.github/workflows/tessl-code-review.yml`: change nothing that already matches
  the intent above. Do not rewrite the file to look freshly generated.
- `summary.md` at the root of the workspace, stating what the current setup does
  and what this run changed, if anything.
- `removal.md` at the root of the workspace, giving the ordered procedure for
  removing Tessl Code Review from this repository, including anything that must
  happen outside the workflow file and anything that would break if the steps
  were done in the wrong order.
