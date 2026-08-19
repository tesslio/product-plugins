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
effort: low
lenses:
  - ref: ./review-lenses/backend/SKILL.md
    globs:
      - apps/backend/**
      - '!apps/backend/**/*.generated.ts'
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

`effort` is optional and sets how hard a lens thinks: `low`, `medium`, or
`high`. The profile may set it for every lens, and any lens may set its own to
think harder or less hard than the rest. A lens without one uses the profile's
`effort`; with neither, the model applies its own default. The `--effort` flag
applies to every lens and takes precedence over both. Higher settings take
longer.

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
routing. It does not add to the file profile.

Treat the profile and its local lenses as executable review policy. Review their
changes with the same care as source code.
