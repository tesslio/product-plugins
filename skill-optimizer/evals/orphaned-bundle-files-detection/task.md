# Bundle File Audit

## Problem Description

A developer has a skill plugin that's grown over time. They've noticed the plugin size is larger than expected and suspect there might be files in the bundle that are no longer referenced. They want to audit their skill bundle to identify any orphaned files that could be removed to reduce bloat, or should be linked if they contain valuable content.

Your job is to analyze the skill bundle below, identify which files are referenced vs orphaned, and provide recommendations for each orphaned file.

## Output Specification

Produce a file `bundle_audit.md` containing:
- A "Bundle Contents" section listing all files in the bundle
- A "Referenced Files" section listing files that are linked from SKILL.md
- An "Orphaned Files" section listing files that exist but are never referenced
- A "Recommendations" section with specific suggestions for each orphaned file (link with routing signals OR remove with justification)

## Input Files

The following files represent the skill bundle. Extract them before beginning.

=============== FILE: database_helper/SKILL.md ===============
---
name: database-helper
description: |
  Helps with database operations including migrations, queries, and connection pooling. Use when working with databases, running migrations, writing SQL queries, or managing database connections.
---

# Database Helper

Simplify database operations with migration management, query building, and connection pooling.

## Quick Start

```python
from db_helper import Database

db = Database(url="postgresql://localhost/mydb")
result = db.query("SELECT * FROM users WHERE active = true")
```

## Migrations

See [MIGRATIONS.md](MIGRATIONS.md) for creating, running, and rolling back database migrations.

## Connection Pooling

Connection pooling is enabled by default with sensible defaults. See [POOLING.md](POOLING.md) for pool sizing, timeout configuration, and connection lifecycle management.

## Query Building

Use the query builder for complex queries:

```python
query = db.select("users").where("active", True).order_by("created_at")
results = query.execute()
```

## Notes

- Always use parameterized queries to prevent SQL injection
- Connection pool defaults to 10 connections
=============== END FILE ===============

=============== FILE: database_helper/MIGRATIONS.md ===============
# Migrations Guide

How to create and run database migrations.

## Creating Migrations

```bash
db-helper migrate create add_users_table
```

## Running Migrations

```bash
db-helper migrate up
```
=============== END FILE ===============

=============== FILE: database_helper/POOLING.md ===============
# Connection Pooling

Configuration options for the connection pool.

- `pool_size`: Maximum number of connections (default: 10)
- `pool_timeout`: Timeout in seconds (default: 30)
- `pool_recycle`: Recycle connections after N seconds (default: 3600)
=============== END FILE ===============

=============== FILE: database_helper/TRANSACTIONS.md ===============
# Transaction Management

How to use transactions for atomic operations.

## Basic Transactions

```python
with db.transaction():
    db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
```

## Nested Transactions

Use savepoints for nested transactions:

```python
with db.transaction():
    db.execute("INSERT INTO orders ...")
    with db.savepoint():
        db.execute("INSERT INTO order_items ...")
```
=============== END FILE ===============

=============== FILE: database_helper/PERFORMANCE.md ===============
# Performance Tips

Optimization strategies for database operations.

## Indexes

Create indexes on frequently queried columns:

```sql
CREATE INDEX idx_users_email ON users(email);
```

## Batch Operations

Use batch inserts for bulk data:

```python
db.batch_insert("users", [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
])
```
=============== END FILE ===============

=============== FILE: database_helper/SECURITY.md ===============
# Security Best Practices

Database security guidelines.

- Always use parameterized queries
- Never store passwords in plaintext
- Use SSL/TLS for connections in production
- Rotate credentials regularly
- Apply principle of least privilege
=============== END FILE ===============

=============== FILE: database_helper/LEGACY_EXAMPLES.md ===============
# Legacy Examples

Old examples from version 1.x (deprecated).

These examples use the old API and should not be used. Kept for reference during migration.

```python
# OLD API - DO NOT USE
db = DBConnection(host="localhost", port=5432)
db.connect()
db.raw_query("SELECT * FROM users")
db.disconnect()
```
=============== END FILE ===============

=============== FILE: database_helper/DRAFT_REPLICATION.md ===============
# Replication Setup (Draft)

THIS IS A WORK IN PROGRESS - NOT YET IMPLEMENTED

Notes on future replication feature:
- Master-slave replication
- Read replicas
- Automatic failover

TODO: Finish implementation before documenting.
=============== END FILE ===============
