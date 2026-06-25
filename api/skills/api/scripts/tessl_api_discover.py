#!/usr/bin/env python3
"""Tessl API endpoint discovery — token-efficient search/show over openapi.json.

Stdlib only (Python 3). No pip installs. Invoked as a subprocess by the
`tessl/api` skill so an agent can find the right Tessl API endpoint and its
shape WITHOUT loading the whole spec into context.

Commands:
  search <keywords...>            Weighted keyword search across endpoints.
  search --by-property <name>     Match schema property names only.
  show <METHOD> <path>            Drill into one endpoint (loose path matching).

The spec is fetched from https://api.tessl.io/openapi.json (public, no auth) and
cached for 5 minutes. Calling an endpoint is done by the agent via `tessl api`;
this script never handles tokens.
"""

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request

SPEC_URL = "https://api.tessl.io/openapi.json"
CACHE_NAME = "tessl-openapi-cache.json"
CACHE_TTL = 300  # 5 minutes
PAGE_SIZE = 20
FETCH_TIMEOUT = 20

# Field weights for `search` scoring.
W_PATH = 3.0
W_TAG = 3.0
W_SUMMARY = 2.0
W_DESCRIPTION = 1.0
W_PARAM = 1.0
W_PROPERTY = 0.5


# --------------------------------------------------------------------------- #
# Caching / fetching
# --------------------------------------------------------------------------- #
def cache_path():
    base = os.environ.get("TMPDIR") or "/tmp"
    if not os.path.isdir(base):
        base = "/tmp"
    return os.path.join(base, CACHE_NAME)


