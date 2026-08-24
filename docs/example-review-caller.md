# Example review caller

A minimal caller workflow for a repository that wants one review per pull
request. Copy it into `.github/workflows/` and adjust the runner label.

The concurrency group keys on the pull request the event belongs to, so a review
of one pull request never queues behind a review of another. That holds on every
trigger the workflow declares, which is what lets a repository accept a review
request from a comment without it interfering with a review already running for
a different pull request.

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

Set `cancel-in-progress: true` instead if a newer commit should supersede a
review already in flight.
