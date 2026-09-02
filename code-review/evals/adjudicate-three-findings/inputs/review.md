# Tessl Code Review, round 1: Changes requested

1. **major** `src/orders/cancel.ts:7` Nothing checks the order's current status.
   An order already shipped or delivered can be cancelled, leaving a shipped
   parcel against a cancelled order. Refuse when status is shipped or delivered.

2. **major** `src/orders/cancel.ts:3` `cancelOrder` takes a userId but nothing
   guarantees the caller is authenticated, so an unauthenticated request can
   cancel any order it can name.

3. **minor** `src/orders/refund.ts:4` `processor.refund` has no retry or
   idempotency handling. A transient failure loses the refund. Since this PR
   touches order lifecycle, add retry with an idempotency key here.
