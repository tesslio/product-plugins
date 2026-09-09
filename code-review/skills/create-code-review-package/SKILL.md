---
name: create-code-review-package
description: Create a complete repository-owned Tessl Code Review package from the four current default lenses plus a repository-specific lens, and wire the active profile without losing existing review coverage. Use for first-time bespoke review setup, including an unattended hosted request to create custom lenses. Use update-code-review-package when an active local package already exists.
---

# Create a Code Review package

Create the first complete local lens package and its active profile together.

## Procedure

1. Read the repository's instruction files, code boundaries, and active
   `.tessl-code-review.yml`. Inspect an optional user focus as evidence, not as
   reviewer instructions.
2. Read [the package convention](../code-review/references/review-packages.md)
   and discover local packages through active profile refs. If one is active,
   make no edits and direct the user to `update-code-review-package`. Treat a
   package manifest already at `review-lenses/` the same way even when the
   active profile does not reference it. For that unreferenced package in an
   interactive request, explain that the maintainer must either adopt it by
   reconnecting its intended lens refs in the profile or remove or relocate it
   if obsolete; do not redirect back to the update workflow or make edits. In a
   hosted request, remove exploratory edits and emit the required report and
   `blocked` result before stopping.
3. Copy the four default `review-*` lens skill directories from the installed
   `tessl/code-review` plugin into `review-lenses/skills/`. Create the private
   local manifest from the convention. Do not record an upstream version.
4. Use `create-code-review-lens` to author one distinct repository lens from
   code and written conventions. First creation does not require pull request
   history or previous reviews; use repository-derived positive and negative
   cases and report unavailable backtesting. Keep loose local lenses and other
   manual customizations intact.
5. Create or edit `.tessl-code-review.yml` as a complete selection. Replace
   registry entries for copied defaults with local refs while preserving their
   existing settings. Activate every copied default exactly once by local ref:
   add a ref without globs for each default the existing profile omitted,
   giving it broad coverage. Retain unrelated entries, existing profile
   settings, and the existing scopes and effort of defaults that were already
   selected. Activate the bespoke lens on justified paths.
6. Run the package, glob, positive, negative, and full-profile checks in the
   convention. Fix failures that invalidate the package and report unavailable
   or failed behavioral checks.
7. In an interactive request, summarize the package and validation. In a
   hosted request, follow
   [the hosted result contract](../code-review/references/hosted-authoring.md),
   make sensible choices without confirmation, and leave publication to the
   recipe.