def fetch_spec_from_network():
    req = urllib.request.Request(SPEC_URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def write_cache_atomic(path, raw):
    """Write the cache via a temp file + atomic rename (best-effort).

    Writing in place with mode "w" truncates the existing cache before the new
    bytes land; an interruption mid-write would destroy the last known-good spec
    that offline fallback relies on. Staging to a sibling temp file and renaming
    keeps the old cache intact until the replacement is fully written.
    """
    cache_dir = os.path.dirname(path) or "."
    try:
        fd, tmp_path = tempfile.mkstemp(prefix=f"{CACHE_NAME}.", dir=cache_dir)
    except OSError:
        return  # caching is best-effort
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(raw)
        os.replace(tmp_path, path)
    except OSError:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def load_spec(refresh=False):
    """Return the parsed spec, honoring the on-disk cache and TTL.

    Network failure with a stale cache present -> use it and warn on stderr.
    Network failure with no cache -> raise so the caller exits non-zero.
    """
    path = cache_path()
    fresh = False
    if os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        fresh = age < CACHE_TTL

    if not refresh and fresh:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            pass  # corrupt cache -> fall through to a fetch

    try:
        raw = fetch_spec_from_network()
        spec = json.loads(raw)
        write_cache_atomic(path, raw)
        return spec
    except (urllib.error.URLError, OSError, ValueError) as err:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    spec = json.load(fh)
                sys.stderr.write(
                    f"warning: could not fetch spec ({err}); using stale cache at {path}\n"
                )
                return spec
            except (OSError, ValueError):
                pass
        raise RuntimeError(
            f"could not fetch {SPEC_URL} ({err}) and no usable cache at {path}"
        )


# --------------------------------------------------------------------------- #
# Spec traversal helpers
# --------------------------------------------------------------------------- #
HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


def iter_operations(spec):
    """Yield (path, method, operation) for every endpoint in the spec."""
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method.lower() in HTTP_METHODS and isinstance(op, dict):
                yield path, method.lower(), op


def collect_property_names(schema, acc):
    """Recursively gather every object-property name reachable from a schema."""
    if isinstance(schema, dict):
        props = schema.get("properties")
        if isinstance(props, dict):
            for name, sub in props.items():
                acc.add(name)
                collect_property_names(sub, acc)
        for key in ("items", "not"):
            if key in schema:
                collect_property_names(schema[key], acc)
        for key in ("anyOf", "oneOf", "allOf"):
            for sub in schema.get(key, []) or []:
                collect_property_names(sub, acc)
        ap = schema.get("additionalProperties")
        if isinstance(ap, dict):
            collect_property_names(ap, acc)
    elif isinstance(schema, list):
        for sub in schema:
            collect_property_names(sub, acc)


def request_schema(op):
    body = op.get("requestBody")
    if not isinstance(body, dict):
        return None
    content = body.get("content") or {}
    for media in content.values():
        if isinstance(media, dict) and "schema" in media:
            return media["schema"]
    return None


def response_schemas(op):
    """Return {status_code: schema} for declared responses that carry JSON."""
    out = {}
    for code, resp in (op.get("responses") or {}).items():
        if not isinstance(resp, dict):
            continue
        content = resp.get("content") or {}
        schema = None
        for media in content.values():
            if isinstance(media, dict) and "schema" in media:
                schema = media["schema"]
                break
        out[str(code)] = schema
    return out


def visible_parameters(op):
    """Parameters minus the per-endpoint Authorization header (CLI owns auth)."""
    out = []
    for prm in op.get("parameters", []) or []:
        if not isinstance(prm, dict):
            continue
        if prm.get("in") == "header" and (prm.get("name") or "").lower() == "authorization":
            continue
        out.append(prm)
    return out


def endpoint_property_names(op):
    acc = set()
    rs = request_schema(op)
    if rs is not None:
        collect_property_names(rs, acc)
    for schema in response_schemas(op).values():
        if schema is not None:
            collect_property_names(schema, acc)
    return acc


# --------------------------------------------------------------------------- #
# Search
# --------------------------------------------------------------------------- #
def build_index(spec):
    """Precompute per-endpoint searchable text fields."""
    index = []
    for path, method, op in iter_operations(spec):
        params = visible_parameters(op)
        index.append(
            {
                "path": path,
                "method": method,
                "summary": op.get("summary", "") or "",
                "tags": op.get("tags", []) or [],
                "fields": {
                    "path": path.lower(),
                    "tag": " ".join(op.get("tags", []) or []).lower(),
                    "summary": (op.get("summary", "") or "").lower(),
                    "description": (op.get("description", "") or "").lower(),
                    "param": " ".join(p.get("name", "") for p in params).lower(),
                    "property": " ".join(sorted(endpoint_property_names(op))).lower(),
                },
            }
        )
    return index


FIELD_WEIGHTS = {
    "path": W_PATH,
    "tag": W_TAG,
    "summary": W_SUMMARY,
    "description": W_DESCRIPTION,
    "param": W_PARAM,
    "property": W_PROPERTY,
}


def score_entry(entry, terms, fields):
    """Return (terms_matched, weighted_score) for one endpoint."""
    matched_terms = 0
    score = 0.0
    for term in terms:
        term_hit = False
        for field in fields:
            text = entry["fields"].get(field, "")
            if term in text:
                score += FIELD_WEIGHTS[field]
                term_hit = True
        if term_hit:
            matched_terms += 1
    return matched_terms, score


def cmd_search(spec, terms, by_property, page):
    terms = [t.lower() for t in terms if t.strip()]
    if not terms:
        sys.stderr.write("error: search needs at least one keyword\n")
        return 2

    fields = ["property"] if by_property else list(FIELD_WEIGHTS.keys())
    index = build_index(spec)

    scored = []
    for entry in index:
        matched, score = score_entry(entry, terms, fields)
        if matched > 0:
            scored.append((matched, score, entry))

    # More-terms-matched ranks above single-term; then by weighted score; then
    # a stable path/method tiebreak for deterministic output.
    scored.sort(key=lambda x: (-x[0], -x[1], x[2]["path"], x[2]["method"]))

    total = len(scored)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, pages))
    start = (page - 1) * PAGE_SIZE
    window = scored[start : start + PAGE_SIZE]

    if total == 0:
        kind = "property" if by_property else "keyword"
        print(f"No endpoints matched the {kind} search: {' '.join(terms)}")
        if not by_property:
            print("Tip: try `search --by-property <fieldName>` to match schema property names.")
        return 0

    for _matched, _score, entry in window:
        print(f"{entry['method'].upper()} {entry['path']}")
        if entry["summary"]:
            print(f"  {entry['summary']}")
        if entry["tags"]:
            print(f"  tags: {', '.join(entry['tags'])}")
        print()

    print(f"page {page}/{pages} — {total} matches")
    return 0


# --------------------------------------------------------------------------- #
# Show: loose path resolution
# --------------------------------------------------------------------------- #
def is_template_seg(seg):
    return seg.startswith("{") and seg.endswith("}")


def segments(path):
    return [s for s in path.strip("/").split("/") if s != ""]


