# Test Generator Skill

## When to use this skill
Use this skill when a user asks to write, scaffold, or add test coverage to a module or function.

## Steps

1. Read the target module and identify public functions and exported classes.
2. For each function, generate test cases covering: happy path, edge cases (empty input, null, boundary values), and expected error conditions.
3. Group tests by function in a single test file named `<module>.test.ts` (or `.spec.ts` per project convention).
4. Use the project's existing test framework (Jest, Vitest, Pytest — detect from `package.json` or `pyproject.toml`).
5. Add a brief comment above each `describe` block explaining what scenario it covers.

## Important notes
- Do not add tests for private/internal helpers unless explicitly asked.
- Mock external dependencies (HTTP, file system, databases) using the framework's standard mock library.
- Each test should have exactly one assertion or a clearly documented reason for multiple assertions.
- If a module has no public exports, explain this and do nothing.
