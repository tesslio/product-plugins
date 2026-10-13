# tessl/code-review

Tessl Code Review in one plugin: set it up on a repository, run it, tune what it catches, and answer what it finds.

Tessl Code Review reviews a change with several reviewers in parallel, one per lens, then merges and grades their findings into one review. It runs from the CLI as `tessl code review`, and on GitHub as the Tessl Review GitHub App.

## Install

```bash
tessl install tessl/code-review
```

A current Tessl CLI already carries the agent skills below inside `tessl agent`, so installing is only needed to pin the plugin in a project or to use it from another agent.

## Start here

Tell your agent what you want. The `code-review` skill works out which job it is and hands off.

| You want to | Skill | Say something like |
| --- | --- | --- |
| Add Code Review to a repository | the Tessl Review GitHub App, below | "Set up Tessl Code Review on this repo" |
| Review a change right now | `tessl code review` | "Review this branch against main" |
| Make reviews catch something they miss, or stop flagging something they should not | `create-code-review-lens` | "Our reviews keep missing N+1 queries" |
| Deal with a review that has arrived on your pull request | `respond-to-code-review` | "Address the Tessl review on PR 42" |

## Set it up

Tessl Code Review runs on GitHub as the **Tessl Review GitHub App**. Installing the App is the supported way to install it:

https://docs.tessl.io/tutorials/setting-up-agentic-code-review

Installing the App is not enough on its own. The repository also has to be enabled in Tessl before any review runs.

## Run it

```bash
tessl code review                                  # working tree against the default branch
tessl code review --base origin/main --head HEAD
tessl code review --pr 42
tessl code review --json > review.json             # one document, on success and on failure
```

Check `status` in the JSON before counting anything: only an `ok` run is a completed review. A `failed` or `skipped` run with no findings otherwise looks like a clean review.

### The default lenses

These four skills are the set a review runs by default. Between them they cover the dimensions a review is expected to catch, and they were tuned to run together. They are reviewer instructions, loaded into the reviewer agents by `tessl code review`. They are not skills to follow directly.

- **review-correctness-and-data-integrity**: whether the change does what it is meant to do, and whether the data it touches survives it intact.
- **review-maintainability-and-code-quality**: whether the next person can understand the change and modify it safely.
- **review-scale-and-resilience**: what the change costs as load, data volume, and concurrency grow, and what it does when something it depends on fails.
- **review-security-and-privacy**: what an adversary could do with the change, and what it exposes about people.

### Selecting lenses

`--skill` states the complete lens set, in the order supplied. It **replaces** the defaults rather than adding to them, so naming one lens makes it the whole review. A reference can be a local path, an installed skill name, or a registry ref `workspace/plugin[@version]#skill`. A registry ref without a version follows the newest published version of the plugin, so what it reviews for changes when the plugin is republished. A ref with a version stays fixed until someone edits it. A review with no profile and no `--skill` runs these lenses at `tessl/code-review@0.2.0`. The CLI sets that version, so installing or upgrading this plugin does not change it. To run this release's lenses instead, name them with this plugin's version, or with no version to follow the newest.

```bash
tessl code review --skill tessl/code-review@0.2.0#review-security-and-privacy
tessl code review \
  --skill tessl/code-review@0.2.0#review-security-and-privacy \
  --skill tessl/code-review@0.2.0#review-correctness-and-data-integrity
tessl code review --skill ./review-lenses/review-scale-and-resilience   # a lens you keep locally
```

An automated review runs the same defaults unless the repository has a profile. The profile is `.tessl-code-review.yml` at the repository root. It names the complete ordered lens set, can route each lens to paths with globs, and can list paths, under `ignore`, that no lens selects. A file renamed into an ignored path is still reviewed. The App reads it once it exists on the default branch. The CLI reads it when you pass `--profile ./.tessl-code-review.yml`. The format is in [`skills/code-review/references/repository-profile.md`](skills/code-review/references/repository-profile.md).

## Tune it

`create-code-review-lens` turns a review concern into a lens that has been run, tuned, and pinned. It settles the review question and the bar a finding has to clear, drafts the lens, runs it against a change that should trip it and one that should not, backtests it against changes that already carry review feedback, and gives it a reference a review can select.

The default lenses are meant to be forked. Copy one into your repository, tune it, and reference it by local path. A skill needs `name` and `description` frontmatter; past that, the shape most lenses use is Scope, Method, Threshold, Reporting. Keep a lens short and carry only what makes it distinct.

## Answer it

`respond-to-code-review` works a review that has arrived on your pull request. It starts from what the pull request was opened to do, verifies each finding against the code, then gives each one disposition: fix, refute, or decline with a reason. A finding it cannot check gets no disposition yet; it stays open with a note of what would settle it. It replies on every thread, resolves the settled ones, and asks for the next round with `@tessl-code-review` when the code is pushed. When rounds stop converging it stops and puts the disagreement in front of a human instead of running another one.

## Skills

| Skill | Description |
| --- | --- |
| `code-review` | Start here. Routes a request to the right job below, and runs a review from the CLI. |
| `create-code-review-lens` | Settle the review question and threshold, draft the lens, run and backtest it, then pin it. |
| `respond-to-code-review` | Adjudicate each finding on your pull request, reply, and keep the pull request on its goal. |
| `review-correctness-and-data-integrity` | Default lens. Functional defects, data loss, duplicate writes, ordering, integration contracts. |
| `review-maintainability-and-code-quality` | Default lens. Naming, weak contracts, local precedent, misleading comments, unenforced surfaces. |
| `review-scale-and-resilience` | Default lens. Load, volume, concurrency, retries, rollout, dependency failure. |
| `review-security-and-privacy` | Default lens. Trust boundaries, authorization, injection, secrets, disclosure. |

## Related

- [Setting up agentic code review](https://docs.tessl.io/tutorials/setting-up-agentic-code-review), the supported install path.
- `tessl/plugin-creator`, for packaging a lens of your own as a plugin to share across repositories.
- `tessl/review-plugin-creator`, for `tessl review` rubrics, which score skill quality rather than code.