def seg_match(spec_path, user_path):
    sp = segments(spec_path)
    up = segments(user_path)
    if len(sp) != len(up):
        return False
    for s, u in zip(sp, up):
        if is_template_seg(s) or is_template_seg(u):
            continue  # template segment on either side is a wildcard
        if s.lower() != u.lower():
            return False
    return True


def resolve_endpoint(spec, method, user_path):
    """Resolve a loose (possibly partial/templated) path to one (path, method, op).

    Returns ('ok', path, op) | ('ambiguous', candidates) | ('none', None).
    """
    method = method.lower()
    ops = list(iter_operations(spec))

    # 0. Exact path match wins outright — a literal path the agent typed in full
    #    should never be reported ambiguous against a templated sibling.
    norm = "/" + "/".join(segments(user_path))
    exact = [(p, m, op) for p, m, op in ops if m == method and "/" + "/".join(segments(p)) == norm]
    if len(exact) == 1:
        return "ok", exact[0][0], exact[0][2]

    # 1. Segment-wise match honoring template wildcards on either side.
    cands = [(p, m, op) for p, m, op in ops if m == method and seg_match(p, user_path)]
    if len(cands) == 1:
        return "ok", cands[0][0], cands[0][2]
    if len(cands) > 1:
        return "ambiguous", [(p, m) for p, m, _ in cands]

    # 2. Substring fallback (agent supplied a fragment of the real path).
    needle = user_path.strip("/").lower()
    cands = [(p, m, op) for p, m, op in ops if m == method and needle in p.lower()]
    if len(cands) == 1:
        return "ok", cands[0][0], cands[0][2]
    if len(cands) > 1:
        return "ambiguous", [(p, m) for p, m, _ in cands]

    return "none", None


# --------------------------------------------------------------------------- #
# Show: schema rendering
# --------------------------------------------------------------------------- #
ERROR_ENVELOPE_KEY = "__error_envelope__"


def is_error_envelope(schema):
    """Match the standard JSON:API error shape {error:{title,status,message}}."""
    if not isinstance(schema, dict):
        return False
    props = schema.get("properties") or {}
    err = props.get("error")
    if not isinstance(err, dict):
        return False
    eprops = err.get("properties") or {}
    return {"title", "status", "message"}.issubset(set(eprops.keys()))


def discriminator_label(schema):
    """For an object branch in a union, pick a short label.

    Prefer a single-value enum on a discriminator-ish property (source/type/kind),
    else any single-value enum property, else the bare type.
    """
    if not isinstance(schema, dict):
        return "object"
    props = schema.get("properties") or {}
    candidates = []
    for name, sub in props.items():
        if isinstance(sub, dict):
            enum = sub.get("enum")
            if isinstance(enum, list) and len(enum) == 1:
                candidates.append((name, str(enum[0])))
    for preferred in ("source", "type", "kind"):
        for name, val in candidates:
            if name == preferred:
                return val
    if candidates:
        return candidates[0][1]
    return schema.get("type", "object") if isinstance(schema.get("type"), str) else "object"


def union_branch_label(schema):
    if not isinstance(schema, dict):
        return "object"
    if schema.get("type") == "null":
        return "null"
    enum = schema.get("enum")
    if isinstance(enum, list) and len(enum) == 1:
        return str(enum[0])
    t = schema.get("type")
    if t == "object" or "properties" in schema:
        return discriminator_label(schema)
    if t == "array":
        return "array"
    if isinstance(t, str):
        return t
    return "object"


def type_label(schema):
    """A compact inline type label for a schema (collapsed view)."""
    if not isinstance(schema, dict):
        return "any"

    for key in ("anyOf", "oneOf"):
        if key in schema:
            labels = []
            for branch in schema[key]:
                lbl = union_branch_label(branch)
                if lbl not in labels:
                    labels.append(lbl)
            return f"anyOf[{'|'.join(labels)}]"

    if "allOf" in schema:
        return "object"

    enum = schema.get("enum")
    if isinstance(enum, list):
        if len(enum) == 1:
            return f"enum({enum[0]})"
        return f"enum({'|'.join(str(e) for e in enum)})"

    t = schema.get("type")
    if t == "array":
        items = schema.get("items") or {}
        return f"array<{type_label(items)}>"
    if isinstance(t, list):
        return "|".join(t)
    if isinstance(t, str):
        fmt = schema.get("format")
        return f"{t}({fmt})" if fmt else t
    if "properties" in schema:
        return "object"
    return "any"


