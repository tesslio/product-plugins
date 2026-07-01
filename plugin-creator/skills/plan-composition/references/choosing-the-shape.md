# Choosing the shape

Decide the smallest arrangement that solves the problem. Guide the user, do not interrogate.

## Simple vs rich

- **Simple problem → a single skill.** One workflow or one body of knowledge. It is already a minimal plugin under the hood.
- **Richer problem → a plugin.** Reach for a plugin when the problem has several distinct parts (each its own skill), related skills belong together, or you need more than instructions (a rule or an MCP server).

Do not escalate to a plugin for its own sake. If a single skill solves it, that is the answer.

## Which primitive for which intent

| The user wants the agent to... | Use a... |
|---|---|
| Follow a workflow when a task comes up | Skill |
| Always obey a convention, unprompted | Rule |
| Run a named action on demand | Command |
| Use a tool or live data it does not have | MCP server |
| Run something automatically at a lifecycle event | Hook (not GA, defer) |

## Heuristics

- A skill is instructions; an MCP server is capability.
- Rules are for the always-on minority; task-specific guidance belongs in a skill.
- One responsibility per plugin; two unrelated jobs are two plugins.
- Do not add primitives to look complete.

## Eval is downstream

Evaluation is not part of choosing the shape, and not part of this plugin. Once the composition is built, skill-optimizer handles eval as a separate step. The only thing composition owes eval is a well-formed skill or plugin for it to run on.
