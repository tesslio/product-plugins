# Repository review packages

A repository review package keeps its complete lens set in source control. The
active `.tessl-code-review.yml` profile selects the package's lenses and any
unrelated coverage the repository already uses.

## Default layout

Create new packages at `review-lenses/`:

```text
review-lenses/
├── .tessl-plugin/plugin.json
└── skills/
    ├── review-correctness-and-data-integrity/SKILL.md
    ├── review-maintainability-and-code-quality/SKILL.md
    ├── review-scale-and-resilience/SKILL.md
    ├── review-security-and-privacy/SKILL.md
    └── review-<repository-concern>/SKILL.md
```

Use this manifest for a package that stays in the repository:

```json
{
  "name": "local/code-review",
  "version": "0.1.0",
  "description": "Repository-local Tessl Code Review lenses.",
  "private": true,
  "skills": "./skills/"
}
```

The active profile references a lens with a path such as
`./review-lenses/skills/review-security-and-privacy/SKILL.md`.

## Discovering the active package

1. Read `.tessl-code-review.yml` before treating any local lens as active.
2. Resolve each local `ref` relative to the profile and stay inside the
   repository.
3. Walk from each referenced skill toward the repository root. A containing
   `.tessl-plugin/plugin.json` whose `name` is exactly `local/code-review`
   identifies a repository review package.
4. Treat that package as active only when the profile references at least one
   skill under its declared `skills` directory. Loose local lenses and lenses
   inside another plugin do not establish this package.

Use an active package at another path in place. Do not move it to the default
layout.

## Profile preservation

- Preserve profile-level `effort`, `reviewMode`, `requestChangesAt`, `ignore`,
  comments, and unknown-but-valid settings.
- Preserve unrelated lens entries, local custom lenses, their order, and their
  effort and glob settings.
- Replace every selected registry-default entry with its local copy in place,
  carrying that entry's `globs` and `effort` to the local ref.
- Creation activates each copied default. Add one local ref without globs only
  for an omitted default so it receives broad coverage without duplicate
  coverage. Preserve unrelated entries and their order. Duplicate refs and
  aliases resolving to the same local lens are invalid; if replacement would
  create one, report the conflicting entries rather than combining or dropping
  their settings. Activate the bespoke lens with the narrowest justified
  positive globs. Omit globs only when the concern applies across the repository.
- Keep no more than eight lenses applicable to one changed path. Do not drop
  coverage merely to fit the limit; report a conflict that needs a maintainer
  decision.

## Package validation

- Lint the package skills and validate the profile.
- Confirm every local ref resolves inside the repository.
- Check positive and excluded paths for each changed glob set.
- Run changed lenses alone on a case that should find a problem and one that
  should not.
- Run the complete active profile when credentials and suitable changes are
  available.
- Record failed and unavailable checks as limitations. File existence and a
  clean lint do not establish review quality.

Once created, the local package is the source of truth. Its manifest does not
record an upstream version, and updating it does not compare with registry
defaults. When an update changes files inside the package, increment the
manifest's patch version once. A profile-only change and a no-change result do
not change the package version.
