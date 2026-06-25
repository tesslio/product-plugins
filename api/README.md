# api

Find and call Tessl API endpoints token-efficiently, without loading the whole `openapi.json` spec into context.

## Install

```bash
tessl install tessl/api
```

## What it does

The Tessl OpenAPI spec is deeply nested JSON:API schemas with repeated unions and byte-identical error envelopes — loading it whole wastes context. This plugin's helper script searches the spec and renders just the endpoint you need, suppressing the noise.

Fires whenever an agent needs a Tessl REST API endpoint — to discover which endpoint does something, learn its path, parameters, request-body, or response shape, or actually call it via `tessl api`. Reach for it instead of reading the raw `openapi.json`.

- **Search by keyword** — weighted, case-insensitive search across path, tags, summary, description, and parameter names.
- **Search by property** — match schema property names only, when you know a field but not the endpoint.
- **Show an endpoint** — drill into one endpoint's description, parameters, request body, and responses, with `anyOf` unions collapsed and a ready-to-run `tessl api` invocation line.
- **Call it** — the Tessl CLI handles auth; you never set tokens.

The helper is stdlib-only Python 3 (no installs) and caches the fetched spec for 5 minutes.

## Skills

| Skill | Description |
|-------|-------------|
| `api` | Search and render single Tessl API endpoints from the OpenAPI spec, then call them via `tessl api` |
