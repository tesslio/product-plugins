---
name: review-per-row-calls
description: Reviews changes that issue one database or service call per element of a collection where a single batched or joined call would do, in code paths whose collection size grows with production data.
---

# Per-row calls

## Scope

Loops, comprehensions, and mapped async work that issue a database query, a
cache lookup, or an outbound request once per element.

## Method

For each such loop in the change, establish where the collection comes from and
what bounds its size. A collection read from a table, an API page, or a request
body is bounded by production data rather than by the code. Then establish
whether the per-element call has a batched form: an `IN` query, a join, a
multi-get, or a bulk endpoint.

## Threshold

Report when the collection is bounded by production data and a batched form
exists, so the call count grows with rows and the work can be done in one call.

Do not report a loop over a collection the code itself bounds to a handful of
elements, a call that is already batched, or a call the provider offers no
batched form for.

## Reporting

Name the loop, what bounds the collection, and the batched form that replaces it.
