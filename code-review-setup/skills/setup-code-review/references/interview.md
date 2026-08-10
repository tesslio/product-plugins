# The setup interview

Two questions. They are orthogonal. Ask both, state the default, and keep the
trade-offs to a sentence each.

Their consequences are not independent, though: what a gate can enforce depends
on the cadence. Read "What gate mode can actually enforce" below before proposing
any gate setup.

## Question 1: when do reviews run?

| Option | What happens | Cost and latency | What the author has to remember |
| --- | --- | --- | --- |
| Manual only | Nothing runs until someone asks, by mentioning `@tessl-code-review` in a comment on the pull request or by dispatching the workflow | Lowest. One review per explicit request | To ask. No review appears on its own |
| Ready once, plus mentions (default) | One review when the pull request opens or leaves draft, and another whenever someone mentions `@tessl-code-review` in a comment | One review per pull request, plus requested rounds | To ask for a fresh round after pushing fixes |
| Every commit | Adds a review on every push to the pull-request branch, with the in-flight run canceled when a newer commit lands | Highest. Scales with how often the branch is pushed | Nothing |

Every-commit is safe to run without extra admission logic. The Action verifies
the pull-request head immediately before publishing and refuses to publish for a
superseded head, and its publication is idempotent, so a canceled or retried run
cannot leave a duplicate or stale review behind.

## Question 2: do findings block?

| Option | What happens | Effect on merging |
| --- | --- | --- |
| Advisory (default) | The Action publishes a `COMMENT` review. Findings never fail the check | None. The review is information |
| Gate | A converged review approves the pull request and the check passes. A non-converged review requests changes, publishes the full review, and fails the check | Merging is blocked while the check is required and failing |

Gate mode has two prerequisites the workflow file cannot satisfy on its own, so
raise them during the proposal:

- Enforce the gate by making the job's check a **required status check** in
  branch protection. Branch protection matches the **job** name, not the workflow
  name, so require `review` (or whatever the job is keyed in the installed file).
  Do not enforce it through review-state protection such as "require approval
  from someone with write access". The Action's approval comes from GitHub
  Actions, and treating it as a human approval is not what the gate is for.
- Approving requires the repository setting that allows GitHub Actions to create
  and approve pull requests. Without it, GitHub refuses the review event. The
  Action handles that refusal rather than failing silently: it publishes the
  completed review as a visible comment, explains the configuration problem, and
  still fails the gate. The review is never lost, but the gate stays red until
  the setting is turned on.

## What gate mode can actually enforce

A required status check is evaluated against the pull request's current head SHA.
A workflow run reports its check against the commit it was triggered for, and
only `pull_request` runs are triggered against a pull-request head. A run started
by `issue_comment` or `workflow_dispatch` is associated with the default branch,
so its result does not land on the pull request's head and cannot satisfy or fail
a required check there.

Two consequences, both of which have to reach the user before they choose:

- **A mention-driven round cannot clear a required check.** It publishes a real
  review, and in gate mode a converged one still attempts to approve, but the
  check itself stays as it was.
- **A head with no `pull_request` run has no check to satisfy.** Branch
  protection reports the required check as expected and never received, which
  blocks the pull request until a run is triggered for that head.

So the pairings behave like this:

| Gate with | What enforcement you get |
| --- | --- |
| Every commit | Works as written. Every head gets a `pull_request` run, so the required check is always reported against the head being merged |
| Ready once | The first head is gated. After any push, the new head has no run and the required check is never reported, so the pull request stays blocked and no comment can clear it |
| Manual only | No `pull_request` run ever happens, so a required check on this job is never reported for any head |

**Recommend every-commit whenever the user wants gate mode enforced by a required
status check.** If they want gate on another cadence, say plainly what they get:
the review outcome is published and visible, and a non-converged review still
requests changes, but the required-check mechanism does not do the blocking. In
that case the honest enforcement story is the requested-changes review state, not
a status check, which is a different control from the one this setup recommends.

Do not paper over this by adding a step that reports a check against the head
yourself. That is a second execution path, and it belongs in the Action if it
belongs anywhere.

## The contract to spell out

Whenever gate mode runs on a cadence that does not review pushes, state the
contract in the summary and leave it as a comment in the installed workflow:

> A blocked pull request does not unblock itself. Pushing fixes does not trigger
> a new review, and a mention-driven round does not clear a required status
> check.

Gate plus every-commit is the closest thing to continuous enforcement. It costs
the most, and the gate flips red and green as the branch moves.
