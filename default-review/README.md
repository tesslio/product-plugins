# default-review

The default `tessl review` rubric, packaged as a plugin. It is the exact reviewer `tessl review` uses out of the box.

## Install

```bash
tessl install tessl/default-review
```

## What it does

`tessl review` scores a skill against a **reviewer plugin**. This is that reviewer: rubric-based LLM judges plus a deterministic validation pass, scoring a `SKILL.md` for description and content quality against Anthropic best practices.

It scores three components (weights live in `config.json`):

| Component | Weight | What it measures |
|-----------|--------|------------------|
| `validation` | 0.2 | Deterministic checks: frontmatter, line count, schema, licence |
| `description` judge | 0.4 | How well the skill's description drives activation |
| `content` judge | 0.4 | Quality of the SKILL.md body |

Use it two ways:

- **As the reference reviewer** — the identity `tessl review` resolves when no other reviewer is selected.
- **As a base to fork** — start from this rubric and adjust weights, anchors, or judges with [`tessl/review-plugin-creator`](../review-plugin-creator/).

## Skills

| Skill | Description |
|-------|-------------|
| `skill-reviewer` | Evaluate a SKILL.md for quality using rubric-based LLM judges for description and content |
