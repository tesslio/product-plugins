---
name: create-context
description: Use when someone wants to turn a problem, a messy or sprawling skill, or some existing work into well-shaped reusable context for their agent. Triggers include "help me make a skill for X", "my skill is a mess, sort it out", "I want to get more out of Tessl with this skill", or "package this so my team can use it". Runs the arc - understand the problem, gather the artifacts, plan the right composition, build it - then points to eval as a separate next step.
---

# Create context

Start from the user's problem, not from "let's make a plugin." Most users are not asking to package anything. They usually already tried to solve their problem and now have a skill that is sprawling, too long, or not getting enough out of Tessl, and they want help. Your job is to understand what they are trying to do and shape their work into the right form.

A plugin is just the packaging mechanism. Do not lead with it. And do not run evals here, evaluation is a separate, downstream step (see the end).

## The arc

Run these phases in order. Each has a skill.

1. **Understand and gather** — `gather-context`. Understand the problem, take stock of what the user already has (an existing skill or plugin, code, a prompt or transcript, or a pointer like "go look at my PRs"), and fill the gaps by asking or by hunting. The material you need may already be the thing they are trying to create. Make sure you have enough before moving on.
2. **Plan the composition** — `plan-composition`. Decide the right shape to solve the problem. Simple problems want a single skill; richer ones want a plugin, possibly with rules or an MCP server. Produce a short plan and confirm it.
3. **Build the composition** — `build-composition`. Create it: author or restructure the skill(s), decompose anything too big (`decompose-into-skills`), and assemble the plugin with the primitives the plan called for. Scaffold with the CLI, do not hand-write manifests.
4. **Publish (optional)** — `publish-plugin`, only if the user wants to share it now.

## Then, separately: eval

Once the composition exists and everything is in the right place, the natural next step is to prove it works. That is a **separate, sibling flow**: hand off to `tessl/skill-optimizer`. Do not pull the user into evals while they are still creating, and do not run evals as part of this arc. Offer it as the next thing once they are done here.

## Principles

- **Honour what the user brings.** Restructure rather than rewrite. Change a user's skill content only if a review flags a real problem and they agree.
- **Narrate the why.** Make the value of decomposition or packaging visible.
- **Default to the smallest thing that solves the problem.** If a single skill does it, stop there. A plugin must earn its place.
- **Know the real CLI.** Scaffold with `tessl skill new` / `tessl plugin new`; inspect `tessl --help` rather than inventing commands.

## When to stop

Stop when the user has well-shaped context, a skill or a plugin, in the right place, and knows that eval via skill-optimizer is the next step if they want it.