def has_children(schema):
    if not isinstance(schema, dict):
        return False
    if isinstance(schema.get("properties"), dict) and schema["properties"]:
        return True
    if schema.get("type") == "array":
        return has_children(schema.get("items") or {})
    return False


def is_union(schema):
    return isinstance(schema, dict) and ("anyOf" in schema or "oneOf" in schema)


def should_recurse(schema, expand):
    """Whether render_schema should descend into a property's sub-schema."""
    if has_children(schema):
        return True
    if not expand:
        return False
    if is_union(schema):
        return True
    if isinstance(schema, dict) and schema.get("type") == "array":
        return is_union(schema.get("items") or {})
    return False


def render_schema(schema, indent, expand, lines):
    """Render a schema as an indented field skeleton.

    Collapsed (default): anyOf unions become one-line labels; nested objects are
    expanded as `name: type [required]` trees. Expanded: unions are inlined.
    """
    pad = "  " * indent
    if not isinstance(schema, dict):
        lines.append(f"{pad}any")
        return

    # Unions
    for key in ("anyOf", "oneOf"):
        if key in schema:
            if not expand:
                lines.append(f"{pad}{type_label(schema)}")
                return
            lines.append(f"{pad}{key}:")
            for i, branch in enumerate(schema[key]):
                lines.append(f"{pad}  - [{union_branch_label(branch)}]")
                render_schema(branch, indent + 2, expand, lines)
            return

    t = schema.get("type")

    if t == "array" or (t is None and "items" in schema):
        items = schema.get("items") or {}
        if has_children(items) or (expand and is_union(items)):
            lines.append(f"{pad}array of:")
            render_schema(items, indent + 1, expand, lines)
        else:
            lines.append(f"{pad}array<{type_label(items)}>")
        return

    props = schema.get("properties")
    if isinstance(props, dict) and props:
        required = set(schema.get("required", []) or [])
        for name, sub in props.items():
            req = "  [required]" if name in required else ""
            label = type_label(sub)
            lines.append(f"{pad}{name}: {label}{req}")
            if should_recurse(sub, expand):
                render_schema(sub, indent + 1, expand, lines)
        return

    # Scalar / leaf
    lines.append(f"{pad}{type_label(schema)}")


# --------------------------------------------------------------------------- #
# Show: request body template + invocation line
# --------------------------------------------------------------------------- #
def sample_for_schema(schema, depth=0):
    """Build a minimal placeholder value covering only required fields."""
    if not isinstance(schema, dict) or depth > 6:
        return None

    for key in ("anyOf", "oneOf"):
        if key in schema:
            # Pick the first non-null branch as the template.
            for branch in schema[key]:
                if isinstance(branch, dict) and branch.get("type") != "null":
                    return sample_for_schema(branch, depth + 1)
            return None

    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        return enum[0]

    t = schema.get("type")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), t[0]) if t else None

    if t == "object" or "properties" in schema:
        props = schema.get("properties") or {}
        required = schema.get("required", []) or []
        obj = {}
        for name in required:
            obj[name] = sample_for_schema(props.get(name, {}), depth + 1)
        return obj
    if t == "array":
        return []
    if t == "string":
        fmt = schema.get("format")
        return f"<{fmt}>" if fmt else "<string>"
    if t in ("integer", "number"):
        return 0
    if t == "boolean":
        return False
    if t == "null":
        return None
    return None


def invocation_line(path, method, op):
    """Build a ready-to-run `tessl api` command for this endpoint."""
    method = method.upper()
    params = visible_parameters(op)
    required_query = [p for p in params if p.get("in") == "query" and p.get("required")]

    parts = ["tessl api"]
    if method != "GET":
        parts.append(f"-X {method}")
    parts.append(path)  # path templates are left as {placeholders}
    for q in required_query:
        parts.append(f"-F {q.get('name')}=<value>")

    line = " ".join(parts)

    rs = request_schema(op)
    if rs is not None and method != "GET":
        body = sample_for_schema(rs)
        if body in (None, {}, []):
            body = {}
        body_json = json.dumps(body, indent=2)
        return (
            f"{line} --input - <<'JSON'\n{body_json}\nJSON"
        )
    return line


# --------------------------------------------------------------------------- #
# Show command
# --------------------------------------------------------------------------- #
ERROR_REFERENCE = "standard error envelope"


