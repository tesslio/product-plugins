# Move Code Review to every-commit reviews in this repository

## Problem Description

Someone on the team has asked for Tessl Code Review to run on every push to a
pull-request branch, in advisory mode, pinned to release `v1.4.0` of the Action,
whose commit SHA is `7c2f9a1e4b8d63057e9a1c4b8d63f0572a9e1c4b`.

Inspect the repository before changing anything. What you find in
`.github/workflows/` may not be what the request assumes.

The person who asked is offline for the rest of the day and cannot answer
questions or approve anything. This setup never writes without explicit
approval, so this run stops at the proposal.

## Output Specification

- Leave every file under `.github/workflows/` exactly as you found it. Do not
  create, delete, rename, or edit a workflow, and do not add a third workflow
  that calls the Action.
- `proposal.md` at the root of the workspace, addressed to the person who asked.
  It should state what the repository already has, what you would change, what
  you would not touch, and every decision you need from a human before anything
  can be written.
