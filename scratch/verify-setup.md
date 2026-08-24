# Scratch: verify the Code Review setup

Throwaway file for checking that the installed lenses fire on a real pull
request. Delete with the branch.

## Example caller

Paste this into `.github/workflows/` to review one pull request at a time. The
concurrency group keys on the pull request, so a review of one pull request
never queues behind a review of another, on any of the three triggers.

```yaml
name: Example Review

on:
  pull_request:
    types: [opened]
  pull_request_review_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      pr-number:
        required: true

concurrency:
  group: example-review-${{ github.event.issue.number }}
  cancel-in-progress: false

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - run: echo "reviewing PR ${{ github.event.issue.number }}"
```
