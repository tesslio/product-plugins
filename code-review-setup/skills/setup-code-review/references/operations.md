# Operating the installed workflow

What to tell the user after the workflow is written, and the procedures for
changing or undoing it later. Pull out the parts that apply to what they chose.

## The token secret

The workflow reads a repository secret named `TESSL_TOKEN` and passes it to the
Action as the `tessl-token` input. It authenticates the Tessl CLI. Without it the
Action fails its input validation on the first run.

Create it from a Tessl API token:

```bash
gh secret set TESSL_TOKEN --repo <owner>/<repo>
```

An organization-level secret works too, as long as the repository is in its
selected-repositories list.

The token is never placed in a command argument, a log line, an output, or an
uploaded artifact.

## The permissions, and why each one

```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

| Permission | Why the Action needs it |
| --- | --- |
| `contents: read` | Resolve and check out the exact pull-request head |
| `pull-requests: write` | Publish one native pull-request review |
| `issues: write` | Publish and later clear a visible failure notice |

These apply to the automatic `GITHUB_TOKEN`, which the Action uses for
publication. Declaring the `permissions` block at all narrows the token to
exactly this list, so do not widen it and do not remove it.

## Branch protection, for gate mode

Enforce the gate with a **required status check** on the protected branch. Branch
protection lists checks by **job** name, not workflow name, so the entry to
require is `review`, or whatever the job is keyed in the installed file, rather
than `Tessl Code Review`. Requiring a name nothing reports enforces nothing while
looking configured.

A required check only does its job on a cadence that reviews every head. The
check is reported against the commit its run was triggered for, and only
`pull_request` runs are triggered against a pull-request head. A run started by a
`/tessl-review` comment or by `workflow_dispatch` is associated with the default
branch: it publishes a real review, but it does not report a check on the pull
request. On the manual-only and ready-once cadences, a head that had no
`pull_request` run therefore never gets the required check reported, and branch
protection holds the pull request waiting for a status that will not arrive.

Do not enforce it through review-state protection instead. The Action's approval
comes from GitHub Actions rather than a person, and a required-approvals rule
that counts it is not the control anyone intends.

Approval additionally needs the repository or organization setting that allows
GitHub Actions to create and approve pull requests
(Settings, Actions, General, Workflow permissions). Without it GitHub refuses the
review event. The Action does not lose the review when that happens: it publishes
the completed review as a visible comment, explains the configuration problem,
and fails the gate.

## Updating

Two things change over time, and they change independently.

**The pinned Action revision.** Read the target release's notes, then replace the
40-character SHA on the `uses:` line with the one the release publishes. Keep it a
full commit SHA. A tag or a branch name is a moving reference, and `canary` is an
experimental channel that can change CLI behavior without the compatibility
guarantees of a release.

**The policy.** Cadence is the `on:` block, the job `if:` guard, and
`cancel-in-progress`. Blocking is the `mode` input. What the reviewer looks for is
`profile` and `lenses`. Each is a small edit to the one caller workflow.

Re-running this skill against a repository that already has a caller performs an
update: it keeps the runner, timeout, job name, extra steps, any `model` or
`effort` input already set, and any compatible triggers, and changes only the
pinned SHA and whatever the interview decided.

## Removing

1. Delete the caller workflow file.
2. Delete the `TESSL_TOKEN` repository secret if nothing else uses it.
3. If gate mode was enabled, remove the job's check from branch protection.
   A required check that no workflow reports will block every pull request
   indefinitely, so do this before or with step 1.

Past reviews and comments stay on their pull requests. Nothing removes them.

## When something is wrong

| Symptom | Cause to check first |
| --- | --- |
| Nothing runs on a fork pull request | Expected. The Action rejects cross-repository pull requests, and a fork `pull_request` run receives no repository secrets either |
| Nothing runs on a `/tessl-review` comment, anywhere | The caller workflow is not on the default branch yet. `issue_comment` always runs the default-branch copy |
| Nothing runs on a `/tessl-review` comment, on one pull request | The comment is on an issue rather than a pull request, the body does not start with the command, the comment was edited rather than newly posted, or the commenter's author association is not `OWNER`, `MEMBER`, or `COLLABORATOR` |
| Two reviews appear per event | A second workflow also calls the Action. Putting both on one concurrency group only serializes them, it does not stop the second review |
| Gate check fails with the review posted as a plain comment | The repository setting that allows GitHub Actions to approve pull requests is off |
| The run fails immediately on input validation | `TESSL_TOKEN` is missing or empty, or `mode` is neither `advisory` nor `gate` |
| A required check sits at "expected, waiting for status" forever | Gate mode on a cadence that does not review every head. Only a `pull_request` run reports a check against the head. See the branch-protection section |
| A pull request stays blocked after pushing fixes | Gate mode on a cadence that does not review pushes. A `/tessl-review` round publishes a review but does not clear the required check |
