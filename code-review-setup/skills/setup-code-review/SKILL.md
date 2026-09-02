---
name: setup-code-review
description: Moved to tessl/code-review. This plugin no longer carries the Code Review setup skill. Use when this plugin is installed and someone asks to set up, configure, or remove Tessl Code Review, so they can be pointed at the plugin that now does it.
---

# This skill has moved

The Code Review setup skill now lives in the `tessl/code-review` plugin, together
with the default lenses, lens authoring, and review responses.

Install that plugin and use its `setup-code-review` skill:

```bash
tessl install tessl/code-review
```

A current Tessl CLI already carries it inside `tessl agent`, so no install is
needed there.

Do not attempt the setup from this skill. It holds no procedure.
