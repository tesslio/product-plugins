# tessl/code-review

Tessl Code Review in one plugin: set it up on a repository, run it, tune what it catches, and answer what it finds.

Tessl Code Review reviews a change with several reviewers in parallel, one per lens, then merges and grades their findings into one review. It runs from the CLI as `tessl code review`, and on GitHub through the [Tessl Code Review Action](https://github.com/tesslio/code-review-action).

## Install

```bash
tessl install tessl/code-review
```

A current Tessl CLI already carries the agent skills below inside `tessl agent`, so installing is only needed to pin the plugin in a project or to use it from another agent.

## Start here

Tell your agent what you want. The `code-review` skill works out which job it is and hands off.

| You want to | Skill | Say something like |
| --- | --- | --- |
| Add Code Review to a repository, change when it runs or whether it blocks, or remove it | `setup-code-review` | "Set up Tessl Code Review on this repo, advisory, on every PR" |
| Review a change right now | `tessl code review` | "Review this branch against main" |
| Make reviews catch something they miss, or stop flagging something they should not | `create-code-review-lens` | "Our reviews keep missing N+1 queries" |
| Deal with a review that has arrived on your pull request | `respond-to-code-review` | "Address the Tessl review on PR 42" |

## Set it up

`setup-code-review` inspects the repository, asks two questions, and writes one thin caller workflow that invokes the Action. Nothing else is copied into the repository.

The two questions:

- **When do reviews run.** Once when the pull request becomes ready plus requested rounds (the default); on every commit; or manual only, where a review runs on an explicit dispatch or an `@tessl-code-review` mention.
- **Do findings block.** Advisory, where the review is a comment and no outcome fails the check; or gate, where changes approved passes the check and changes requested fails it.

The workflow references the Action by its major tag, `@v1`, so fixes reach the repository without editing the file. A repository that wants the revision frozen gets the current release's full commit SHA instead. The skill then explains the `TESSL_TOKEN` secret, the four permissions it grants, the branch-protection step for gate mode, and how to update or remove the setup.

## Run it

```bash
tessl code review                                  # working tree against the default branch
tessl code review --base origin/main --head HEAD
tessl code review --pr 42
tessl code review --json > review.json             # one document, on success and on failure
```

Check `status` in the JSON before counting anything: a failed run carries no findings and otherwise looks like a clean review.

### The default lenses

These four skills are the set a review runs by default. Between them they cover the dimensions a review is expected to catch, and they were tuned to run together. They are reviewer instructions, loaded into the reviewer agents by `tessl code review`. They are not skills to follow directly.

- **review-correctness-and-data-integrity**: whether the change does what it is meant to do, and whether the data it touches survives it intact.
- **review-maintainability-and-code-quality**: whether the next person can understand the change and modify it safely.
- **review-scale-and-resilience**: what the change costs as load, data volume, and concurrency grow, and what it does when something it depends on fails.
- **review-security-and-privacy**: what an adversary could do with the change, and what it exposes about people.

### Selecting lenses

`--skill` states the complete lens set, in the order supplied. It **replaces** the defaults rather than adding to them, so naming one lens makes it the whole review. A reference can be a local path, an installed skill name, or a registry ref `workspace/plugin@version#skill`. Pin the version in any reference you keep; an unpinned ref changes meaning when the plugin is republished.

```bash
tessl code review --skill tessl/code-review@0.2.0#review-security-and-privacy
tessl code review \
  --skill tessl/code-review@0.2.0#review-security-and-privacy \
  --skill tessl/code-review@0.2.0#review-correctness-and-data-integrity
tessl code review --skill ./review-lenses/review-scale-and-resilience   # a lens you keep locally
```

The Action runs the same defaults unless its `lenses` input names a complete ordered set of its own:

```yaml
lenses: >-
  ["tessl/code-review@0.2.0#review-security-and-privacy"]
```

A repository YAML profile can also route lenses to paths with globs. `setup-code-review` knows the profile format.

## Tune it

`create-code-review-lens` turns a review concern into a lens that has been run, tuned, and pinned. It settles the review question and the bar a finding has to clear, drafts the lens, runs it against a change that should trip it and one that should not, backtests it against changes that already carry review feedback, and pins the reference a workflow can select.

The default lenses are meant to be forked. Copy one into your repository, tune it, and reference it by local path. A skill needs `name` and `description` frontmatter; past that, the shape most lenses use is Scope, Method, Threshold, Reporting. Keep a lens short and carry only what makes it distinct.

## Answer it

`respond-to-code-review` works a review that has arrived on your pull request. It starts from what the pull request was opened to do, verifies each finding against the code, then gives each exactly one disposition: fix, refute, or decline with a reason. It replies on every thread, resolves the settled ones, and asks for the next round with `@tessl-code-review` when the code is pushed. When rounds stop converging it stops and puts the disagreement in front of a human instead of running another one.

## Skills

| Skill | Description |
| --- | --- |
| `code-review` | Start here. Routes a request to the right job below, and runs a review from the CLI. |
| `setup-code-review` | Detect, interview, propose, write, verify, and explain the Code Review caller workflow. |
| `create-code-review-lens` | Settle the review question and threshold, draft the lens, run and backtest it, then pin it. |
| `respond-to-code-review` | Adjudicate each finding on your pull request, reply, and keep the pull request on its goal. |
| `review-correctness-and-data-integrity` | Default lens. Functional defects, data loss, duplicate writes, ordering, integration contracts. |
| `review-maintainability-and-code-quality` | Default lens. Naming, weak contracts, local precedent, misleading comments, unenforced surfaces. |
| `review-scale-and-resilience` | Default lens. Load, volume, concurrency, retries, rollout, dependency failure. |
| `review-security-and-privacy` | Default lens. Trust boundaries, authorization, injection, secrets, disclosure. |

## Related

- [Tessl Code Review Action](https://github.com/tesslio/code-review-action), which the caller workflow invokes.
- `tessl/plugin-creator`, for packaging a lens of your own as a plugin to share across repositories.
- `tessl/review-plugin-creator`, for `tessl review` rubrics, which score skill quality rather than code.
