---
name: code-review
description: Start here for Tessl Code Review. Use when someone mentions Tessl Code Review or Tessl's AI review, wants automated review of pull requests in a repository, asks to review a diff, branch, or pull request ("review this change", "check this diff for security issues", "what would Code Review say"), asks what Tessl Code Review does, or asks for something and it is not yet clear which Code Review job it is. Works out whether they want to set it up in a repository, run a review, change what reviews catch, or answer a review's findings, and hands off to setup-code-review, create-code-review-lens, respond-to-code-review, or the tessl code review command. The review-* skills in this plugin are lenses that tessl code review runs as reviewer instructions; do not follow one directly to review code, run the command instead.
---

# Tessl Code Review

Tessl Code Review reviews a pull request or a local change with several
reviewers running in parallel, one per **lens**, then merges and grades what they
found into one review. It runs from the CLI as `tessl code review`, and on GitHub
through the Tessl Code Review Action, which a repository installs with a thin
caller workflow.

This plugin holds every part a user touches:

| Job | Skill | Signals |
| --- | --- | --- |
| Install, update, or remove Code Review on a repository | `setup-code-review` | set up, enable, install, configure, gate mode, advisory, cadence, remove, the caller workflow, `TESSL_TOKEN` |
| Change what a review looks for | `create-code-review-lens` | the review missed something, keeps flagging something it should not, write a lens, fork a lens, tune a lens, custom review rules |
| Answer a review that has arrived | `respond-to-code-review` | address the findings, respond to the review, the reviewer left comments, changes requested, the review loop is not converging |
| Run a review now | the `tessl code review` command, below | review this change, review my PR, what would Code Review say about this diff |

The four `review-*` skills are the default lenses. They are reviewer
instructions that `tessl code review` loads into its own reviewer agents. Do not
activate one to review code yourself: a lens on its own has no supervisor to
merge and grade findings, and the result is not a Tessl Code Review.

## Route the request

Read the request and the repository before choosing. One question is usually
enough when the request is ambiguous; do not interview.

1. **Is Code Review installed here?** Look for a workflow under
   `.github/workflows/` that uses `tesslio/code-review-action`. No caller and a
   request about reviewing pull requests automatically is a setup job. A caller
   that exists and a request to change when reviews run or whether they block is
   also a setup job.
2. **Is there a review to answer?** A pull request with a Tessl Code Review on it,
   or a pasted set of findings, and a request to deal with them is a respond job.
3. **Is the complaint about what reviews catch?** Missed classes of bug, noisy
   findings, a concern the team keeps raising by hand, or a request for a custom
   rule is a lens job. A request to change *when* or *whether* reviews run is not.
4. **Otherwise, run a review.** A request to look at a change now, with no
   installation or lens work implied, is a CLI run.

Hand off by following the named skill. Say which one you are using and why in one
line. If two jobs are present, do the one that unblocks the other first: a setup
before a lens, since the caller workflow is where a new lens is selected, and a
respond before anything else when a review is waiting.

## Running a review from the CLI

`tessl code review` reviews the working tree's change against the default branch
when given nothing. It takes a range with `--base` and `--head`, or a pull request
with `--pr`.

```bash
tessl code review
tessl code review --base origin/main --head HEAD
tessl code review --pr 42
```

The default lens set is the four `review-*` skills in this plugin, pinned to a
version of this plugin, so a plain run needs no lens selection. `--skill`
replaces that set with the complete ordered set you name; it does not add to it.
A reference is a local path, an installed skill name, or a registry ref
`workspace/plugin@version#skill`. Pin the version in any ref you keep.

```bash
tessl code review --skill ./review-lenses/review-test-reliability
tessl code review --skill tessl/code-review@0.2.0#review-security-and-privacy
```

`--json` writes one document to stdout on success and failure alike. Read
`status` before counting findings: a failed run carries none and otherwise looks
like a clean review.

Never pass `--publish` unless the user asked for the review to be posted to the
pull request. A local run is a preview.

## What not to do here

- Do not hand-write a caller workflow, a profile, or a lens. Each has a skill,
  and each skill knows the contract the Action and the CLI enforce.
- Do not answer findings for the user without reading `respond-to-code-review`.
  Fix, refute, and decline are distinct dispositions with distinct consequences.
- Do not describe the plugin's internals when asked what Code Review does. Say
  what it reviews, where it runs, and offer the four jobs.
