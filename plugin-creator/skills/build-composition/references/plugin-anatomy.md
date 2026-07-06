# Plugin anatomy

## Minimum structure

```
<plugin-name>/
  .tessl-plugin/
    plugin.json          # manifest (required)
  skills/
    <skill-name>/
      SKILL.md
      references/        # optional
  rules/                 # optional
    <rule-name>.md
  commands/              # optional
    <command-name>.md
  .mcp.json              # optional (bundled MCP servers)
```

Scaffold this with `tessl plugin new` (or `tessl skill new` for a single skill) rather than writing it by hand. A single skill created with `tessl skill new` is already a minimal plugin, it gets a `.tessl-plugin/plugin.json`.

## `plugin.json` fields

**Required:** `name` (`<workspace>/<plugin-name>`, matches the key in `tessl.json`), `version` (semver), `description` (the registry shopfront, what others see to decide whether to install).

**Optional metadata:** `author`, `homepage`, `repository`, `license`, `private` (true keeps it workspace-only; public is irreversible).

**Content paths (string or array):** `skills` (defaults to `./skills/`), `rules` (defaults to `./rules/`), `commands`, `mcpServers` (literal `".mcp.json"` or `"./.mcp.json"`).

Hooks (`hooks` / `nativeHooks`) exist in the schema but are not GA. Do not include them in a published plugin.

## The five primitives, and who triggers each

- **Skill** — a workflow the *model* loads when the task matches its `description`.
- **Rule** — an always-on convention the agent follows passively. Plain markdown.
- **Command** — an action the *user* invokes explicitly (a slash command).
- **MCP server** — external tools or data, declared in a bundled `.mcp.json`.
- **Hook** — a shell command at a lifecycle event. Not GA yet.

Rule of thumb: always-on → rule; reach-for-it-when-relevant → skill; a button the user presses → command; needs live tools or data → MCP server.
