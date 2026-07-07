# plugin-creator

Turn a problem, or a messy existing skill, into well-shaped agent context. plugin-creator understands what you are trying to do, takes stock of what you already have, plans the right shape (a single skill, or a plugin with rules and MCP servers), and builds it. Evaluation is a separate, downstream step handled by `tessl/skill-optimizer`; this gets you to a well-formed composition first.

## Install

```bash
tessl install tessl/plugin-creator
```

Then just tell your agent what you want it to do better.

## How it works

understand → gather → plan the composition → build → (then, separately) eval

## Skills

| Skill | Description |
|-------|-------------|
| `create-context` | Orchestrator. Runs the flow and points to eval at the end. |
| `gather-context` | Understand the problem and take stock of what exists; fill gaps by asking, hunting (PRs and logs), or inferring. |
| `plan-composition` | Decide the shape: a single skill, or a plugin with the right primitives. |
| `build-composition` | Create it, scaffolding with the CLI rather than hand-written manifests. |
| `decompose-into-skills` | Split a big skill into focused, independently-verifiable skills. |
| `publish-plugin` | Optional. Publish or re-publish to the registry. |

## Companion

For quality (review, eval scenarios, optimisation), `tessl/skill-optimizer` is the sibling flow, once a composition is built.
