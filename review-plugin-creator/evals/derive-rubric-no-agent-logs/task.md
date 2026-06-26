# Rubric Design from PR Feedback (No Agent Logs Available)

## Problem/Feature Description

Your team maintains a set of skills used by AI agents in a cloud-based CI pipeline. Over the past quarter, the team has accumulated a significant backlog of PR review comments about skill quality — and your tech lead wants to introduce automated skill review to catch recurring issues before they reach code review.

You have been asked to produce a rubric design document that can be handed off to the plugin scaffolder. The design should describe which judges to create, what each judge evaluates, the rubric dimensions and their relative weights, and example anchors drawn from real review comments.

You are working in a cloud sandbox environment where `tessl agent-logs` is unavailable and the `tessl` CLI cannot be run. You will need to work from the provided skills and PR feedback alone.

Three sample skills are available in `inputs/sample-skills/` — one for code formatting, one for test generation, and one for API scaffolding. A collection of recurring PR review comments is available in `inputs/pr-feedback.md`.

## Output Specification

Produce a single file `rubric-design.md` in your working directory. The design document should include:

- A statement acknowledging that agent-log evidence is unavailable and describing what that means for the design
- A list of proposed judges, each with:
  - A name
  - An `evaluation_target` (what type of artifact it judges)
  - A list of rubric dimensions with proposed weights (weights within each judge should sum to 1.0)
  - For each dimension: a question the judge will answer, and example anchors drawn from the actual PR feedback provided
- For each evidence pattern from the PR feedback, a classification of what kind of quality check it represents — e.g. a subjective judgment call vs. a binary pass/fail check — with a brief reason
- A note on how weights were assigned, referencing the frequency and severity information in `inputs/pr-feedback.md`
- A final section explaining what `/create-review-plugin` would need to do next with this design document (but do NOT scaffold any directories, copy any schemas, or run any CLI commands)
