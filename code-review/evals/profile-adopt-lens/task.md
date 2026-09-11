# Start running the lens we wrote

## Problem Description

Tessl Code Review runs on this repository through the Tessl Review GitHub App.
We have never configured it, so it reviews with whatever it runs by default,
and that is fine: we want to keep all of it.

We wrote `review-lenses/review-per-row-calls/SKILL.md` after an incident and we
have run it by hand. Make it run on every review from now on, without losing
anything the review catches today.

## Output Specification

- `plan.md` at the workspace root: which job this is, which skill handles it,
  and why, in a few lines. Then what a review runs after the change, and how we
  should check it before merging.
- Whatever files that job produces in the repository.
- Leave `review-lenses/review-per-row-calls/SKILL.md` unchanged.
