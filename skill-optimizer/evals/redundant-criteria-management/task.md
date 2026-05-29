# API Integration Tile: Eval Rubric Review

## Problem Description

Your API integration tile has been running evals for two months, and the overall scores look great — agents consistently score above 90%. But a team member raised a concern: "Are we actually measuring anything useful? Some of these criteria might just be testing general REST knowledge that any competent agent would implement correctly, not the specific guidance our tile provides."

You've pulled the latest eval results and noticed that several criteria have near-perfect scores even in the *baseline* condition (when agents work without any tile context). This raises the question of whether those criteria are earning their place in the rubric.

Your job is to review these results, make recommendations about each potentially-redundant criterion, and update the eval rubric accordingly — documenting your reasoning. There is at least one criterion that is clearly still adding value and should not be touched.

## Output Specification

Produce a file called `rubric_review.md` that:
1. Lists each criterion you've reviewed with its baseline and with-tile scores
2. For each criterion that agents handle well without the tile, presents at least two options for what to do about it (with a brief note on the trade-offs of each)
3. Documents your final decision for each criterion and your reasoning

Update `inputs/criteria.json` to reflect your decisions. If you remove any criteria, ensure the weights of the remaining criteria are redistributed so they still sum to 100. Save your updated file.

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/eval_results.json ===============
{
  "tile": "rest-api-integration",
  "eval_id": "eval_2026_02_28_api",
  "scenarios": [
    {
      "name": "third-party-api-setup",
      "criteria": [
        {
          "name": "JSON response format",
          "description": "API responses use JSON with Content-Type: application/json header",
          "max_score": 15,
          "baseline_score": 14,
          "with_context_score": 15
        },
        {
          "name": "HTTP headers included",
          "description": "Requests include standard HTTP headers (Authorization, Content-Type, Accept)",
          "max_score": 15,
          "baseline_score": 15,
          "with_context_score": 15
        },
        {
          "name": "4xx error handling",
          "description": "Client errors (4xx) are handled separately from server errors (5xx)",
          "max_score": 10,
          "baseline_score": 9,
          "with_context_score": 10
        },
        {
          "name": "Custom Retry-After header",
          "description": "On 429 rate-limit responses, reads the Retry-After header value and waits exactly that many seconds before retrying",
          "max_score": 30,
          "baseline_score": 3,
          "with_context_score": 24
        },
        {
          "name": "Idempotency key rotation",
          "description": "Generates a fresh idempotency key for each new request attempt, but reuses the same key for retries of the same operation",
          "max_score": 30,
          "baseline_score": 5,
          "with_context_score": 25
        }
      ]
    }
  ]
}

=============== FILE: inputs/criteria.json ===============
{
  "context": "Tests whether the agent correctly implements the API integration tile when setting up a connection to a third-party REST API",
  "type": "weighted_checklist",
  "checklist": [
    {
      "name": "JSON response format",
      "description": "API responses use JSON with Content-Type: application/json header",
      "max_score": 15
    },
    {
      "name": "HTTP headers included",
      "description": "Requests include standard HTTP headers (Authorization, Content-Type, Accept)",
      "max_score": 15
    },
    {
      "name": "4xx error handling",
      "description": "Client errors (4xx) are handled separately from server errors (5xx)",
      "max_score": 10
    },
    {
      "name": "Custom Retry-After header",
      "description": "On 429 rate-limit responses, reads the Retry-After header value and waits exactly that many seconds before retrying",
      "max_score": 30
    },
    {
      "name": "Idempotency key rotation",
      "description": "Generates a fresh idempotency key for each new request attempt, but reuses the same key for retries of the same operation",
      "max_score": 30
    }
  ]
}
