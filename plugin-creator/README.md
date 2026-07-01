# plugin-creator (working name)

> First draft, not published. Built for Marc to review. Working name only, this is not plugin-first. See `DRAFT-NOTES.md`.

Turn a problem, or a messy existing skill, into well-shaped agent context. It understands what you are trying to do, takes stock of what you already have, plans the right shape (a single skill, or a plugin with rules and MCP servers), and builds it. Evaluation is a separate, downstream step, handled by `tessl/skill-optimizer`; this gets you to a well-formed composition first.

## The arc

understand → gather → plan the composition → build → (then, separately) eval

## Skills

| Skill | Description |
|-------|-------------|
| `create-context` | Orchestrator. Runs the arc and points to eval at the end. |
| `gather-context` | Understand the problem and take stock of what exists; fill gaps by asking, hunting (PRs/logs), or inferring. |
| `plan-composition` | Decide the shape: a single skill, or a plugin with the right primitives. |
| `build-composition` | Create it, scaffolding with the CLI, not hand-written manifests. |
| `decompose-into-skills` | Split a big skill into focused, independently-verifiable skills. |
| `publish-plugin` | Optional. Publish or re-publish to the registry. |

## Companion

For quality (review, eval scenarios, optimisation), `tessl/skill-optimizer` is the sibling flow, after a composition is built.
