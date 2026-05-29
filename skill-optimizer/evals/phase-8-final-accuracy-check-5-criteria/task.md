# Skill Post-Edit Quality Audit

## Problem Description

A developer has just applied a set of changes to a `log-analyzer` skill file and wants to make sure nothing was broken in the process. Before they commit the updated skill, they want a thorough quality audit that checks for common mistakes that can sneak in during editing: broken code syntax, invalid commands, dead links, and content that shouldn't be in the skill at all.

Audit the updated SKILL.md below and produce a structured quality report. Check every potential issue category and give a clear pass/fail result for each, with specific details where problems are found.

## Output Specification

Produce a file `accuracy_check.md` containing:
- A structured checklist with pass/fail status for each category of check
- Specific details for any failures (what's wrong, where, suggested fix)
- A final summary indicating whether the skill is ready to publish

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: skills/log-analyzer/SKILL.md ===============
---
name: log-analyzer
description: |
  Analyzes application logs to identify error patterns and performance issues. Helps engineers debug production incidents and understand system behavior.
---

# Log Analyzer

Parse and analyze application logs using our internal `logq` tool.

## Common Queries

Find errors in the last hour:

```bash
logq query --source app-logs --level error --since 1h --format json
```

Count error types:

```python
import subprocess
import json

def count_errors(log_source: str, window: str = "1h") -> dict:
    result = subprocess.run(
        ["logq", "query", "--source", log_source, "--level", "error", "--since", window, "--format", "json"],
        capture_output=True, text=True
    )
    logs = json.loads(result.stdout
    error_counts = {}
    for entry in logs:
        err_type = entry.get("error_type", "unknown")
        error_counts[err_type] = error_counts.get(err_type, 0) + 1
    return error_counts
```

Export results to CSV:

```javascript
const { exec } = require('child_process');
const fs = require('fs');

function exportLogs(source, outputFile) {
  exec(`logq export --source ${source} --format csv --output ${outputFile}`, (err, stdout, stderr) => {
    if (err) throw err;
    console.log('Export complete:', outputFile);
  });
}
```

For more query patterns and aggregation options see [QUERY_PATTERNS.md](QUERY_PATTERNS.md).

## Performance Analysis

Use `logq stats` to get percentile breakdowns:

```bash
logq stats --source app-logs --metric response_time --percentiles 50,95,99 --since 24h
```

Note: HTTP is a stateless request/response protocol. Each log entry represents one request-response cycle. TCP connections may be reused.
=============== END FILE ===============

=============== FILE: skills/log-analyzer/QUERY_PATTERNS.md ===============
# Query Patterns Reference

Advanced logq query patterns and aggregations.

## Aggregations
- `logq aggregate --group-by error_type --count`
- `logq aggregate --group-by service --sum response_time`

## Time Windows
- `--since 1h` — last 1 hour
- `--since 24h` — last 24 hours
- `--since 7d` — last 7 days
=============== END FILE ===============
