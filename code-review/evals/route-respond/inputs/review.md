# Tessl Code Review, round 1: Changes requested

## Findings

1. **major** `src/cart/discounts.ts:14` A percent discount above 100 (for example
   a misconfigured 150) makes `gross * (1 - 1.5)` negative, so `lineTotal`
   returns a negative total and the invoice shows a refund. Clamp the
   percentage, or the result, at zero as the fixed branch already does.

2. **minor** `src/cart/discounts.ts:18` `applyDiscount` mutates the `cart` it is
   given, so callers holding the original see discounted prices. Return a new
   object instead.

3. **minor** `src/cart/tax.ts:2` `taxCents` still returns fractional cents.
   Since this PR introduces `roundCents`, apply it here too so the invoice is
   consistent.
