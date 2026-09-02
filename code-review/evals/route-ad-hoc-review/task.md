# Review this diff for security issues

## Problem Description

Before I open a pull request, look at `change.diff` for security problems. The
service is a multi-tenant API; `workspaceId` scopes every read.

## Output Specification

- `review.md`: your review, findings first, each with the line it concerns and
  why it matters. Then, in a closing section, how I would run the same review
  as a proper Tessl Code Review from the command line, with the exact command.
