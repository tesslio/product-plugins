---
name: review-markdown
description: Review a change to Markdown that is not part of an agent plugin (standalone skills, AGENTS.md and CLAUDE.md, READMEs, and documentation) for whether it is true of the repository, whether an agent or reader following it acts correctly, and whether it meets the repository's own rules for that content. Use as one lens in a code review run.
---

# Review lens: Markdown

Markdown in a repository is read by people and, more and more, executed by
agents: an `AGENTS.md` or a standalone skill is standing instruction, and a
README or guide is what someone follows to get something done. Review a changed
document for what a reader does after reading it.

## Scope

- **Truth** Whether what the document says matches the repository at the change's head: the commands, flags, paths, configuration keys, defaults, and behavior it describes.
- **Followability** Whether an agent or reader following the document in order reaches the outcome it describes: a step that cannot be completed as written, two readings that lead to different outcomes, a block that does not work when pasted as printed, or a statement that contradicts another standing instruction or document.
- **Repository rules** Whether the document meets what the repository's own `AGENTS.md` or `CLAUDE.md` requires of that kind of content, such as a required section or listing row, or content that must not be committed.
- **Selection** For a standalone skill, whether its `description` says what it does and when to use it, without colliding with another skill an agent sees beside it.

## Method

Read the `AGENTS.md` or `CLAUDE.md` chain governing the changed files, from the
repository root down, for rules about this content and for standing
instructions the change may contradict.

Trace each concrete thing the changed text names against the repository, not
against what the name suggests. A document describing code is checked against
that code.

For instruction, follow it as the agent would, in order, with only the context
the repository supplies, and note the first point where it would act wrongly or
have to guess. A guard or answer stated elsewhere in the same document, or in a
file it points to, counts. Two statements that apply under different conditions,
such as a rule and an exception that waits for the user's say-so, do not
contradict each other.

## Threshold

Report a statement that is false of the repository, an instruction an agent or
reader would act on wrongly, a fork where a reasonable reading leads to a wrong
outcome and nothing settles it, a block that fails as
printed, or a document that breaks a rule the repository sets for it.

A document is not a program. Do not report it for what code would do if it
executed it literally: unbounded waits, retries, concurrency, or an input with no
explicit branch that a careful reader handles from context. Such a gap is a
finding only when the document directs a specific wrong action there. An
instruction to repeat or wait with no end condition and no point at which to
stop is such a direction. Do not ask for a document to be deterministic or
exhaustive about edge cases a careful reader resolves acceptably either way, or
for a conflict reached only through an unusual combination of circumstances.

Do not report wording, tone, length, structure, or a preference about what the
document should cover. Do not report a description of planned work that says it
is planned.

Files inside a plugin, a directory holding a `.tessl-plugin/` manifest
directory, are the plugin lens's. Read them for context, and never report on
them, even when one is routed to this lens.

## Reporting

- Name the file and quote the statement, then what is true or what a reader does instead.
- For a name that does not resolve, give the current name and its path, or say nothing in the repository answers to it.
- For an ambiguity, give both readings and what each leads to.
- For a broken rule, quote the rule and its file.
- State the corrected text or the fact it should state.
