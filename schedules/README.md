# tessl/schedule-setup

Set up a repo-defined schedule from a plain-language description.

A repo-defined schedule is a recurring run declared in your project's `tessl.json`. It is reviewed and version-controlled next to the code it runs against. On push to the default branch, Tessl reads the file and creates the schedule.

This skill turns a plain-language request into a validated `schedules` entry. Describe the task, cadence, and environment in your own words, and the skill chooses the most readable supported format, writes the entry, validates it, and explains what happens on push. If you don't have a skill for the task yet, it can author a repo-local one with credential pre-flight checks for Linear, Slack, and Notion.

## What the skill does

1. **Gathers requirements one at a time.** Which skill to run, how often, and which environment. Optional fields (agent, model, timezone, instructions) only if you raise them.
2. **Authors a new skill if needed.** When you don't have a skill for the task, the skill scaffolds one with `tessl skill new`, writes the workflow in `SKILL.md`, and wires up credential pre-flight scripts for any provider it uses.
3. **Picks the right schedule format.** Human-readable shorthand first (`daily at 09:00`, `weekdays at 14:00`), structured object when needed, raw cron as a last resort. You describe the cadence in plain language; the skill translates it.
4. **Writes and validates the entry.** Adds it to the `schedules` block in `tessl.json`, runs `tessl schedule validate`, and fixes anything it catches.
5. **Explains what happens next.** Commit, push to the default branch, and Tessl creates the schedule. The skill tells you what to expect and what to check if the schedule doesn't appear.

## Example

Ask your agent:

> "Set up a nightly report that runs at 2am UTC using the production environment"

The skill will ask which skill to run (or offer to create one), confirm the cadence, and write:

```json
{
  "schedules": {
    "nightly-report": {
      "skill": "acme/report-writer",
      "schedule": "daily at 02:00",
      "environment": "production",
      "description": "Nightly report"
    }
  }
}
```

## Skills

| Skill | Description |
| --- | --- |
| `schedule-setup` | Turn a plain-language request into a validated `schedules` entry in `tessl.json`. |

## Related

- [Schedules documentation](https://docs.tessl.io/schedules/overview) for the full field reference and sync behaviour.
- [Validate schedules in CI](https://docs.tessl.io/schedules/validate-in-ci) to catch errors before they reach production.
