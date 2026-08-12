# Make our code review catch the thing we keep catching by hand

## Problem Description

We run Tessl Code Review on the payments service with the four default lenses. It is useful, but the same class of comment keeps coming from human reviewers instead, and it is the class that costs us most when it slips through: changes that behave correctly but cannot be diagnosed once they are running.

`pr-feedback.md` collects the review comments from last quarter. Not everything in there is the concern we mean.

We do not run this lens yet. It will be a fifth lens alongside the four defaults, and we are not turning it on until we have reason to trust it.

## Output Specification

Produce two things in the workspace:

- `review-lenses/review-observability/SKILL.md`, the lens itself, ready to run as a reviewer skill.
- `validation-plan.md`, saying how we should check it before we adopt it.
