# Backtest: review-observability

Run over 12 merged pull requests in the payments service that already carry human review comments about diagnosability. Each pull request was reviewed at its original base and head, with the lens run on its own.

31 findings produced. Sorted below.

## Useful matches (6)

The lens raised something the original review also raised.

- #4471 the `catch` in `reconcileBatch` that returns an empty list on failure
- #4488 the retry loop that gives up after 5 attempts with no record
- #4502 the new provider call with no timing recorded
- #4519 the `debug`-level log on the payload validation failure path
- #4530 two early exits from the payout export that are not recorded

## Novel useful findings (2)

Real problems the original review missed.

- #4553 a scheduled job whose only failure signal is the process exit code
- #4561 a fallback branch that substitutes a default and continues silently

## False positives (19)

- 14 of the form "this function does not log". All were internal helpers whose only caller already logs the operation on entry and on failure. Example from #4477: "`normalizeAccountRef` performs a transformation with no logging; consider adding a debug log for the input and output." The caller logs both.
- 5 on pure functions with no I/O and no failure mode: formatters, comparators, and a currency rounding helper. Example from #4544: "`roundToMinorUnits` has no metric recording how often it is called."

## Unplaced findings (4)

Findings with no line to sit on, which arrived in the review summary rather than as inline comments. All four were verdicts on the change as a whole rather than anything an author could act on, for example on #4502: "Observability posture of this change is weak overall; the team should consider a broader instrumentation strategy for the settlement path."

## Misses (5)

In scope for this lens, raised by the original human review, not flagged by the lens.

- #4519 `throw new Error('invalid payload')` with no payload id, so a production failure cannot be traced back to the request
- #4536, #4547, #4558 three more thrown errors whose message names the failure but not the record, job, or account it happened on
- #4561 an error wrapped and rethrown with the original cause dropped
