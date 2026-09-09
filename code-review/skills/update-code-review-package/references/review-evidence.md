# Review-package update evidence

Use the evidence manifest supplied by the caller. Respect its cutoff, history
window, byte limits, and named unavailable sources. Do not expand the search
silently.

## Preserve attribution

For each useful item, retain:

- pull request and review-round identity;
- the code revision the comment reviewed;
- actor kind: human, Tessl reviewer, or another agent;
- thread state and replies;
- recorded disposition when present: fixed, refuted, declined, or unverified.

A resolved thread records workflow state, not agreement. A decline can confirm
the concern while placing it outside that pull request's goal. A later revision
can make an earlier comment stale.

## Classify before editing

- **Missed concern:** a concrete problem the active lenses did not raise.
- **Noisy finding:** a raised concern that did not reproduce or fell below the
  lens's stated consequence bar.
- **Existing-rule application failure:** the active lens already states the
  right guidance, but the review missed or misapplied it.
- **Valid but declined:** the concern reproduced, but the pull request did not
  owe the fix. Do not rewrite it as a false positive.
- **Insufficient evidence:** the available revision, context, or reconciliation
  cannot settle what happened.

Change package guidance only for missed concerns, repeatable noise, or stale
instructions supported by the bounded set. Report application failures and
insufficient evidence without encoding individual comments into permanent
rules.

## Validation

Replay only against the exact revision a review saw. Keep the target feedback
out of the reviewer's prompt and compare the new result afterward. A useful
comparison distinguishes reproduced findings, new useful findings, false
positives, and misses. Report the number of cases actually checked and all
unavailable cases. Do not infer quality from a clean lint, a resolved thread,
or a count without reading the findings.
