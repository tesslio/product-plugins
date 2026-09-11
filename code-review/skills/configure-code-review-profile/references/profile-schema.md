# The `.tessl-code-review.yml` format

The authoritative definition is the CLI's profile parser. This page describes
what that parser accepts, the limits it enforces, and what each key decides.

## Where the file lives, and who selects it

The three consumers of a profile do not agree on how it is found:

- **The Tessl Review GitHub App**, the supported install path, looks for
  `./.tessl-code-review.yml` at the repository root and uses it when it is
  there. Nothing has to point at it. A profile at any other path is not read.
- **The CLI** selects a profile explicitly and reads none by default:

  ```sh
  tessl code review --profile ./.tessl-code-review.yml
  ```

- **The unsupported GitHub Action** selects one explicitly too, through its
  `profile` input:

  ```yaml
  with:
    tessl-token: ${{ secrets.TESSL_TOKEN }}
    profile: ./.tessl-code-review.yml
    mode: advisory
  ```

Whichever consumer reads it, the path must end in `.yml` or `.yaml` and must
resolve inside the repository.

## Document shape

The file must be a block-style YAML mapping. Flow-style YAML, JSON, and
JSON-shaped documents are rejected, as are multiple documents in one file. The
file may be up to 1 MB.

The schema is strict: an unknown key is an error rather than something ignored,
at the top level and inside a lens entry alike. A misspelled key fails the
profile instead of silently doing nothing.

```yaml
schemaVersion: 1
effort: medium
requestChangesAt: major
ignore:
  - '**/*.generated.ts'
  - vendor/**
lenses:
  - ref: ./review-lenses/review-migrations/SKILL.md
    globs:
      - db/migrations/**
  - ref: tessl/code-review@0.4.0#review-security-and-privacy
    effort: high
  - ref: tessl/code-review@0.4.0#review-correctness-and-data-integrity
```

## Keys

**`schemaVersion`** is required and must be `1`.

**`lenses`** is required: an ordered list of at least one and at most 100
entries. It is the complete lens set for the run. It replaces the default lens
set rather than adding to it.

Each entry accepts three keys and nothing else:

- **`ref`** is required: a registry reference such as
  `workspace/plugin@version#skill`, or a path relative to the profile such as
  `./review-lenses/review-migrations/SKILL.md`. A local ref must stay inside the
  repository and must resolve to a readable path. Duplicate refs are rejected,
  as are two different refs that resolve to the same local lens. A ref is at
  most 512 characters.
- **`globs`** is optional: one to 32 patterns bounding which changed paths this
  lens reviews. A lens without `globs` reviews the whole change. When present,
  at least one pattern must be positive.
- **`effort`** is optional: `low`, `medium`, or `high` for this lens alone.

**`ignore`** is optional: one to 64 patterns naming paths no lens reviews. See
[Ignore patterns](#ignore-patterns).

**`effort`** at the top level is optional and sets the reasoning effort for
every lens that does not set its own: `low`, `medium`, `high`, or `adaptive`.
`adaptive` is resolved by the executor once it knows whether the run is a full
review or a later round, so it is a profile setting rather than a value a lens
or the supervisor can take. A lens with neither its own `effort` nor a profile
`effort` runs at the model's own default. The CLI's `--effort` flag applies to
every lens and takes precedence over both. Higher settings take longer.

**`requestChangesAt`** is optional and sets the severity at which a finding
starts requesting changes: `critical`, `major`, `minor`, or `nit`. See
[What `requestChangesAt` decides](#what-requestchangesat-decides).

**`reviewMode`** is optional: `strict`, `standard`, or `relaxed`, defaulting to
`standard`. It decides how much strength a finding needs before it blocks rather
than being published as a suggestion. Strength comes from how far the finding's
consequence sits above the `requestChangesAt` bar and how likely the reviewer
judged it to be. `strict` blocks any finding whose consequence clears the bar at
all, `standard` requires a little more, and `relaxed` more again.
`requestChangesAt` sets the bar; `reviewMode` sets how convincingly a finding
has to clear it.

**`model`**, **`supervisorModel`**, and **`supervisorEffort`** are optional and
restricted. Setting any of them makes the run an override, which most accounts
are refused. Leave them out.

## Glob patterns

Patterns are repository-relative POSIX patterns. They are case-sensitive and
they match dotfiles. Absolute paths, a leading `./`, `..` segments, backslashes,
and drive letters are all rejected, as are unbalanced brackets or braces. A
pattern is at most 256 characters.

Within one lens's `globs`, patterns are evaluated in order and the last one to
match decides:

- A matching positive pattern selects a path.
- A matching pattern prefixed with `!` deselects it.
- A later positive pattern can select it again.

A renamed file selects a lens when either its old or its new path matches, and
both paths are then passed to git so the complete rename patch is available to
the reviewer.

Each lens receives only its selected files in its prompt and its diff tools. It
cannot reach files routed only to another lens through those tools.

Only lenses that select at least one changed file count toward the supported
ceiling of eight lenses in a run. If no lens selects anything, the command exits
successfully with a `skipped` result and `reason: no-matching-lenses`. No model
runs, and no approval is implied.

## Ignore patterns

`ignore` follows the same pattern rules as `globs`, with two differences the
parser enforces:

- **Every pattern is positive** and excludes what it matches. A leading `!` is
  rejected outright rather than treated as a re-inclusion.
- A pattern of `**` on its own is rejected, because it would exclude every path
  and leave every lens with nothing to review.

The list holds at most 64 patterns.

`ignore` applies to every lens, including a lens that declares no `globs` of its
own, and it is applied after whatever a lens selected, so it overrides the
lens's own routing. A lens cannot opt back into an ignored path.

Two consequences worth stating to anyone who asks what `ignore` guarantees:

- Because a file is selected when either rename endpoint matches, a file renamed
  into an ignored path is still reviewed under its other path, and that path
  appears in the rename patch.
- `ignore` bounds which paths a lens reviews. It is not a guarantee that the
  contents of those files never reach a model.

## What `requestChangesAt` decides

A finding at or above the threshold requests changes, and the review requests
changes overall when any finding does. A finding below it is published as an
optional suggestion, and an approving review carrying suggestions states how
many it approved over. Omit the key and every round runs at `major`. There is no
Action input and no CLI flag for the threshold, so the profile is the only place
a repository sets it.

The threshold also bounds what a later round raises. A first review publishes
every finding whatever its severity. On a later round a finding below the
threshold appears only if an earlier round already raised it, in which case it
continues on its existing comment thread. A fresh finding below the threshold is
not published on that round and is not held over: a later round either finds it
in the code again or it is gone. At `requestChangesAt: nit` nothing is below the
threshold, so every finding requests changes and every round raises everything.

## Limits

- 1 MB per profile file.
- 100 lenses per profile, and 8 lenses with matching work per run.
- 32 globs per lens, 64 ignore patterns, 256 characters per pattern.
- 512 characters per lens ref.

## Interaction with `--skill`

Passing `--skill` replaces the profile's complete lens list, including its glob
routing and its `ignore` patterns. It does not add to the profile.

## Treat a profile as executable policy

The profile and the local lenses it references become reviewer instructions that
run with a reviewer's authority, and a review reads them from the head of the
pull request under review. A change that narrows routing or widens `ignore`
therefore takes effect on the review of the change that makes it. Review a
change to a profile with the same care as a change to source code.
