# YAML file profiles and the Action

A repository-owned YAML profile decides which lenses a review runs, which paths
each lens reviews, and which paths no lens reviews. Use one when the Action
should route different lenses to different parts of a change, or when the
repository wants a different severity threshold for requesting changes.

The format, the keys, the limits, and the routing rules are documented once, in
[the profile skill's reference](../../configure-code-review-profile/references/profile-schema.md).
Read that before writing or editing a profile. `configure-code-review-profile`
is the skill that writes one, including the check to run against it afterwards.
This page carries only what is specific to the Action.

## Selecting the profile

The Action does not discover a profile. It reads the one its `profile` input
names, and reviews with the default lens set when the input is absent:

```yaml
with:
  tessl-token: ${{ secrets.TESSL_TOKEN }}
  profile: ./.tessl-code-review.yml
  mode: advisory
```

The CLI behaves the same way, selecting a profile only through
`--profile ./.tessl-code-review.yml`.

The supported install path differs here, and a user moving between them will
notice: the Tessl Review GitHub App looks for `./.tessl-code-review.yml` at the
repository root and uses it when it is there, with nothing to configure. So a
repository that keeps its profile at that path gets it read automatically on the
App, and has to name it on the Action and on the CLI.

Keep the file at the repository root under that name even when the Action is the
only consumer. It costs nothing, it is where a reader looks for it, and it is
what the App would read if the repository ever moves to the supported path.

## The `lenses` input against a profile

Both the Action's `lenses` input and a profile's `lenses` list state a complete
ordered lens set, replacing the defaults rather than adding to them. They are
not equivalent, though: the input is a flat list of refs and carries no glob
routing and no `ignore` patterns, where the profile carries both. A repository
that routes by path states its selection in the profile and leaves the input
unset, so the routing cannot be lost to a second selection stated elsewhere.

## Gate mode and the threshold

`mode` decides whether the Action's check fails. It does not decide which
findings make it fail: that is `requestChangesAt`, which exists only in a
profile. A repository that sets no profile threshold gates at `major`, so a
Minor finding is published as a suggestion and does not hold the pull request.

## Treat a profile as executable review policy

A profile and the local lenses it references become reviewer instructions.
Review changes to them with the same care as changes to source code.
