---
name: build-composition
description: Use once there is a confirmed composition plan, to create it. Scaffolds the plugin, authors or restructures the skill(s), decomposes anything too big, and adds any rules or MCP servers the plan called for. Uses the CLI to scaffold the plugin, then adds further skills by hand.
---

# Build the composition

Turn the confirmed plan into real files, in the right place. Do not re-litigate the plan here, build it.

## 1. Scaffold the plugin once

First choose **where** to author it: a repo-owned directory you commit, defaulting to `tessl-plugins/<plugin-name>/` when `.tessl/memory/preferences/plugins.md` names no other. **Never author under `.tessl/plugins/`** — that is Tessl's installed-content cache, not source. See [references/plugin-anatomy.md](references/plugin-anatomy.md).

Create the plugin skeleton with the CLI. Inspect `tessl plugin new --help` first, and note two things it requires:
- Pass `--skill` (with `--skill-name` and `--skill-description`) or `--rules` to seed initial content; it errors with neither.
- Pass `--workspace <name>` explicitly. The workspace in `--name workspace/plugin` is **not** parsed from the name.

- A single standalone skill → `tessl skill new` (creates the `SKILL.md` and its `plugin.json`).
- A plugin → `tessl plugin new --skill --skill-name <first> --skill-description "..." --workspace <ws>`.
- Wrapping an existing loose `SKILL.md` into a plugin → `tessl skill import`.

See [references/plugin-anatomy.md](references/plugin-anatomy.md).

## 2. Add each further skill by hand, not with `tessl skill new`

To add more skills to an existing plugin, **create the file directly**:

```
skills/<skill-name>/SKILL.md      # plus a references/ folder as needed
```

The manifest's `skills: ./skills/` discovers them automatically.

**Do not run `tessl skill new` again inside a plugin to add a skill.** That command always scaffolds a standalone skill-as-plugin, which nests a second plugin inside yours (`skills/<name>/.tessl-plugin/...`). `tessl plugin lint` may still call the result "valid", but `tessl plugin pack` silently drops the mis-nested skill, so the plugin ships incomplete. Only the plugin's own `plugin.json` should be CLI-scaffolded; individual `SKILL.md` files are authored directly.

## 3. Author or restructure the skills

- Write a strong `description` (what + when, it drives discovery) and lean, ordered steps, with depth pushed into `references/`. See [references/shaping-and-decomposition.md](references/shaping-and-decomposition.md).
- **Honour existing content.** If you are wrapping the user's skill, restructure rather than rewrite. Change wording only if a review flags a real problem and the user agrees. Keep authorship attributed.
- If a skill is too big or does several jobs, hand to `decompose-into-skills`.

## 4. Add the other primitives the plan called for

Only add what the plan specified, do not pad.

- **Rule** — a plain `.md` under `rules/` for an always-on convention. If the plan identified a convention the agent should always follow (see `plan-composition`), it belongs here, not in a skill.
- **MCP server** — a bundled `.mcp.json` when the plan calls for a capability. Point the manifest at it (`"mcpServers": ".mcp.json"`). Two transports: `http` (a URL) and `stdio` (a command plus args). Do not hard-code secrets.
- **Command** — a `.md` under `commands/` for a user-invoked action.

## 5. Validate with lint AND pack

`tessl plugin lint <plugin-dir>` is the primary structural check; pack confirms what actually ships. Because lint can pass on a mis-nested skill, always do both:

```bash
tessl plugin lint <plugin-dir>
tessl plugin pack <plugin-dir> --output /tmp/check.tgz
tar tzf /tmp/check.tgz                    # inspect the full file list
```

Then assert **each** intended file is present, do not settle for a bare `grep SKILL.md` (it passes as soon as any one skill appears, so it hides a dropped skill). List the paths the plan called for and fail on the first miss:

```bash
missing=0
for p in skills/<first>/SKILL.md skills/<second>/SKILL.md rules/<rule>.md commands/<cmd>.md; do
  tar tzf /tmp/check.tgz | grep -q "/$p\$\|^$p\$" || { echo "MISSING: $p"; missing=1; }
done
[ "$missing" -eq 0 ]   # nonzero exit if any intended file is absent
```

`tessl skill lint <skill-dir>` is a separate tool for a single loose `SKILL.md` not yet inside a plugin. Do not run it against a skill folder within your plugin, `tessl plugin lint` already covers those; if it errors about missing plugin metadata, you pointed it at the wrong shape, drop it.

Optionally install into a throwaway project (a `file:` dependency) and confirm the skills, rules, and any MCP servers materialise.

If the plugin ships an MCP server, scripts, or otherwise touches secrets, auth, file or network access, or CI, also run a security review: `tessl review run security <path> --workspace <name>` (inspect `tessl review run --help` for the current form). Pass `--workspace <name>` on any non-interactive `tessl review run`, quality or security (e.g. `tessl review run quality <path> --workspace <name>`), or the CLI opens an interactive workspace selector and hangs. Expect findings and triage each, a flagged item is not automatically a blocker but should be reviewed with the user.

## 6. Hand off

The composition now exists. Point the user at the next steps: eval via `tessl/skill-optimizer` (a separate flow), and `publish-plugin` if they want to share it. Do not run evals here.

## When to stop

Stop when the composition is built, lints clean, packs with every intended skill, and the user knows the next steps.
