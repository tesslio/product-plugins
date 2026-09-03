---
name: respond-to-code-review
description: Answer a Tessl Code Review on a pull request the responder authored. Decides what each finding deserves, fixes, refutes, or declines it with a reason, replies on the thread, and keeps the pull request doing what it was opened to do. Use when review feedback has arrived on an open pull request and the responder is the one answering it, for example "address the review", "respond to the findings", "Tessl left comments", "deal with the review comments", "the check is red and there are findings", or when review rounds keep coming and are not converging. Not for performing a review of someone else's change; that is tessl code review.
---

# Responding to a Tessl Code Review

A Tessl Code Review arrives as one pull-request review: a summary with a
verdict, either changes approved or changes requested, and inline comments on
changed lines, each a finding with a severity. Findings graded `critical` or
`major` are what made the verdict request changes. Findings marked advisory, or
graded `minor` or `nit`, did not. A later round reconciles earlier findings:
each is reported fixed, still open, or come back.

## Start from the goal, not the findings

Before reading a single finding, state two things: what this pull request was
opened to do, and what it does now.

The goal comes from the issue the pull request implements. If there is none,
use the pull-request description **as it stood when the pull request opened**,
never the current one. A responder that has been widening the description as it
works will otherwise read its own scope creep back as the goal.

What it does now is the diff: the files and lines it touches, and how that has
grown since the first review round.

If those two have diverged, **the divergence is the first thing to address**,
ahead of any finding. A pull request that has grown past its goal does not get
back on track by servicing more findings.

## A finding is a claim, not a mandate

The review is advisory. A finding can be right, wrong, stale, or right but not
here, and its severity label says how the reviewer weighted it, not whether it
is true or in scope. Work the findings, not the count: addressing all of them is
not the goal and is not evidence you did the job. A turn that changes no code is
a complete turn. If every finding is invalid or out of scope, say so in the
replies and stop rather than manufacturing a change to show effort.

## Adjudicate each finding

**Verify before you dispose.** A finding claims the code has a specific flaw,
gap, or behavior. Settle whether the claim is true against the actual code
before choosing a disposition.

For a behavioral claim, a bug, a wrong output, a crash, an unsafe path, verify by
tracing the execution: name the input or state that triggers it, the path that
reaches the changed lines, and the wrong outcome. If you cannot trace all three,
the claim did not reproduce. A claim you cannot check at all, because the
evidence is not in the repository or needs access you lack, is unverified, not
refuted. It gets no disposition yet: reply with what you would need to check it,
leave its thread open, and list it under what a human still has to decide.

For a non-behavioral claim, missing coverage, incomplete documentation, a
maintainability concern, a name, the standard is evidence rather than execution.
Check what the review says is absent or inadequate against what is actually in
the code, tests, or docs.

A disposition reached without this check is a guess wearing a label.

Then exactly one of:

- **Fix.** The claim is true and in scope. Make the change inside the pull
  request's existing boundary. Never widen scope to satisfy a finding.
- **Refute.** The claim is false. It did not reproduce, misreads the code, or
  describes behavior the system does not have. Never for a finding that is true
  and unwelcome.
- **Decline.** The claim is true and you are not actioning it here. The code
  stays, with a rationale anchored, strongest first, on:
  1. the goal the pull request was opened to serve;
  2. an explicit maintainer decision, or a rule the project documents;
  3. your own judgment, a smallest-change or not-yet call, stated plainly enough
     that a maintainer can overrule it.

  If the concern is real but belongs elsewhere, raise it as follow-up work and
  say where it went.

Declining is not dismissal. It is how a pull request keeps its shape while a
review runs, and using it is part of the job.

**Refute and decline are not interchangeable.** Refuting a true finding puts a
falsehood on the record; declining a false one concedes something never owed.
Settle whether the claim is true first, then decide what to do about it.

In short, for every finding:

1. Restate the claim in one line.
2. Verify it against the code: trace it, or check the evidence.
3. True and in scope: fix. False: refute. True and not here: decline, with an anchor.
   Cannot be checked: no disposition; say what is missing and leave it open.
4. Write the reply for its thread.

## Some findings cannot be declined

A finding that names a broken build, a failing test, a violated invariant the
project documents, or work the originating issue explicitly asked for must be
fixed, once you have established that the pull request caused it. Check whether
the failure reproduces on the base branch without your changes. If it does, it
is pre-existing or environmental and may be declined with that evidence. If it
reproduces only with your changes, the pull request introduced it, and it is
fixed here or escalated to a human when the fix needs scope this pull request
does not have.

A red check caused by this pull request is not a matter of opinion. "Out of
scope" is not an answer to it, and neither is a green local rerun.

## Adjudicate the root, not the leaf

When a finding is a consequence of code an earlier finding asked for, the
finding to adjudicate is the earlier one. A run of findings inside work the goal
never covered is evidence that the first acceptance was wrong. Reopen that
decision, say so, and take the work back out, rather than answering each
consequence as it arrives.

## Advisory findings

Findings marked advisory, or graded `minor` or `nit`, are not change requests.
Act on one only when it is plainly right.

## Reply on the thread

Every finding gets a reply on its own comment thread, so the next round can
reconcile it:

- Fixed: what changed, in one or two sentences. The next round checks the code,
  not your word.
- Refuted: what failed to reproduce, or what the finding misread. Name the line
  or the behavior.
- Declined: the anchor you used and, if deferred, where the follow-up went.
- Unverified: what evidence or access would settle it, and who can supply it.

Resolve a thread only when its disposition is settled. Leave it open when the
reviewer asked a question that still needs an answer, or when a human still has
to decide. A finding skipped silently returns next round as a finding you
skipped.

## Ask for the next round, or for approval

When every finding has a reply and the code is pushed, ask for a fresh round by
commenting `@tessl-code-review` on the pull request. The comment must begin with
the mention; a mention inside a quote or a code span asks for nothing. Who may
ask is decided by the repository's caller workflow.

Some repositories let a comment beginning `@tessl-code-review approve` request
approval without another review round. Use it only when the repository's
documented review policy permits it for the paths the pull request touches, and
only after every finding has a disposition. It is a short circuit for a settled
review, not a way past an open one.

## When rounds stop converging

Watch the shape of the review across rounds, not just this one. The loop is not
converging when the same concern returns after you have answered it, when a
round's findings are mostly about the previous round's fixes, or when the diff
keeps growing while the goal stays still.

Another round will not fix any of those. Stop, summarize what is settled and what
is disputed, and put it in front of a human. A disagreement escalated early costs
less than five more rounds of agreeing.

## Finishing a turn

Record, for every finding you took: which finding, what you decided, and why.
Then say what is left: work you deferred and where it went, and anything a human
still needs to decide.
