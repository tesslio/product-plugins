# Build a cross-agent post-edit validation plugin

The Meridian web team wants a deterministic check to run after an AI coding agent edits a file. The same behavior must work across supported agents:

- Trigger after `Edit` or `Write` tool calls.
- Run `npm run validate:changed` from the consuming project.
- Keep the hook entrypoint inside the plugin so it ships with the plugin.
- Do not modify Claude Code, Cursor, or any other agent's configuration directly.

Create a Tessl plugin named `meridian/validate-after-edit` under `validate-after-edit/`. Produce the complete plugin files on disk, ready for `tessl plugin lint` and `tessl plugin pack`. Use the smallest composition that implements the deterministic lifecycle behavior; do not add a skill or rule that merely describes the check.
