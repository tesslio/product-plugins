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
  hooks/                 # optional; packaged hook entrypoints
    <hook-name>.sh
  .mcp.json              # optional (bundled MCP servers)
```

Scaffold this with `tessl plugin new` (or `tessl skill new` for a single skill) rather than writing it by hand. A single skill created with `tessl skill new` is already a minimal plugin, it gets a `.tessl-plugin/plugin.json`.

## Where to author the source

Author the plugin in a **repo-owned directory you commit and control**. If `.tessl/memory/preferences/plugins.md` names a plugins dir, use it. Otherwise the default is `tessl-plugins/<plugin-name>/`, referenced from `tessl.json` with `file:<path>`. (Some repos keep plugins under `plugins/<plugin-name>/` instead; follow that only when it is already the repo's convention.)

**Do not author source under `.tessl/plugins/`.** That path is Tessl's installed-content cache, where installed plugins are materialised, not a source directory. Anything you write there can be overwritten or wiped by install operations.

## `plugin.json` fields

**Required:** `name` (`<workspace>/<plugin-name>`, matches the key in `tessl.json`), `version` (semver), `description` (the registry shopfront, what others see to decide whether to install).

**Optional metadata:** `author`, `homepage`, `repository`, `license`, `private` (true keeps it workspace-only; public is irreversible).

**Content paths (string or array):** `skills` (defaults to `./skills/`), `rules` (defaults to `./rules/`), and `commands`. `mcpServers` is an optional fixed pointer whose value is `".mcp.json"` or `"./.mcp.json"`.

**Lifecycle behavior:** `hooks` declares cross-agent commands against Tessl's generic event contract. `nativeHooks` declares per-agent hook entries and is reserved for an event or field the generic contract cannot express. Hook scripts conventionally live under `hooks/` and are shipped with the plugin.

See [hooks-and-mcp.md](hooks-and-mcp.md) for the current manifest shapes and validation rules.

## The primitives, and who triggers each

- **Skill** — a workflow the *model* loads when the task matches its `description`.
- **Rule** — an always-on convention the agent follows passively. Plain markdown.
- **Command** — an action the *user* invokes explicitly (a slash command).
- **MCP server** — external tools or data, declared in a bundled `.mcp.json`.
- **Hook** — a deterministic command an *agent lifecycle event* invokes.

Rule of thumb: always-on guidance → rule; reach-for-it-when-relevant → skill; a button the user presses → command; deterministic lifecycle behavior → hook; live tools or data → MCP server.
