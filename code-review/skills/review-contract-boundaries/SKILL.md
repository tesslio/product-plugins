---
name: review-contract-boundaries
description: Review a diff for contract and compatibility risks at boundaries — API schemas, generated clients, CLI flags, event payloads, database migrations, and workflow or job contracts — where a change can break an existing consumer. Use as a contract review lens in `tessl change review` or a GitHub Actions review workflow. Reports high-confidence, file-anchored findings.
---

# Review Contract Boundaries

A contract review lens for `tessl change review`. Boundaries are where one piece
of software relies on the shape of another. Review the diff for changes that
break, or risk breaking, an existing consumer of a boundary, and report
concrete, actionable findings.

## Stance

- Review the diff first. Read a schema, client, or consumer only to confirm
  whether a changed contract still satisfies it.
- Report a finding when you can name the boundary, the change, and the consumer
  it affects.
- Distinguish a backwards-compatible addition from a breaking change. Flag the
  break and the missing migration or version step.
- If the change keeps its contracts intact, say so in one line.

## What to look for

1. **API schemas.** Request or response fields removed, renamed, retyped, or made
   required; status codes or error shapes changed; endpoints removed or moved.
2. **Generated clients.** Hand edits to generated client code, or schema changes
   not accompanied by a regenerated client where the repo expects one.
3. **CLI flags.** Flags renamed or removed, defaults changed, required args
   added, or output format changes that scripts may parse.
4. **Event payloads.** Emitted event or message fields removed or retyped while
   consumers still read them; new required fields without a default.
5. **Database migrations.** Columns or tables dropped or renamed, non-nullable
   columns added without a default or backfill, type narrowing, and migrations
   that are not reversible or not safe to run against existing data.
6. **Workflow and job contracts.** Changed inputs, outputs, queue names, or step
   signatures that an in-flight or scheduled job depends on.
7. **Backwards compatibility.** Any of the above shipped without a deprecation
   path, version bump, or compatibility shim where existing consumers need one.

## How to report

- Anchor each finding to the changed line that alters the contract.
- Name the boundary, the breaking change, and the consumer at risk.
- State the safe path: additive change, default value, deprecation window,
  version bump, or regenerated client.
