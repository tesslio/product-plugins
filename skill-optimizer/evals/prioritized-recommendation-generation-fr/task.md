# Skill Improvement Recommendations

## Problem Description

An internal tooling team has just reviewed their `deploy-helper` skill and received raw output from their skill evaluation tool. The feedback contains a mix of errors, missing required elements, and style issues — but the raw output is hard to act on. The team wants a structured, prioritized recommendation document they can work through systematically.

Your task is to process the skill review output below and produce a clear, actionable recommendations document. The document should tell the team exactly what to fix, in what order, how to make each change, and why each change matters for their skill's quality.

## Output Specification

Produce a file `recommendations.md` containing actionable, structured recommendations the team can work through to improve the skill. Organize them so the most important fixes are tackled first. For each recommendation include enough context that a developer can understand the issue and implement the change without needing additional research.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: review_output.txt ===============
=== Skill Review: deploy-helper ===
Overall Score: 51%

ERRORS (must fix):
  [ERROR] Description field is missing the "Use when..." trigger clause
  [ERROR] Broken file reference: [deployment checklist](DEPLOY_CHECKLIST.md) - file not found

Dimension Scores:
  Completeness:   1/3  (33%)  - Missing "Use when" clause reduces routing accuracy
  Actionability:  1/3  (33%)  - Instructions are abstract; no executable examples provided
  Conciseness:    2/3  (66%)  - Some repeated explanations; several paragraphs explain concepts Claude already knows (e.g., what JSON is, how HTTP works)
  Robustness:     2/3  (66%)  - Good error handling patterns, could add retry logic examples

Judge Suggestions:
  - The description doesn't tell agents WHEN to activate this skill, making routing unreliable
  - Replace prose instructions with runnable code snippets showing actual deploy commands
  - Remove the explanation of REST API concepts - agents already know this
  - The broken DEPLOY_CHECKLIST.md link will cause confusion when agents try to follow it
  - Consider adding a retry pattern example for transient deployment failures
=============== END FILE ===============

=============== FILE: deploy_helper/SKILL.md ===============
---
name: deploy-helper
description: |
  Helps engineers deploy services to our internal Kubernetes cluster.
---

# Deploy Helper

This skill helps you deploy services to the internal platform.

## How Deployments Work

REST APIs use HTTP methods like GET, POST, PUT, and DELETE to communicate. JSON is a text format for data exchange. Our deploy system uses these standard patterns.

When you want to deploy a service, you should:
1. Make sure your container image is built and pushed to the registry
2. Update the deployment configuration with the new image tag
3. Apply the configuration to the cluster
4. Monitor the rollout status
5. Verify the service is healthy after deployment

For more information see the [deployment checklist](DEPLOY_CHECKLIST.md).

## Configuration

The deployment configuration should include your service name, image reference, replica count, and resource limits. Make sure these are set correctly before deploying.
=============== END FILE ===============
