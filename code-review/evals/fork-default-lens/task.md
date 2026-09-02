# Fork the scale lens for the payments service

## Problem Description

We run the four default Tessl Code Review lenses. The scale-and-resilience lens
is useful but two things are off for this service. We deploy atomically, so its
rollout and mixed-version concerns never apply and only add noise. And the
concern that actually bites us is idempotency of payment writes under retry:
a charge or refund issued twice because a retry re-ran a non-idempotent step.

Fork the default lens into a local one that drops the rollout dimension and
adds the payment-idempotency dimension. Keep the rest as it is.

## Output Specification

- `review-lenses/review-scale-and-resilience-payments/SKILL.md`: the fork.
- `usage.md`: how to run it locally while iterating, and the exact `lenses`
  input for our caller workflow once adopted, so that the other three defaults
  keep running alongside it. Our workflow currently sets no `lenses` input.
