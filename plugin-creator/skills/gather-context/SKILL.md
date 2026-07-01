---
name: gather-context
description: Use at the start of creating context, to understand the problem the user is solving and take stock of what they already have. The user may arrive with an existing skill or plugin, code, a written prompt or transcript, or nothing but a pointer ("go look at my PRs"). Gathers what exists and fills the gaps - by asking or by hunting - until there is enough to plan a composition.
---

# Gather context

Before shaping anything, understand the problem and take stock of the material. Users arrive in different states, meet them where they are.

## 1. Understand the problem

What does the user want the agent to do better? Often they have already tried to solve it and now have a skill that is messy, too long, or underperforming. Get the problem clear in a sentence or two.

## 2. Take stock of what exists

Look at what they have. The material you need may already be the thing they are trying to create.

- **An existing skill or plugin** — read it. This is often the starting point ("my skill is a mess").
- **Code, configs, or docs** — the conventions to capture may be implicit in the codebase.
- **A prompt, transcript, or notes** — raw intent to structure.
- **A pointer** — "go find it in my PRs / recent sessions."

## 3. Fill the gaps

Work out what is missing to solve the problem, then fill it the right way:

- **Ask the user** — when the gap is knowledge only they have (the trigger, the exact steps, constraints). Probe specifically: "you have given me the what; I still need when the agent should reach for this, and the two or three steps you follow."
- **Hunt for it** — when the user wants you to find the evidence yourself (recurring PR feedback, agent logs). See [references/hunting-artifacts.md](references/hunting-artifacts.md).
- **Infer it** — when you can read it from the artifacts already in front of you. Do not ask for what you can find.

## 4. Confirm you have enough

Before handing to `plan-composition`, make sure you understand the problem and have the material (existing or gathered) to solve it. If not, keep gathering. Do not jump to building.

## When to stop

Stop when you can state the problem and have resolved the artifacts and gaps well enough to plan the composition.
