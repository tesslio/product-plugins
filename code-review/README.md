# tessl/code-review

Code review lenses for use from Tessl Agent and GitHub Actions review workflows via `tessl change review`. Each lens is its own skill, so a workflow can point at exactly the lenses it wants.

Between them they cover the common dimensions a review is expected to catch, and they are designed to run together. Name them all unless a workflow is scoped to paths that carry one signal.

## Lenses

- **review-correctness-and-data-integrity**: whether the change does what it is meant to do, and whether the data it touches survives it intact. Edge cases in changed logic, what a write path can lose or duplicate, and whether the two sides of an independently deployed boundary still agree.
- **review-maintainability-and-code-quality**: whether the next person can understand the change and modify it safely. Precedent the codebase already has, surfaces that do not enforce what they claim, and names or comments a reader is likely to misread.
- **review-scale-and-resilience**: what the change costs as load, data volume, and concurrency grow, and what it does when something it depends on fails, including duplicate execution and deployments where old and new code run together.
- **review-security-and-privacy**: what an adversary could do with the change, and what it exposes about people. Untrusted input reaching a sensitive operation, and data disclosed to a party not entitled to receive it.

## Selecting lenses

`tessl change review` takes one or more `--skill` references. A reference can be a local path (a `SKILL.md` file or a skill directory), an installed skill name, or a registry ref `workspace/plugin[@version]#skill`. Pass only the lenses you want; skills are not auto-discovered.

Pin the version in a reference you keep. An unpinned ref resolves to whatever the latest published version is, so its meaning changes under you when the plugin is republished.

```bash
tessl change review --skill tessl/code-review@0.0.3#review-security-and-privacy
```

Several lenses in one run:

```bash
tessl change review \
  --skill tessl/code-review@0.0.3#review-security-and-privacy \
  --skill tessl/code-review@0.0.3#review-correctness-and-data-integrity
```

Or a lens you keep in your own repository, which is also how you iterate on one you have forked:

```bash
tessl change review --skill ./review-lenses/review-scale-and-resilience
```

## Using from GitHub Actions

`tessl change review` only emits structured review data; a GitHub caller posts it as an overall review plus inline comments. In a workflow step, select the lenses relevant to the changed paths and write the result to a file:

```bash
tessl change review \
  --skill tessl/code-review@0.0.3#review-security-and-privacy \
  --skill tessl/code-review@0.0.3#review-correctness-and-data-integrity \
  --base origin/main \
  --json --output review.json
```

Then post `review.json` from a later step. Because each lens is a separate `--skill`, a workflow can choose lenses per changed path, for example running only the security lens on a workflow scoped to `src/auth/**`.

## Forking a lens

The lenses are meant to be forked. Copy one into your own repository and tune it for your codebase, then reference it by local path instead of by registry ref. Or publish it to the registry to share it across your repositories.

A skill needs `name` and `description` frontmatter. Past that, the shape is a suggestion rather than a contract, and a reasonable starting point if you have no strong view of your own:

- **Scope**: what the lens covers.
- **Method**: how to go looking, where that differs from reading the diff in file order.
- **Threshold**: the bar a finding has to clear, and what not to report.
- **Reporting**: what a finding has to name to be actionable.

Several of these lenses hold two or three related dimensions, so treat one lens per dimension as a tendency rather than a rule. What matters more is that a lens stays short and carries only what makes it distinct.

## Earlier lenses

This version also contains `review-code-legibility`, `review-contract-boundaries`, `review-local-precedent`, `review-security-risks` and `review-test-risk`, unchanged from `0.0.1`. The lenses above supersede them. They are retained so existing unpinned references keep resolving, and they are not part of the recommended set.
