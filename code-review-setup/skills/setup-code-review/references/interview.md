# The setup interview

Two questions. They are orthogonal, and every combination of the two is a valid
setup. Ask both, state the default, and keep the trade-offs to a sentence each.

## Question 1: when do reviews run?

| Option | What happens | Cost and latency | What the author has to remember |
| --- | --- | --- | --- |
| Manual only | Nothing runs until someone asks, by commenting `/tessl-review` on the pull request or by dispatching the workflow | Lowest. One review per explicit request | To ask. No review appears on its own |
| Ready once, plus mentions (default) | One review when the pull request opens or leaves draft, and another whenever someone comments `/tessl-review` | One review per pull request, plus requested rounds | To ask for a fresh round after pushing fixes |
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

- Enforce the gate by making the workflow's check a **required status check** in
  branch protection. Do not enforce it through review-state protection such as
  "require approval from someone with write access". The Action's approval comes
  from GitHub Actions, and treating it as a human approval is not what the gate
  is for.
- Approving requires the repository setting that allows GitHub Actions to create
  and approve pull requests. Without it, GitHub refuses the review event. The
  Action handles that refusal rather than failing silently: it publishes the
  completed review as a visible comment, explains the configuration problem, and
  still fails the gate. The review is never lost, but the gate stays red until
  the setting is turned on.

## The combination to spell out

Gate plus ready-once is the combination that surprises people, so state the
contract explicitly in the summary and leave it as a comment in the installed
workflow:

> A blocked pull request does not unblock itself. Pushing fixes does not trigger
> a new review. Comment `/tessl-review` to request a fresh round against the new
> head.

Gate plus manual is not a degraded setup. It is a deliberate pull-based mode:
nothing runs unless someone asks, and because the Action refuses to publish for a
superseded head, every merged head carries a converged review of exactly that
head.

Gate plus every-commit is the closest thing to continuous enforcement. It costs
the most, and the gate flips red and green as the branch moves.
