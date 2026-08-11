---
name: review-local-precedent
description: Review a diff for missed reuse — whether new code should have reused an existing helper, component, schema, route shape, fixture, or local convention instead of reimplementing it. Follows a strict, bounded search budget so it inspects only a few plausible precedent files, never the whole repository. Use as a code-reuse review lens in `tessl change review` or a GitHub Actions review workflow.
---

# Review Local Precedent

A code-reuse review lens for `tessl change review`. New code often reimplements
something the repository already has. Review the diff for cases where an obvious
existing helper, component, schema, route shape, fixture, or local convention
should have been reused, and report concrete, actionable findings.

## Stance

- Stay within the search budget below. Do not scan the whole repository; inspect
  a small number of plausible precedent files and stop.
- Report a finding only when you can name the existing thing and the changed
  lines that duplicate it. No precedent located within budget means no finding.
- Distinguish real duplication from surface similarity. Two pieces of code can
  look alike for opposite reasons; confirm the existing one is meant to be
  reused before flagging.
- If the change reuses what it should, or no precedent exists within budget, say
  so in one line.

## Search budget

Work through these steps in order and stop early once you have a concrete
duplicate, or once you have inspected a small number of plausible precedent
files (about five) without finding one:

1. **The diff itself.** Identify the new helpers, components, schemas, routes,
   fixtures, and conventions the change introduces.
2. **Nearest project guidance.** The closest `AGENTS.md`, `CLAUDE.md`, or
   `README` that states a convention the change should follow.
3. **Same package or app.** The directory the change lives in.
4. **Direct imports.** Modules the changed files already import.
5. **Sibling files.** Files next to the changed files.
6. **Targeted symbol search.** A few `rg` searches for the exact symbol names,
   domain nouns, or route shapes the change introduces — not broad exploratory
   reads.

Stop at the first concrete duplicate. Do not open files beyond this budget, and
do not read a file in full when the relevant export or signature is enough.

## What to look for

- A new helper or utility that duplicates one already in the same package or an
  imported module.
- A component, hook, or wrapper reimplemented when an existing one fits.
- A schema, type, or validation rule redefined instead of imported.
- A route, handler, or endpoint shaped differently from sibling routes for no
  stated reason.
- A test fixture or factory rebuilt when a shared one exists.
- A local convention (error handling, logging, config access, naming) the change
  diverges from.

## How to report

- Anchor each finding to the changed line, and name the existing precedent with
  its file path.
- State whether to reuse, import, or follow the existing thing, and why it fits.
- Note when divergence looks deliberate so the author can confirm or correct it.
