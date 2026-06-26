# Agent-log excerpt — `tessl agent-logs view` output (provider: claude-code)

Two sessions are reproduced below. Transcripts are trimmed to the relevant turns.

## Session 1 — skill did NOT activate when it should have

```
user: Add a GET /workspaces/:id/members endpoint to the backend that returns the
      members of a workspace.
assistant: I'll create the route handler and schema directly.
  [no Skill tool_use block; no /add-api-endpoint slash command anywhere in the session]
  ... hand-writes src/routes/workspaces/members/get.ts ...
```

The task squarely matches `add-api-endpoint`'s purpose, but neither activation form
(a `Skill` tool_use nor a `/add-api-endpoint` slash command) appears. The agent
re-derived the route boilerplate from scratch.

## Session 2 — skill activated but a step was ignored, and the user corrected the agent

```
user: /add-api-endpoint for the billing webhook
assistant: [tool_use: Skill, input.skill = "add-api-endpoint"]
  ... creates the route handler and the request/response schema ...
  ... does NOT regenerate API types ...
assistant: Done — the billing webhook endpoint is in place.
user: You forgot to sync the types. CI is red on api-types-check. Run `bun run api:sync`.
```

The skill fired, but step 3 ("Make sure the types are in sync") was vague enough that the
agent skipped the concrete action, and the user had to redirect it.
