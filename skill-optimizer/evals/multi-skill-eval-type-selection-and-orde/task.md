# Eval Kickoff Plan for invoice-processor Plugin

## Problem Description

The engineering team at Fieldstone has built an invoice-processor plugin containing several specialized skills for handling different parts of their invoice automation pipeline. The plugin is new — no evals have been run against it yet. Before investing hours of compute time in scored evals, the tech lead wants a clear plan for how to kick off evaluation in the right order.

The team has heard that running the wrong type of eval first can waste time (e.g., running scored evals against scenarios that route to the wrong skill). They want a concrete plan — ideally a shell script — that:

1. Detects what kind of plugin they're working with
2. Chooses the right eval strategy based on what's found
3. Describes what to do after the first round of results comes in

The plugin is already present on disk at `./invoice-processor/`.

## Output Specification

Produce a file called `eval-kickoff-plan.sh` (a shell script) and a short `eval-notes.md` explaining the reasoning behind the eval ordering strategy chosen.

The script should:
- Detect the number of skills in the plugin
- Run the appropriate eval type first given the plugin structure and the absence of existing results
- Show what commands to run after the first results are available

The notes file should explain:
- Why the chosen eval type was run first
- What to do after those results come back
- Under what circumstances you would skip the first eval type entirely
