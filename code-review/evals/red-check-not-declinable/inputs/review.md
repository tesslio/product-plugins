# Tessl Code Review, round 1: Changes requested

1. **major** `src/money/format.ts:3` The check is red: formatPrice(1200, '$')
   renders '$12' and the test expects '$12.00'. Whole-unit amounts lose their
   decimals. Format with two fixed decimals.

2. **major** `test/legacy.test.ts:3` The check is red: legacyHeader returns a
   semicolon-separated header and the test expects commas. Fix the exporter.
