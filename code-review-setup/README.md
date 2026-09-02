# code-review-setup

Install Tessl Code Review into a GitHub repository, by writing the thin caller
workflow that invokes the supported Tessl Code Review Action.

## The Action repository

The supported Action lives at `tesslio/code-review-action`. An installed caller
workflow names it on its `uses:` line.

## Install

```bash
tessl install tessl/code-review-setup
```

## What it does

The Action owns getting a review run: pull-request resolution, checkout of the
exact head, Tessl CLI setup, the check run it reports on the reviewed head,
failure notices, and result artifacts. The Tessl CLI it installs runs the review
and publishes it, which is where stale-head protection and idempotent retries
live. The repository owns a caller workflow: triggers, concurrency, runner,
timeout, permissions, the token secret, and the review policy.

This plugin writes that caller and nothing else. It never copies review or
publication logic into the repository, so there is only ever one execution path.

Setup is two questions:

- **When do reviews run.** Manual only, where a review runs on an explicit
  dispatch or an `@tessl-code-review` mention and never on its own; once when the
  pull request becomes ready, with recovery on the first later commit if GitHub
  suppressed that initial workflow while the pull request was conflicted, plus
  requested rounds (the default); or on every commit.
- **Do findings block.** Advisory, where the review is a comment and no review
  outcome fails the check, or gate, where changes approved passes the check and
  changes requested fails it.

Gate mode decides whether the check fails, not which findings make it fail. That
is `requestChangesAt` in a repository YAML profile, and a repository that sets no
threshold requests changes at Major on every round, so a Minor is published as a
suggestion. Setup names the key when gate is chosen rather than asking for a
value, because the default suits almost every repository.

The two are independent choices, and every pairing is installable. The Action
reports its own check, named `Tessl Code Review`, against the head it reviewed on
every trigger, so a gate holds on any cadence once that check is required in
branch protection. What the cadence decides is when a fresh verdict arrives, and
the skill says plainly that on the non-automatic cadences a blocked pull request
stays blocked until someone asks for a new round.

Around those two answers, the skill inspects the repository first and asks only
for what it cannot infer: existing workflow conventions, an existing Code Review
caller and its pinned revision, conflicting callers, the `TESSL_TOKEN` secret,
fork traffic, and current branch protection. It proposes the change, waits for
explicit approval, writes idempotently, verifies the result, and then explains the
permissions, the secret, the branch-protection step, and how to update or remove
the setup.

The installed workflow references the Action by its major tag, which moves to
each 1.x release, so a fix reaches the repository without anyone editing the
file. A repository that wants the revision frozen gets the current release's full
commit SHA instead, resolved at setup time rather than invented, and accepts that
updates then need a deliberate bump. A branch is never installed for either.

Mention-driven rounds are requested by mentioning `@tessl-code-review` in a
comment on the pull request. That token belongs to the Action, whose published
review asks reviewers to use it, so the caller matches it rather than inventing a
command of its own. Who may request a round is a choice the skill puts to the
user, defaulting to owners, organization members, and invited collaborators.

A comment can also ask Tessl to approve the pull request rather than review it,
or to review the whole change again rather than the narrower later round. Both
are permitted for owners, members and collaborators, and for any comment author
named in `approver-logins`, which is the only route open to a GitHub App: an App
comments with author association `NONE` whatever its permissions, so no
association names one.

## Skills

| Skill | Description |
|-------|-------------|
| `setup-code-review` | Detect, interview, propose, write, verify, and explain the Code Review caller workflow |

## Customizing what gets reviewed

Cadence and blocking are what this plugin sets. What the reviewer looks for is
the `profile` and `lenses` inputs, documented in the Action repository's README.
The Action supports the built-in `standard` profile and explicitly selected
repository YAML profiles.
