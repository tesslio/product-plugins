# Tessl API Endpoint Discovery Script

## Problem Description

Your team is building internal developer tooling on top of the Tessl platform and needs a reliable way to discover all Tessl REST API endpoints related to software installation workflows. The spec evolves frequently, so any discovery process must always pull a fresh copy rather than rely on a potentially stale cache.

A colleague has noticed that installation-related endpoints are numerous and has asked you to write a reusable shell script that a developer can run at any time to get a comprehensive, up-to-date picture of what's available. The script should be robust enough to automatically retrieve all matching results rather than stopping prematurely.

Once the full list has been gathered, the script should pick one promising endpoint, retrieve its complete details, and record the findings in a human-readable report. The report will be shared with the wider team so developers know exactly how to invoke the endpoint without having to run the tooling themselves.

The helper discovery script is available at `scripts/tessl_api_discover.py` and is the intended interface for this kind of API exploration.

## Output Specification

Produce the following two files in your working directory:

1. **`discover-endpoints.sh`** — A shell script that:
   - Searches for all Tessl API endpoints related to "install"
   - Retrieves the complete set of matching results
   - Ensures results are always up to date
   - Selects one endpoint from the results and retrieves its full details
   - Writes its findings to `discovery-report.md`

2. **`discovery-report.md`** — A markdown report that includes:
   - An overview of how many endpoints were found in total
   - The full detail output for the chosen endpoint (description, parameters, request body, responses)
   - The command a developer can run to call that endpoint directly via the Tessl CLI
