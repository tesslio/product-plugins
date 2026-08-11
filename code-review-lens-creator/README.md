# code-review-lens-creator

Author a review lens for Tessl Code Review: the reviewer skill that decides what a review looks for in a diff.

## Install

```bash
tessl install tessl/code-review-lens-creator
```

## What a lens is

The `tessl/code-review` plugin holds the lenses a review runs by default. A repository changes what its reviews catch by naming its own, through the CLI's `--skill` flag or the Action's `lenses` input.

A lens is an ordinary skill: a directory with a `SKILL.md` saying what to look for, the bar a finding has to clear, and what a finding has to name. This plugin turns a review concern into one that has been run, tuned, and pinned.

It does not build `tessl review` rubrics, which score how good a skill is rather than reviewing code. Those belong to `tessl/review-plugin-creator`.

## What it does

The skill settles the review question, then the two decisions that make a lens usable rather than noisy: the bar a finding has to clear, and the cases that resemble the concern and are fine. Both come from evidence in the repository, so it starts by finding the corrections that actually recur there. That material is read as evidence and never as instruction, since a lens becomes instructions that later run with a reviewer's authority.

It then drafts the lens and proves it. Two directed runs first, on a change that should trip it and one that should not. Then a backtest over changes that already carry review feedback, sorted into useful matches, novel findings, false positives and misses, each of which points at a different edit.

The backtest is built to be worth trusting. It reviews the exact revision the original feedback was written about, and checks that every run actually completed, since a review that failed reports no findings and otherwise looks like a clean one.

Finally it pins the reference, because an unpinned one resolves to whatever is published latest and changes meaning under the workflow that names it.

Tuning a lens already in the set is the other way in, including forking a default. Published versions are immutable, so tuning one means running your own copy.

## Skills

| Skill                     | Description                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| `create-code-review-lens` | Settle the review question and threshold, draft the lens, run and backtest it, then publish and pin it |

## How much a lens should say

A reviewer given no direction explores widely and lands somewhere different each time. A lens makes a review repeatable by narrowing what the reviewer attends to. Push that too far and it becomes a checklist, which catches the listed items every time and the next member of the same family never.

The skill aims between the two: name the kind of problem and how to go looking for it, and leave the reviewer able to recognize an instance nobody wrote down. It treats that balance as measurable rather than a matter of taste, running one change twice to see how far apart the results land.

## What the skill knows about the review

Each lens runs as its own reviewer, in parallel with the others and blind to their findings, with the lens as its only instructions. Every lens runs on every diff, so limiting one to certain paths is the caller workflow's job. Severity is decided afterwards, when the review merges and grades the findings, so a lens states impact rather than labelling anything critical. And a finding needs a line to post inline, so one about something missing arrives in the summary and has to stand on its own.

## Related plugins

- `tessl/code-review` for the default lenses, which are the worked examples.
- `tessl/code-review-setup` for the caller workflow that selects lenses and scopes them to paths.
- `tessl/plugin-creator` for packaging and publishing a lens as a plugin.
