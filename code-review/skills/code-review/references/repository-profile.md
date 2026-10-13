# The repository profile

A repository profile is a YAML file that states which lenses a review runs,
which paths each lens reviews, and which paths no lens reviews. Use one when the
user wants to add a lens to a repository's reviews, route different lenses to
different parts of a change, or keep generated and vendored files out of review.

The Tessl Review GitHub App reads the profile from `.tessl-code-review.yml` at
the repository root. The App uses a profile only once that file exists on the
default branch. When the pull request's author has write access to the
repository, or is a GitHub App, the review uses the copy on the pull request's
head, so a pull request can change the profile it is reviewed with. For any other author, the
review uses the copy on the default branch. Without the file on the default
branch, the App runs the default lenses.

If an approval from the Tessl reviewer is required before merging, an author
whose pull request is reviewed with the head copy can edit
`.tessl-code-review.yml`, or a local lens it references, and have that pull
request reviewed under the edited version. To stop that change merging unseen,
add CODEOWNERS entries for `.tessl-code-review.yml` and for each local lens
directory it references, and turn on "Require review from Code Owners" in the
default branch's protection rules.

The CLI uses a profile only when you pass it:

```sh
$ tessl code review --profile ./.tessl-code-review.yml
```

The CLI does not look for a profile file and does not make one the default. The
file path must end in `.yml` or `.yaml`.

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
  - .tessl/plugins/**
  - '**/tessl__*'
  - '**/tessl__*/**'
lenses:
  - ref: ./review-lenses/backend/SKILL.md
    globs:
      - apps/backend/**
  - ref: tessl/code-review@0.2.0#review-security-and-privacy
    effort: high
    globs:
      - infra/**
  - ref: ./review-lenses/general/SKILL.md
```

The last three `ignore` patterns keep installed plugins out of review:
`tessl install` copies a plugin under `.tessl/plugins/`, and links each skill
into most agents' skill directories as `tessl__<skill>`. Git records each link as a single
path, so `'**/tessl__*/**'` alone does not match it.

`schemaVersion` is required and must be `1`. `lenses` is an ordered, non-empty
list. Every lens needs a `ref`, which can be a registry reference or an explicit
local path. A registry ref with a version, like `@0.2.0` above, stays fixed
until someone edits it; one without a version follows the newest published
version. Local refs are relative to the profile, must use path syntax such as
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
requesting changes: `critical`, `major`, `minor`, or `nit`. A finding whose
assessed consequence is at or above it requests changes when the review also
judges it likely enough and attributes it to the pull request's own change, so
a finding's published severity alone does not say whether it blocks. The review requests changes overall when any finding does.
Other findings are published as advisory, and an approving review carrying
suggestions states how many it approved over. Omit the key and every round runs
at `major`. There is no CLI flag for the threshold, so this profile is the only
way a repository sets it.

The threshold also bounds what a later round raises. A first review publishes
every finding whatever its severity. On a later round a finding that does
not request changes appears only if an earlier round already raised it, in which
case it continues on its existing comment thread. A fresh finding that does not
request changes is not published on that round and is not held over: a later
round either finds it in the code again or it is gone. Lowering the threshold to
`nit` makes every severity eligible to request changes, but the likelihood and
attribution conditions above still apply, so some findings stay advisory even
at `nit`.

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

Only lenses with matching work count toward the limit of eight lenses. When
more than eight match, the run fails with `too-many-lenses` before any lens runs.
If no lens matches, the command exits successfully with a `skipped` result and
`reason: no-matching-lenses`. No model runs and no approval is implied.

Passing `--skill` replaces the profile's complete lens list, including its glob
routing and its `ignore` patterns. It does not add to the file profile.

Treat the profile and its local lenses as executable review policy. Review their
changes with the same care as source code.
