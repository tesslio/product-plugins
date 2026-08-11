---
name: review-scale-and-resilience
description: Review a change for what happens when there is more of it than expected, and when something it depends on fails. Use as one lens in a code review run.
---

# Review lens: Scale and Resilience

Review what the change costs as load, data volume, and concurrency grow, and what it does when something it depends on fails.

## Scope

- **Performance** What the change does repeatedly that it could do once, and what it costs per unit of work.
- **Scalability** How that cost grows with the size of the input, the number of callers, or the depth of the data.
- **Stability** How the change behaves under realistic failure and rollout conditions: slow dependencies, duplicate execution, and deployments where old and new code run concurrently.
- **Availability** Whether a failure stays bounded, visible and recoverable, or turns a transient fault into a persistent or expanding one.

## Method

Prioritize work on request paths, fan-out operations, and batch processing.

Derive failure cases from the operations the change performs, including external calls, writes, and retries. Check behavior for delayed, duplicate, and missing responses.

What counts as adequate failure coverage or a safe rollout is often a written project rule rather than a judgment call. Read the `AGENTS.md` or `CLAUDE.md` chain governing the changed files, from the repository root down.

## Threshold

Report costs that grow materially with expected workload, or failures that can affect work beyond the original request or operation.

Do not report cold-path inefficiencies or scenarios that depend on several unlikely failures occurring together.

## Reporting

- Name what scales the cost, per request, per row, per user or per tenant, and the realistic upper bound.
- For a failure, name the fault that triggers it and what breaks when it does.
- State what would contain it: the bound, the timeout, the checkpoint, the signal an operator would need.
