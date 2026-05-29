# Tile Eval Readiness Checker

## Problem Description

The developer experience team at a software consultancy has been asked to create a repeatable onboarding kit for engineers who are new to running Tessl tile evaluations. Several engineers have recently hit walls trying to kick off evaluation runs — some were pointing at the wrong directory, others didn't realize they needed active credentials, and a few had tiles with no scenarios at all. Each of these blockers is only discovered mid-run, wasting time.

The team lead wants a self-contained pre-flight kit: a shell script and a short reference document that any engineer can run before starting an evaluation. The script should walk through all the necessary verification steps in order and surface any blockers clearly. The document should explain the pre-flight process so engineers understand what they're checking and why.

## Output Specification

Produce two files:

- `preflight.sh` — An executable shell script that checks all prerequisites. It should print clear status messages for each check and stop (exit non-zero) with a helpful message if a required condition is not met. It should accept the tile path as an argument (e.g., `./preflight.sh ./my-tile`).

- `runbook.md` — A reference document (under 400 words) that explains the pre-flight process, describes the model options and their trade-offs, and documents what a user should expect in terms of timing and configuration choices before a run begins.
