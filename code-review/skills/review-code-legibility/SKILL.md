---
name: review-code-legibility
description: Review a diff for legibility — whether a reader with no prior context can understand each name, type, return shape, file, and abstraction from what's in front of them. Applies two tests, the cold-reader test and the from-scratch test, and flags structural problems whose fix is renaming, restructuring, narrowing types, inlining, extracting, or removing — not adding comments. Use as a legibility review lens in `tessl change review` or a GitHub Actions review workflow.
---

# Review Code Legibility

A legibility review lens for `tessl change review`. Readers see code, not the
journey that produced it, and they read it literally and locally. Where a piece
of code can only be understood by reading its caller, its producer, or git
history, the code is structurally wrong. Review the diff for those gaps and
report concrete, actionable findings.

## Stance

- Review the diff first. Read a caller or a referenced file only to confirm a
  legibility gap a changed line already suggests.
- The fix is to change the code, not to add a comment. Propose renaming,
  restructuring, narrowing a type, inlining, extracting, or removing.
- Flag substance, not taste. Raise an issue when a reader is likely to infer the
  wrong thing, not for cosmetic preference.
- If the change reads clearly, say so in one line.

## Two tests

Apply both to each structural decision in the diff — a name, a location, a
type, an abstraction:

1. **Cold-reader test.** Read this function, type, or file as if you just opened
   it with no context. Can you tell what each parameter is from its name and
   type, what it returns and what the result shape means, and why the file
   exists from its exports?
2. **From-scratch test.** Would this exist if the codebase were designed today?
   Adding an abstraction, splitting a module, or keeping a name should each
   pass. "Consistent with existing code" does not justify a new instance — apply
   the from-scratch test to the precedent first.

## What to look for

The recurring anti-patterns, with their fixes, are catalogued in
[references/anti-patterns.md](references/anti-patterns.md). The main families:

- **Misleading or change-relative names** — names that no longer match
  behaviour, and comments or names only a reader of this diff or ticket could
  decode.
- **Opaque types and loose signatures** — `Record<string, X>` and similar that
  hide the key/value relationship, and functions whose arguments only make sense
  if you know the caller.
- **Structure that hides intent** — single-consumer helpers named after their
  mechanics, inscrutable function bodies, vestigial abstractions, redundant new
  paths that duplicate an existing one, and files whose exports don't say what
  the file is for.

## How to report

- Anchor each finding to the changed line, naming which test it fails.
- State the structural fix, not "add a comment" or "improve clarity".
- Respect the legitimate exceptions in the reference (generic library code, hot
  loops, mathematical primitives) before flagging opacity.
