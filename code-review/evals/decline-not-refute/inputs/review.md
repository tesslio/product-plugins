# Tessl Code Review, round 1: Changes approved

1. **minor** `src/import/csv.ts:2` The new filter handles the trailing newline,
   but there is no test covering empty or whitespace-only input, so the next
   change here can regress it unnoticed. Add a test for the empty-input case.
