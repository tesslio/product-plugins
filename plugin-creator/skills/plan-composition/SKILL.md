---
name: plan-composition
description: Use once the problem and artifacts are understood, to decide the right shape for the context. Produces a short composition plan - a single skill for simple cases, or a plugin (with rules, MCP servers, or multiple skills) for richer ones - and confirms it with the user before anything is built.
---

# Plan the composition

You know the problem and have the material. Now decide how best to arrange it. This is a plan, not a build, keep it short and confirm it before creating anything.

## Decide the shape

Default to the smallest thing that solves the problem. See [references/choosing-the-shape.md](references/choosing-the-shape.md).

- **A single skill** — for a simple, self-contained workflow or body of knowledge. In Tessl a skill is already a minimal plugin (it gets a `plugin.json`), so this is not a lesser option; it is the right one when the problem is simple.
- **A plugin with several skills** — when the problem has distinct parts (decompose), or when related skills belong together.
- **A plugin with more than skills** — add a **rule** for an always-on convention, or an **MCP server** when the agent needs a tool or live data, not just instructions. Add these only when they clearly earn their place.

Hooks are not GA. Note them as a follow-up if relevant; do not plan to ship them.

## Write the plan

In a few lines, state: the problem, the artifacts, the proposed shape (skill or plugin, plus which primitives), and whether anything needs decomposing. Explain the why, especially if you are proposing to split a big skill. Confirm with the user, or make the call and tell them your reasoning.

## Hand off

Pass the confirmed plan to `build-composition`.

## When to stop

Stop when there is a confirmed composition plan.