def print_error_envelope_once(state):
    if state["printed"]:
        return
    state["printed"] = True
    print("Standard error envelope (shared by all error statuses):")
    print("  error: object  [required]")
    print("    title: string  [required]")
    print("    status: number  [required]")
    print("    message: string  [required]")
    print()


def cmd_show(spec, method, path, expand, status):
    status_kind, resolved, op_or_cands = (None, None, None)
    result = resolve_endpoint(spec, method, path)
    kind = result[0]
    if kind == "ambiguous":
        sys.stderr.write(
            f"Ambiguous path '{method.upper()} {path}' — candidates:\n"
        )
        for p, m in result[1]:
            sys.stderr.write(f"  {m.upper()} {p}\n")
        sys.stderr.write("Re-run `show` with a more specific path.\n")
        return 2
    if kind == "none":
        sys.stderr.write(
            f"No endpoint matched '{method.upper()} {path}'. "
            f"Try `search` to find the right path.\n"
        )
        return 2

    resolved_path, op = result[1], result[2]

    print(f"{method.upper()} {resolved_path}")
    if op.get("summary"):
        print(op["summary"])
    if op.get("tags"):
        print(f"tags: {', '.join(op['tags'])}")
    if op.get("description"):
        print()
        print(op["description"])
    print()

    # Parameters
    params = visible_parameters(op)
    if params:
        print("Parameters:")
        for p in params:
            ptype = type_label(p.get("schema", {})) if p.get("schema") else "string"
            req = "required" if p.get("required") else "optional"
            print(f"  {p.get('name')} ({p.get('in')}, {ptype}, {req})")
        print()

    # Request body
    rs = request_schema(op)
    if rs is not None:
        print("Request body:")
        lines = []
        render_schema(rs, 1, expand, lines)
        print("\n".join(lines))
        print()

    # Responses
    err_state = {"printed": False}
    responses = response_schemas(op)

    codes = sorted(responses.keys())
    if status is not None:
        codes = [c for c in codes if c == str(status)]
        if not codes:
            sys.stderr.write(
                f"status {status} is not declared on {method.upper()} {resolved_path}\n"
            )
            return 2
    else:
        # Default: show 2xx responses in full plus the error envelope once.
        success = [c for c in codes if c.startswith("2")]
        errors = [c for c in codes if not c.startswith("2")]
        codes = success + errors

    print("Responses:")
    for code in codes:
        schema = responses.get(code)
        if schema is not None and is_error_envelope(schema):
            if status is not None:
                # Explicitly requested a single error status: show it in full.
                print(f"  {code}:")
                print_error_envelope_once(err_state)
            else:
                if not err_state["printed"]:
                    print(f"  {code}: see standard error envelope below")
                    print_error_envelope_once(err_state)
                else:
                    print(f"  {code}: {ERROR_REFERENCE}")
            continue
        print(f"  {code}:")
        if schema is None:
            print("    (no JSON body)")
        else:
            lines = []
            render_schema(schema, 2, expand, lines)
            print("\n".join(lines))
    print()

    # Ready-to-run invocation line
    print("Call it with:")
    print(invocation_line(resolved_path, method, op))
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tessl_api_discover.py",
        description="Token-efficient search/show over the Tessl OpenAPI spec.",
    )
    parser.add_argument("--refresh", action="store_true", help="Force a fresh spec fetch.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Weighted keyword search across endpoints.")
    p_search.add_argument("keywords", nargs="*", help="Search keywords.")
    p_search.add_argument(
        "--by-property",
        action="store_true",
        help="Match schema property names only (request + response bodies).",
    )
    p_search.add_argument("--page", type=int, default=1, help="Result page (20/page).")

    p_show = sub.add_parser("show", help="Drill into one endpoint.")
    p_show.add_argument("method", help="HTTP method, e.g. GET / POST.")
    p_show.add_argument("path", help="Endpoint path (loose/partial/templated OK).")
    p_show.add_argument(
        "--expand", action="store_true", help="Fully inline unions and nested schemas."
    )
    p_show.add_argument("--status", help="Limit responses to a single status code.")

    args = parser.parse_args(argv)

    try:
        spec = load_spec(refresh=args.refresh)
    except RuntimeError as err:
        sys.stderr.write(f"error: {err}\n")
        return 1

    if args.command == "search":
        return cmd_search(spec, args.keywords, args.by_property, args.page)
    if args.command == "show":
        return cmd_show(spec, args.method, args.path, args.expand, args.status)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
