---
name: schedule-setup
description: Create a repo-defined schedule in a project's tessl.json from a plain-language description, optionally authoring the repo-local skill it runs. Use when the user wants to schedule a skill to run on a recurring cadence ("run X every morning", "kick off the report nightly", "schedule this weekly"), set up a recurring launch run, or add a `schedules` block to tessl.json. The user describes the task, cadence, and environment in plain words; this skill chooses the most readable supported schedule format, adds and validates the entry, and explains what happens on push. Not for one-off runs (use `tessl launch`) or for moving an existing UI/CLI schedule into the file (use schedule-migrate).
---

# Set up a repo-defined schedule

Turn a plain-language request ("run the nightly report at 2am") into a valid
`schedules` entry in the project's `tessl.json`, optionally author the
repo-local skill it runs, validate the entry, and tell the user what happens
next.

A repo-defined schedule is a recurring launch run declared in `tessl.json` so it
is reviewed and version-controlled next to the code it runs against. On push to
the default branch, Tessl reads the file and creates the schedule.

Read [the schedules block reference](references/schedules-block.md) for the full
field list and [the cadence reference](references/cron-cadence.md) before writing
a schedule.

## Communication rules

- Ask about one thing at a time. Do not ask for the skill, cadence, and
  environment in a single prompt.
- Explain each concept in one or two plain sentences, right before the user
  needs it.
- The user describes the cadence in plain language. You choose a supported
  shorthand first, then a structured schedule object or raw cron when needed.
  Never ask the user for a cron expression.
