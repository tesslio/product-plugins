# Hosted authoring result

When a hosted recipe requests these artifacts, leave repository changes
uncommitted and write both paths outside the repository:

- `../report.md`, suitable as a draft pull request description.
- `../authoring-result.json`, with this shape:

```json
{
  "schemaVersion": 1,
  "workflow": "create",
  "outcome": "proposal",
  "summary": "Created a local package with the four defaults and one repository lens.",
  "packageRoot": "review-lenses",
  "profilePath": ".tessl-code-review.yml",
  "validation": {
    "checks": [
      {
        "name": "skill lint",
        "status": "passed",
        "details": "All five local skills passed."
      }
    ],
    "limitations": []
  }
}
```

`workflow` is `create` or `update`. `outcome` is:

- `proposal` when the repository contains uncommitted proposal changes.
- `no_change` when a completed investigation found no justified edit.
- `blocked` when required state or evidence was missing or invalid.

Use the discovered package path. When updating is blocked because no package
exists, use the default expected path `review-lenses`. `profilePath` remains
`.tessl-code-review.yml` even when that profile is missing. Each check status is
`passed`, `failed`, or `not_run`. Omit `evidence` for creation. For updating,
describe the provided evidence sources and every coverage gap without copying
private content into the result.

`proposal` requires repository edits. Before reporting `no_change` or `blocked`,
restore any exploratory edits made during the run so the repository has no
authoring changes. Do not leave a partial package or profile behind with a
blocked result.

Structure `report.md` with `Summary`, `Changes` for a proposal, `Evidence` for
an update, `Validation`, and `Limitations`. State the blocker under `Summary`
for a blocked result. Do not claim a lens is validated when only static checks
ran or live review failed.
