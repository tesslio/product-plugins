---
name: review-skill-instruction-integrity
description: Review a change to an agent-facing skill for whether an agent following it reaches the outcome the skill describes. Use as one lens in a code review run.
---

# Review lens: Skill Instruction Integrity

A skill is executable instruction. An agent reads it and acts, with no author to
ask. Review changed instruction for the places an agent following it lands
somewhere other than where the skill says it will.

## Scope

- **Internal agreement** A fact stated in more than one place in the same skill, where the change moves one statement and leaves the others behind.
- **Substituted outcomes** A fallback, default, or error path that carries on under the name of what was asked for, having produced something else.
- **Claims the mechanism does not support** Instruction telling an agent to read a signal as proof, where the described mechanism can produce that signal for another reason, or fail to produce it when the thing did happen.
- **Undirected material** A bundled reference, script, or example the skill never says when to read or run, leaving the agent to load all of it or none.

## Method

Start from what the change asserts, then find every other place the same skill
speaks about it: another phase of the procedure, a reference file, an eval task,
the plugin README. A skill and its bundled files are one document here.

The changed instruction is the subject. Those other files are read to see whether
the skill still agrees with itself, and a defect that belongs to one of them on
its own account belongs to another lens.

Then follow the changed instruction as an agent would, in order, and at each step
ask what the agent does when the step cannot be completed as written, and what it
has to decide that the skill has not settled.

## Threshold

Report an instruction that leads an agent somewhere other than where the skill
says, contradicts another statement in the same skill, or leaves the agent to
resolve something the skill and the repository do not answer.

Do not report wording, ordering, or house style that leaves the outcome intact,
and do not report a fact restated consistently in two places.

Read the prose, not the blocks. Whether an embedded workflow, command, or
configuration block behaves as printed, including every expression inside it,
belongs to Copyable Snippets, even where the prose introducing it is what made
the block wrong.

## Reporting

- Name the instruction, the step an agent reaches it at, and where it lands instead.
- Quote the statement it disagrees with, and its file.
- State the correction as the outcome the skill should describe, not as a rewording.
