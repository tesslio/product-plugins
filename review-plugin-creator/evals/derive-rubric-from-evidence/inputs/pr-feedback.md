# find-optimizations output — PR window: last 4 weeks, scoped to skill PRs

Findings below were produced by `/find-optimizations` over the skill's PR history.
Each finding carries a **Type**, **Summary**, and **Evidence**.

## Finding 1

- **Type**: skill
- **Summary**: The `add-api-endpoint` skill never tells the agent to regenerate the API
  client types after changing a route. Reviewers repeatedly have to ask for
  `bun run api:sync`, and CI fails on type drift until they do.
- **Evidence**:
  - PR #4821 — reviewer: "CI is red on api-types-check. Run `bun run api:sync` and commit the regenerated files."
  - PR #4855 — reviewer: "Same as last time — you changed a route schema but didn't run `bun run api:sync`."
  - PR #4902 — reviewer: "Need `bun run api:sync` here too; the frontend client is out of date."
  - Three PRs, same recurring comment from the same reviewer.

## Finding 2

- **Type**: verifier
- **Summary**: Every route handler must return through the typed `reply.send(...)` helper,
  never via raw `res.end(...)`. This is a binary, observable property of the committed file.
- **Evidence**:
  - PR #4877 — reviewer: "Use `reply.send` here, not `res.end` — we lose response typing otherwise."

## Finding 3

- **Type**: skill
- **Summary**: Reviewers and teammates note the skill is hard to discover — its description
  doesn't say what kind of work triggers it, so agents hand-roll routes instead of using it.
- **Evidence**:
  - PR #4902 — reviewer: "Was there not a skill for this? The route boilerplate is all slightly wrong."
