#!/usr/bin/env bash
# hooks/skill-guard.sh
#
# Cross-agent skill guard, written against the Tessl generic hook event schema
# (SCHEMA_VERSION 1). Declared in ../.tessl-plugin/plugin.json under `hooks`:
#
#   PreToolUse (no matcher)   → block non-tessl skill loading + tessl.json writes
#   UserPromptSubmit          → soft steer away from non-tessl skills
#
# The PreToolUse group declares no `matcher`: tool names are passed through
# verbatim and differ per agent (Claude `Read` vs Cursor `read_file`), so a
# single matcher string can't be correct for every agent. The group fires for
# every tool call and this script filters on `tool_name` below.
#
# The Tessl dispatcher (`tessl hook run`) translates each agent's native event
# into this normalized schema on stdin and translates our stdout back to the
# agent's native format. So there is ONE script and ONE payload shape here —
# no per-runtime detection, no per-runtime output formats.
#
# DEPENDENCY-FREE: this script parses the incoming JSON and builds its outgoing
# JSON in pure bash — no jq, no python, no node. It runs unchanged in enterprise
# environments that ship nothing beyond bash and POSIX utilities. `grep`, `sed`,
# `basename`, and bash builtins are the only external tools used.
#
# INPUT (stdin, generic schema)
#   PreToolUse:       { hook_event_name, cwd, tool_name, tool_input, ... }
#   UserPromptSubmit: { hook_event_name, cwd, prompt, attachments?, ... }
#
# OUTPUT (stdout, generic schema) + exit code
#   Block a tool:   {"decision":"block","permissionDecision":"deny", reason...}  exit 2
#   Steer a prompt: {"additionalContext":"..."}                                  exit 0
#   Allow:          (no output)                                                  exit 0
#
#   Exit 2 is the documented block signal; on PreToolUse the dispatcher turns
#   our deny into the agent's native permission-deny. On UserPromptSubmit the
#   generic pipeline can only inject `additionalContext` (it does not carry a
#   prompt-level block), so prompt detection is a best-effort steer and the
#   hard enforcement lives at PreToolUse (the Skill tool on Claude, and Read of
#   a file under a skill dir on either agent).
#
# SKILL POLICY
#   Allowed:  tessl__<name> whose base name is listed in tessl.json OR whose
#             directory exists under ${CWD}/.agents/skills/tessl__<name>
#   Allowed:  built-in commands (not present in any user skill directory)
#   Blocked:  any skill found in a user skill directory that isn't tessl-managed
#
# tessl.json WRITE POLICY
#   Blocked:  any file-write or shell command that writes tessl.json (reads are
#             allowed). tessl.json is the skill allow-list, so it must only be
#             changed by the tessl CLI — otherwise the skill block is trivially
#             bypassed by adding the skill to tessl.json.

set -uo pipefail

INPUT=$(cat)

# ── Pure-bash JSON parsing ────────────────────────────────────────────────────
#
# The dispatcher hands us compact JSON (JSON.stringify), so a JSON string value
# is `"key":"…"` with standard backslash escapes. These helpers extract and
# unescape those values without jq. The full JSON grammar is not implemented —
# only what the generic hook schema actually sends: top-level string fields,
# string fields nested one level inside `tool_input`, and the `attachments[]`
# array of `{ file_path }` objects.

# Reverse JSON string escaping on an already-extracted value. Handles the
# escapes JSON.stringify emits for paths and reason text (\" \\ \/ \n \t \r
# \b \f). A \uXXXX escape is left as-is — it does not appear in the paths or
# tool names this guard inspects.
json_unescape() {
  local s="$1"
  local out="" n=${#s} i=0 c nxt
  while ((i < n)); do
    c="${s:i:1}"
    if [[ "$c" == "\\" ]] && ((i + 1 < n)); then
      nxt="${s:i+1:1}"
      case "$nxt" in
      '"') out+='"' ;;
      '\') out+='\' ;;
      '/') out+='/' ;;
      n) out+=$'\n' ;;
      t) out+=$'\t' ;;
      r) out+=$'\r' ;;
      b) out+=$'\b' ;;
      f) out+=$'\f' ;;
      *) out+="$nxt" ;;
      esac
      i=$((i + 2))
    else
      out+="$c"
      i=$((i + 1))
    fi
  done
  printf '%s' "$out"
}

