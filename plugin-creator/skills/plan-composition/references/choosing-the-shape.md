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

## Skill vs rule: do not default to skills

The most common mistake is making everything a skill. A skill fires when the agent judges a task relevant; a rule is always in context. If the user says the agent "keeps getting X wrong", "every time", or "never follows our convention", that is an always-on convention, which is a **rule** (sometimes a rule plus a skill), not a skill on its own. Weigh this explicitly for any conventions-style request before defaulting to a skill.

## Heuristics

- A skill is instructions the agent reaches for; a rule is a convention it always obeys; an MCP server is a capability.
- One responsibility per plugin; two unrelated jobs are two plugins.
- Do not add primitives to look complete.

## Some behaviours are not skills or rules at all

Not every "the agent should X" belongs in the plugin. If a behaviour is better enforced deterministically (a lint, a test, or a hook once hooks are GA), or is a broad observable invariant better expressed as a verifier (`tessl change verify`, an LLM-judge at glob level), say so and point the user at the `change-verify` skill rather than forcing it into skill or rule prose. Context is the right tool for workflows and conventions the agent reasons about, not for deterministic guardrails.

## Eval is downstream

Evaluation is not part of choosing the shape, and not part of this plugin. Once the composition is built, skill-optimizer handles eval as a separate step. The only thing composition owes eval is a well-formed skill or plugin for it to run on.
