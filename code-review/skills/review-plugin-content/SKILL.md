---
name: review-plugin-content
description: Review a change to the contents of an agent plugin (its skills, references, rules, evals, manifest, README, and the scripts and hooks it bundles) for whether the plugin ships, whether an agent picks the right skill, and whether an agent following it acts correctly and safely. Use as one lens in a code review run.
---

# Review lens: Plugin Content

A plugin is the directory that holds a `.tessl-plugin/` manifest directory, and
everything under it ships together. Its skills are instructions an agent
executes, often unattended, with no author to ask. Review a changed file as the
input to an agent's run, not as a program and not as prose a person skims.

## Scope

- **Shipping and selection** Whether what the change adds reaches users and gets used: a skill the manifest does not pick up, a file a skill points to that is missing or excluded from the published bundle, a `description` that does not say when to use the skill or collides with a sibling's, a removed or renamed skill shipped as a patch version, or something the repository's own rules require of every plugin that this one lacks.
- **Instruction correctness** Whether the commands, flags, paths, environment variables, fields, and files an instruction names exist and mean what it claims.
- **Followability** Where an agent following the instructions in order takes a wrong action: two readings of a step that lead to different outcomes, a step whose success the agent cannot tell, a destructive or irreversible step the agent takes without first confirming it acts on the right target, or a statement that contradicts another in the same skill, its references, its evals, or the plugin README.
- **Bundled scripts and hooks** Whether a script or hook does what the instruction that runs it says, breaks on the inputs the skill passes it, and is safe to run on a user's machine. Hold safety to the bar of application code: interpolated input reaching a shell, a destructive command on an unchecked path, a credential written to output, code fetched and executed.

## Method

Read the plugin's manifest, README, and the changed skill with its references,
evals, and scripts as one unit. A guard or answer stated anywhere in that unit
counts.

Read the `AGENTS.md` or `CLAUDE.md` chain governing the plugin, from the
repository root down. Rules about what every plugin must carry, such as eval
scenarios or a README, are this lens's to check, including against files the
change did not add. A required entry for the plugin in a file outside it, such
as a row in a listing, is this lens's only when the change leaves that file
untouched.

Trace each concrete thing a changed instruction names against the repository at
the change's head, not against what the name suggests. Nothing imports a path
written in prose, so a rename elsewhere breaks it silently.

Read a changed `description` beside the descriptions of the sibling skills an
agent will see with it.

Then follow the changed instructions as the agent would, with only the context
the plugin supplies, and note the first point where it would act wrongly or have
to guess.

For a script or hook, start from the instruction that runs it and the arguments
it passes.

## Threshold

Report an instruction an agent would act on wrongly, a fork where a reasonable
reading leads to a wrong outcome and nothing in the plugin or repository settles
it, a skill that will not ship or will not be picked, a requirement the
repository's rules set that the plugin does not meet, or a script that
misbehaves on its real inputs or is unsafe to run.

An agent is not a program. It reads the whole skill, uses judgment, and can stop
and report. Do not report an instruction for what a program would do if it
executed it literally: an unbounded wait, a missing retry, concurrency, batch
size, or an input with no explicit branch that a careful agent handles from
context. Such a gap is a finding only when the skill directs a specific wrong
action there, or forbids the reasonable one. An instruction to repeat or wait
with no end condition and no point at which to stop is such a direction. Do not
ask for instructions to be deterministic or exhaustive: an edge case the rules
leave open, where any choice a careful agent would make is acceptable, is not a
finding. Nor is a conflict an agent reaches only through an unusual combination
of states, unless what it then does is destructive or cannot be undone.

Before reporting that a skill permits or misses something, check the rest of the
unit for the statement that answers it. A concern the skill already handles is
not a finding. Two statements that apply under different conditions, such as a
rule and an exception that waits for the user's say-so, do not contradict each
other.

Do not report wording, tone, length, or structure that leaves the agent's action
unchanged, or hold a script to application standards of scale or
maintainability. Do not assume tools or a directory layout this repository does
not have.

## Reporting

- Name the file and quote the instruction, then the action an agent takes from it and the action it should take.
- For an ambiguity, give both readings and what each leads to.
- For a name that does not resolve, give the current name and its path, or say nothing in the repository answers to it.
- For a selection problem, name the sibling skill it collides with, or the request the description does not cover.
- For a missing required part, quote the repository rule that requires it.
- For a script, name the input that breaks it or the actor who can exploit it, what happens, and the fix.
