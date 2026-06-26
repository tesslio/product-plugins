# default-skill-review

The default `tessl review` rubric, packaged as a plugin. It is the exact reviewer `tessl review` uses out of the box.

## Install

```bash
tessl install tessl/default-skill-review
```

## What it does

`tessl review` scores a skill against a **reviewer plugin**. This is that reviewer: an agent that reads a `SKILL.md` and scores it against rubrics grounded in Anthropic best practices.

It ships two rubrics (their weights live in `config.json`):

| Rubric | What it measures |
|--------|------------------|
| `description` | How well the skill's description drives activation |
| `content` | Quality of the SKILL.md body |

Use it two ways:

- **As the reference reviewer** — the reviewer `tessl review` resolves when no other reviewer is selected.
- **As a base to fork** — start from this rubric and adjust weights, anchors, or judges with [`tessl/review-plugin-creator`](../review-plugin-creator/).

## Skills

| Skill | Description |
|-------|-------------|
| `skill-reviewer` | An agent that reads a SKILL.md and scores it against the description and content rubrics |
