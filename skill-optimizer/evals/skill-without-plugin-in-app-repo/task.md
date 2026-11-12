# Plan Evals for a Skill in an Application Repository

## Problem Description

A developer works in a Go application repository. The repository ships an agent skill with the product, at `skills/pane-reader/SKILL.md`. The developer has never built a Tessl plugin and does not know the difference between a plugin and a skill. They open a terminal at the repository root and ask: "Set up evals for the skill in this repo."

Earlier they ran `tessl scenario generate` from the repository root, and it failed with "No manifest found".

Tessl CLI commands cannot run in this environment, and you cannot ask the developer questions. Write the plan instead: the exact commands, in order, that you would run from the repository root to generate scenarios for the skill and run its first eval.

## Output Specification

Write `eval-setup-plan.md` containing:

1. Which plugin or skill you chose to evaluate, and why.
2. Every command, in order, exactly as you would run it from the repository root.
3. For each command that changes files in the repository, which files it changes.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/repo-files.txt ===============
# Output of `git ls-files` at the repository root
.github/workflows/ci.yml
.tessl/plugins/tessl/factory/.tessl-plugin/plugin.json
.tessl/plugins/tessl/factory/skills/shepherd/SKILL.md
AGENTS.md
README.md
go.mod
internal/cmd/serve.go
internal/cmd/page.go
main.go
skills/pane-reader/SKILL.md
tessl.json
=============== END FILE ===============
