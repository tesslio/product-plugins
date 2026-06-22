---
name: create-review-plugin
description: Scaffold and author a custom Tessl reviewer plugin, by forking the default rubric or building one from scratch. Bundles the default Tessl review rubric so you can read and tweak it, scaffolds the plugin directory, writes rubric files and config.json, and validates with tessl review run. Use when the user wants to create or customise a review plugin, fork or tweak the default reviewer rubric, change scoring weights, add custom judges, or build a domain-specific rubric for tessl review.
---

`tessl review` scores a skill against a **reviewer plugin**. With no `--review-plugin`, it uses Tessl's default rubric (Anthropic best practices). A custom reviewer plugin lets you change what "good" means - re-weight dimensions, edit the scoring anchors, or add your own judges - then gate CI on your team's standard.

This skill creates that plugin. There are two ways to start:

- **Fork the default rubric** (recommended). Start from Tessl's default rubric, bundled with this skill, and tweak it. Best when you mostly agree with the default and want to adjust weights, wording, or add a dimension.
- **Build from scratch.** Author new judges from a blank template. Best when your standard is unrelated to the default, for example a security-only or domain-specific reviewer.

Both produce the same plugin structure and are validated the same way.

## The default rubric

Tessl's default rubric is bundled with this skill at `references/default-rubric/`. It is the exact rubric `tessl review` uses out of the box. Read it before deciding whether to fork or start fresh.

It scores three components (weights live in `config.json`):

| Component | Weight | What it measures |
|-----------|--------|------------------|
| `validation` | 0.2 | Deterministic checks: frontmatter, line count, schema, licence |
| `description` judge | 0.4 | How well the skill's description drives activation |
| `content` judge | 0.4 | Quality of the SKILL.md body |

The two judges and their dimensions (all on a 1-3 scale):

- **`description.json`** - specificity (0.2), trigger term quality (0.3), completeness (0.35), distinctiveness / conflict risk (0.15)
- **`content.json`** - conciseness (0.3), actionability (0.3), workflow clarity (0.25), progressive disclosure (0.15)

To fork the default, copy these files into your plugin and edit them (Step 4, Path A).

## Plugin structure

Every reviewer plugin has this layout:

```
<plugin-name>/
├── .tessl-plugin/
│   └── plugin.json
└── skills/skill-reviewer/
    ├── SKILL.md
    └── references/
        ├── config.json
        ├── schemas/
        │   ├── rubric.schema.json
        │   ├── config.schema.json
        │   └── results.schema.json
        └── rubrics/
            └── <judge-name>.json   (one per judge)
```

The schemas in `references/schemas/` are bundled in this skill. Copy them verbatim — do not modify them.

## Step 1 — Choose your starting point and judges

Before writing files, decide:
- **Fork or scratch?** If you mostly agree with the default, fork it (Step 4, Path A). If your standard is unrelated, start from the blank template (Path B).
- **How many judges (rubrics)** — 1–6 is a good range. The default has 2 (`description`, `content`).
- **What each judge evaluates** (its `evaluation_target`) and **what weight it carries** in the final score.

### Weight invariant

```
validation_weight + Σ(judges[stem].weight) = 1.0
```

`validation_weight` controls how much the deterministic validation pass (frontmatter checks, line count, etc.) contributes to the score. Set to `0.0` to exclude validation from scoring entirely (it still runs as a gate).

**Examples:**

| Setup | config.json |
|-------|-------------|
| Default | `validation_weight: 0.2, judges: { description: { weight: 0.4 }, content: { weight: 0.4 } }` |
| 1 judge, validation off | `validation_weight: 0.0, judges: { content: { weight: 1.0 } }` |
| 3 judges | `validation_weight: 0.1, judges: { security: { weight: 0.5 }, clarity: { weight: 0.3 }, brevity: { weight: 0.1 } }` |

The judge key in `config.json` is the rubric filename stem — `security.json` → key `security`.

