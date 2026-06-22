# Debug a Broken Reviewer Plugin

## Problem Description

Your team recently inherited a custom reviewer plugin from a colleague who left before finishing it. The plugin is supposed to evaluate SKILL.md files for writing quality. However, when the team tried to deploy it, they got a series of cryptic 400 errors from the review system and gave up.

Your job is to get this plugin into a working state. The plugin directory is at `inputs/plugin/`. It contains a `config.json` that configures the scoring weights and references the rubric judges, plus a `rubrics/` directory with the rubric JSON files.

The plugin has multiple issues that are preventing it from running. You'll need to read through the configuration and rubric files, identify what's wrong, fix each issue, and document what you found and changed.

## Output Specification

Produce the following in your working directory:

1. **A corrected `inputs/plugin/` directory** — fix all configuration and rubric issues in-place so the plugin would pass validation if run through the review system.

2. **`fix-log.md`** — a plain-text log documenting:
   - Each problem you found (file, what was wrong, what it should be)
   - The correction you made for each problem