# Echo the (unescaped) JSON string value for KEY found in TEXT, or nothing.
# The value body is matched escape-aware (\\. | non-quote-non-backslash)* so an
# embedded \" does not end the match early. Matches the first occurrence — the
# schema never nests the same key twice within one event payload.
json_string() {
  local text="$1" key="$2" re
  # ERE: "key"<ws>:<ws>"<escaped-body>"  — built so $key is literal and the
  # body class stays a valid regex ('\\.' = escaped char, '[^"\\]' = plain).
  re='"'"$key"'"[[:space:]]*:[[:space:]]*"((\\.|[^"\\])*)"'
  if [[ "$text" =~ $re ]]; then
    json_unescape "${BASH_REMATCH[1]}"
  fi
}

# Echo the first non-empty tool_input string field among the given KEYS.
# PreToolUse carries only `tool_input`, so a whole-payload match on the key is
# equivalent to reading tool_input.<key>.
tool_input_string() {
  local key val
  for key in "$@"; do
    val=$(json_string "$INPUT" "$key")
    if [[ -n "$val" ]]; then
      printf '%s' "$val"
      return 0
    fi
  done
}

EVENT=$(json_string "$INPUT" "hook_event_name")
CWD=$(json_string "$INPUT" "cwd")
CWD="${CWD:-$PWD}"

# Walk up from CWD to find the nearest tessl.json (project root). Agents can
# invoke hooks from a subdirectory without its own tessl.json, so anchoring to
# the literal event cwd would deny all tessl__ skills and miss tessl.json write
# protection in subdirectory sessions.
find_tessl_json() {
  local dir="$1"
  while [[ -n "$dir" && "$dir" != "/" ]]; do
    if [[ -f "${dir}/tessl.json" ]]; then
      printf '%s/tessl.json' "$dir"
      return 0
    fi
    dir="${dir%/*}"
  done
  if [[ -f "/tessl.json" ]]; then
    printf '/tessl.json'
    return 0
  fi
  return 1
}

TESSL_JSON=$(find_tessl_json "$CWD") || TESSL_JSON="${CWD}/tessl.json"

# ── Output helpers ────────────────────────────────────────────────────────────

# JSON-escape a bash string for embedding as a JSON string value. Backslash is
# escaped first so the quote/newline replacements are not double-escaped.
json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

# Hard block (PreToolUse). Emits both `decision`/`reason` and
# `permissionDecision`/`permissionDecisionReason` so the block is recognised
# regardless of which field an agent's translator reads, then exits 2.
deny() {
  local r
  r=$(json_escape "$1")
  printf '{"decision":"block","reason":"%s","permissionDecision":"deny","permissionDecisionReason":"%s"}\n' "$r" "$r"
  exit 2
}

# Soft steer (UserPromptSubmit). The generic pipeline injects this into the
# agent's context; it cannot block the prompt.
steer() {
  local c
  c=$(json_escape "$1")
  printf '{"additionalContext":"%s"}\n' "$c"
  exit 0
}

# ── Skill policy ──────────────────────────────────────────────────────────────

