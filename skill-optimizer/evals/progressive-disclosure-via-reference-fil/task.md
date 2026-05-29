# Skill Length Reduction

## Problem Description

A developer has created a `notification-sender` skill to help agents send alerts through various channels. The skill file has grown large over time as more examples and configuration options were added inline. Users have noticed that the skill takes a long time to parse and the core instructions are buried under walls of examples.

A reference file (`REFERENCE.md`) already exists in the same skill directory and contains detailed examples, template configurations, and provider-specific options. The developer wants to slim down the main SKILL.md so it remains focused and scannable, while keeping the detailed reference material accessible.

Analyze the skill bundle below and produce a set of recommendations to reduce the length of SKILL.md by using the existing reference file more effectively. Include a revised version of SKILL.md in your output.

## Output Specification

Produce two files:
- `recommendations.md` — explaining what content should move where and why, with before/after examples for each proposed change
- `SKILL.md` — the revised, shorter version of the skill file

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: skills/notification-sender/SKILL.md ===============
---
name: notification-sender
description: |
  Sends notifications through Slack, email, and PagerDuty. Use when you need to alert a team about deployment events, incident escalations, on-call pages, or status updates.
---

# Notification Sender

Send alerts through Slack, email, and PagerDuty using our internal notification service.

## Slack Notifications

To send a Slack message, use the `notify` CLI:

```bash
notify slack --channel "#ops-alerts" --message "Deployment complete" --severity info
```

Available severity levels: `info`, `warning`, `critical`. Each maps to a different color in the Slack message:
- `info` → blue sidebar
- `warning` → yellow sidebar
- `critical` → red sidebar, also triggers @here mention

Thread replies can be sent using `--thread-ts <timestamp>` to keep alert threads organized.

For attachments, use `--attachment <file-path>`. Supported formats: PNG, PDF, TXT, JSON (max 5MB).

Slack rate limits: 1 message/second per channel. If sending bursts, add `--delay 1200` (milliseconds) between calls.

Emoji reactions can be added after the fact with `notify slack react --channel "#ops-alerts" --ts <ts> --emoji thumbsup`.

## Email Notifications

To send email:

```bash
notify email --to "oncall@company.com" --subject "Alert: High CPU" --body "CPU usage exceeded 90% on prod-web-01"
```

HTML bodies are supported with `--html-body <file>`. Plain text is preferred for simple alerts.

CC and BCC: use `--cc "manager@company.com"` and `--bcc "audit@company.com"` for copies.

Email templates are stored in `/etc/notify/templates/`. Available templates:
- `incident.html` — for incident notifications
- `deployment.html` — for deployment summaries
- `weekly_report.html` — for weekly digest emails

Template variables use `{{variable_name}}` syntax. Pass them with `--var key=value`.

Reply-to can be set with `--reply-to <address>` to route responses to a different inbox.

SMTP configuration is auto-loaded from environment. If sending fails, check `NOTIFY_SMTP_HOST` and `NOTIFY_SMTP_PORT` vars.

## PagerDuty

To trigger a PagerDuty incident:

```bash
notify pagerduty --service "prod-payments" --summary "Payment processor down" --severity critical
```

Severity levels map to PagerDuty urgency: `info`→low, `warning`→medium, `critical`→high.

Dedup keys prevent duplicate incidents: `--dedup-key <string>`. Use the same key to resolve an incident.

To resolve: `notify pagerduty resolve --dedup-key <string>`.

Custom details can be attached: `--details '{"host": "prod-web-01", "region": "us-east-1"}'.`

PagerDuty escalation policies are configured in the PagerDuty UI, not here.

## Multi-Channel Alerts

Send to multiple channels at once:

```bash
notify multi --channels slack,email,pagerduty \
  --slack-channel "#ops-alerts" \
  --email-to "oncall@company.com" \
  --pagerduty-service "prod-api" \
  --message "Critical: database unreachable" \
  --severity critical
```

This sends to all specified channels simultaneously.

## Error Handling

If a notification fails, `notify` exits with code 1 and prints an error to stderr. Common errors:
- `ECONNREFUSED` — SMTP or API endpoint unreachable
- `RATE_LIMIT` — Too many requests; add delay
- `AUTH_FAILED` — Check API keys in environment

Retry logic: `--retry 3 --retry-delay 5` retries up to 3 times with 5-second delays.

See [REFERENCE.md](REFERENCE.md) for complete CLI reference and advanced configurations.
=============== END FILE ===============

=============== FILE: skills/notification-sender/REFERENCE.md ===============
# Notification Sender — Complete Reference

## Slack

### Full Flag Reference
| Flag | Description | Default |
|------|-------------|---------|
| `--channel` | Target Slack channel | required |
| `--message` | Message text | required |
| `--severity` | info/warning/critical | info |
| `--thread-ts` | Thread parent timestamp | — |
| `--attachment` | File path to attach | — |
| `--delay` | ms delay for rate limiting | 0 |
| `--emoji` | Reaction emoji (with react subcommand) | — |

### Severity Color Mapping
- `info` → blue sidebar
- `warning` → yellow sidebar
- `critical` → red sidebar + @here mention

### Rate Limits
1 message/second per channel. Use `--delay 1200` for bursts.

## Email

### Full Flag Reference
| Flag | Description | Default |
|------|-------------|---------|
| `--to` | Recipient address | required |
| `--subject` | Email subject | required |
| `--body` | Plain text body | — |
| `--html-body` | HTML body file path | — |
| `--cc` | CC addresses | — |
| `--bcc` | BCC addresses | — |
| `--reply-to` | Reply-to address | — |
| `--var` | Template variable (key=value) | — |

### Available Templates
- `incident.html` — for incident notifications
- `deployment.html` — for deployment summaries
- `weekly_report.html` — for weekly digest emails

Templates are in `/etc/notify/templates/`. Variables use `{{variable_name}}` syntax.

## PagerDuty

### Full Flag Reference
| Flag | Description | Default |
|------|-------------|---------|
| `--service` | PagerDuty service name | required |
| `--summary` | Incident summary | required |
| `--severity` | info/warning/critical | warning |
| `--dedup-key` | Deduplication key | — |
| `--details` | JSON details object | — |

### Severity to Urgency Mapping
- `info` → low urgency
- `warning` → medium urgency
- `critical` → high urgency

### Resolving Incidents
```bash
notify pagerduty resolve --dedup-key <string>
```

## Multi-Channel

### Full Flag Reference
| Flag | Description |
|------|-------------|
| `--channels` | Comma-separated: slack,email,pagerduty |
| `--message` | Shared message for all channels |
| `--severity` | Shared severity for all channels |

## Error Handling

### Exit Codes
- 0: Success
- 1: Notification failed

### Common Errors
| Code | Meaning | Fix |
|------|---------|-----|
| ECONNREFUSED | Endpoint unreachable | Check NOTIFY_SMTP_HOST, NOTIFY_API_URL |
| RATE_LIMIT | Too many requests | Add --delay |
| AUTH_FAILED | Bad credentials | Check API keys |

### Retry Options
`--retry <n>` and `--retry-delay <seconds>` for automatic retries.

## Environment Variables
- `NOTIFY_SMTP_HOST` — SMTP server hostname
- `NOTIFY_SMTP_PORT` — SMTP port (default 587)
- `NOTIFY_SLACK_TOKEN` — Slack bot token
- `NOTIFY_PD_KEY` — PagerDuty integration key
=============== END FILE ===============
