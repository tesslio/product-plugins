# The `schedules` block in tessl.json

The `schedules` block is a top-level object in a project's `tessl.json`. It maps
a **schedule key** to a **schedule entry**. Each entry declares one recurring
launch run.

```json
{
  "schedules": {
    "<schedule-key>": {
      "skill": "...",
      "schedule": "weekdays at 09:00",
      "environment": "..."
    }
  }
}
```

## Schedule key

- A lowercase kebab-case slug: `a-z`, `0-9`, single dashes, 1 to 64 chars
  (pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`).
- It is the schedule's stable identity, not a display label. The value ends up
  in refs, so it must survive without escaping.
- Renaming a key is a delete-plus-create, never a rename. Pick a durable slug.

## Entry fields

The entry is validated **strictly**: a field name that is not in this list is a
hard error (this catches typos the author would otherwise only notice when the
schedule misbehaves). Use only these fields.

### Required

| Field | Type | Notes |
| -- | -- | -- |
| `skill` | string | The skill to run: a registry ref `workspace/plugin[@version][#skill]`, or a repo-local `file:path`. Validated server-side at apply time. |
| `schedule` | string or object | Preferred authoring key. Accepts a supported shorthand string, a raw cron string, or a structured schedule object. The value is interpreted in `timezone`. |
| `cron` | string or object | Alias for `schedule`. Use it for a raw cron fallback when the shorthand and structured forms cannot express the cadence. |
| `environment` | string | The workspace environment **name** (not its id). The id is workspace-scoped, so a committed file names the environment and the apply step resolves it to an id in the target workspace. |

Use exactly one of `schedule` or `cron`, never both. Both forms are compiled to
canonical cron before timezone and minimum-interval validation. A shorthand or
structured value is easier for humans to review, so prefer `schedule` for new
entries.

## Schedule values

The supported shorthand strings are:

| Form | Example |
| -- | -- |
| `hourly` | `hourly` |
| `daily at HH:MM` | `daily at 02:00` |
| `weekdays at HH:MM` | `weekdays at 09:00` |
| `weekly on DAY at HH:MM` | `weekly on monday at 13:00` |
| `monthly on Nth at HH:MM` | `monthly on 1st at 00:00` |
| `every N minutes` | `every 15 minutes` |
| `every N hours` | `every 6 hours` |
| `every N minutes between HH:MM-HH:MM` | `every 15 minutes between 09:00-17:00` |
| `every N minutes on weekdays` | `every 15 minutes on weekdays` |

For a cadence that does not fit a shorthand, use a structured object. Each
field is optional and omitted fields match any value:

```json
{
  "schedule": {
    "minute": [0, 30],
    "hour": 9,
    "day": {"between": [1, 7]},
    "month": ["january", "jun"],
    "weekday": ["mon", "wed", "fri"]
  }
}
```

Numeric fields (`minute`, `hour`, and `day`) accept a number, a list of
numbers, `{ "every": number }`, or `{ "between": [start, end] }`. `month` and
`weekday` accept numbers, lists, or supported names such as `january` and
`monday`. Use a raw five-field cron under `cron` when the structured object
cannot express the requested pattern.

### Optional

| Field | Type | Default | Notes |
| -- | -- | -- | -- |
| `timezone` | string | `UTC` | IANA timezone the cron is interpreted in (e.g. `America/New_York`). |
| `baseBranch` | string | `main` | Branch each fired run clones and targets its PR against. |
| `snapshot` | string | none | Commit SHA or tag pinning the repo snapshot each run starts from. |
| `workdir` | string | repo root | Subdirectory of the repo the skill runs in. |
| `agent` | string | workspace default | Agent to run the skill with. Plain string, validated server-side. |
| `model` | string | agent default | Model to run the skill with. Plain string, validated server-side. |
| `inputs` | object | none | Skill input values, keyed by the skill's own placeholder names. String values only; keys must be non-empty. |
| `instructions` | string | none | Free-text instructions appended to the skill prompt. |
| `description` | string | none | Human-readable description of the schedule (max 4096 chars). |

## What `tessl schedule validate` does and does not check

`validate` reads the file and checks the block's **shape**, compiles each
`schedule` or `cron` value, validates the resulting expression against its
timezone, and checks the **minimum 5-minute interval**. It exits non-zero when
the block is invalid, so it works as a CI check. A manifest with no `schedules`
block is valid.

It does **not** check (these are decided at apply time, in the workspace):

- whether the `skill` ref resolves to a plugin the workspace can use;
- whether the named `environment` exists in the workspace or carries a GitHub
  token;
- whether the `agent` and `model` are in the organization's catalogue;
- the limit of 20 active schedules per workspace.

So a file that passes `validate` can still be rejected when applied. A clean
`validate` means the file is well-formed, not that the schedule will fire.

## Example with optional fields

```json
{
  "schedules": {
    "weekly-dependency-digest": {
      "skill": "tessleng/dependency-digest",
      "schedule": "weekly on monday at 13:00",
      "timezone": "UTC",
      "environment": "dependency-digest",
      "agent": "claude",
      "model": "claude-sonnet-4-6",
      "description": "Weekly dependency digest, Mondays 13:00 UTC"
    }
  }
}
```
