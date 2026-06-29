# Build a Security Hygiene Reviewer Plugin

## Problem Description

The platform engineering team at a growing SaaS company has noticed that many skills submitted by internal teams omit any mention of security requirements, data handling responsibilities, or safe usage warnings. When agents execute these skills in production, they sometimes invoke privileged APIs or handle sensitive user data without any guidance baked into the skill itself. The team wants an automated quality gate that scores each new skill specifically for security hygiene — not general writing quality, but whether the skill adequately informs the agent about authorization requirements, how to handle sensitive data, and any warnings a caller should know before using the skill.

The company uses the `tessl` platform to run skill reviews. The platform supports custom reviewer plugins that let teams define their own scoring rubrics and judges. The team wants a brand new reviewer plugin — purpose-built for security hygiene — placed at `./security-reviewer`. Because the review focus is entirely different from the platform's built-in content/description rubric, they want it built fresh rather than adapted from an existing one. The plugin should use a single judge called `security` that carries the entire non-validation scoring weight, with the validation component excluded from the final score. The team also wants a `summary.md` at the root of the workspace that documents the plugin structure you created, the judges configured, and the weight values chosen.

## Output Specification

Produce the following files:

- The complete plugin directory at `./security-reviewer/`, including:
  - Plugin metadata file under `.tessl-plugin/`
  - A `skill-reviewer` skill with a reviewer agent instruction file (`SKILL.md`)
  - Schema files for rubric and config validation under `references/schemas/`
  - A rubric file named `security.json` under `references/rubrics/` defining the security hygiene evaluation dimensions
  - A `config.json` under `references/` wiring up the judge and weights
- `summary.md` — a markdown document describing the plugin structure you created, the judges and rubrics defined, and the weight values chosen

The reviewer plugin should be ready to use with `tessl review run` once the platform is available. Do not attempt to run it — just produce the files.
