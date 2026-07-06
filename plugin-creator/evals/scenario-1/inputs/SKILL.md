---
name: database-admin
description: Database administration tasks including schema changes, backups, monitoring, and user access management.
---

# Database Administration

This skill covers everything related to running and maintaining a PostgreSQL database in production.

## Schema Migrations

When the user needs to change the database schema:

1. Connect to the database using `psql $DATABASE_URL`.
2. Check pending migrations: `SELECT * FROM schema_migrations WHERE applied_at IS NULL ORDER BY version;`
3. Review the migration file carefully before applying.
4. Run the migration: `psql $DATABASE_URL -f migrations/<version>_<name>.sql`
5. Confirm the migration applied: `SELECT version, applied_at FROM schema_migrations ORDER BY applied_at DESC LIMIT 5;`
6. If the migration fails, roll back: `psql $DATABASE_URL -f migrations/<version>_<name>_rollback.sql`
7. Update the application's ORM model if a column was added or removed.
8. Notify the engineering channel in Slack: "#db-changes".

### Migration file conventions
- Filename: `<YYYYMMDDHHMMSS>_<short_description>.sql` (e.g. `20240512140000_add_user_preferences.sql`)
- Always include a corresponding `_rollback.sql` file.
- Migrations must be idempotent where possible (`CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`).
- Never drop a column in the same migration that removes it from the application code — do it in a later release.

---

## Database Backups

When the user asks to back up the database or when a backup is needed before a risky operation:

1. Identify the target database: confirm with the user if unclear.
2. Run a full dump: `pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql`
3. Compress: `gzip backup_*.sql`
4. Upload to S3: `aws s3 cp backup_*.sql.gz s3://company-db-backups/postgres/<env>/`
5. Verify the upload: `aws s3 ls s3://company-db-backups/postgres/<env>/ | tail -5`
6. Delete the local copy after confirming upload: `rm backup_*.sql.gz`
7. Log the backup event in the #db-ops Slack channel.

### Restore procedure
1. Download from S3: `aws s3 cp s3://company-db-backups/postgres/<env>/<file>.sql.gz .`
2. Decompress: `gunzip <file>.sql.gz`
3. Restore: `psql $DATABASE_URL < <file>.sql`
4. Run a quick sanity check: `SELECT COUNT(*) FROM users;` (should match pre-backup count).

---

## Database Monitoring

When the user asks about database health, slow queries, or connection issues:

1. Check active connections: `SELECT count(*), state FROM pg_stat_activity GROUP BY state;`
2. Find slow queries (running > 30s): 
   ```sql
   SELECT pid, now() - pg_stat_activity.query_start AS duration, query
   FROM pg_stat_activity
   WHERE state = 'active' AND now() - query_start > interval '30 seconds'
   ORDER BY duration DESC;
   ```
3. Check table bloat:
   ```sql
   SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
   FROM pg_tables
   ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
   LIMIT 20;
   ```
4. Check index usage:
   ```sql
   SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
   FROM pg_stat_user_indexes
   WHERE idx_scan = 0
   ORDER BY relname;
   ```
5. Summarize findings to the user with recommendations (add index, VACUUM, kill query).
6. If any query has been running for > 5 minutes, ask the user before killing it: `SELECT pg_terminate_backend(<pid>);`

### Common fixes
- High connection count → check application connection pooling, consider PgBouncer.
- Table bloat → run `VACUUM ANALYZE <tablename>;`
- Unused indexes → flag for removal in the next maintenance window.

---

## User & Access Management

When the user needs to create, modify, or revoke database access:

1. List current roles: `SELECT rolname, rolsuper, rolcreaterole, rolcreatedb FROM pg_roles ORDER BY rolname;`
2. To create a read-only user:
   ```sql
   CREATE ROLE <username> WITH LOGIN PASSWORD '<password>';
   GRANT CONNECT ON DATABASE <dbname> TO <username>;
   GRANT USAGE ON SCHEMA public TO <username>;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO <username>;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO <username>;
   ```
3. To create a read-write user:
   ```sql
   CREATE ROLE <username> WITH LOGIN PASSWORD '<password>';
   GRANT CONNECT ON DATABASE <dbname> TO <username>;
   GRANT USAGE ON SCHEMA public TO <username>;
   GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO <username>;
   GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO <username>;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO <username>;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO <username>;
   ```
4. To revoke all access:
   ```sql
   REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM <username>;
   REVOKE CONNECT ON DATABASE <dbname> FROM <username>;
   DROP ROLE <username>;
   ```
5. Never share the password in Slack — send it via 1Password or a secure channel.
6. Notify the requester and log the change in the #db-access Slack channel.

### Audit: check who has access
```sql
SELECT grantee, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public'
ORDER BY grantee, table_name;
```

---

## Shared Reference: Environment Variables

All database tasks rely on these environment variables being set:

- `DATABASE_URL` — full connection string, e.g. `postgresql://user:pass@host:5432/dbname`
- `AWS_PROFILE` or `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` — for S3 backup operations
- `SLACK_WEBHOOK_URL` — for posting notifications to Slack channels

If any of these are missing, ask the user to provide them before proceeding.

---

## Shared Reference: Safety Rules

These rules apply to all database operations:

- **Always take a backup before a destructive operation** (DROP TABLE, DELETE without WHERE, major migration).
- **Never run operations on production without confirming the environment** — check `$ENVIRONMENT` variable.
- **Prefer dry-run or preview mode** when available.
- **Document every change** in the relevant Slack channel.
