# Backtest: review-observability

Run over 12 merged pull requests in the payments service that already carry human review comments about diagnosability. Each pull request was reviewed at its original base and head, with the lens run on its own.

31 findings produced, sorted below by whether they were worth having.

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

Each of these was checked against the code and is not a problem. Nine of the nineteen:

- #4477 "`normalizeAccountRef` performs a transformation with no logging; consider adding a debug log for the input and output." Its one caller logs the operation on entry and on failure.
- #4544 "`roundToMinorUnits` has no metric recording how often it is called." A rounding helper: no I/O, nothing that can fail.
- #4481 "`toProviderRef` does not log the mapping it performs." Called only from the settlement handler, which logs entry and failure.
- #4548 "`compareSettlementDates` emits no telemetry." A comparator used in a sort.
- #4489 "`splitBatch` does not record how many batches it produced." The caller logs the batch count when the run completes.
- #4551 "`formatAccountLabel` has no logging." Builds a display string from its arguments.
- #4495 "`resolveCurrency` has no logging on the lookup." The caller logs the resolved currency and the failure path.
- #4557 "`isSettlementWindowOpen` records nothing about its decision." Compares two timestamps and returns a boolean.
- #4508 "`buildExportRow` does not log the row it constructs." The export loop logs each row as it is written.

The remaining ten are more of the same.

## Unplaced findings (4)

No line to sit on, so these arrived in the review summary rather than as inline comments.

- #4502 "Observability posture of this change is weak overall; the team should consider a broader instrumentation strategy for the settlement path."
- #4519 "This change would benefit from a more systematic approach to error visibility."
- #4530 "Instrumentation in the export path is thin relative to the risk it carries."
- #4553 "Overall the diagnosability of this change is below what we would want for a scheduled job."

## Misses (5)

Raised by the original human review, in scope for this lens, and not flagged.

- #4519 `throw new Error('invalid payload')`, with no payload id
- #4536 `throw new Error('settlement failed')`, with no settlement id
- #4547 `throw new Error('export aborted')`, with no job id
- #4558 `throw new Error('account lookup failed')`, with no account reference
- #4561 an error wrapped and rethrown with the original cause dropped
