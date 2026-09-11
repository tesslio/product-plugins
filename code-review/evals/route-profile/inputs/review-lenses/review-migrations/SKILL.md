---
name: review-migrations
description: Reviews schema migrations for changes that lock a live table, drop data, or leave the running application unable to read the schema it is deployed against.
---

# Migration safety

## Scope

Schema migrations, and the application code that reads the columns they change.

## Method

For each migration in the change, work out what it does to a table that is
already serving traffic: whether it takes a lock that blocks reads or writes,
whether it removes or rewrites data that is not recoverable, and whether the
currently deployed application can still read the schema between the migration
landing and the next deploy.

## Threshold

Report when the migration can block traffic on a table in production, lose data
that is not reconstructible, or leave the deployed application reading a column
that no longer exists.

Do not report a migration that only adds a nullable column, creates a table, or
runs an index build concurrently.

## Reporting

Name the table, the operation, and what production sees while it runs.
