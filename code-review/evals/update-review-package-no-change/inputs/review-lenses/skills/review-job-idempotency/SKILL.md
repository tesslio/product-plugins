---
name: review-job-idempotency
description: Review job changes for repeated side effects after retry. Use as one lens in a code review run.
---

# Review lens: Job idempotency

Trace each durable write across retry. Report when replay can repeat an external
side effect without an idempotency key or durable completion marker. Do not
report reads or writes protected by a unique operation key.
