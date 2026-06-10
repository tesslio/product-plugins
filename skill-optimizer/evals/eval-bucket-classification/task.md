# Payments Plugin Eval Analysis

## Problem Description

Your team has been running evals on your `payments-gateway` plugin for three months. A senior engineer is planning the next round of plugin improvements and wants a clear picture of where the plugin is actually earning its weight versus where it's redundant or causing problems.

Specifically, they want to know:
- Which criteria is the plugin genuinely helping with (agents perform much better with it than without)?
- Which criteria are agents already handling on their own, even without the plugin?
- Which criteria should be top priorities because agents are doing *worse* with the plugin than without it?
- For anything problematic: what's a plausible explanation and where in the plugin should someone look?

The engineer doesn't want raw scores — they want an actionable breakdown that tells them exactly what to do next.

## Output Specification

Produce a file called `analysis_report.md` that:
1. Categorizes each criterion into a status group with a short label
2. For each criterion, shows its scores (baseline and with-plugin) and the percentage of max it achieves
3. For criteria that need action, includes a short diagnosis (1-2 sentences on what's likely missing or wrong) and which file in the plugin to look at
4. Ends with a prioritized list of recommended next steps

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/eval_results.json ===============
{
  "plugin": "payments-gateway",
  "eval_id": "eval_2026_03_15_payments",
  "scenarios": [
    {
      "name": "checkout-flow",
      "criteria": [
        {
          "name": "Stripe idempotency key",
          "description": "Uses idempotency key in Stripe charge requests to prevent duplicate charges",
          "max_score": 15,
          "baseline_score": 2,
          "with_context_score": 13
        },
        {
          "name": "Webhook signature validation",
          "description": "Validates Stripe webhook signatures using the signing secret before processing events",
          "max_score": 10,
          "baseline_score": 1,
          "with_context_score": 5
        },
        {
          "name": "HTTP status code handling",
          "description": "Returns appropriate HTTP status codes (200, 400, 422, 500) in API responses",
          "max_score": 10,
          "baseline_score": 9,
          "with_context_score": 10
        },
        {
          "name": "Currency precision",
          "description": "Represents all currency values as integer cents rather than floating point dollars",
          "max_score": 15,
          "baseline_score": 3,
          "with_context_score": 7
        },
        {
          "name": "API version pinning",
          "description": "Pins the Stripe API version string (e.g. '2023-10-16') in all API requests",
          "max_score": 10,
          "baseline_score": 6,
          "with_context_score": 4
        }
      ]
    }
  ]
}
