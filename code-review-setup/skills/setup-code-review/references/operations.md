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
  checks: write
  issues: write
  pull-requests: write
```

| Permission | Why the Action needs it |
| --- | --- |
| `contents: read` | Resolve and check out the exact pull-request head |
| `checks: write` | Report the `Tessl Code Review` check on the reviewed head |
| `pull-requests: write` | Publish one native pull-request review |
| `issues: write` | Publish and later clear a visible failure notice |

Without `checks: write` the Action still reviews and still publishes, logs a
warning naming the missing permission, and reports no check. A gate has nothing
to enforce in that state, so treat the permission as required rather than
optional.

These apply to the automatic `GITHUB_TOKEN`, which the Action uses for
publication. Declaring the `permissions` block at all narrows the token to
exactly this list, so do not widen it and do not remove it.

## Branch protection, for gate mode

Enforce the gate with a **required status check** on the protected branch. The
entry to require is `Tessl Code Review`, the check the Action reports against the
head it reviewed.

Do not require the caller's job instead. A job status lands on the pull request
only for a `pull_request` run, so requiring it leaves every comment-driven or
dispatched round reporting nothing, and branch protection holds the pull request
waiting for a status that will not arrive. The Action resolves the reviewed head
itself, so its own check lands on that head whatever the trigger was, and the
gate holds on all three cadences.

What the cadence still decides is when a fresh verdict arrives. On manual-only
and ready-once, a head nobody has asked about carries no verdict yet, and the
pull request waits until a requested round reviews it.

Do not enforce it through review-state protection instead. The Action's approval
comes from GitHub Actions rather than a person, and a required-approvals rule
that counts it is not the control anyone intends.

Approval additionally needs the repository or organization setting that allows
GitHub Actions to create and approve pull requests
(Settings, Actions, General, Workflow permissions). Without it GitHub refuses the
review event. The Action does not lose the review when that happens: it publishes
the completed review as a visible comment, explains the configuration problem,
and fails the gate.

## What the check reports, once it is required

Four behaviors are worth stating before anyone relies on the check to hold a
branch:

- **The gate fails closed.** A review that reaches no approval verdict fails the
  check rather than passing the head through. Only a verdict approves.
- **A superseded run concludes neutral.** If the head moves while the review is
  running, the Action publishes nothing for the head it reviewed and asserts
  nothing about the head that replaced it. The job fails so an unpublished review
  cannot read as a completed one, and the new head is reviewed by whatever run
  covers it.
- **Neutral must not block.** The conclusions above assume a neutral check does
  not hold a required status. Confirm that against the branch protection rule or
  ruleset the repository actually uses before requiring the check.
- **A killed run leaves the check in progress.** A job timeout or a lost runner
  ends the run before it can conclude its check, and a check stuck in progress
  holds every pull request that requires it. Re-run the workflow: a later check
  of the same name replaces the abandoned one.

## Updating

Two things change over time, and they change independently.

**The pinned Action revision.** Resolve the target release to a commit SHA with
the lookup in the skill's proposal phase, and replace the 40-character SHA on the
`uses:` line with the result. Keep the pin a full commit SHA. A tag or a branch
name is a moving reference that hands `TESSL_TOKEN` to whatever it currently
points at, and a pre-release revision does not carry the compatibility guarantees
of a release.

The pin fixes the Action, not the Tessl CLI the Action installs. The Action
installs the current CLI release on every run, so CLI changes reach a repository
without any edit to its workflow.

**The policy.** Cadence is the `on:` block, the job `if:` guard, and
`cancel-in-progress`. Blocking is the `mode` input. What the reviewer looks for is
`profile` and `lenses`. Each is a small edit to the one caller workflow.

Re-running this skill against a repository that already has a caller performs an
update: it keeps the runner, timeout, job name, extra steps, any input the
interview does not decide, and any compatible triggers, and changes only the
pinned SHA and whatever the interview decided. A re-run that finds nothing to
change leaves the file untouched and says so.

This setup neither adds nor tunes an `effort` input; a repository that wants to
tune how hard its lenses think sets `effort` in its profile instead. A caller
that already carries the input keeps it.

## Removing

1. Delete the caller workflow file.
2. Delete the `TESSL_TOKEN` repository secret if nothing else uses it.
3. If gate mode was enabled, remove the `Tessl Code Review` check from branch
   protection. A required check that nothing reports will block every pull
   request indefinitely, so do this before or with step 1.

Past reviews and comments stay on their pull requests. Nothing removes them.

## When something is wrong

| Symptom | Cause to check first |
| --- | --- |
| Nothing runs on a fork pull request | Expected. The Action rejects cross-repository pull requests, and a fork `pull_request` run receives no repository secrets either |
| Nothing runs on an `@tessl-code-review` mention, anywhere | The caller workflow is not on the default branch yet. `issue_comment` always runs the default-branch copy |
| Nothing runs on an `@tessl-code-review` mention, on one pull request | The comment is on an issue rather than a pull request, the pull request is closed or merged, the comment was edited rather than newly posted, or the commenter's author association is outside the allowlist the workflow installs |
| Two reviews appear per event | A second workflow also calls the Action. Putting both on one concurrency group only serializes them, it does not stop the second review |
| Gate check fails with the review posted as a plain comment | The repository setting that allows GitHub Actions to approve pull requests is off |
| The run fails immediately on input validation | `TESSL_TOKEN` is missing or empty, or `mode` is neither `advisory` nor `gate` |
| A required check sits at "expected, waiting for status" forever | Branch protection requires the caller's job rather than `Tessl Code Review`, or the workflow does not grant `checks: write`. Either way nothing reports the required name |
| A required check sits "in progress" and never finishes | The run was killed before it concluded, by the job timeout or a lost runner. Re-run the workflow to replace the check |
| A pull request stays blocked after pushing fixes | Gate mode on a cadence that does not review pushes. The new head has no verdict yet, so mention `@tessl-code-review` to have it reviewed |
