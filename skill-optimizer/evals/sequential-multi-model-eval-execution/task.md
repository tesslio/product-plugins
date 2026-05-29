# Multi-Model Tile Benchmark Automation

## Problem Description

A platform team maintains a growing library of Tessl tiles and needs to reliably benchmark each tile's skill quality across the range of Claude models their customers use. The process is currently done manually — engineers run commands one at a time and lose track of job IDs when multiple models are running. Benchmarks are sometimes kicked off in parallel by mistake, causing noisy results and billing surprises, and when a job fails it often goes unnoticed until the engineer checks back hours later.

The team wants a single, self-contained shell script that automates the full execution phase of a multi-model benchmark: starting all model runs in the correct order, tracking each job, providing links for real-time monitoring, polling until every run finishes, and handling job failures automatically. The tile being benchmarked is located at `./analytics-tile` and already has eval scenarios in place.

## Output Specification

Produce one file:

- `benchmark.sh` — An executable shell script that runs the full benchmark. It should print progress updates as each job starts and completes. It should exit with a non-zero status if any run cannot be successfully completed even after a retry attempt.

The script should be written for `bash` and should work on a standard Linux environment with the `tessl` CLI available on PATH.
