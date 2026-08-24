# The setup interview

Two questions. They are orthogonal. Ask both, state the default, and keep the
trade-offs to a sentence each.

Every pairing of them is installable. What the cadence decides is when a fresh
verdict arrives, which changes what a blocked pull request has to do to become
unblocked. Read "What gate mode enforces" below before proposing any gate setup.

## Question 1: when do reviews run?

| Option | What happens | Cost and latency | What the author has to remember |
| --- | --- | --- | --- |
| Manual only (dispatch and mentions) | Nothing runs until someone asks, by mentioning `@tessl-code-review` in a comment on the pull request or by dispatching the workflow with a pull-request number. Both request paths are part of this cadence | Lowest. One review per explicit request | To ask. No review appears on its own |
| Ready once, plus mentions (default) | One review when the pull request opens, reopens, or leaves draft, and another whenever someone mentions `@tessl-code-review` in a comment | One review per pull request, plus requested rounds | To ask for a fresh round after pushing fixes |
| Every commit | Adds a review on every push to the pull-request branch, with the in-flight run canceled when a newer commit lands | Highest. Scales with how often the branch is pushed | Nothing |

Every-commit is safe to run without extra admission logic. The pull-request head
is verified immediately before publishing, publication is refused for a
superseded head, and publication is idempotent, so a canceled or retried run
cannot leave a duplicate or stale review behind.

## Question 2: do findings block?

| Option | What happens | Effect on merging |
| --- | --- | --- |
| Advisory (default) | A `COMMENT` review is published. Findings never fail the check | None. The review is information |
| Gate | A review that approves the changes approves the pull request and the check passes. A review that requests changes publishes the full review and fails the check | Merging is blocked while the check is required and failing |

Blocking is three settings rather than one, and this question decides only the
middle one. `requestChangesAt` in a YAML profile decides which findings request
changes, `mode` decides whether the Action's check then fails, and branch
protection decides whether a failing check holds the pull request. A repository
that sets no threshold gates at `major` on every round, so a Minor is published
as a suggestion and does not hold the pull request.

Do not turn that into a third interview question. Name the key when the user
picks gate, in one line, so they know the bar exists and where it lives, and
point at [file-profiles.md](file-profiles.md) for the values. Most repositories
should leave it at the default, and a repository that wants Minors held on every
round sets `requestChangesAt: minor` in a profile whenever it is ready to.

Gate mode has two prerequisites the workflow file cannot satisfy on its own, so
raise them during the proposal:

- Enforce the gate by making the Action's own check a **required status check**
  in branch protection. The name to require is `Tessl Code Review`, the check the
  Action reports against the head it reviewed. Never require the caller's job
  instead: a job status only lands on the pull request for a `pull_request` run,
  so requiring it turns every comment-driven or dispatched round into a check
  that never arrives.
  Do not enforce it through review-state protection such as "require approval
  from someone with write access". The Action's approval comes from GitHub
  Actions, and treating it as a human approval is not what the gate is for.
- Approving requires the repository setting that allows GitHub Actions to create
  and approve pull requests. Without it, GitHub refuses the review event. The
  refusal is handled rather than failing silently: the completed review is
  published as a visible comment, the configuration problem is explained, and the
  gate still fails. The review is never lost, but the gate stays red until
  the setting is turned on.

## What gate mode enforces

The Action reports its own check run, named `Tessl Code Review`, against the
pull-request head it resolved, on every trigger. A comment-driven or dispatched
round resolves the same head a `pull_request` run would, so its verdict reaches
the pull request whatever started it. Requiring that check enforces the gate on
all three cadences.

Gate mode also fails closed: an outcome carrying no approval verdict fails the
check rather than passing a head that nothing judged.

What the cadence decides is when a fresh verdict arrives:

| Gate with | What the user gets |
| --- | --- |
| Every commit | Every push is reviewed, so every head carries a verdict and the check clears itself once the findings are addressed |
| Ready once | The first ready head is reviewed. A later push produces a head with no verdict yet, and branch protection holds the pull request until a requested round reviews it |
| Manual only | No head carries a verdict until someone asks, so branch protection holds every pull request until the first round runs against its current head |

**Recommend every-commit when the user wants the gate to keep up with the branch
on its own.** On the other two cadences the gate is just as real. Say plainly:
clearing the gate is a deliberate act. Someone mentions `@tessl-code-review` or
dispatches the workflow, the new round reviews the current head, and that
verdict is what the required check reports for that head. Nothing about the gate
is weaker on these cadences. It waits to be asked.

Do not add a step that reports a check of your own. The Action already reports
one against the head it reviewed, and a second is a second execution path.

## The contract to spell out

Whenever gate mode runs on a cadence that does not review pushes, state the
contract in the summary and leave it as a comment in the installed workflow:

> A blocked pull request does not unblock itself. Pushing fixes does not start a
> review, so mention `@tessl-code-review` on the pull request to have the new
> head reviewed and the check reported against it.

Gate plus every-commit is the closest thing to continuous enforcement. It costs
the most, and the gate flips red and green as the branch moves.
