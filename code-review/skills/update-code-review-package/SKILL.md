---
name: update-code-review-package
description: Improve the active repository-owned Tessl Code Review package from bounded review feedback and repository changes while preserving maintainer edits and unrelated coverage. Use for missed checks, noisy findings, stale local guidance, periodic improvement runs, or an unattended hosted request to improve custom lenses. The current local package is the only baseline; this workflow never compares with registry defaults.
---

# Update a Code Review package

Propose small, evidenced changes to the package the repository currently uses.

## Procedure

1. Read [the package convention](../code-review/references/review-packages.md)
   and discover the active local package from `.tessl-code-review.yml`. If none
   is active, make no edits. When an unreferenced package manifest already
   occupies `review-lenses/`, do not redirect to creation: in an interactive
   request, explain that the maintainer must either adopt it by reconnecting its
   intended lens refs in the profile or remove or relocate it if obsolete. For
   other missing-package cases, direct the user to `create-code-review-package`.
   In a hosted request, emit the required report and `blocked` result before
   stopping.
2. Treat the current package and profile, including maintainer edits, as the
   source of truth. Do not fetch, inspect, compare, or synchronize registry
   defaults.
3. Read the supplied bounded evidence and repository changes using
   [the evidence rules](references/review-evidence.md). Missing or invalid
   evidence, or evidence with no attributable review item, blocks an update.
   Make no edits. In an interactive request, explain what evidence is needed
   and gather it through supported access when available before editing. In a
   hosted request, emit `blocked` artifacts. Useful partial evidence may support
   a bounded update when its omissions are recorded. Record what was and was
   not covered before editing.
4. Separate a missed concern from failure to apply an existing lens. For a real
   gap, use `create-code-review-lens` to tune the relevant local lens or add a
   distinct lens. Change routing only when path evidence justifies it.
5. Preserve unrelated lenses, globs, profile settings, and manual wording.
   Prefer the smallest change that accounts for repeated or consequential
   evidence. Scope generated-output exclusions to evidenced paths. Exclude a
   whole directory only when repository ownership evidence establishes that
   the directory is reserved for generated output; preserve paths that may
   contain future hand-authored files. Apply the exclusion only to the lens
   evidenced as noisy; preserve unrelated lens checks. A completed investigation
   may produce no change.
6. Run proportionate positive and negative checks for each candidate, then the
   complete active profile when available. Reconcile results with the original
   revisions, revise and recheck against the same bounded cases, and report
   remaining misses, noise, and coverage limits.
7. In an interactive request, summarize the evidence and result. In a hosted
   request, follow
   [the hosted result contract](../code-review/references/hosted-authoring.md),
   make sensible choices without confirmation, and leave publication to the
   recipe.
