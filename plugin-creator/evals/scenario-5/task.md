# Package a commit-message skill as a Tessl plugin

## Background

You are working inside an existing repository that already uses Tessl. The team
wants a reusable Tessl plugin that helps an agent write Conventional Commits
style commit messages: one skill that, given a staged diff, produces a properly
formatted commit message (type, optional scope, imperative summary, body, and
footer).

This is a simple, self-contained workflow, so a single skill is the right shape.

## Your task

Create the plugin on disk in this repository, ready to validate:

- Scaffold a Tessl plugin named `commit-writer` in the `tessl` workspace, with a
  single skill that writes Conventional Commits messages.
- Author the skill's `SKILL.md` with a strong description (what it does and when
  to reach for it) and a few ordered steps.
- Run the appropriate Tessl CLI validation to confirm the plugin is structurally
  sound.

Do not publish. Leave the finished plugin on disk in the repository.
