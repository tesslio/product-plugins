# Move the existing Code Review setup to every-commit reviews

## Problem Description

This repository already runs Tessl Code Review. The caller workflow lives at
`.github/workflows/tessl-code-review.yml` and currently reviews a pull request
once when it becomes ready, plus any round requested by a `/tessl-review`
comment.

The team now wants a review on every push to a pull-request branch, with the
in-flight review superseded when a newer commit lands. Everything else about
their setup stays as it is: still advisory, still the standard profile, still
their self-hosted runner, their 45-minute timeout, their job name, and the step
that writes the review status into the run summary.

At the same time, pin the Action to the revision from the release they are
adopting: `4c8e1d0a9b7f6e5d4c3b2a1908f7e6d5c4b3a291`.

## Output Specification

Update the repository in place:

- `.github/workflows/tessl-code-review.yml` reflects the new cadence and the new
  pinned revision, with the team's own settings preserved.
- `summary.md` at the root of the workspace, listing exactly what changed in the
  workflow and what was deliberately left alone, and explaining why superseding a
  running review is safe.

Do not add a second workflow that calls the Action.
