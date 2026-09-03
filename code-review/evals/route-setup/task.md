# We want Tessl to look at our pull requests

## Problem Description

We heard Tessl can review pull requests. This repository has one workflow,
`.github/workflows/ci.yml`, which runs the tests. Nothing reviews the code.

Make it so that Tessl reviews our pull requests. We do not have strong opinions:
take whatever defaults you recommend, but tell us what you chose. The review
should not block merging for now. The Tessl API token is stored as the
repository secret `TESSL_TOKEN`. The team pins third-party actions to the
reference the vendor recommends.

## Output Specification

- `plan.md` at the workspace root: which job this request is, which skill
  handles it, and why, in a few lines. Then the choices you made on our behalf.
- Whatever files that job produces in the repository.
- Leave `.github/workflows/ci.yml` unchanged.
