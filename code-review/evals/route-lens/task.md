# Our reviews keep missing N+1 queries

## Problem Description

Tessl Code Review runs on this repository already, with the four default
lenses, through `.github/workflows/tessl-code-review.yml`. It is useful, but in
the last quarter three incidents traced back to a loop that issued one database
or service call per row, and the review said nothing each time. Human reviewers
caught two of them late. `review-comments.md` has the comments they left.

Fix this. We want the review to catch this class of change before it merges.
Do not change when reviews run or whether they block; that is settled.

## Output Specification

- `plan.md` at the workspace root: which job this is, which skill handles it,
  and why, in a few lines.
- The lens, as `review-lenses/review-per-row-calls/SKILL.md`, ready to run as a
  reviewer skill.
- `validation-plan.md`: how we should check the lens before adopting it, and
  how it gets selected once adopted.
- Leave `.github/workflows/tessl-code-review.yml` unchanged.
