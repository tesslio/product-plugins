# Skill Bundle Validation

## Problem Description

A developer at a tools company has been iterating on a SKILL.md file for an internal automation tool. Before publishing it to the team's shared tile repository, they want to make sure all code examples in the skill are correct and all referenced files actually exist. In the past, a broken code example caused confusion when agents tried to follow the guidance — a syntax error in a Python snippet made the example unrunnable, and a linked file didn't exist.

Your job is to validate the skill bundle below and produce a structured validation report. Check every code block in the skill for correctness and check that all file references resolve. For each issue found, clearly state what is wrong and suggest a fix.

## Output Specification

Produce a file `validation_report.md` containing:
- A section for each type of validation performed (Python syntax, JavaScript syntax, command flag validity, file references)
- For each check: the item being checked, pass/fail status, and details of any errors found
- A summary section at the end listing all issues found

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: skill_bundle/SKILL.md ===============
---
name: data-pipeline-helper
description: |
  Helps engineers set up and run ETL pipelines using our internal tooling. Use when you need to ingest data from external APIs, transform records, or load results into the warehouse.
---

# Data Pipeline Helper

Automate data ingestion and transformation tasks using our internal ETL framework.

## Quickstart

Run a pipeline:

```python
import pipeline_sdk

def run_ingestion(source_url: str, dest_table: str:
    client = pipeline_sdk.Client()
    job = client.create_job(source=source_url, destination=dest_table)
    result = job.run()
    return result.records_processed
```

Check job status:

```javascript
const { PipelineClient } = require('pipeline-sdk');

const client = new PipelineClient();
const status = await client.getJobStatus(jobId)
console.log(`Job ${jobId}: ${status.state}`);
```

Validate your config:

```bash
pipeline validate --config pipeline.yaml --strict-mode --output-format json
```

See [setup guide](SETUP_GUIDE.md) for initial configuration and [troubleshooting tips](TROUBLESHOOT.md) for common errors.

## Notes

- Always call `job.run()` before accessing results
- The `--strict-mode` flag enables schema enforcement
=============== END FILE ===============

=============== FILE: skill_bundle/TROUBLESHOOT.md ===============
# Troubleshooting

Common issues and fixes for the data pipeline helper.

- Connection timeout: increase `timeout_ms` in config
- Schema mismatch: run `pipeline validate` first
=============== END FILE ===============
