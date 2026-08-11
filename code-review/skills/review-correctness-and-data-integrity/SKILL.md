---
name: review-correctness-and-data-integrity
description: Review a change for whether it does what it is meant to do, and whether the data it touches survives it intact. Use as one lens in a code review run.
---

# Review lens: Correctness and Data Integrity

Review for incorrect results in changed logic, persisted data, and integration boundaries.

## Scope

- **Functional Correctness** Whether changed logic handles valid edge cases correctly, including absent or empty values, boundary values, inverted conditions, and cases with no matching branch.
- **Data Integrity** What the change can lose, duplicate, reorder or silently reinterpret on the way through, and what a half-finished run leaves behind.
- **Integration** Whether the things on either side of a boundary still agree, given they were written at different times and ship separately.

## Method

Challenge each changed calculation, comparison, and branch against valid edge cases and against existing data that may be valid but unusual.

For each write path, trace a record from input to persistence and check the state left by an interrupted run.

At an integration boundary, check compatibility between the independently deployed versions of each side.

Some contracts are written down rather than expressed in types. Read the `AGENTS.md` or `CLAUDE.md` chain governing the changed files, from the repository root down, for the rules a caller is expected to follow.

## Threshold

Report incorrect results that can occur in a realistic input or system state.

Prioritize those that persist incorrect data, because application code can be redeployed but written data may require repair.

Do not report guards for states the types or the callers already rule out.

## Reporting

- State the concrete impact and the input or state that triggers it.
- At a boundary, name the boundary, the breaking change, the consumer at risk, and the missing migration, deprecation window, or version step.
- If coverage is missing, identify the exact case: an error path, boundary value, or regression scenario. Avoid a general request for more tests.
- State the smallest plausible fix or verification.
