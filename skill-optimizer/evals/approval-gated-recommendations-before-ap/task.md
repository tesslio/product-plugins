# Approval-Gated Skill Change Proposal

## Problem Description

A developer has a `webhook-handler` skill that needs improvement. Their team enforces a strict approval gate: **no changes may be applied to the SKILL.md file until the tech lead explicitly approves them**. The developer has review output and needs to produce a formal proposal document — but the hard part isn't identifying improvements, it's presenting them in a way that earns informed approval.

The tech lead cares about three things:
1. **Trade-offs** — many improvements conflict with each other (e.g., adding detail for completeness vs. removing detail for conciseness). The proposal must surface these tensions and recommend a resolution rather than pretending every change is purely additive.
2. **Risk** — each change could introduce new problems (broken references, lost context, routing regressions). The proposal must assess what could go wrong for each recommendation.
3. **Batching** — related changes should be grouped into coherent units that can be approved or rejected together, not presented as an unrelated laundry list.

Given the review output and current SKILL.md below, create a proposal document that the tech lead can act on. Do NOT apply any changes to the SKILL.md itself — that file must remain untouched. The proposal must end with an explicit approval request asking the tech lead to confirm before any edits proceed.

## Output Specification

Produce `proposal.md` — a structured change proposal designed for an approval workflow. Requirements:

- **Group related changes** into logical batches (e.g., "Routing & Discovery", "Content Quality") that can be approved or rejected as units.
- **Surface trade-offs** where recommendations conflict or create tension — recommend a resolution but acknowledge the cost.
- **Assess risk** for each recommendation: what could break or regress if the change is applied incorrectly.
- **End with an explicit approval gate**: a clear request for the tech lead to approve, reject, or request changes before any edits are made.
- The SKILL.md must NOT be modified in any way.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: review_output.txt ===============
=== Skill Review: webhook-handler ===
Overall Score: 61%

ERRORS (must fix):
  [ERROR] Description missing "Use when" trigger clause — reduces routing to 0% effectiveness

Dimension Scores:
  Completeness:   1/3  (33%)  - Missing trigger clause
  Actionability:  2/3  (66%)  - Some examples but they show output not commands
  Conciseness:    2/3  (66%)  - Explains HMAC authentication in detail (agent already knows this)
  Robustness:     2/3  (66%)  - No retry or idempotency patterns

Judge Suggestions:
  - Critical: Add "Use when receiving webhook events from external services, validating signatures, or processing event payloads" to description
  - Replace the HMAC explanation paragraph with a code example using the actual verify-sig command
  - Add an idempotency example showing how to use the event ID to prevent duplicate processing
=============== END FILE ===============

=============== FILE: webhook_handler/SKILL.md ===============
---
name: webhook-handler
description: |
  Handles incoming webhook events from external services. Validates signatures, parses payloads, and routes events to appropriate handlers.
---

# Webhook Handler

Process incoming webhooks from external services using our internal webhook framework.

## Signature Validation

Webhooks use HMAC-SHA256 for signature validation. HMAC (Hash-based Message Authentication Code) is a cryptographic technique that uses a shared secret key and a hash function to verify message authenticity. The sender computes an HMAC over the request body using the shared secret, and the receiver recomputes it to verify the signature matches. This prevents tampering and confirms the request came from the expected sender.

To validate:

```python
import hmac
import hashlib

def validate_webhook(body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## Payload Processing

Parse the incoming event:

```bash
webhook-cli process --event-type push --payload @payload.json
```

## Event Routing

Events are routed based on the `event_type` field in the payload. Supported types: `push`, `pull_request`, `release`, `deployment`.
=============== END FILE ===============
