# We want Tessl to look at our pull requests

## Problem Description

We heard Tessl can review pull requests. This repository has one workflow,
`.github/workflows/ci.yml`, which runs the tests. Nothing reviews the code.

Set Tessl Code Review up as a GitHub Action, the same way our tests run. The
review should not block merging for now. The Tessl API token is stored as the
repository secret `TESSL_TOKEN`.

## Output Specification

- `plan.md` at the workspace root: which job this request is, which skill
  handles it, and why, in a few lines. Then what you did, and what is left for
  us to do.
- Leave `.github/workflows/ci.yml` unchanged.
