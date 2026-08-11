# Caller workflow templates

One template per cadence. They are deliberately near-identical: the cadence
changes the `on:` block, the job's `if:` guard, and `cancel-in-progress`, and
nothing else. The blocking choice changes one input, `mode`.

Install to `.github/workflows/tessl-code-review.yml` unless the repository has an
existing caller or a different naming convention.

Adjust `runs-on` and `timeout-minutes` to match the repository's other workflows,
and replace `<full-commit-sha>` with the SHA resolved from the current supported
release. A template is not installable while that placeholder is still in it: if
no release resolves, stop rather than writing the file. Everything else is the
contract and should be left alone.

`tesslio/code-review` on the `uses:` line is the Action repository named in
SKILL.md, and it is the one thing in these templates that changes at public
launch.

The `@tessl-code-review` mention token is part of the Action's contract, not a
local naming choice. The review the Action publishes tells reviewers to mention
`@tessl-code-review` when fixes or replies are ready, so a caller that listens
for anything else installs a review that teaches a token its own workflow
ignores. Do not rename it.

## What differs between the three

| | Manual only | Ready once plus mentions | Every commit |
| --- | --- | --- | --- |
| `pull_request` trigger | absent | `[opened, reopened, ready_for_review]` | `[opened, reopened, ready_for_review, synchronize]` |
| `cancel-in-progress` | `false` | `false` | `true` |
| `if:` guard | no `pull_request` clause | includes it | includes it |

## Cadence: ready once plus mentions (default)

```yaml
name: Tessl Code Review

# One review when the pull request is ready for review, and another whenever
# someone mentions @tessl-code-review in a comment on it. Pushing new commits
# does not start a review on its own.
on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      pr-number:
        description: Pull-request number to review
        required: true

# The minimum the Action needs: read the head to review it, report the
# Tessl Code Review check on it, publish a native review, and post or clear a
# visible failure notice.
permissions:
  contents: read
  checks: write
  issues: write
  pull-requests: write

# One review at a time per pull request. A newer run waits instead of
# superseding the running one. GitHub holds only one waiting run per group, so
# a third request arriving during a run replaces the one already waiting.
concurrency:
  group: tessl-code-review-${{ github.event.pull_request.number || github.event.issue.number || inputs['pr-number'] }}
  cancel-in-progress: false

jobs:
  review:
    # Run for a ready pull request, for an explicit dispatch, or for a comment
    # posted on a pull request that mentions @tessl-code-review, by an owner, an
    # organization member, or an invited collaborator. The author-association
    # check keeps the mention from being driven by arbitrary commenters. The
    # body match is a plain substring, so a comment naming a longer handle that
    # starts with the token also starts a round.
    if: >-
      (github.event_name == 'pull_request' && github.event.pull_request.draft == false) ||
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'issue_comment' &&
        github.event.issue.pull_request != null &&
        contains(github.event.comment.body, '@tessl-code-review') &&
        contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'), github.event.comment.author_association))
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      # Pinned to a full commit SHA, resolved from the current supported Tessl
      # Code Review release when this workflow was written, and changed only as
      # a reviewed update. The Action checks out the pull-request head itself,
      # so this job needs no checkout step.
      - uses: tesslio/code-review@<full-commit-sha>
        with:
          tessl-token: ${{ secrets.TESSL_TOKEN }}
          # Named review profile. The standard profile is the supported default.
          profile: standard
          # advisory publishes a COMMENT review. No review outcome fails this
          # check, though a technical failure to run or publish still does.
          mode: advisory
          # Optional. A JSON array replaces the profile's lens selection with an
          # exact ordered list.
          # lenses: >-
          #   ["tessl/code-review@0.0.3#review-correctness-and-data-integrity"]
          #
          # Supplies the pull-request number for events that carry no
          # pull-request context. Empty on pull_request events, where the Action
          # resolves the pull request itself.
          pr-number: ${{ github.event.issue.number || inputs['pr-number'] }}
```

## Cadence: manual only

```yaml
name: Tessl Code Review

# Nothing runs until someone asks. Mention @tessl-code-review in a comment on a
# pull request, or dispatch this workflow with a pull-request number.
on:
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      pr-number:
        description: Pull-request number to review
        required: true

permissions:
  contents: read
  checks: write
  issues: write
  pull-requests: write

concurrency:
  group: tessl-code-review-${{ github.event.issue.number || inputs['pr-number'] }}
  cancel-in-progress: false

jobs:
  review:
    # Run for an explicit dispatch, or for a comment posted on a pull request
    # that mentions @tessl-code-review, by an owner, an organization member, or
    # an invited collaborator.
    if: >-
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'issue_comment' &&
        github.event.issue.pull_request != null &&
        contains(github.event.comment.body, '@tessl-code-review') &&
        contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'), github.event.comment.author_association))
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: tesslio/code-review@<full-commit-sha>
        with:
          tessl-token: ${{ secrets.TESSL_TOKEN }}
          profile: standard
          mode: advisory
          pr-number: ${{ github.event.issue.number || inputs['pr-number'] }}
```

## Cadence: every commit

