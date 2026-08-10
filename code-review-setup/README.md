# code-review-setup

Install Tessl Code Review into a GitHub repository, by writing the thin caller
workflow that invokes the supported `tesslio/code-review` Action.

## Install

```bash
tessl install tessl/code-review-setup
```

## What it does

The Action owns running a review: pull-request resolution, checkout of the exact
head, Tessl CLI setup, review publication, stale-head protection, idempotent
retries, failure notices, and result artifacts. The repository owns a caller
workflow: triggers, concurrency, runner, timeout, permissions, the token secret,
and the review policy.

This plugin writes that caller and nothing else. It never copies review or
publication logic into the repository, so there is only ever one execution path.

Setup is two questions, and every combination of the two is valid:

- **When do reviews run.** Manual only, once when the pull request becomes ready
  plus requested rounds (the default), or on every commit.
- **Do findings block.** Advisory, where the review is a comment and never fails
  the check, or gate, where a converged review approves and a non-converged one
  requests changes and fails the check.

Around those two answers, the skill inspects the repository first and asks only
for what it cannot infer: existing workflow conventions, an existing Code Review
caller and its pinned revision, conflicting callers, the `TESSL_TOKEN` secret,
fork traffic, and current branch protection. It proposes the change, waits for
explicit approval, writes idempotently, verifies the result, and then explains the
permissions, the secret, the branch-protection step, and how to update or remove
the setup.

The installed workflow always pins the Action to a full commit SHA. Tags and
branches are moving references and this plugin does not install them.

## Skills

| Skill | Description |
|-------|-------------|
| `setup-code-review` | Detect, interview, propose, write, verify, and explain the Code Review caller workflow |

## Customizing what gets reviewed

Cadence and blocking are what this plugin sets. What the reviewer looks for is
the `profile` and `lenses` inputs, documented by the `tessl/code-review` plugin.
