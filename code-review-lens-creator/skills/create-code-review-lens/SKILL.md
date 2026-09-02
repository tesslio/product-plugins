---
name: create-code-review-lens
description: Moved to tessl/code-review. This plugin no longer carries the Code Review lens authoring skill. Use when this plugin is installed and someone asks to write, fork, tune, or debug a code review lens, so they can be pointed at the plugin that now does it.
---

# This skill has moved

The lens authoring skill now lives in the `tessl/code-review` plugin, together
with the default lenses it forks from, the setup skill, and review responses.

Install that plugin and use its `create-code-review-lens` skill:

```bash
tessl install tessl/code-review
```

A current Tessl CLI already carries it inside `tessl agent`, so no install is
needed there.

Do not attempt to author a lens from this skill. It holds no procedure.
