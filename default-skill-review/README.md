# default-skill-review

The default `tessl review` rubric, packaged as a plugin. It is the exact reviewer `tessl review` uses out of the box.

## Install

```bash
tessl install tessl/default-skill-review
```

## What it does

`tessl review` scores a skill against a **reviewer plugin**. This is that reviewer: rubric-based LLM judges that score a `SKILL.md` against Anthropic best practices.

It ships two judges (their weights live in `config.json`):

| Judge | What it measures |
|-------|------------------|
| `description` | How well the skill's description drives activation |
| `content` | Quality of the SKILL.md body |

Use it two ways:

- **As the reference reviewer** — the reviewer `tessl review` resolves when no other reviewer is selected.
- **As a base to fork** — start from this rubric and adjust weights, anchors, or judges with [`tessl/review-plugin-creator`](../review-plugin-creator/).

## Skills

| Skill | Description |
|-------|-------------|
| `skill-reviewer` | Evaluate a SKILL.md for quality using rubric-based LLM judges for description and content |
