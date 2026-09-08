---
name: code-review
description: Start here for Tessl Code Review. Use when someone mentions Tessl Code Review or Tessl's AI review, wants automated review of pull requests in a repository, asks to review a diff, branch, or pull request ("review this change", "check this diff for security issues", "what would Code Review say"), asks what Tessl Code Review does, or asks for something and it is not yet clear which Code Review job it is. Works out whether they want to install it on a repository, run a review, change what reviews catch, or answer a review's findings. Installing is the Tessl Review GitHub App, which this skill points at the documentation for, unless the user names the unsupported GitHub Action, which hands off to setup-code-review; the other jobs hand off to create-code-review-lens, respond-to-code-review, or the tessl code review command. The review-* skills in this plugin are lenses that tessl code review runs as reviewer instructions; do not follow one directly to review code, run the command instead.
---

# Tessl Code Review

Tessl Code Review reviews a pull request or a local change with several
reviewers running in parallel, one per **lens**, then merges and grades what they
found into one review. It runs from the CLI as `tessl code review`, and on GitHub
as the **Tessl Review GitHub App**.

This plugin holds every part a user touches:

| Job | Skill | Signals |
| --- | --- | --- |
| Install Code Review on a repository | [Installing on a repository](#installing-on-a-repository), below | set up, enable, install, turn on reviews on this repo, get Tessl reviewing our pull requests |
| Install the unsupported GitHub Action instead | `setup-code-review` | the user names the Action: install the action, set it up as a GitHub Action, I want the Action |
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

1. **Has the user named the GitHub Action?** An install request that asks for
   the GitHub Action by name, for example "install the action", "set it up as a
   GitHub Action", or "I want the Action", is a setup job. Follow
   `setup-code-review`, and do not follow
   [Installing on a repository](#installing-on-a-repository) instead. This rule
   takes precedence over the next one; nothing short of naming the Action counts.
2. **Is this about getting Code Review running on a repository?** Any other
   request to install, enable, set up, or configure automatic review of pull
   requests is an install job. Follow
   [Installing on a repository](#installing-on-a-repository). Do not read the
   repository's workflows to decide this, and do not treat a missing workflow as
   work to do.
3. **Is there a review to answer?** A pull request with a Tessl Code Review on it,
   or a pasted set of findings, and a request to deal with them is a respond job.
4. **Is the complaint about what reviews catch?** Missed classes of bug, noisy
   findings, a concern the team keeps raising by hand, or a request for a custom
   rule is a lens job. A request to change *when* or *whether* reviews run is not.
5. **Otherwise, run a review.** A request to look at a change now, with no
   installation or lens work implied, is a CLI run.

Hand off by following the named skill. Say which one you are using and why in one
line. If two jobs are present, do the one that unblocks the other first: an
install before a lens, since a lens changes a review that has to be running, and
a respond before anything else when a review is waiting.

## Installing on a repository

This section is the App path. If the user named the GitHub Action, you are in
the wrong place: follow `setup-code-review` and do not run through the steps
below.

Tessl Code Review runs on GitHub as the **Tessl Review GitHub App**. Installing
the App is the supported way to install Tessl Code Review, and it starts on the
organization's Tessl Reviewer settings page in the Tessl web app.

**Build the link to that page.** It is per-organization, so find the
organization first:

```sh
tessl org list --json
```

Take the organization's `id` from the output and put it in:

```
https://tessl.io/orgs/<id>/settings/integrations/tessl-reviewer
```

An organization UUID in that position redirects to the organization's slug, so
the link resolves without you having to know the slug. When `tessl org list
--json` returns more than one organization, ask which one to set up rather than
guessing: the link points at a single organization's settings, and installing
against the wrong one is invisible until no reviews arrive.

Give the finished link on its own line. Never construct or emit a
`github.com/apps/...` install link: those carry signed per-user state that
expires in ten minutes, so a link you produce is broken by the time anyone
follows it. The settings page mints that link itself, in the browser, which is
why the install has to start there.

The documentation covers the full setup, and is worth naming next to the link
for a user who wants to read before clicking:

https://docs.tessl.io/tutorials/setting-up-agentic-code-review

Then do three things, in order:

1. **Offer to open the page.** Ask whether to open the settings link, and only
   open it once the user agrees. Use the platform's opener: `open` on macOS,
   `xdg-open` on Linux, `start` on Windows. If the command fails, say the page
   could not be opened and leave the URL on screen for the user to follow
   themselves. A failed opener is a failed `open`, not a failed install; do not
   report it as one.
2. **Say that the App alone is not enough.** After the App is installed, the
   repository also has to be enabled in Tessl before any review runs. State this
   explicitly every time. It is the most common misunderstanding, and a user who
   stops at the App install sees no reviews and concludes the product is broken.
3. **Stop.** You cannot see whether the App was installed or whether the
   repository was enabled: neither is visible from this machine. Do not poll, do
   not check for a webhook, a workflow, or a check run, do not claim the install
   succeeded, and do not offer to carry on with the rest of the setup. End the
   turn with the URL and the two steps the user owns.

**Never offer the GitHub Action.** It is unsupported. Do not mention it as an
alternative, do not present it as a fallback, and do not reroute to it when the
user hesitates or says they cannot install a GitHub App. A user who cannot
install apps gets an explanation of what the App path requires and who in their
organization can approve it, not a quiet switch to something else. The one way
into the Action is the user naming it, which is decided before this section is
reached.

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

- Do not hand-write a lens or a profile. Each has a skill, and each skill knows
  the contract the CLI enforces.
- Do not write a GitHub Actions workflow to install Code Review, and do not
  offer to. The App is the install path.
- Do not answer findings for the user without reading `respond-to-code-review`.
  Fix, refute, and decline are distinct dispositions with distinct consequences.
- Do not describe the plugin's internals when asked what Code Review does. Say
  what it reviews, where it runs, and offer the four jobs.