```yaml
name: Tessl Code Review

# A review on every push to a ready pull request, plus requested rounds. The
# in-flight review is canceled when a newer commit lands.
on:
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      pr-number:
        description: Pull-request number to review
        required: true

permissions:
  contents: read
  checks: write
  issues: write
  pull-requests: write

# Superseding a run per pull request is safe here: the Action verifies the head
# immediately before publishing and refuses to publish for a superseded head,
# and its publication is idempotent, so no duplicate or stale review survives a
# cancellation or a retry.
concurrency:
  group: tessl-code-review-${{ github.event.pull_request.number || github.event.issue.number || inputs['pr-number'] }}
  cancel-in-progress: true

jobs:
  review:
    if: >-
      (github.event_name == 'pull_request' && github.event.pull_request.draft == false) ||
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'issue_comment' &&
        github.event.issue.pull_request != null &&
        contains(github.event.comment.body, '@tessl-code-review') &&
        contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'), github.event.comment.author_association))
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: tesslio/code-review@<full-commit-sha>
        with:
          tessl-token: ${{ secrets.TESSL_TOKEN }}
          profile: standard
          mode: advisory
          pr-number: ${{ github.event.issue.number || inputs['pr-number'] }}
```

## Applying the gate choice

Gate mode is one input change on any of the three templates. Replace the
`mode: advisory` line on the Action step, keeping its indentation:

```yaml
          mode: gate
```

Before installing it, read "What gate mode enforces" in
[interview.md](interview.md). The Action reports the `Tessl Code Review` check
against the head it reviewed on every trigger, so the gate holds on all three
cadences. What the cadence decides is when a fresh verdict arrives.

When the cadence is manual only or ready once plus mentions, also record the
invocation contract where the pull-request author will read it, immediately above
the `on:` block:

```yaml
# Gate mode: changes approved passes the Tessl Code Review check, changes
# requested fails it. A blocked pull request does not unblock itself, because
# pushing commits does not start a review. Mention @tessl-code-review in a
# comment to have the new head reviewed and the check reported against it.
```

Gate mode also needs two things this file cannot set. Both belong in the summary
you give the user:

- the Action's own check, `Tessl Code Review`, made a required status check in
  branch protection. Never the caller's job, which reports nothing on a
  comment-driven or dispatched round;
- the repository setting that allows GitHub Actions to create and approve pull
  requests.

## Notes on the shared parts

**The mention guard.** `issue_comment` fires for issues as well as pull requests,
for every comment regardless of body, and for any commenter. The guard narrows it
to all three of: a comment on a pull request, a body carrying
`@tessl-code-review`, and a commenter with `OWNER`, `MEMBER`, or `COLLABORATOR`
association. The token itself is fixed by the Action, so the part to discuss with
the user is the association allowlist, not the token.

The match is case-sensitive and can sit anywhere in the body, so
`@tessl-code-review` fires and `please take another look @tessl-code-review`
fires too. It is a plain substring match, so a body naming a longer handle that
starts with the token starts a round as well. Because the trigger is
`types: [created]`, editing an existing comment to add the mention does nothing.
Mention both when explaining the trigger, since each one surprises someone.

`issue_comment` runs the copy of the workflow on the **default branch**, not the
copy on the pull-request branch. The mention trigger therefore does nothing at
all until the caller workflow is merged, and edits to the guard take effect only
once they land on the default branch.

Author association is a proxy, not a permission check. `MEMBER` means a member
of the owning organization, which in an organization with open membership is not
the same as write access to this repository. The three alternatives, which the
skill puts to the user rather than deciding for them:

- keep the `OWNER`, `MEMBER`, `COLLABORATOR` allowlist, the recommended default;
- drop the association condition, so any commenter on a pull request can start a
  review;
- query the commenter's permission level through the API instead, which is
  stricter than association but costs an extra call and a token that can read it.

Whichever the user picks, the mention round runs privileged and spends the
repository's Tessl credits, which is the reason the choice is worth making
deliberately.

**Draft pull requests.** The `draft == false` check means an opened draft is not
reviewed and the `ready_for_review` transition is what starts the first review.
Drop the clause if the repository wants drafts reviewed too.

**Forks.** The Action rejects cross-repository pull requests before running a
review, so a repository whose contributions arrive as fork pull requests gets no
reviews from this workflow on any trigger. That rejection is the control, and it
is worth being precise about why, because the two triggers differ:

- On `pull_request`, a fork run additionally receives no repository secrets, so
  `tessl-token` would be empty even if the Action allowed it.
- On `issue_comment`, the run is not a fork run at all. It executes on the base
  ref with repository secrets and a writable token, including when the comment
  sits on a fork pull request. Here the Action's cross-repository rejection is
  the only thing standing between an outside pull request and a privileged run,
  which is why the association allowlist is the recommended default for a
  repository that takes fork pull requests.

Do not reach for `pull_request_target` to work around any of this: it runs with a
privileged token in the base repository's context against untrusted head code,
which is exactly the trust boundary the Action is built to keep.

**Outputs.** Later steps in the same job can read the Action's `status`,
`head-sha`, `review-id`, `result-path`, `publication-path`, and `result-artifact`
outputs. Add such a step only when the user asks for one, and give the Action
step an `id` when you do.
