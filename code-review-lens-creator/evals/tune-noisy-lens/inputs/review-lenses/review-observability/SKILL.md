---
name: review-observability
description: Review a change for observability. Use as one lens in a code review run.
---

# Review lens: Observability

Review the change for observability and make sure the team can understand what the system is doing in production.

## Scope

- **Logging** Whether the code logs.
- **Metrics** Whether the code emits metrics.
- **Tracing** Whether operations are traced.

## Method

Read the diff and consider the observability of each function that was added or changed. Think about whether an engineer looking at this code in production would have enough information.

## Threshold

Report anywhere the observability of the change could be improved. Be thorough: observability gaps are cheap to fix at review time and expensive later, so it is better to raise a possible gap than to miss one.

## Reporting

- Assess the overall observability posture of the change and summarize it.
- Mark a finding as critical when the gap affects a production code path, and minor when it does not.
- Recommend improving the logging where it is weak.
