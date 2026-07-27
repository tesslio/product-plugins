# Hooks and MCP servers

Use this reference after the composition plan has selected a hook or MCP server. The public contracts are the source of truth:

- [Plugin configuration and hooks](https://docs.tessl.io/reference/configuration#hooks)
- [Add an MCP server](https://docs.tessl.io/creating-skills-and-plugins/add-an-mcp-server)

## Cross-agent hooks: the paved road

Declare agent-independent lifecycle behavior in the top-level `hooks` field of `.tessl-plugin/plugin.json`. It maps one or more generic events to hook groups:

- `PreToolUse`
- `PostToolUse`
- `UserPromptSubmit`
- `SessionStart`
- `Stop`

Each group contains a required `hooks` array and an optional `matcher`. A matcher filters tool names for `PreToolUse` and `PostToolUse`; it can be one tool name, a pipe-separated list such as `Edit|Write`, or a regex. Omit it for non-tool events and when every tool call should match.

Agents vary in which generic events they support. An unsupported event is skipped for that agent, so choose an event implemented by the agents the plugin targets.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash",
            "args": ["${TESSL_PLUGIN_DIR}/hooks/lint.sh"]
          }
        ]
      }
    ]
  }
}
```

A command hook has `type: "command"` and supports two forms:

- **Exec form:** include `args`. `command` is the executable and Tessl spawns it directly, without a shell. Pipes, globs, and `&&` are not interpreted.
- **Shell form:** omit `args`. `command` is a command string run through POSIX `sh -c`. Quote `"${TESSL_PLUGIN_DIR}/..."` in the command string so paths containing spaces work.

An optional `env` map can set a static string or forward a variable at hook-fire time with `{ "fromEnv": "VARIABLE_NAME" }`.

## Native hooks: the escape hatch

Use top-level `nativeHooks` only when the requested event or payload field is specific to an agent and the generic tier cannot express it. Key the map by the recognized agent id, then use that agent's native hook shape:

```json
{
  "nativeHooks": {
    "claude-code": {
      "Notification": [
        {
          "matcher": "idle_prompt",
          "hooks": [
            {
              "type": "command",
              "command": "\"${TESSL_PLUGIN_DIR}/hooks/notify.sh\""
            }
          ]
        }
      ]
    }
  }
}
```

Refer to the target agent's documentation for its accepted event names, matchers, and entry fields. Do not translate a generic event into `nativeHooks` simply to target the agent the user currently prefers.

## Plugin-owned hook paths and shipping

Hook commands run with the event's project directory as cwd, not the plugin directory. Reference plugin-owned files with the exact braced `${TESSL_PLUGIN_DIR}` token in `command` or `args`; a bare relative path does not point into the installed plugin.

Put hook scripts and entrypoints under the conventional `hooks/` directory. The packer includes that directory and rejects declared plugin-relative references that would not ship. Registry archives do not preserve executable bits, so Tessl marks files directly referenced by hook declarations executable at install time. If an entrypoint calls an undeclared sibling, invoke that sibling through an interpreter or arrange its executable mode separately.

Generic hook tokens are resolved when the hook fires. Native hook tokens are resolved when the plugin is installed into the agent's configuration. In both tiers, keep referenced paths inside the plugin.

## Bundled MCP servers

Create `.mcp.json` at the plugin root with a top-level `mcpServers` map. Tessl discovers this file by convention. Add `"mcpServers": ".mcp.json"` to the manifest as an explicit pointer; the pointer is optional and does not replace the map inside `.mcp.json`.

```json
{
  "mcpServers": {
    "component-library": {
      "type": "http",
      "url": "https://components.example.com/mcp"
    },
    "schema-linter": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@example/schema-linter-mcp"]
    }
  }
}
```

Supported transports are:

- `http`: `type`, an `http` or `https` `url`, and optional string-valued `headers`.
- `stdio`: `type`, `command`, and optional string-array `args` and string-valued `env`.

Do not hard-code credentials. Use environment-based configuration supported by the server rather than committing tokens or passwords. Do not edit each consuming agent's MCP configuration; Tessl materializes the bundled declaration into supported agents on install.

## Validation

Run `tessl plugin lint` and `tessl plugin pack`, then inspect the archive for `.tessl-plugin/plugin.json`, every directly referenced hook entrypoint, and `.mcp.json`. For hooks and MCP servers, install into a throwaway project when practical and inspect the supported agent configuration to verify materialization and cleanup.