# True if BASE is an installed Tessl-managed skill. Checks two ways:
#   1. Listed under any dependency's include.skills in tessl.json.
#   2. Installed as a tessl__<base> directory under any project skill dir
#      (handles dependencies whose plugin.json declares the skill without an
#      include.skills block in tessl.json — the installer still places it on
#      disk as tessl__<name>).
in_tessl_json() {
  local base="$1" content flat work arr inner val
  [[ -f "$TESSL_JSON" ]] || return 1
  content=$(cat "$TESSL_JSON" 2>/dev/null) || return 1
  flat=${content//$'\n'/ }
  work="$flat"
  local arr_re='"skills"[[:space:]]*:[[:space:]]*\[([^]]*)\]'
  local str_re='"((\\.|[^"\\])*)"'
  while [[ "$work" =~ $arr_re ]]; do
    arr="${BASH_REMATCH[1]}"
    work="${work#*"${BASH_REMATCH[0]}"}"
    inner="$arr"
    while [[ "$inner" =~ $str_re ]]; do
      val=$(json_unescape "${BASH_REMATCH[1]}")
      inner="${inner#*"${BASH_REMATCH[0]}"}"
      [[ "$val" == "$base" ]] && return 0
    done
  done

  # Fall back to checking whether tessl__<base> is installed in the project
  # skill dir. Many tessl-managed plugins omit include.skills but their skills
  # are still installed on disk by `tessl install`.
  local proj_dir
  proj_dir="${TESSL_JSON%/tessl.json}"
  { [[ -e "${proj_dir}/.agents/skills/tessl__${base}" ]] ||
    [[ -L "${proj_dir}/.agents/skills/tessl__${base}" ]]; } && return 0

  return 1
}

# True if NAME is a user-installed skill in any directory either runtime uses.
# Built-in commands are not present in any of these. Global dirs store entries
# as "namespace:name" on disk but invoke them as "namespace__name", so the
# function translates back. -L catches broken symlinks (installed but missing
# tile source).
is_user_skill() {
  local name="$1"
  local d

  # Project: .agents/skills/ (both runtimes), .cursor/skills/, .claude/skills/
  for d in "${CWD}/.agents/skills" "${CWD}/.cursor/skills" "${CWD}/.claude/skills"; do
    { [[ -e "${d}/${name}" ]] || [[ -L "${d}/${name}" ]]; } && return 0
  done

  # Global: ~/.agents/skills/ (plain name)
  { [[ -e "${HOME:-}/.agents/skills/${name}" ]] || [[ -L "${HOME:-}/.agents/skills/${name}" ]]; } && return 0

  # Global: ~/.cursor/skills/ and ~/.claude/skills/ (namespace:name on disk)
  local dir
  for dir in "${HOME:-}/.cursor/skills" "${HOME:-}/.claude/skills"; do
    [[ -d "$dir" ]] || continue
    { [[ -e "${dir}/${name}" ]] || [[ -L "${dir}/${name}" ]]; } && return 0
    if [[ "$name" == *__* ]]; then
      local ns="${name%%__*}" rest="${name#*__}"
      { [[ -e "${dir}/${ns}:${rest}" ]] || [[ -L "${dir}/${ns}:${rest}" ]]; } && return 0
    fi
  done

  return 1
}

# Echo a non-empty reason if SKILL must be blocked; echo nothing if allowed.
skill_policy_violation_reason() {
  local skill="$1"
  if [[ "$skill" == tessl__* ]]; then
    local base="${skill#tessl__}"
    if [[ ! -f "$TESSL_JSON" ]]; then
      echo "tessl.json not found at '${TESSL_JSON}'. Cannot verify that skill '${skill}' is authorised."
      return 0
    fi
    if ! in_tessl_json "$base"; then
      echo "Skill '${skill}' is not listed in tessl.json. Run 'tessl install' to register it."
    fi
    return 0
  fi
  if is_user_skill "$skill"; then
    echo "Skill '${skill}' is not managed by Tessl. Only Tessl-managed skills (tessl__ prefix, installed via 'tessl install') are permitted."
  fi
}

# Heuristic: True if CMD looks like it writes to a tessl.json (redirect, tee,
# in-place edit, move/copy, truncate/install, node/python file write). Read-only
# uses (cat, grep) do not match. Named to make clear this is pattern-based
# detection, not an authoritative write oracle.
cmd_looks_like_tessl_json_write() {
  local cmd="$1"
  printf '%s' "$cmd" | grep -q 'tessl\.json' || return 1
  printf '%s' "$cmd" | grep -qE '>{1,2}[[:space:]]*["'"'"']?[^|&;]*tessl\.json' && return 0
  printf '%s' "$cmd" | grep -qE '\btee\b[^|&;]*tessl\.json' && return 0
  printf '%s' "$cmd" | grep -qE '\b(sed|perl|awk)\b.*-i.*tessl\.json' && return 0
  printf '%s' "$cmd" | grep -qE '\b(mv|cp)\b[[:space:]]+[^[:space:]]+[[:space:]]+["'"'"']?[^"'"'"'[:space:]]*tessl\.json' && return 0
  printf '%s' "$cmd" | grep -qE '\b(truncate|install)\b.*tessl\.json' && return 0
  printf '%s' "$cmd" | grep -qE \
    "tessl\.json.*open[[:space:]]*\(.*['\"]w|open[[:space:]]*\(.*['\"]w.*tessl\.json|writeFile(Sync)?[[:space:]]*\(.*tessl\.json|tessl\.json.*writeFile" \
    && return 0
  printf '%s' "$cmd" | grep -qE \
    'Path[[:space:]]*\([^)]*tessl\.json[^)]*\)\.(write_text|write_bytes)[[:space:]]*\(' \
    && return 0
  return 1
}

# Echo the skill id (in invocation form) if PATH is inside a known skill
# directory; otherwise echo nothing. Global dirs store "namespace:name" on disk
# but skills are invoked as "namespace__name" — this normalizes both forms so
# the policy check sees a consistent id.
skill_name_from_read_path() {
  local path="$1" marker rest name
  [[ -z "$path" ]] && return 0
  for marker in ".agents/skills/" ".cursor/skills/" ".claude/skills/"; do
    if [[ "$path" == *"$marker"* ]]; then
      rest="${path#*"$marker"}"
      name="${rest%%/*}"
      # Normalize on-disk "namespace:name" → invocation form "namespace__name"
      [[ "$name" == *:* ]] && name="${name%%:*}__${name#*:}"
      [[ -n "$name" ]] && echo "$name"
      return 0
    fi
  done
  return 0
}

# ── Event: PreToolUse (hard enforcement) ──────────────────────────────────────

if [[ "$EVENT" == "PreToolUse" ]]; then
  TOOL=$(json_string "$INPUT" "tool_name")

  # Skill tool (Claude only). Cursor has no Skill tool; it loads skills via file
  # reads, caught by the read arm below.
  if [[ "$TOOL" == "Skill" ]]; then
    SKILL=$(tool_input_string "skill")
    [[ -z "$SKILL" ]] && exit 0
    reason=$(skill_policy_violation_reason "$SKILL")
    [[ -n "${reason:-}" ]] && deny "$reason"
    exit 0
  fi

  # Read tools: gate reads into skill dirs — the escape hatch around the Skill
  # tool, and the primary skill-load path on Cursor. Reading tessl.json itself
  # is allowed, so this arm returns before the write-protection below.
  # Tool names are passed through verbatim per agent and are NOT normalized by
  # the generic schema: Claude's read tool is `Read`, Cursor's is `read_file` /
  # `read_file_v2`.
  case "$TOOL" in
  Read | read_file | read_file_v2)
    FILE=$(tool_input_string "file_path" "target_file" "path")
    skill=$(skill_name_from_read_path "$FILE")
    [[ -z "$skill" ]] && exit 0
    reason=$(skill_policy_violation_reason "$skill")
    [[ -n "${reason:-}" ]] && deny "$reason"
    exit 0
    ;;
  esac

  # tessl.json write-protection. The skill allow-list is read from tessl.json,
  # so letting the agent edit it directly is an obvious bypass — adding a skill
  # to tessl.json would authorise it. Only the Tessl CLI should modify it.
  # Matched tool-name-agnostically: any non-read tool whose write-path field
  # targets tessl.json (Claude Edit/Write/NotebookEdit, Cursor edit_file, …),
  # or any shell command that writes to it.
  WRITE_PATH=$(tool_input_string "file_path" "notebook_path" "target_file")
  if [[ -n "$WRITE_PATH" && "$(basename "$WRITE_PATH")" == "tessl.json" ]]; then
    deny "tessl.json is managed exclusively by the Tessl CLI. Use 'tessl install / uninstall / update' instead of editing it directly."
  fi

  CMD=$(tool_input_string "command")
  if [[ -n "$CMD" ]] && cmd_looks_like_tessl_json_write "$CMD"; then
    deny "tessl.json is managed exclusively by the Tessl CLI. Shell-level writes to tessl.json are blocked."
  fi

  exit 0
