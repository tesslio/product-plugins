# Reviews keep reading our generated client

## Problem Description

Tessl Code Review runs on this repository through the Tessl Review GitHub App,
on the default lenses. Two things are wrong with what it reviews.

Every review spends time on `src/api/generated/`, which `pnpm codegen` rewrites
from the payments provider's OpenAPI document, and on the lockfile. Nobody edits
either by hand, and findings about them are noise.

We also wrote a migrations lens, `review-lenses/review-migrations/SKILL.md`. It
should run, but only over our migrations. It has nothing to say about the rest
of the repository.

Do not change when reviews run or whether they block. Keep everything the
default lenses review today.

## Output Specification

- `plan.md` at the workspace root: which job this request is, which skill
  handles it, and why, in a few lines. Then what you changed and what a review
  now reads.
- Whatever files that job produces in the repository.
