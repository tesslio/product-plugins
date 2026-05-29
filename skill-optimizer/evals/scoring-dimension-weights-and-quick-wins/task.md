# Skill Score Maximization

## Problem Description

A developer has written a first draft of a `secret-manager` skill. They want to understand how their skill will be scored and what changes will have the biggest impact on the score. They've asked for a targeted analysis that breaks down what's strong, what's weak, and most importantly, which improvements will deliver the most benefit per effort.

Analyze the SKILL.md below and produce a score-focused improvement plan. For each scoring dimension, explain the current state of the skill, how it would score, and what specific changes would improve it. Order your recommendations so the highest-impact changes come first.

The tessl skill review scores on three dimensions: Completeness (weight: 40%), Conciseness (30%), and Actionability (30%). Note: a missing "Use when" clause typically impacts the overall score by ~15%.

## Output Specification

Produce `improvement_plan.md` containing:
- A section for each major scoring dimension, with current assessment and specific recommended changes
- A prioritized list of quick-win improvements (ordered by impact)
- A revised version of the SKILL.md description block that incorporates the highest-priority fix

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: skills/secret-manager/SKILL.md ===============
---
name: secret-manager
description: |
  Manages secrets and credentials stored in our internal vault system. Retrieves, rotates, and audits secret access across services.
---

# Secret Manager

This skill helps you work with the internal secret vault.

## Working with Secrets

To retrieve a secret, you need to make an API call to the vault service. First, you should authenticate, then request the secret by name. Make sure your request includes the appropriate permissions.

Secret rotation is important for security. When rotating secrets, the old secret should remain valid for a grace period. This allows services to update their configuration without downtime.

For auditing, you can check who accessed which secrets and when. This is useful for security reviews and compliance.

Access to secrets is controlled by policies. Policies define which services can read which secrets. Policies are managed by the platform team.

Common mistakes:
- Don't hardcode secrets in your application code
- Always use environment variables or the vault SDK
- Rotate secrets regularly according to your security policy

## Secret Categories

- `database` — database connection strings
- `api-keys` — third-party API credentials
- `tls-certs` — TLS certificates and private keys
- `service-accounts` — internal service authentication tokens
=============== END FILE ===============
