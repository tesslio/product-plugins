# Expand Eval Coverage for shopify-connector Plugin

## Problem Description

The shopify-connector plugin already has three evaluation scenarios that the team has been using for several months. These scenarios cover order processing, webhook handling, and authentication flows. The team recently ran a new scenario generation job (run ID: `scen-gen-7742`) that produced two additional scenarios covering edge cases around rate limiting and bulk import operations. They want to add these new scenarios alongside the existing ones.

A previous intern accidentally ran the download command without specifying any strategy flag and overwrote all the existing scenarios. The team wants to make sure this doesn't happen again — they need a download command that explicitly adds new scenarios without touching the existing three.

After downloading, they want to see a verified list of what's in the evals folder to confirm both old and new scenarios are present.

The plugin is located at `./shopify-connector/`. The existing scenarios are:
- `evals/order-processing/`
- `evals/webhook-handling/`
- `evals/auth-flow/`

## Output Specification

Produce a shell script called `download-scenarios.sh` that:
1. Downloads the newly generated scenarios from run ID `scen-gen-7742` into the plugin's evals directory without removing existing scenarios
2. Verifies the download by listing the scenario files in the evals directory

The script should be safe to re-run if something goes wrong mid-download.
