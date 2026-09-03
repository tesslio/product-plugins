---
name: review-maintainability-and-code-quality
description: Review a code change for maintainability, naming, weak contracts, duplicated local precedent, misleading comments, and API or code surfaces that do not enforce what they promise. Use when reviewing for readability, refactoring, code quality, or API design issues.
---

# Review lens: Maintainability and Code Quality

Review whether the changed code, tests included, can be understood and modified safely without relying on its original author or review context.

## Scope

- **Maintainability** What the next change to this code will cost: a helper, schema or convention the codebase already has and this one rebuilds, a decision whose rationale exists nowhere, structure that hides its intent.
- **Code Quality** What the code's surfaces enforce: a type loose enough to admit a wrong value or to conflate things that should stay distinct, a public name or description that leaks the internals behind it, a dependency the caller can forget to supply.
- **Legibility** What a reader is likely to misread: a name that promises what the code does not do, a comment or docstring describing behavior the code does not have.

## Method

Written standards nest: a root AGENTS.md or CLAUDE.md, and often another in each subproject. Read the chain governing the files this change touches, not only the closest one.

Read each new or changed name against what the code behind it does, and each comment or docstring against the body it describes.

At a public boundary, read the signature and its description as a consumer who cannot see the implementation.

When a changed helper stops enforcing what its name or previous behavior promised, cite that contract and the caller misuse it now permits.

## Threshold

Report an issue when a reader cannot determine the code's intent, constraints, or relationship to established project patterns, or when a surface does not enforce what it claims.

Before suggesting reuse, verify that the existing code is the appropriate precedent.

Do not report a stylistic preference as a defect, though a convention the team has written down is not a preference.

## Reporting

- Name the question a future reader is left with that the code does not answer.
- For a misleading contract, name the promised behavior, the local evidence for it, the caller misuse it permits, and the structural fix.
- Where the codebase already has the thing, name the precedent with its file path, and say whether to reuse it, import it, or follow it.
- Note when a divergence looks deliberate, so the author can confirm or correct it.
- State the structural fix, not "add a comment" or "improve clarity": renaming, restructuring, narrowing a type, inlining, extracting, removing.
