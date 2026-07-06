# Skill Improvement Context Analysis

## Background

The platform team at Acme Corp has a deployment skill that's been in use for several months. Recently, the team lead noticed that the same mistakes keep appearing in PRs — engineers keep skipping steps or getting confused about what the deployment process actually requires. The team wants to improve the skill so these gaps are closed.

A colleague has handed over two artifacts for you to work with:

- `inputs/SKILL.md` — the current deployment skill as it exists today
- `inputs/pr-feedback.json` — a summary of recurring review comments left by senior engineers on recent deployment PRs, showing patterns of what goes wrong repeatedly

The team lead's request is: "I want to improve this skill and package it up properly. Can you analyze what we have and tell me what we know and what we still need to find out?"

## Output Specification

Produce a file called `context-analysis.md` in the current directory with the following sections:

1. **Problem Summary** — One or two sentences describing what is wrong with the current skill, based on what you can see in the existing materials.

2. **What We Already Know** — A list of gaps, missing steps, or improvements that can be inferred directly from the existing `SKILL.md` and the PR feedback. For each item, note the source (e.g., which recurring comment pattern it came from, or what in the SKILL.md reveals it).

3. **Questions for the Team Lead** — A list of questions that genuinely cannot be answered from the available materials — things that only the team lead or domain experts would know. Do not include questions whose answers are already present in the artifacts.

4. **Proposed Skill Description** — A revised one-sentence description for the improved skill. This should state both what the skill does and when a developer should reach for it.
