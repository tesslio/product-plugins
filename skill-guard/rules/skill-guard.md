# Skill guard

Agents in this project may only load skills that Tessl manages. A skill is Tessl-managed when it is a `tessl__<name>` whose base name is either listed under some dependency's `include.skills` in `tessl.json`, or installed as a `tessl__<name>` directory in `.agents/skills/` by `tessl install` (some plugins omit `include.skills` but still place the skill on disk). Built-in agent commands (those that map to no file in a user skill directory) also stay allowed.

Do not load, read, or slash-invoke a skill that lives in a user skill directory (`.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, or their `~/` equivalents) unless it is Tessl-managed. Do not edit `tessl.json` to add a skill so it passes the guard: `tessl.json` is the allow-list, and hand-editing it to widen the allow-list defeats the guard. Add skills through `tessl install` instead.

The `skill-guard.sh` hook enforces this at `PreToolUse` as a hard block (exit 2) and steers away from it at `UserPromptSubmit`. The block is best-effort: an agent that can run arbitrary shell can still sidestep it, so treat this rule as the contract and the hook as the backstop.
