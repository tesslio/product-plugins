---
name: decompose-into-skills
description: Use during build when a skill or a problem is too big for one skill - a sprawling SKILL.md doing several jobs, or a large problem the user wants a single skill for. Splits it into focused, independently-verifiable skills, with a plugin as the superstructure that holds them together.
---

# Decompose into skills

Big skills are hard to get right and hard to verify. Splitting them into focused pieces is often the most valuable thing this plugin does, so lead with the value, do not treat it as tidying. This is invoked from `build-composition` (or `plan-composition` when the plan already calls for a split).

## 1. Spot the seams

A skill is too big when it does several distinct jobs, has unrelated triggers, or is so long the core procedure is hard to follow. Identify the independent responsibilities inside it.

## 2. Propose the split

Draft a decomposition: one skill per responsibility, each with its own clear trigger. Show the user the proposed structure and the reasoning. Make the call for them, but bring them in, explain why each split makes the result more reliable and easier to prove later. This is the moment to make the benefit visible.

## 3. Restructure

Create the focused skills (`tessl skill new`). Move shared depth into `references/`. If skills depend on one another, make that explicit so they are not used in isolation. The plugin becomes the superstructure that bundles them, a legitimate reason to go from a single skill to a plugin.

Honour the original content: preserve the user's wording and intent, restructure rather than rewrite, unless a review flags a real problem and the user agrees.

## 4. Result

Hand the decomposed set back to `build-composition` to finish assembling. Note to the user that each skill can now be evaluated independently, later, via skill-optimizer, that independence is a big part of why decomposition was worth it. Do not run evals here.

## When to stop

Stop when the big skill has become a set of focused, independently-triggerable skills the user is happy with.
