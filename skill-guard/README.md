# skill-guard

Cross-agent guard that blocks agents from loading skills not managed by Tessl.

## Install

```bash
tessl install tessl/skill-guard
```

## What it does

Once installed, agents in the project may only load Tessl-managed skills:

- **Allowed** — `tessl__<name>` skills whose base name is listed under a dependency's `include.skills` in `tessl.json`, or installed as a `tessl__<name>` directory under `.agents/skills/` by `tessl install`. Built-in agent commands (which map to no file in a user skill directory) also stay allowed.
- **Blocked** — any other skill found in a user skill directory (`.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, or their `~/` equivalents).

It also blocks direct writes to `tessl.json` (file-edit tools and shell commands alike). `tessl.json` is the skill allow-list, so hand-editing it would trivially bypass the guard — skills must be added through `tessl install` instead. Reads are unaffected.

## How it works

The plugin has two parts:

- **`rules/skill-guard.md`** — the contract. Injected into agent context so agents know the policy and follow it without being blocked.
- **`hooks/skill-guard.sh`** — the backstop. Registered for two hook events:
  - `PreToolUse` — hard block (exit 2). Denies the `Skill` tool for unauthorised skills (Claude), reads of files under a skill directory for unauthorised skills (the escape hatch on Claude, the primary skill-load path on Cursor), and any tool call or shell command that writes `tessl.json`.
  - `UserPromptSubmit` — soft steer. Slash-command invocations (`/some-skill`) and skill-path attachments can't be blocked at this stage, so the hook injects `additionalContext` warning the agent off; hard enforcement still happens at `PreToolUse`.

The hook is written against the Tessl generic hook event schema: the Tessl dispatcher (`tessl hook run`) translates each agent's native event into one normalized payload and translates the hook's output back, so a single script covers Claude Code and Cursor without per-runtime branches. It registers no `PreToolUse` matcher because tool names pass through verbatim and differ per agent (Claude `Read` vs Cursor `read_file`); the script filters on `tool_name` itself.

The script is dependency-free bash — no `jq`, `python`, or `node` — so it runs unchanged in environments that ship nothing beyond bash and POSIX utilities.

## Limitations

Enforcement is best-effort, not a sandbox: an agent that can run arbitrary shell can still sidestep the hook. Treat the rule as the contract and the hook as the backstop. `tessl.json` shell-write detection is pattern-based (redirects, `tee`, in-place edits, moves, script-level file writes), not an authoritative write oracle.
