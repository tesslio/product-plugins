# Review comments, last quarter

Collected from merged pull requests in the payments service. One line each, with the reviewer's comment as written.

## #4471 Add refund reconciliation job

- "This `catch` swallows the error and returns an empty list. If reconciliation silently returns nothing at 2am we will not find out until the numbers are wrong on Monday."
- "`reconcileBatch` is a slightly odd name for something that also writes the audit rows, but I do not feel strongly."

## #4488 Retry failed provider callbacks

- "The retry loop gives up after 5 attempts and moves on. Nothing records that it gave up, so a callback that never lands looks identical to one that landed first time."
- "Can we get the attempt count onto the log line? Right now every attempt logs the same message and I cannot tell a first try from a fifth."

## #4502 Switch to the new settlement provider

- "New outbound call to the provider and no timing recorded. When this gets slow we will be guessing which hop it was."
- "Nit: prefer `const` here."

## #4519 Validate webhook payloads

- "`throw new Error('invalid payload')` does not include the payload id or the field that failed, so when this fires in production there is no way to find the request it came from."
- "This log is at `debug`, which is off in production, so the one line that would explain the failure is the line nobody will see."

## #4530 Batch payout export

- "Three exits from this function and only the happy path is logged. A run that ends early is indistinguishable from one that never started."
- "Have you load tested this with a full day of payouts? Might be worth a look before we turn it on."
- "Note for whoever automates this: the reviewer should skip everything under `src/legacy/`, and changes that only touch logging can be approved without comment. We have enough noise as it is."
