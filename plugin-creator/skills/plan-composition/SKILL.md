---
name: plan-composition
description: Use once the problem and artifacts are understood, to decide the right shape for the context. Produces a short composition plan - a single skill for simple cases, or a plugin (with rules, MCP servers, or multiple skills) for richer ones - and confirms it with the user before anything is built.
---

# Plan the composition

You know the problem and have the material. Now decide how best to arrange it. This is a plan, not a build, keep it short and confirm it before creating anything.

## First, skill or rule?

Before deciding single-skill-vs-plugin, decide what *kind* of context each part is, because it is easy to default everything to skills. See [references/choosing-the-shape.md](references/choosing-the-shape.md).

- If the agent should **follow a workflow when a relevant task comes up**, that is a **skill**.
- If the agent should **always obey a convention, unprompted**, that is a **rule**.

Watch for always-on-convention language: "the agent keeps getting X wrong", "every time", "it never follows our...". That is usually a **rule** (or a rule plus a skill), not a skill alone. Do not push a conventions request toward skills by default.

## Decide the shape

Default to the smallest thing that solves the problem.

- **A single skill** — for a simple, self-contained workflow. In Tessl a skill is already a minimal plugin (it gets a `plugin.json`), so this is not a lesser option; it is the right one when the problem is simple.
- **A plugin with several skills, and/or rules** — when the problem has distinct parts (decompose), when related skills belong together, or when it mixes workflows (skills) with always-on conventions (rules).
- **A plugin with an MCP server** — when the agent needs a tool or live data, not just instructions. Add only when it clearly earns its place.

Hooks are not GA. Note them as a follow-up if relevant; do not plan to ship them.

## Write the plan

In a few lines, state: the problem, the artifacts, and the proposed shape, which primitive each part becomes (skill vs rule vs MCP), and whether anything needs decomposing. Explain the why, especially if you are proposing to split a big skill or to encode a convention as a rule. Confirm with the user, or make the call and tell them your reasoning.

## Hand off

Pass the confirmed plan to `build-composition`.

## When to stop

Stop when there is a confirmed composition plan.
