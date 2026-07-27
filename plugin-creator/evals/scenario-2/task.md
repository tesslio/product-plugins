# Plugin Shape Planning for a Backend Engineering Team

## Problem/Feature Description

The Meridian backend team has been using AI coding assistants for a few months and wants to make the experience more consistent across engineers. They've identified four areas where they want AI assistance baked into their workflow:

1. **Pull request review workflow**: Engineers follow a specific internal PR review process — they check diff size, scan for missing tests, look for breaking API changes, and verify that CHANGELOG entries are present. This workflow is something they invoke on demand when reviewing a PR, not something that should fire constantly.

2. **Import ordering convention**: The team always wants Python imports sorted in a specific order (stdlib → third-party → internal), no exceptions. This should apply whenever the agent touches a Python file — they don't want to invoke it, it should just always be enforced.

3. **Internal metrics dashboard**: During incident response and performance reviews, engineers frequently need to query the team's internal metrics API (`https://metrics.meridian.internal/api`) to pull latency percentiles, error rates, and deployment event timelines. The agent needs to be able to call this API with a bearer token to fetch live data on demand.

4. **Post-edit validation**: Whenever the agent edits or writes a file, the team wants a deterministic validation script to run automatically. The check is agent-independent and should work across supported agents — no manual invocation needed.

Your job is to produce a `composition-plan.md` file that describes how you would build this out in Tessl — which components to use for each need, the overall shape of the solution, and anything the team should know or confirm before you start building.

## Output Specification

Produce a single file named `composition-plan.md` in the working directory.

The plan should describe how each of the four team requirements maps to the appropriate Tessl building blocks, and note anything the team should know before work begins.
