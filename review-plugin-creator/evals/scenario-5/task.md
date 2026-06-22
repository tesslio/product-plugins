# API Documentation Reviewer Plugin

## Problem Description

Your team is responsible for maintaining a set of internal developer tools, and the quality of API documentation has become a recurring issue. Engineers frequently publish API integration skills that are technically correct but poorly documented — the descriptions are vague, code examples are incomplete or wrong, and error handling guidance is either missing or confusing. This has led to a growing backlog of support tickets from developers who can't figure out how to properly use the APIs.

The team lead has asked you to create a custom reviewer plugin that evaluates API integration skills across three distinct areas: description quality (does the skill clearly convey when and how to use the API?), code example quality (are the usage examples accurate, runnable, and well-structured?), and error handling guidance (does the skill cover common failure modes and how to recover from them?). Each area should be covered by its own judge.

You have access to the `create-review-plugin` skill, which bundles the schema files and tooling you'll need. Use it to author the plugin from scratch — the team has specific opinions about what makes good API documentation that differ substantially from the default, so starting fresh is the right call. Place the completed plugin in `./api-docs-reviewer/`.

## Output Specification

Produce a complete, loadable reviewer plugin at `./api-docs-reviewer/`. The plugin should be fully self-contained: it must include the plugin manifest, a configuration file that distributes scoring weight across all three judges, the rubric files that define how each judge evaluates skills, and the schema files required by the platform.

Do not include a custom reviewer agent prompt — use the platform's built-in default.