fi

# ── Event: UserPromptSubmit (soft steer) ──────────────────────────────────────

if [[ "$EVENT" == "UserPromptSubmit" ]]; then
  PROMPT=$(json_string "$INPUT" "prompt")

  # Slash-command invocation of a skill (e.g. "/docx ...").
  if [[ "$PROMPT" =~ ^/([a-zA-Z0-9_-]+) ]]; then
    reason=$(skill_policy_violation_reason "${BASH_REMATCH[1]}")
    [[ -n "${reason:-}" ]] && steer "$reason"
  fi

  # Skills passed as prompt attachments (skill paths under a skill dir).
  # Isolate the attachments array, then walk every "file_path":"…" it contains.
  if [[ "$INPUT" =~ \"attachments\"[[:space:]]*:[[:space:]]*\[([^]]*)\] ]]; then
    attach="${BASH_REMATCH[1]}"
    fp_re='"file_path"[[:space:]]*:[[:space:]]*"((\\.|[^"\\])*)"'
    while [[ "$attach" =~ $fp_re ]]; do
      fpath=$(json_unescape "${BASH_REMATCH[1]}")
      attach="${attach#*"${BASH_REMATCH[0]}"}"
      [[ -z "$fpath" ]] && continue
      skill=$(skill_name_from_read_path "$fpath")
      [[ -z "$skill" ]] && continue
      reason=$(skill_policy_violation_reason "$skill")
      [[ -n "${reason:-}" ]] && steer "$reason"
    done
  fi

  exit 0
fi

exit 0
