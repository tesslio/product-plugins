# Writing a schedule from a plain-language cadence

The user describes how often to run in plain words. Use the `schedule` key with
the closest supported shorthand whenever possible. Never ask the user for a
cron expression.

If no shorthand matches, use a structured schedule object when its fields can
describe the cadence. Otherwise fall back to a raw five-field cron under the
`cron` key. The `schedule` key also accepts raw cron, but keeping raw cron as an
explicit fallback makes the readable cases easier to spot.

## Supported shorthand

Shorthand is case-insensitive and uses a 24-hour clock with two-digit hours and
minutes. Write it under `schedule`.

| User cadence | `schedule` value | Reading |
| -- | -- | -- |
| every hour | `hourly` | top of every hour |
| every day at 2am | `daily at 02:00` | daily, 02:00 |
| weekdays at 8am | `weekdays at 08:00` | Monday to Friday, 08:00 |
| every Monday at 1pm | `weekly on monday at 13:00` | weekly, Monday 13:00 |
| every Sunday night at 11 | `weekly on sunday at 23:00` | weekly, Sunday 23:00 |
| first of the month at midnight | `monthly on 1st at 00:00` | monthly, 1st at 00:00 |
| every 15 minutes | `every 15 minutes` | :00, :15, :30, :45 |
| every 6 hours | `every 6 hours` | 00:00, 06:00, 12:00, 18:00 |
| every 15 minutes during the workday | `every 15 minutes between 09:00-17:00` | every 15 minutes from 09:00 through 16:45 |
| every 15 minutes on weekdays | `every 15 minutes on weekdays` | every 15 minutes, Monday to Friday |

Supported forms are:

- `hourly`
- `daily at HH:MM`
- `weekdays at HH:MM`
- `weekly on DAY at HH:MM` (full or three-letter weekday names)
- `monthly on Nth at HH:MM` (for example, `1st`, `2nd`, or `11th`)
- `every N minutes`
- `every N hours`
- `every N minutes between HH:MM-HH:MM`
- `every N minutes on weekdays`

Intervals must compile to a cron field exactly. For example, `every 15
minutes` is valid, but `every 7 minutes` is not. A minute window excludes its
end time and multi-hour windows must start and end on whole hours.

## Raw cron fallback

Use `cron` only when the requested pattern is not covered by the shorthand or
structured object forms:

```json
{
  "cron": "0 9 1 * 1"
}
```

This runs at 09:00 on Mondays and on the first day of each month. The
shorthand and structured object forms do not express this combined pattern.

## Field order

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday = 0)
│ │ │ │ │
* * * * *
```

The cron is interpreted in the entry's `timezone` (UTC by default). If the user
gives a local time ("9am Eastern"), set `timezone` to the matching IANA name
(e.g. `America/New_York`) rather than converting the time to UTC by hand.

## The 5-minute floor

The tightest interval between two fires must be **at least 5 minutes**. A
per-minute cron (`* * * * *`) or `*/1 * * * *` is rejected by
`tessl schedule validate`. If the user asks for something more frequent than
every 5 minutes, tell them the floor and agree on the closest allowed cadence
(e.g. `*/5 * * * *`).

## Confirm before writing

State the chosen schedule back in plain words so the user can catch a mistake,
for example, "`weekdays at 09:00` runs Monday to Friday at 09:00 UTC." A wrong
schedule fires silently at the wrong time, so this readback is worth the extra
line.
