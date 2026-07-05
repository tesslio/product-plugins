# Build a PR Review Skill for the Engineering Team

## Problem Description

Your engineering team has started using Tessl to share reusable agent workflows, and the team lead wants to add a pull-request review workflow to the shared plugin registry. Right now, developers rely on ad hoc checklists or personal notes when reviewing PRs — there is no consistent process, and newer team members miss common issues around correctness, style, and security.

The team lead has asked you to create a Tessl skill that an agent can follow when reviewing a pull request. The skill should cover the full review process: checking for logic bugs, evaluating code style consistency, flagging potential security concerns, and summarising findings. It should be written so that another developer or an AI agent can pick it up and use it without hand-holding.

The team lead wants this shipped as the smallest reasonable Tessl artifact — not a large multi-skill bundle unless that is genuinely needed. The skill (and any supporting files) should be placed on disk in a directory structure ready for use with Tessl tooling.

## Output Specification

Produce the following on disk:

- A Tessl plugin directory (e.g. `.tessl-plugin/` or a named folder) containing:
  - A `plugin.json` manifest
  - A skill folder containing a `SKILL.md` entry point
  - Any supporting reference files your skill links to
- A `plan.md` file at the top level of your working directory that explains:
  - The shape you chose (single skill vs multi-skill plugin) and why
  - How you named the skill and why
  - What you put in `SKILL.md` versus any `references/` files, and why
  - Any design decisions about the description field

Do not include the actual CLI output or session logs — just the final files and the `plan.md` explaining your decisions.
