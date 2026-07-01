---
name: build-composition
description: Use once there is a confirmed composition plan, to create it. Authors or restructures the skill(s), decomposes anything too big, wraps existing skills, and assembles the plugin with any rules or MCP servers the plan called for. Scaffolds with the CLI rather than hand-writing manifests.
---

# Build the composition

Turn the confirmed plan into real files, in the right place. Do not re-litigate the plan here, build it.

## 1. Scaffold with the CLI

Create the skeleton with the CLI, never hand-write manifests:

- A single skill → `tessl skill new` (creates the `SKILL.md` and its `plugin.json`).
- A richer plugin → `tessl plugin new` (can seed skills and rules).
- Wrapping an existing loose `SKILL.md` → `tessl skill import` to generate its `plugin.json`.

Inspect `tessl skill new --help` / `tessl plugin new --help` for the current flags. See [references/plugin-anatomy.md](references/plugin-anatomy.md).

## 2. Author or restructure the skills

- For each skill in the plan, write a strong `description` (what + when, it drives discovery) and lean, ordered steps, with depth pushed into `references/`. See [references/shaping-and-decomposition.md](references/shaping-and-decomposition.md).
- **Honour existing content.** If you are wrapping the user's skill, restructure rather than rewrite. Change wording only if a review flags a real problem and the user agrees. Keep authorship attributed.
- If a skill is too big or does several jobs, hand to `decompose-into-skills`.

## 3. Add the other primitives the plan called for

Only add what the plan specified, do not pad.

- **Rule** — a plain `.md` under `rules/` for an always-on convention.
- **MCP server** — a bundled `.mcp.json` when the plan calls for a capability. Point the manifest at it (`"mcpServers": ".mcp.json"`). Two transports: `http` (a URL) and `stdio` (a command plus args). Do not hard-code secrets.
- **Command** — a `.md` under `commands/` for a user-invoked action.

## 4. Validate

```bash
tessl plugin lint <plugin-dir>
```

Optionally install into a throwaway project (a `file:` dependency) and confirm the skills, rules, and any MCP servers materialise.

## 5. Hand off

The composition now exists. Point the user at the next steps: eval via `tessl/skill-optimizer` (a separate flow), and `publish-plugin` if they want to share it. Do not run evals here.

## When to stop

Stop when the composition is built, lints clean, and the user knows the next steps.
