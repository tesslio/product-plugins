# Our new review lens is too noisy to turn on

## Problem Description

We wrote an observability lens and backtested it over 12 pull requests before adopting it. The results are in `backtest-results.md`. It found real things, but 19 of its 31 findings were noise, it missed a whole family of problems that the human reviewers caught every time, and four of its findings never made it to an inline comment.

Nobody will read a review with that hit rate, so the lens is not going on until the numbers are better.

The lens is at `review-lenses/review-observability/SKILL.md`.

## Output Specification

- Revise `review-lenses/review-observability/SKILL.md` in place.
- Write `tuning-notes.md` explaining each change you made, which category of backtest result it addresses, and what has to happen before we adopt the lens.

Do not create a second lens.
