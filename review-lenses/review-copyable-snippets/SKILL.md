---
name: review-copyable-snippets
description: Review a change to a code block a reader is meant to copy — a workflow, command, config file, or manifest embedded in documentation — for whether it works as printed. Use as one lens in a code review run.
---

# Review lens: Copyable Snippets

Documentation here ships templates. A reader pastes a block into their own
repository unchanged, so a defect in it runs in their repository rather than in
this one, and no test covers it. Review changed blocks as runnable artifacts.

## Scope

- **Behavior as printed** What the block does when pasted unchanged, against what the surrounding prose says it does.
- **Divergent copies** The same block, command, or value appearing more than once in the change, where it is updated in one place and not the other.
- **Substitution points** A placeholder a reader cannot resolve, or that is indistinguishable from a literal value they are meant to keep.

## Method

Read each changed block as its runtime reads it, not as prose.

For a declarative configuration block, resolve every expression it contains
against each input the block itself declares, and ask what the expression
evaluates to when a field is absent from that input. For a command, ask what
happens on an unset variable, an empty match, and a path containing a space.

Then read the prose immediately around the block and compare what it promises
against what the block does, and check the change for another copy of the same
block.

## Threshold

Report a block that fails, silently does something other than what it says, or
diverges from the prose introducing it, when pasted as printed.

Do not report style, ordering, or a block that is plainly illustrative rather
than runnable: an ellipsis, or a fragment quoted to make a point, is not claiming
to run. A placeholder is exempt only where the surrounding prose says what to put
there; one the reader is left to guess at is a substitution point, and in scope.

Where a block and the prose introducing it disagree, the finding is this lens's,
whichever of the two is wrong. Skill Instruction Integrity covers prose that
misdirects an agent on its own, away from any block.

## Reporting

- Name the file and the block, and the input or event that makes it misbehave.
- State what the block produces then, and what the prose said it would.
- Give the corrected line.
