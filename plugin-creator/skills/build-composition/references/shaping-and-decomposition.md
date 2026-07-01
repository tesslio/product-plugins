# Shaping and decomposition

The most common authoring mistakes are cramming everything into one skill and packing unrelated skills into one plugin. Fixing both is a core part of the value this plugin adds.

## Right-size each skill

- **One skill = one goal-oriented workflow.** Name it as a verb (`write-endpoint`, not `endpoints`). Avoid skills that are thin wrappers over a single CLI command.
- **Keep `SKILL.md` lean.** If it is long or repetitive, move detail into `references/` files and link to them, so the core procedure stays scannable (progressive disclosure).
- **Move supporting material into the skill directory.** Templates, examples, and scripts live alongside `SKILL.md`.
- **A strong `description` is what makes a skill discoverable.** It must say what the skill does and when to use it.

## Right-size the plugin

- One responsibility per plugin. A plugin is a focused bundle, not a junk drawer.
- A few tightly-related skills, not fifty.
- An orchestrator skill plus a small number of sub-skills it delegates to is a good shape.

## Decomposition (why it matters)

A big skill is hard to get right and hard to verify. Splitting it into focused skills makes each one:

- **Independently verifiable** — each can be evaluated on its own, later, so its quality can be proven.
- **Independently triggerable** — each has a clear, narrow description, so the agent routes accurately.
- **Easier to maintain** — a change to one does not risk the others.

The `decompose-into-skills` skill owns this workflow. Lead with the benefit: decomposition is not tidying, it is what makes the result reliable.

## Split signals

Decompose a skill when it does several distinct jobs, has unrelated triggers, is long enough that the core procedure is hard to follow, or repeats content and mixes "what to do" with deep reference detail.
