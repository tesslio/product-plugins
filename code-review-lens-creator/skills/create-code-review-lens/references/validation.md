# Validating a lens

How to run a lens against real changes, and how to judge what comes back.

## Pointing the review at a change

`tessl code review` reviews the local change by default. The other selectors pick a different subject:

- `--base <ref>` alone reviews the working tree against that ref, staged and unstaged changes included. Use this while iterating: it picks up an edit without a commit.
- `--base <ref>` with `--head <ref>` reviews the range between two commits, which is how to reproduce the diff a past review saw. `--base` alone here would review your working tree instead.
- `--pr <number-or-url>` reviews a pull request, including its existing review conversation. It reaches GitHub, so it needs credentials. Right for looking at a live pull request, wrong for a measured backtest, for the reason below.

## Isolating the lens

`--skill` replaces the default lenses rather than adding to them, so naming one lens makes it the whole review:

```bash
tessl code review --skill ./review-lenses/review-test-reliability --base origin/main
```

That is what you want while iterating: every finding is attributable to this lens, and the run is as cheap as it gets. Before adopting the lens, run it once alongside the lenses it will actually run with, to see how its findings fare once they are merged and graded with the rest.

## Reading what comes back

`--json` writes one document to stdout, on success and on failure alike. There is no output flag, so redirect it.

```bash
tessl code review --skill ./review-lenses/review-test-reliability \
  --base origin/main --json > findings.json
```

Keep one file per run so counts stay comparable. Each finding carries a title, body, evidence, the lenses that contributed it, a severity, and a location. A location with no line means the finding did not sit on a particular changed line, so it arrived in the summary rather than as an inline comment.

**Check `status` before counting anything.** A failed run writes the same shaped document and carries no findings, so an exhausted credit balance, a missing token, or an unresolvable lens reference is indistinguishable from a clean review unless the status is read. Counted blind, a broken run is a negative case that passes and a backtest entry that found nothing. Confirm every run reports `"status": "ok"`, and rerun the ones that did not.

## Two directed checks first

Before any backtest, run the lens twice: on a change that should trip it, and on a change that should not. The negative case is what catches an over-broad lens, and it is the one people skip.

If the lens fires on the negative case, that is a threshold or exclusion problem, and it is cheaper to fix now than after a backtest has measured it across twenty pull requests.

## Then the same change twice

Run the positive case a second time. Two runs over one change say something one cannot: reviews vary, and a lens that leaves too much to the reviewer's discretion varies a lot.

If the two runs broadly agree on what matters, the lens is directing the review. If they find substantially different things, it is not saying enough about where to look, which is usually Method rather than Scope.

The cure for that is also the overdose. Listing instances makes a lens perfectly repeatable and blind to everything it did not list, so pair the two runs with the test in [lens-anatomy.md](lens-anatomy.md): would this lens work on a codebase in another language? Unstable means under-directed. Language-specific means over-directed.

## The backtest set

Choose changes that already carry review feedback in the lens's area, so there is something to compare against:

- merged pull requests with human review comments, requested changes, or follow-up fix commits in the area the lens covers;
- pull requests a prior automated reviewer already commented on;
- a recent window, narrowed by label, directory, or team when the repository is large.

Aim for enough changes to show a pattern rather than one pull request's quirks or one run's. Each pull request is a full run, so a set of twenty costs twenty reviews. Weigh that against how many reviews the lens will run in once adopted.

Review the same revision the original feedback saw, by reconstructing its base and head:

```bash
tessl code review --skill ./review-lenses/review-test-reliability \
  --base <merge-base> --head <original-head> --json > backtest-4471.json
```

A lens run against a later head is being judged on a diff the original reviewer never saw.

**Do not backtest with `--pr`.** It brings the pull request's review conversation into the run, which is the material being compared against. Worse, a pull request that already carries a Tessl review is treated as a re-review: the lens sees only the change since that review, and the results come back as reconciliation of the earlier findings. The counts would describe a different diff from the one the original feedback was written about. That applies most to the pull requests that look most attractive for a backtest, so use explicit base and head every time.

## Comparing

Sort each finding the lens produced into one of:

- **Useful match**: the lens flags something the original review also raised.
- **Novel useful finding**: the lens flags a real problem the original review missed.
- **False positive**: the lens flags something that is not a problem.
- **Unplaced finding**: no line to sit on, so it appeared in the summary rather than as an inline comment. An observation rather than a verdict, and it splits two ways below.

Then read the original feedback again for anything in the lens's scope with no matching finding:

- **Miss**: the original review raised something this lens should have caught.

A miss has no finding to sort, so it surfaces only from this second pass. Skip the pass and misses go uncounted.

## What each category asks you to change

- **False positives**: tighten the bar, or name the exclusion that covers this case. Adding caution to the lens rarely works; naming the specific case that is fine does.
- **Misses**: add the signal the lens never names, or change Method so the reviewer reaches the code where the problem lives.
- **Unplaced findings**: read them before deciding anything. One that had an obvious line to sit on means the lens is producing conclusions where it should be producing observations about specific code, and the reporting rules are what to change. One about something missing had nowhere to sit and is working as intended; judge it on whether it is specific enough to act on from the summary alone. A run whose unplaced findings are all whole-change verdicts is the case worth fixing.
- **Useful matches that duplicate another lens**: narrow the scope. Two lenses covering the same ground pay for the same finding twice.

Report the counts per category with a few examples of each: the strongest matches and novel findings, the clearest false positives and misses, and any recurring unplaced finding. Then re-run the same set after tuning, so a gain in one category is not quietly paid for out of another.
