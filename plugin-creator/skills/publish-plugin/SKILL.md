---
name: publish-plugin
description: Use when a composition is built and the user wants to share it, to publish or re-publish it to the Tessl registry. Lints it, confirms private/public visibility, and publishes.
---

# Publish a plugin

Publishing makes a plugin installable from the registry. It lives in this plugin for now; the broader distribute workflow (rollout across repos, org distribution) is a larger surface that may absorb parts of this later. Only invoke this when the user explicitly wants to publish.

## 1. Confirm visibility, and ask

Never publish without an explicit yes, and confirm public vs private first. The `private` field in `.tessl-plugin/plugin.json` controls it:

- `"private": true` (default): only the workspace can see and install it.
- `"private": false`: anyone can discover and install it. **This is irreversible, a public plugin cannot be made private again.**

If the user is new to Tessl, be extra clear about what public means.

## 2. Handle provenance

If the plugin wraps skills the user did not author, do not publish on their behalf without making ownership clear. Wrapping and publishing someone else's work is a real sensitivity, surface it.

## 3. Lint and dry-run

Inspect the live CLI first (`tessl plugin publish --help`). Then:

```bash
tessl plugin lint <plugin-dir>
tessl plugin publish <plugin-dir> --dry-run
```

Fix all issues. Publishing requires Tessl auth (`tessl login`, or `TESSL_TOKEN` in CI). Published plugins should have evals (the internal bar is review and task-eval scores of 80%+); if they are missing, point the user at `tessl/skill-optimizer` first, evals are a separate, downstream flow.

## 4. Publish

```bash
tessl plugin publish <plugin-dir>
```

Bump the version each release (`--bump patch|minor|major`, or edit `version`).

## Undo

- `tessl plugin unpublish` works only within 2 days.
- `tessl plugin archive` is the normal way to retire a plugin: blocks new installs, keeps existing ones working.

## When to stop

Stop when the plugin is published at the intended visibility, or the user chooses to keep it local.
