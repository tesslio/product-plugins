---
name: review-test-risk
description: Review a diff for test risk — changed behaviour without meaningful tests, bug fixes without a regression test, async/error/edge branches left uncovered, and brittle tests that assert implementation trivia instead of behaviour. Use as a test-coverage review lens in `tessl change review` or a GitHub Actions review workflow. Reports high-confidence, file-anchored findings.
---

# Review Test Risk

A test-coverage review lens for `tessl change review`. Review the diff for gaps
between what the change does and what its tests actually exercise, and report
concrete, actionable findings.

## Stance

- Review the diff first. Read an existing test file only to confirm whether a
  changed behaviour is covered.
- Judge what the tests exercise, not how many there are. A passing test that
  never reaches the changed line is a gap.
- Keep findings high-confidence. Name the changed behaviour and the missing or
  weak test.
- If the change is adequately tested, say so in one line.

## What to look for

1. **Changed behaviour without meaningful tests.** New or modified logic with no
   test that reaches it, or a test that asserts only that the code runs.
2. **Bug fixes without a regression test.** A fix to a reported or evident bug
   with no test that would have failed before the fix and passes after.
3. **Uncovered branches.** Async paths, error and rejection handling, early
   returns, and edge cases (empty, null, boundary, large input) introduced by
   the change but never asserted.
4. **Brittle tests.** Assertions on implementation trivia — exact log strings,
   call counts, private fields, mock internals, or incidental ordering — that
   break on safe refactors without protecting behaviour.
5. **Weakened or deleted coverage.** Tests removed, skipped, or loosened
   alongside a behaviour change, hiding a regression.

## How to report

- Anchor each finding to the changed line whose behaviour is untested, or to the
  brittle assertion.
- Name the specific case to cover (the error branch, the boundary value, the
  pre-fix regression) or what the brittle test should assert instead.
- Prefer naming the missing test over restating "add more tests".

Example finding:

> test gap: `parseRange` (range.ts:42) now returns `null` on an empty input,
> but no test exercises the empty case — add one asserting `parseRange('')`
> returns `null` so the new branch is covered.
