# Data Pipeline Plugin: Consistency Audit

## Problem Description

Your team has been iterating on a data pipeline plugin over the past few months. Three different engineers have contributed to different parts of it — one owns the main skill file, another maintains the operational rules, and a third recently added a reference doc for error handling. No one has done a cross-file review since the initial version.

Recent eval scores on the retry logic scenario have been inconsistent, with agents implementing wildly different retry counts. This suggests there may be conflicting guidance somewhere in the plugin. Before the next release, you need a full consistency audit to find any statements that contradict each other across all plugin files — not just the retry-related ones.

## Output Specification

Produce a file called `contradiction_report.md` that:
1. Lists every contradiction found across the plugin files
2. For each contradiction: identifies the specific files involved, quotes the conflicting statements verbatim, and explains why they conflict
3. Includes a severity note for each (would this likely cause agent confusion or regression?)

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/SKILL.md ===============
---
name: data-pipeline
description: Ingest, transform, and deliver data between systems reliably
---

# Data Pipeline Skill

## Overview

This skill handles data ingestion, transformation, and delivery between upstream producers and downstream consumers.

## Authentication

All connections to data sources must use service account credentials.
If authentication fails at connection time, abort the pipeline run immediately and raise an alert.

## Ingestion

1. Connect to the upstream source using the configured service account
2. Fetch records in batches of 500
3. Validate schema on each record before queuing
4. If a record fails validation, skip it and log the failure — do not abort the pipeline

## Transformation

Apply the configured transform functions in the order specified in the pipeline manifest.
If a transform raises an exception, retry the transform up to 5 times before marking the record as failed.

## Delivery

Push transformed records to the downstream sink in the same batch order they were received.
Confirm delivery acknowledgement from the sink before marking records as successfully delivered.

## Error Handling

On any unrecoverable error, write a failure record to the dead-letter queue and continue processing remaining records.

=============== FILE: inputs/rules/retry-policy.md ===============
# Retry Policy

All retry operations in this plugin follow a conservative retry policy to protect downstream services:

- Maximum retries: 3 attempts (not counting the initial attempt)
- Retry only on transient errors (5xx responses, network timeouts, connection resets)
- Do not retry on client errors (4xx responses) or validation failures
- Log each retry attempt with: attempt number, error type, and timestamp

This policy applies to all operations in the plugin unless explicitly overridden by a specific step.

=============== FILE: inputs/docs/error-handling.md ===============
# Error Handling Reference

## Philosophy

The pipeline is designed to be resilient and self-healing. Failures in individual records or connections should not halt the entire pipeline unless they are truly unrecoverable.

## Authentication Failures

If an authentication failure occurs mid-pipeline (e.g., a token expires while the pipeline is running), the pipeline should attempt to refresh credentials and continue. If the refresh also fails, skip the affected batch and log the error — do not abort the full pipeline run.

## Record-Level Errors

For records that cannot be processed after all retries are exhausted, write them to the dead-letter queue. The pipeline continues processing all remaining records regardless of individual record failures.

## Transform Failures

Transform failures are transient in nature. The pipeline should retry failed transforms with a brief pause between attempts. After retries are exhausted, the record is moved to the dead-letter queue.
