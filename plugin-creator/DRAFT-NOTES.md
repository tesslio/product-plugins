# Draft notes (for Marc's review)

Draft of the context/plugin creator plugin. Uncommitted, unpublished, untracked in git. Working name only.

## Model (updated 2026-07-01, per Marc): composition plan

**Problem-first, and eval is downstream.** Users are not asking to package anything. They usually already tried to solve their problem and now have a skill that is a mess, too long, or not getting enough out of Tessl. This plugin understands the problem, gathers what they have, plans the right shape, builds it, and *then* points them to eval, which stays in skill-optimizer as a separate sibling flow. We never run evals mid-creation. Sprawl/rot is skill-inventory's concern, not this plugin's.

Note: in Tessl a "skill" is already a minimal single-skill plugin (`tessl skill new` / `import` create the `plugin.json`). So packaging-for-eval is cheap; this plugin's job ends at *composition created*.

## The arc (and the 6 skills)

understand → gather → plan → build → (then, separately) eval

| Skill | Phase / role |
|---|---|
| `create-context` | Orchestrator. Runs the arc; hands off to skill-optimizer for eval at the end. |
| `gather-context` | Understand the problem; take stock of artifacts (skill, plugin, code, prompt, or "go find it"); fill gaps by asking, hunting, or inferring. |
| `plan-composition` | Decide the shape: single skill vs plugin (+ rules / MCP). Produce a short composition plan and confirm it. |
| `build-composition` | Create it: author/restructure/wrap skills, add rules/MCP per plan. Scaffolds with `tessl skill new` / `plugin new`. |
| `decompose-into-skills` | Split a big skill into focused, independently-verifiable skills. Invoked during build. |
| `publish-plugin` | Optional. Kept in for now; distribute workflow may absorb it later. |

`author-skill-from-intent`, `find-context-opportunities`, `wrap-skills-into-plugin`, and `add-mcp-server-to-plugin` from the previous draft were **absorbed**: gathering (incl. the PR/log hunt) folded into `gather-context`; authoring/wrapping/MCP folded into `build-composition`.

## What changed this round

- Reframed to the composition-plan arc; eval is a downstream sibling, never woven in.
- Dropped the "skill → evals → plugin" ladder (it implied evaling mid-flow).
- Unified the entry points into `gather-context` (Marc: author-from-intent and find-opportunities are aspects of the same gathering).
- Folded MCP into `build-composition` (no standalone MCP skill).
- Kept publishing in (Marc: distribute is undefined; pull it out later if needed).
- Removed sprawl/rot as a design anchor.

## QA status

- `tessl plugin lint` — PASS. Clean install — PASS, all 6 skills materialise.
- Quality review (`tessl review run`) — still needs `tessl login`.

## Parked actions / decisions

1. **Name** (not plugin-first; Sandra may weigh in) — decide once the flow is pinned.
2. **Update skill-optimizer** so that when a user brings it a skill, it can decide to package it and call *these* skills to do so (sibling ↔ sibling).
3. **Fate of existing creators**: `tessl-labs/tile-creator` is deprecated (no tiles; Labs = prototype). The `harness-engineering/plugin-creator` placeholder is closer to a product surface (ships with Tessl agent) so replacing it needs care.
4. Does this plugin own publishing long-term, or defer to distribute?
5. Is 6 skills the right cut?
