# YAML file profiles

Use a repository-owned YAML profile when the user wants a CLI or Action review
to route different lenses to different parts of a change. The profile must be
selected explicitly.

For the CLI:

```sh
$ tessl code review --profile ./.tessl-code-review.yml
```

For the Action:

```yaml
with:
  tessl-token: ${{ secrets.TESSL_TOKEN }}
  profile: ./.tessl-code-review.yml
  mode: advisory
```

Tessl does not discover profile files or make one the default. The file path
must end in `.yml` or `.yaml`.

## Schema

The file must be a block-style YAML mapping. JSON, JSON-shaped flow YAML,
unknown fields, and multiple YAML documents are rejected.

```yaml
schemaVersion: 1
requestChangesAt: major
effort: low
ignore:
  - '**/*.generated.ts'
  - vendor/**
lenses:
  - ref: ./review-lenses/backend/SKILL.md
    globs:
      - apps/backend/**
  - ref: tessl/code-review@0.1.0#review-security-and-privacy
    effort: high
    globs:
      - infra/**
  - ref: ./review-lenses/general/SKILL.md
```

`schemaVersion` is required and must be `1`. `lenses` is an ordered, non-empty
list. Every lens needs a `ref`, which can be a registry reference or an explicit
local path. Local refs are relative to the profile, must use path syntax such as
`./review-lenses/backend/SKILL.md`, and must resolve inside the repository.
Duplicate refs and aliases that resolve to the same local lens are rejected.

`globs` is optional. A lens without it applies to the whole change. When present,
it must be a non-empty list with at least one positive pattern. Each profile may
declare up to 100 lenses, each lens may declare up to 32 globs, and the profile
may be up to 1 MB.

`ignore` is optional and bounds which paths any lens reviews, so generated code,
lockfiles, snapshots, and vendored directories are named once instead of negated
inside every lens. Each pattern is positive and excludes what it matches, so a
leading `!` is rejected, as is a bare `**` that would leave every lens with
nothing to review. It applies to every lens, including one that declares no
`globs`, a lens's own `globs` still narrow it further, and `ignore` overrides
anything a lens selected. At most 64 patterns are allowed. Because a file is
selected when either rename endpoint matches, a file renamed into an ignored path
is still reviewed and that path appears in the rename patch, and `ignore` bounds
which paths a lens reviews rather than keeping their contents out of a model's
context.

`effort` is optional and sets how hard a lens thinks: `low`, `medium`, or
`high`. The profile may set it for every lens, and any lens may set its own to
think harder or less hard than the rest. A lens without one uses the profile's
`effort`; with neither, the model applies its own default. The `--effort` flag
applies to every lens and takes precedence over both. Higher settings take
longer.

`requestChangesAt` is optional and sets the severity at which a finding starts
requesting changes: `critical`, `major`, `minor`, or `nit`. A finding at or above
it requests changes, and the review requests changes overall when any finding
does. A finding below it is published as an optional suggestion, and an approving
review carrying suggestions states how many it approved over. Omit the key and
every round runs at `major`. There is no Action input and no CLI flag for the
threshold, so this profile is the only way a repository sets it.

The threshold also bounds what a later round raises. A first review publishes
every finding whatever its severity. On a later round a finding below the
threshold appears only if an earlier round already raised it, in which case it
continues on its existing comment thread. A fresh finding below the threshold is
not published on that round and is not held over: a later round either finds it
in the code again or it is gone. At `requestChangesAt: nit` nothing is below the
threshold, so every finding requests changes and every round raises everything.

## Routing behavior

Globs are case-sensitive, repository-relative POSIX patterns and include
dotfiles. Absolute paths, `./`, `..`, backslashes, and drive letters are not
valid patterns. Patterns are evaluated in order:

- A matching positive pattern includes a path.
- A matching pattern prefixed with `!` excludes it.
- A later positive pattern can include it again.

A renamed file selects a lens when either its old or new path matches. Each
lens receives only its selected files in its prompt and diff tools. It cannot
inspect files routed only to another lens through those tools.

Only lenses with matching work count toward the limit of eight lenses.
If no lens matches, the command exits successfully with a `skipped` result and
`reason: no-matching-lenses`. No model runs and no approval is implied.

Passing `--skill` replaces the profile's complete lens list, including its glob
routing and its `ignore` patterns. It does not add to the file profile.

Treat the profile and its local lenses as executable review policy. Review their
changes with the same care as source code.