- Confirm the schedule you derived in plain words ("that's every day at 02:00
  UTC") so the user can catch a mistake.

## 1. Preflight

- Work from the repository root, where `tessl.json` lives.
- Confirm the file exists. If there is no `tessl.json`, the project is not a
  Tessl project yet; tell the user to run `tessl init` first and stop.
- Read the current `tessl.json`. Note whether a `schedules` block already
  exists and what keys it holds, so a new entry does not collide with an
  existing key.
- Check the current Tessl CLI surface with `tessl schedule --help` rather than
  assuming flags.

## 2. Gather what to schedule

Collect these one at a time. The three the file requires are the **skill**, the
**cadence**, and the **environment**.

- **Skill**: which skill runs on the schedule. If the user names an existing
  skill, use it without running the authoring branch. It becomes the entry's
  `skill` field in one of two forms:
  - A registry ref: `workspace/plugin[@version][#skill]` (e.g.
    `tessleng/dark-factory-report`, or `acme/reports#weekly` to pick one skill
    from a multi-skill plugin).
  - A repo-local plugin: `file:path/to/plugin` (e.g.
    `file:plugins/dark-factory-report`), relative to the repo root.
  - If the user names a plugin but not which skill, and the plugin has more
    than one skill, ask which skill.
  - If the user does not name a skill, ask whether they want to choose an
    existing one or create a repo-local skill. If they want a new skill,
    collect what it must do, then follow **Author a new skill** after choosing
    the environment. Use the new repo-local plugin's `file:` ref in the
    schedule entry.
- **Cadence**: how often, in plain language. Convert common patterns to a
  supported shorthand using [the cadence reference](references/cron-cadence.md).
  Use the `schedule` key for shorthand strings. For patterns that shorthand
  cannot express, use a structured schedule object or fall back to a raw
  five-field cron. Default the timezone to UTC. If the user gives a local time,
  ask which timezone (or use a timezone they have already stated) and set
  `timezone` to an IANA name (e.g. `America/New_York`).
- **Environment**: the workspace environment whose variables each run gets.
  This is the environment **name**, not its id (a committed file names the
  environment; the id is resolved per workspace at apply time). If the user is
  unsure, list options with `tessl env list --workspace <workspace>` and let
  them pick.

Optional fields, only if the user raises them (see
[the schedules block reference](references/schedules-block.md) for all of them):
`agent`, `model`, `baseBranch`, `snapshot`, `workdir`, `inputs`,
`instructions`, `description`.

## 3. Author a new skill

Skip this section when the schedule uses an existing skill. Do not edit or add
files to that skill.

When the user asks for a new skill:

1. Scaffold the requested skill as a repo-local plugin with `tessl skill new`,
   using the selected workspace and a path that follows the repository's
   existing plugin conventions. If none exist, use `plugins/<skill-name>`. Write
   the requested workflow in the generated `SKILL.md`, then use the plugin
   path as the schedule entry's `file:` ref.
2. Identify which of Linear, Slack, and Notion the requested skill calls. For
   each provider it uses, create the new skill's `scripts/` directory and copy
   that provider's `.sh` file verbatim and unmodified from this skill's
   `scripts/` directory. If it uses none of the three providers, create no
   `scripts/` directory and skip the remaining pre-flight steps.
3. Inspect the selected environment's variable names with
   `tessl env view --json --workspace <workspace> <environment>`. Values are
   sealed; only the names for the providers the skill uses are needed.
4. Make credential pre-flight the generated skill's first step, before any
   other work. Add one invocation for each copied script:

   ```bash
   bash "$(git rev-parse --show-toplevel)/<skill-path>/scripts/linear.sh" "LINEAR_TOKEN"
   bash "$(git rev-parse --show-toplevel)/<skill-path>/scripts/slack.sh" "SLACK_BOT_TOKEN"
   bash "$(git rev-parse --show-toplevel)/<skill-path>/scripts/notion.sh" "NOTION_TOKEN"
   ```

   Replace `<skill-path>` with the repo-relative path of the skill directory
   that holds the copied scripts (`<plugin-path>/skills/<skill-name>`), not the
   plugin path from step 1. Do not use a bare `scripts/...` path. Include only
   the lines for providers the skill uses. Pass the same variable name that the
   generated skill uses for that provider's API calls. Prefer the canonical
   name. If it is absent, use a name ending `_LINEAR_TOKEN`,
   `_SLACK_BOT_TOKEN`, or `_NOTION_TOKEN` on the matching line. If more than one
   accepted name is available, ask which one the skill should use. Match an
   exact canonical name or the underscore-prefixed suffix only; a bare
   substring is not a match.

5. State in the generated skill that a non-zero result from any invocation
   means stop before doing anything else.

This pre-flight covers only the pinned providers the authored skill uses:
Linear, Slack, and Notion. A skill that uses another service or none of these
three gets no check; do not guess or create checks for other services. It
covers only skills created through this branch; existing skills are untouched.
Checking every scheduled skill would require a platform launch-preflight hook
and is outside this workflow.

## 4. Choose a schedule key

The key is the schedule's stable identity in the `schedules` map: a
lowercase kebab-case slug (`a-z`, `0-9`, single dashes), not a display label.
Derive it from the job (e.g. `nightly-sales-report`). Renaming a key later is a
delete-plus-create, so pick a durable one. It must not collide with an existing
key in the block.

## 5. Write the entry

Add the entry under a top-level `schedules` object in `tessl.json`. Create the
`schedules` object if it does not exist; otherwise add the key alongside the
existing ones. Preserve the rest of the file. Do not reorder or drop other
keys.

A minimal entry:

```json
{
  "schedules": {
    "nightly-sales-report": {
      "skill": "file:plugins/dark-factory-report",
      "schedule": "daily at 02:00",
      "environment": "dark-factory-report",
      "description": "Nightly sales report"
    }
  }
}
```

Rules that the validator enforces. Get them right the first time:

- `skill`, one of `schedule` or `cron`, and `environment` are required. Use
  `schedule` for shorthand strings and structured objects by default.
- `schedule` and `cron` are aliases; never include both in one entry. Use
  `cron` with a raw expression only when the shorthand and structured forms do
  not express the requested cadence.
- The entry is **strict**: an unknown or misspelled field name is a hard error,
  not a silent ignore. Only use the fields listed in the reference.
- A shorthand or structured schedule is compiled to cron for validation. Its
  tightest interval must be **at least 5 minutes** apart. A per-minute cron is
  rejected.
- Keep JSON valid: quote every key and string, no trailing commas, no comments.

## 6. Validate

Run the check from the repo root:

```bash
tessl schedule validate
```

It reads `tessl.json`, validates the `schedules` block, and reports every
problem against the key it belongs to. It exits non-zero when the block is
invalid. Fix anything it reports and run it again until it passes.

`validate` checks the file only: shape, schedule expressions, and the minimum
interval. It does **not** confirm that the environment exists in the workspace,
that the skill is installable, or that the agent/model are in the
catalogue. Those are checked when the file is applied. Tell the user this so a
clean `validate` is not mistaken for a guarantee the schedule will fire.

## 7. Explain what happens next

Once `validate` passes, tell the user in plain language:

1. Commit the `tessl.json` change and push it to the repo's **default branch**
   (usually `main`). Repo-defined schedules are reconciled only from the
   default branch. A push to a feature branch does nothing.
2. On that push, Tessl's GitHub App reads `tessl.json` and creates the
   schedule. This needs the Tessl GitHub App installed on the repo and the
   repo-defined-schedules feature enabled for the workspace.
3. The new schedule then appears in `tessl schedule list` and in the UI, and
   fires a launch run on its cron.

If the schedule does not appear after the push, the usual causes are: the push
was not to the default branch, the named environment does not exist in the
workspace, the feature is not enabled, or the workspace has reached the limit of
**20 active schedules**. The active-schedule cap is enforced at apply time and
not reported by `validate`: the schedule is silently skipped, not rejected with
an error. If nothing else explains a missing schedule, run
`tessl schedule list --json --limit 100` and count the active entries. Point the
user at these causes rather than re-editing the file.
