# tessl/code-review

Code review lenses for `tessl code review` and the Tessl Code Review GitHub Action. Each lens is its own skill, so a run can point at exactly the lenses it wants.

The lenses below are the set a review runs by default. Between them, they cover the common dimensions a review is expected to catch, and they were tuned to run together.

## Lenses

- **review-correctness-and-data-integrity**: whether the change does what it is meant to do, and whether the data it touches survives it intact. Edge cases in changed logic, what a write path can lose or duplicate, and whether the two sides of an independently deployed boundary still agree.
- **review-maintainability-and-code-quality**: whether the next person can understand the change and modify it safely. Precedent the codebase already has, surfaces that do not enforce what they claim, and names or comments a reader is likely to misread.
- **review-scale-and-resilience**: what the change costs as load, data volume, and concurrency grow, and what it does when something it depends on fails, including duplicate execution and deployments where old and new code run together.
- **review-security-and-privacy**: what an adversary could do with the change, and what it exposes about people. Untrusted input reaching a sensitive operation, and data disclosed to a party not entitled to receive it.

## Lenses outside the default set

These ship with the plugin but do not run unless a review names them. They read
a surface the default lenses have nothing to grip on, so running them on a whole
repository would mostly produce nothing.

- **review-plugin-authoring**: whether an agent will reach the right skill and then act correctly on it. Frontmatter descriptions that collide or under-trigger, a command or path an instruction names that does not resolve, a step an agent has to guess through, and what a change adds to the standing context cost of every session. Scope it to the paths that hold plugin and skill content.

```bash
tessl code review --skill tessl/code-review@0.2.0#review-plugin-authoring
```

## Selecting lenses

`tessl code review` runs these by default, so a plain run needs no lens selection at all:

```bash
tessl code review
```

`--skill` states the complete lens set instead, in the order supplied. It **replaces** the defaults rather than adding to them, so naming one lens makes it the whole review. A reference can be a local path (a `SKILL.md` file or a skill directory), an installed skill name, or a registry ref `workspace/plugin[@version]#skill`.

Pin the version in a reference you keep. An unpinned ref resolves to whatever the latest published version is, so its meaning changes under you when the plugin is republished.

```bash
tessl code review --skill tessl/code-review@0.1.0#review-security-and-privacy
```

Several lenses in one run:

```bash
tessl code review \
  --skill tessl/code-review@0.1.0#review-security-and-privacy \
  --skill tessl/code-review@0.1.0#review-correctness-and-data-integrity
```

Or a lens you keep in your own repository, which is also how you iterate on one you have forked:

```bash
tessl code review --skill ./review-lenses/review-scale-and-resilience
```

## Reading the result

`--json` writes one document to stdout, on success and on failure alike. There is no output flag, so redirect it:

```bash
tessl code review --base origin/main --json > review.json
```

Check `status` before counting anything: a failed run writes the same shaped document and carries no findings, so a broken run is indistinguishable from a clean review unless the status is read.

## Using from GitHub Actions

The [Tessl Code Review Action](https://github.com/tesslio/code-review-action) runs the review and publishes it as one native pull-request review with inline comments. It runs the same defaults unless its `lenses` input names a complete ordered set of its own:

```yaml
lenses: >-
  ["tessl/code-review@0.1.0#review-security-and-privacy"]
```

For the caller workflow — triggers, permissions, advisory versus gating — use `tessl/code-review-setup`.

## Forking a lens

The lenses are meant to be forked. Copy one into your own repository and tune it for your codebase, then reference it by local path instead of by registry ref. Or publish it to the registry to share it across your repositories.

A skill needs `name` and `description` frontmatter. Past that, the shape is a suggestion rather than a contract, and a reasonable starting point if you have no strong view of your own:

- **Scope**: what the lens covers.
- **Method**: how to go looking, where that differs from reading the diff in file order.
- **Threshold**: the bar a finding has to clear, and what not to report.
- **Reporting**: what a finding has to name to be actionable.

Several of these lenses hold two or three related dimensions, so treat one lens per dimension as a tendency rather than a rule. What matters more is that a lens stays short and carries only what makes it distinct.

For authoring, validating and backtesting a lens of your own, use `tessl/code-review-lens-creator`.