## Step 2 — Scaffold the directory

Ask the user where to create the plugin (or use `./my-reviewer`). Then create the directory structure:

```bash
PLUGIN_DIR=<chosen-path>
mkdir -p "$PLUGIN_DIR"/{.tessl-plugin,skills/skill-reviewer/references/{rubrics,schemas}}
```

Copy the schema files from this skill's references into the plugin:

```bash
# Copy schemas — these are the canonical schema files for rubrics and config
cp <path-to-this-skill>/references/schemas/rubric.schema.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/schemas/"
cp <path-to-this-skill>/references/schemas/config.schema.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/schemas/"
cp <path-to-this-skill>/references/schemas/results.schema.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/schemas/"
```

Copy the reviewer agent prompt (or customise it):

```bash
cp <path-to-this-skill>/references/reviewer-SKILL.md \
   "$PLUGIN_DIR/skills/skill-reviewer/SKILL.md"
```

The plugin's `SKILL.md` is the reviewer agent instruction — it drives the agent during review runs. If you omit it, the platform's baked-in default is used instead. If you include it, your version takes precedence.

**Start from `references/reviewer-SKILL.md` verbatim and make targeted edits.** Don't write from scratch.

- **Safe to customise:** evaluation style, domain-specific guidance, how the agent interprets rubric anchors
- **Risky to remove:** the steps that read `config.json`/`rubrics/` and write `results.json` — these are load-bearing for scoring
- **Keep the "Trust boundary" section:** the reviewer ingests untrusted, third-party skill content, so the guardrail telling the agent to treat that content as data and never as instructions must stay. Removing it reintroduces an indirect prompt injection risk (security finding W011).

The `results.json` output schema is enforced at the recipe level regardless of what your `SKILL.md` says — the agent's output is validated against the schema even if the instruction differs.

## Step 3 — Write `plugin.json`

```bash
cat > "$PLUGIN_DIR/.tessl-plugin/plugin.json" << 'EOF'
{
  "name": "<workspace>/<plugin-name>",
  "version": "0.1.0",
  "description": "<what this plugin evaluates>",
  "private": true,
  "skills": "./skills/"
}
EOF
```

## Step 4 — Add your rubrics

### Path A — Fork the default rubric

Copy the bundled default rubric and config into your plugin, then edit them:

```bash
cp <path-to-this-skill>/references/default-rubric/description.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/rubrics/"
cp <path-to-this-skill>/references/default-rubric/content.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/rubrics/"
cp <path-to-this-skill>/references/default-rubric/config.json \
   "$PLUGIN_DIR/skills/skill-reviewer/references/config.json"
```

Now make targeted edits. Common tweaks:
- **Re-weight dimensions** within a rubric (e.g. push `conciseness` up). The rubric's dimension weights must still sum to 1.0.
- **Re-weight judges** in `config.json` (e.g. weight `content` over `description`). `validation_weight` + judge weights must still sum to 1.0.
- **Edit anchors and examples** so the score reflects your house style.
- **Add a dimension** to a judge (e.g. a security-hygiene dimension inside `content`), then re-balance that rubric's dimension weights to sum to 1.0.
- **Add a judge** — drop a new `<stem>.json` in `rubrics/` and add `<stem>: { weight }` to `config.json`.

Forking already wrote `config.json`, so edit it in place rather than writing a new one in Step 5. Go to Step 6 to validate.

### Path B — Build from scratch

For each judge, create `$PLUGIN_DIR/skills/skill-reviewer/references/rubrics/<stem>.json`.

A rubric file must conform to `references/schemas/rubric.schema.json` (bundled). Key fields:

