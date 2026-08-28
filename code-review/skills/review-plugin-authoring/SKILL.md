---
name: review-plugin-authoring
description: >-
  Review a change to plugin and skill content (SKILL.md bodies and frontmatter,
  always-on rules, hooks, reference files, bundled scripts, evals, and the
  plugin manifest) for whether an agent will reach the right skill and then act
  correctly on it. Use as one lens in a code review run.
---

# Review lens: Plugin authoring

The files in a plugin are instructions an agent executes, not prose a person
skims. A defect here does not fail a build. It surfaces later as a wrong action
in an unattended session, so read every changed line as the input to a run
rather than as documentation.

## Scope

Files a plugin ships, and skills that stand alone without a manifest:
`SKILL.md` bodies and frontmatter, the reference files a skill points to,
`rules/` and other always-on context, `hooks/`, scripts a skill tells the agent
to run, `evals/`, and the plugin manifest.

- **Activation** Whether the frontmatter `description` states both what the
  skill does and when to use it, in terms a user would actually type, and
  whether it stays distinct from the descriptions of sibling skills the same
  agent will see.
- **Instruction correctness** Whether the commands, flags, paths, env vars,
  table columns, and API fields the instructions name exist and mean what the
  instructions claim. An invented flag or a renamed path is this lens's
  equivalent of a null dereference.
- **Followability** Where an instruction leaves the agent a fork it has to
  guess through: two readings of one step, a step whose success condition is
  unstated, or a destructive or batch operation with no verification step
  before or after it.
- **Context cost** What the change adds to every future session. Always-on
  content (`rules/`, agent entry points) is paid on every request, skill
  content only when it activates, and a reference file only when it is read.
- **Packaging** Whether the change ships. Where there is a manifest, a new
  skill directory absent from its `skills` list is inert; a reference file no
  instruction points to is never read.
- **Eval coverage** Whether a change to what a skill does leaves its `evals/`
  criteria asserting the old behavior.

## Method

Trace every concrete thing the changed instructions name (command, flag, path,
script, column, endpoint) against the repository as it is now, not against what
the name suggests. Plugin prose is the surface where a rename lands silently:
nothing imports it, so nothing broke when the thing it names moved.

Read a changed `description` beside the descriptions of the skills that ship
alongside it, not on its own. Overlap is only visible in the set: two skills
whose triggers collide leave the agent picking by chance.

For a changed workflow, read the steps in order as the agent, with only the
context the skill supplies. Note the first point where you would have to decide
something the text does not decide for you.

For always-on content, ask what it costs when the session is about something
else entirely, and whether the same guidance stated as an activating skill
would be paid for only when it applies.

## Threshold

Report an instruction an agent would act on wrongly, a description that sends
it to the wrong skill or to none, a fork it must guess through, or an addition
whose standing context cost exceeds what it buys.

`tessl tile lint` gates manifest schema, the existence of a file the manifest
names, markdown links, and skill-name validity, and a repository's own CI
commonly gates the version bump. Do not restate a finding one of those
produces. Tile lint does not read a path inside an instruction, so a script or
file a step tells the agent to use is this lens's to check.

The other lenses in a review read program logic, and a plugin's paths are
usually outside what they are scoped to. Where that is so, a bundled script or
hook is this lens's to read as code as well as as an instruction, and a defect
a correctness or security lens would have raised in it belongs here.

Prose is not a defect for being plainer or longer than you would write it.
Report a wording change only where the wording changes what the agent does, or
where the copy is user-facing and wrong.

An eval is in scope only as the thing that asserts a changed behavior. A
scenario that is merely hard, a criterion that is merely strict, and a behavior
no scenario covers are all findings about the eval suite rather than about this
change, and this lens does not raise them.

## Reporting

- Give the file the instruction is in, quote the instruction, and name the
  action an agent would take from it, then the action it should take.
  "Ambiguous" without both readings is not a finding.
- For a name that does not resolve, give the current one with its path. Where
  nothing in the repository answers to it, say so and name the remedy: ship the
  file or drop the reference.
- For an activation finding, name the sibling skill it collides with, or the
  phrase a user would type that the description does not cover.
- For context cost, say where the content should live instead (a skill, a
  reference file, or nowhere) rather than asking for it to be shortened.
