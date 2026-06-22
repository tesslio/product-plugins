# review-plugin-creator

Guided workflow for creating a custom Tessl reviewer plugin, by forking the default rubric or building one from scratch.

## Install

```bash
tessl install tessl/review-plugin-creator
```

## What it does

`tessl review` scores a skill against a reviewer plugin. With no `--review-plugin`, it uses Tessl's default rubric (Anthropic best practices). This plugin walks you through creating your own reviewer plugin so reviews reflect your team's standard, then gating CI on that score.

Two starting points:

- **Fork the default rubric** — start from Tessl's default rubric (bundled with the skill) and tweak weights, anchors, or dimensions.
- **Build from scratch** — author new judges from a blank template for a security-only or domain-specific reviewer.

The default rubric is bundled at `skills/create-review-plugin/references/default-rubric/` so you can read exactly what `tessl review` uses out of the box before deciding which path to take.

## Skills

| Skill | Description |
|-------|-------------|
| `create-review-plugin` | Scaffolds the plugin, writes rubric files and config.json, and validates with `tessl review run` |