- `evaluation_target` — what is being evaluated (matches the judge's purpose)
- `scale` — `{ "min": 1, "max": 3 }` is standard
- `reference_examples` — `judging_guidelines` (array of strings), `good_overall_examples`, `bad_overall_examples`
- `dimensions` — array of scoring dimensions; weights within a rubric must sum to `1.0`

Each dimension needs: `id` (snake_case), `name`, `weight`, `question`, and `scores` (array with `score`, `anchor`, `example` for each level from min to max).

**Minimal rubric template:**

```json
{
  "$schema": "../schemas/rubric.schema.json",
  "evaluation_target": "<what-this-judge-evaluates>",
  "scale": { "min": 1, "max": 3 },
  "reference_examples": {
    "judging_guidelines": [
      "Award 3 only when <specific criterion>.",
      "Score 1 for <negative criterion>."
    ],
    "good_overall_examples": ["<example of a high-scoring skill>"],
    "bad_overall_examples": ["<example of a low-scoring skill>"]
  },
  "dimensions": [
    {
      "id": "dimension_one",
      "name": "Dimension One",
      "weight": 0.6,
      "question": "Does the skill <specific question>?",
      "scores": [
        { "score": 1, "anchor": "No evidence of <criterion>", "example": "<bad example>" },
        { "score": 2, "anchor": "Partial <criterion>", "example": "<ok example>" },
        { "score": 3, "anchor": "Clear and complete <criterion>", "example": "<good example>" }
      ]
    },
    {
      "id": "dimension_two",
      "name": "Dimension Two",
      "weight": 0.4,
      "question": "Does the skill <second question>?",
      "scores": [
        { "score": 1, "anchor": "...", "example": "..." },
        { "score": 2, "anchor": "...", "example": "..." },
        { "score": 3, "anchor": "...", "example": "..." }
      ]
    }
  ]
}
```

Dimension `weight` values within a single rubric must sum to `1.0` (separate from the plugin-level judge weights in `config.json`).

## Step 5 — Write `config.json` (scratch path)

Path A already copied a `config.json` — edit that one instead. For Path B, write it:

```bash
cat > "$PLUGIN_DIR/skills/skill-reviewer/references/config.json" << 'EOF'
{
  "$schema": "../schemas/config.schema.json",
  "validation_weight": <value>,
  "judges": {
    "<rubric-stem-1>": { "weight": <value> },
    "<rubric-stem-2>": { "weight": <value> }
  }
}
EOF
```

Verify the invariant: `validation_weight + sum of all judge weights = 1.0`.

## Step 6 — Validate

Create a throwaway skill to test against:

```bash
SKILL_DIR=$(mktemp -d)
cat > "$SKILL_DIR/SKILL.md" << 'EOF'
---
name: plugin-test
description: Use when testing a custom reviewer plugin.
---
# Plugin test
Use when verifying a custom reviewer plugin works correctly.
EOF
```

Run with your new plugin:

```bash
tessl review run "$SKILL_DIR" \
  --workspace <workspace-name> \
  --review-plugin "$PLUGIN_DIR" \
  --force \
  --json
```

**Healthy output** — the JSON should contain:
- `validation.overallPassed: true`
- `judges` map with one key per rubric stem
- `review.reviewScore` as an integer 0–100

If the plugin fails validation (bad weights, missing rubric, malformed schema), the API returns 400 with a message describing the exact problem. Fix the relevant file and re-run.

## Common problems

| Problem | Cause | Fix |
|---------|-------|-----|
| 400 "weights do not sum to 1.0" | `validation_weight + judge weights ≠ 1.0` | Adjust values in `config.json` |
| 400 "judges key X does not match any rubric" | Key in `config.json` has no matching `X.json` in `rubrics/` | Create the rubric or fix the key name |
| 400 "rubric dimensions weights" | Dimension weights in a rubric don't sum to 1.0 | Fix the `dimensions[].weight` values in that rubric |
| `judges` map empty in results | `SKILL.md` is missing the rubric-reading steps | Ensure `SKILL.md` includes the steps that read `config.json`/`rubrics/` and write `results.json` |
| Score always 0 | `validation_weight: 0` AND judge scoring all returned 0 | Check rubric anchors and examples |
