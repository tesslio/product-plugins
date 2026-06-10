# Webhook Processor Plugin: Retry Reliability Fix

## Problem Description

Your platform team maintains a plugin for webhook processing that multiple agent-driven services rely on. Recently, during a traffic spike, several services started hammering the downstream API with rapid retry bursts when webhooks failed — causing cascading failures and rate-limit errors. After reviewing the incidents, the team agreed the plugin's retry guidance was too vague, leaving agents to implement whatever retry strategy seemed reasonable.

You've been given the plugin along with the eval rubric that's currently used to grade agents on their retry implementations. Your job is to update the plugin so agents have unambiguous, specific guidance on how to retry failed webhook deliveries — without disrupting the parts of the plugin that are already working well.

## Output Specification

Update the `inputs/SKILL.md` file in place with the improvements. Do not rewrite sections that aren't related to retry behavior. Save a brief `change_summary.md` documenting: which sections you changed, what you added or modified, and why.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/SKILL.md ===============
---
name: webhook-processor
description: Process incoming webhooks reliably with signature validation and retry logic
---

# Webhook Processor

## Setup

Configure your webhook endpoint to accept HTTPS connections with TLS 1.2 or higher.
Use HMAC-SHA256 to validate incoming signatures against your webhook secret before processing any payload.

## Processing

1. Validate the incoming signature before touching the payload
2. Parse the JSON body and extract the event type
3. Route the event to the appropriate handler based on event type
4. Acknowledge receipt with a 200 response as quickly as possible (before heavy processing)

## Reliability

If processing fails after acknowledgement, retry the operation up to 3 times.
Wait between retries to avoid overwhelming the downstream service.
Log each retry attempt including the attempt number and error received.

## Observability

Emit a structured log entry for every webhook received, including:
- Event type
- Source IP
- Processing duration in milliseconds
- Final outcome (success or failure after retries)

=============== FILE: inputs/eval_criteria.json ===============
{
  "context": "Tests whether agents implement robust retry logic for failed webhook processing",
  "type": "weighted_checklist",
  "checklist": [
    {
      "name": "Exponential backoff timing",
      "description": "Retry delays follow exponential backoff with intervals of 1s, 2s, then 4s",
      "max_score": 25
    },
    {
      "name": "Max retry count",
      "description": "Maximum of 3 retry attempts before marking the webhook as failed",
      "max_score": 15
    },
    {
      "name": "HMAC-SHA256 validation",
      "description": "Validates incoming webhook signature using HMAC-SHA256 algorithm",
      "max_score": 20
    },
    {
      "name": "Retry logging",
      "description": "Each retry attempt is logged with attempt number and error details",
      "max_score": 20
    },
    {
      "name": "Fast acknowledgement",
      "description": "Returns 200 acknowledgement before heavy processing begins",
      "max_score": 20
    }
  ]
}
