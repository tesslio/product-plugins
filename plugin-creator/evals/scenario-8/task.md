# Build a live component-search MCP plugin

The Meridian frontend team has an existing unauthenticated MCP service at:

`https://components.meridian.internal/mcp`

They want AI coding agents to query it for live component metadata during a session. This is a runtime capability, not a workflow or an always-on convention.

Create a Tessl plugin named `meridian/component-search` under `component-search/`, ready for `tessl plugin lint` and `tessl plugin pack`. Bundle the MCP declaration in the plugin and make the manifest explicit about it. Do not create or modify consuming-agent configuration files; Tessl should materialize the server when the plugin is installed. Do not add credentials or invented headers.
