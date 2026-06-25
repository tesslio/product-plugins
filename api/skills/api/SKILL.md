---
name: api
description: >-
  Find and call Tessl API endpoints. Use this WHENEVER you need a Tessl REST API
  endpoint — to discover which endpoint does something, to learn an endpoint's
  path, parameters, request body shape, or response shape, or to actually call
  the Tessl API. Reach for this skill INSTEAD OF reading the raw `openapi.json`
  spec.
---

# Tessl API endpoint discovery

The Tessl OpenAPI spec (`https://api.tessl.io/openapi.json`) is deeply nested
JSON:API schemas with repeated unions and byte-identical error envelopes. Loading
it whole wastes context. This skill's helper script searches the spec and renders
just the endpoint you need, suppressing the noise.

**You never handle API tokens.** Discovery is read-only over the public spec.
Calling an endpoint is done by you via `tessl api <path>`, which the Tessl CLI
authenticates against the current user.

## The helper

```sh
python3 scripts/tessl_api_discover.py <command> [...]
```

Stdlib-only Python 3 — no installs. The spec is fetched once and cached to
`$TMPDIR/tessl-openapi-cache.json` (falling back to `/tmp`) for 5 minutes. Pass
`--refresh` to force a fresh fetch. If the network is down but a cached spec
exists, the script uses it and warns on stderr.

## Workflow

1. **Search by keyword** — the cheap default. Case-insensitive, weighted across
   path, tags, summary, description, parameter names, and (lightly) schema
   property names. Output is `METHOD /path`, summary, and tags — no schemas.

   ```sh
   python3 scripts/tessl_api_discover.py search install policy
   ```

   Results are 20/page; add `--page N`. The footer shows `page X/Y — N matches`.

2. **If keyword search misses, search by property** — matches schema property
   names only (request bodies + responses). Useful when you know a field name
   but not the endpoint.

   ```sh
   python3 scripts/tessl_api_discover.py search --by-property securityLevel
   ```

3. **Show the endpoint** — drill into one endpoint to see its description,
   parameters, request body, and responses. The path is matched loosely, so you
   don't need to reproduce `{templated}` segments exactly; if your path is
   ambiguous the script lists the candidates.

   ```sh
   python3 scripts/tessl_api_discover.py show post /v1/install/policy/evaluate
   ```

   `anyOf` unions are collapsed to one-liners like `anyOf[registry|git|file]`.
   The standard error envelope (404/500/…) is printed once and referenced
   elsewhere. Every `show` ends with a ready-to-run `tessl api` invocation line.

4. **Expand only if the collapsed view isn't enough.** `--expand` fully inlines
   unions and nested schemas; `--status <code>` limits to one response status.

   ```sh
   python3 scripts/tessl_api_discover.py show post /v1/install/policy/evaluate --expand
   python3 scripts/tessl_api_discover.py show get /v1/tiles/{workspaceName}/{tileName} --status 200
   ```

5. **Call it.** Copy the `tessl api …` invocation line printed at the end of
   `show`, fill in the placeholders (path params and any `<value>` / request-body
   fields), and run it. The CLI handles auth.

   ```sh
   tessl api -X POST /v1/install/policy/evaluate --input - <<'JSON'
   {
     "sources": []
   }
   JSON
   ```

## Notes

- The per-endpoint `Authorization` header is suppressed in `show` output — the
  CLI supplies auth, so you never set it.
- Request-body templates include only the **required** fields. Add optional
  fields from the rendered schema as needed.
- For path-templated endpoints the invocation line keeps the `{placeholders}`;
  substitute real values before running.
