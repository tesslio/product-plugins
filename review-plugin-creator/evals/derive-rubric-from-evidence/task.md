# Derive a review-plugin rubric from gathered evidence

You are deriving a custom `tessl review` plugin rubric for a single skill, grounded in
evidence about how agents actually behaved with it. The evidence has already been gathered
for you (the gathering tools that would normally collect it — `/find-optimizations` and
`tessl agent-logs view` — are not available in this environment), so work from the files
provided rather than calling those tools.

## Inputs (in `./inputs/`)

- `inputs/target-skill/SKILL.md` — the skill the produced plugin will score. This is the baseline.
- `inputs/pr-feedback.md` — `/find-optimizations` output: recurring review findings, each with a
  Type, Summary, and Evidence.
- `inputs/agent-log.md` — an agent-log excerpt with two sessions.

## What to produce

Following the `derive-review-rubrics` workflow, map the evidence to rubric content and write
a single rubric **design file** to `./design.md` in your working directory. Do not scaffold a
plugin, copy schemas, or run `tessl review run` — that is `create-review-plugin`'s job, which
happens later. Do not modify any file under `./inputs/`.

The design file should describe the judges and their `evaluation_target`s, the scoring
dimensions with anchors and examples drawn from the evidence, the `scope` and `scoring_notes`
for any `content` judge, and the weight split. It should also record any evidence pattern that
does NOT belong in the rubric and where it should go instead.
