# skill-optimizer

Optimize your skills and plugins: review SKILL.md quality, generate eval scenarios, run evals, compare across models, diagnose gaps, and re-run until scores improve.

## Install

```bash
tessl install tessl/skill-optimizer
```

## Concepts

This plugin combines two complementary approaches to improving your skills:

- **Plugin evals** (`tessl eval run`) — measure whether a plugin makes agents better at real tasks. Scenarios are generated from the plugin, an agent solves each task with and without the plugin, and a judge scores outputs against a per-scenario rubric. The delta between baseline and with-plugin scores shows the value-add.
- **Skill reviews** (`tessl review run`) — assess the quality of a skill itself, without executing any tasks. The review packs the whole bundle (SKILL.md plus references/scripts/assets) and judges score it on dimensions like completeness, actionability, and conciseness to check whether it's well-structured for routing and agent comprehension. `tessl review fix` runs this as an automated review-and-fix loop. Both use the default reviewer unless you pass `--review-plugin` to customize the judges.

The `optimize-skill-performance-and-instructions` skill combines both into a single end-to-end cycle: review → eval → improve.

## Skills

| Skill | Description |
|-------|-------------|
| `optimize-skill-performance-and-instructions` | Runs the full optimization cycle |
| `setup-skill-performance` | Sets up performance testing for a skill |
| `optimize-skill-performance` | Improves how well a skill executes its tasks |
| `optimize-skill-instructions` | Improves how reliably a skill gets invoked |
| `compare-skill-model-performance` | Compares how a skill performs across different Claude models |
