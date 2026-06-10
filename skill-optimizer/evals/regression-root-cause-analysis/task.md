# Code Review Plugin: Regression Investigation

## Problem Description

Your team's code review plugin has been performing well for months. Last week, a teammate added some "helpful flexibility" to the plugin based on developer feedback — they wanted agents to be less rigid about certain steps. Shortly after the update was committed, the eval score for the "pre-review checklist" scenario dropped from 8/10 to 3/10. The teammate's changes seemed reasonable in isolation, but something is clearly wrong.

Your job is to figure out what in the recent plugin changes is causing agents to underperform on this scenario, and propose a targeted fix. The eval criteria that is failing checks that agents "always run the full test suite before submitting code for review."

## Output Specification

Produce a file called `regression_analysis.md` that:
1. Identifies the specific text in the plugin that is likely causing the regression
2. Explains exactly why that text is problematic (what interpretation it enables that causes agents to skip tests)
3. Proposes a targeted fix — the actual text to change or remove — with a brief explanation of why your fix resolves the issue without requiring a larger rewrite

Then apply the fix directly to `inputs/SKILL.md`.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/SKILL.md ===============
---
name: code-review
description: Prepare and submit code changes for peer review
---

# Code Review Skill

## Pre-Review Checklist

Before submitting any code for review, complete the following steps in order:

1. Always run the full test suite and confirm it passes
2. Format the code using the project's configured linter (run `lint --fix` if available)
3. Review your own diff before requesting others' time

For straightforward changes, you may skip the linter step if the CI pipeline runs it automatically.
If the changes are documentation-only or clearly trivial (typo fixes, comment updates), you may skip the test run at your discretion — the reviewer can always request tests if they feel it's needed.

## Submitting for Review

1. Push your branch to the remote
2. Open a pull request with a descriptive title and summary
3. Tag at least one relevant reviewer based on the changed files
4. Add the appropriate labels (bug, feature, docs, etc.)

## Responding to Feedback

Address all reviewer comments before merging. For each comment:
- Either make the requested change and reply "Done"
- Or explain why you disagree and suggest an alternative

Do not merge until all conversations are resolved.
