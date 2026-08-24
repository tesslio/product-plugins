---
name: review-eval-scenario-integrity
description: Review a change to an eval scenario for whether its result means anything — whether the task can discriminate, and whether a judge applying its criteria reaches the same verdict twice. Use as one lens in a code review run.
---

# Review lens: Eval Scenario Integrity

An eval scenario is a measurement, and its score is published. Review changed
scenarios for the ways a score comes back looking like evidence when it is not.

## Scope

- **Discrimination** Whether the task can be completed just as well without the skill it exists to exercise: a task restating the procedure, enumerating what its own output should contain, or working out for the agent what the agent was meant to work out, has handed over the reasoning under test.
- **Judgeability** Whether a criterion can be applied to one transcript twice and reach the same verdict: an aggregate or arithmetic claim no observer can compute, or a criterion resting on a term it never fixes the meaning of.
- **Drift against the skill** A scenario still measuring behavior the same change replaced or removed.

## Method

Take every changed task first, before any criterion. The scenario is the subject
throughout: the skill it exercises is read to judge the scenario, not reviewed
alongside it.

Read the task as the agent under test sees it, with the skill absent, and ask
what that agent would produce. Whatever it would produce anyway is what the
scenario cannot measure. Then read the task beside the skill it exercises,
sentence by sentence: a sentence of the task that appears in the skill as a step,
as a list of the parts an output has, or as a conclusion the skill reaches, is a
sentence the agent no longer has to produce.

Then take the criteria, reading each as the judge sees it, holding only the
transcript, and name the evidence in the transcript that would satisfy it.

Where the change touches a skill and its scenarios together, take each changed
instruction and find the criterion that claims to check it.

## Threshold

Report a task that tells the agent what to work out or lists the parts its own
output should have, where the skill under test is what supplies that. Report a
criterion whose verdict depends on something a judge cannot observe in the
transcript or cannot compute from it. Report a scenario the same change left
measuring behavior that is gone.

Do not report absent coverage. A behavior no scenario reaches, a criterion that
could also check something new, and how many scenarios a plugin has are all
findings about the size of the eval suite rather than about this change, and this
lens does not raise them. Do not report a task that is merely hard, or a
criterion that is strict.

## Reporting

- Quote the task line or criterion.
- Say what two judges could each reasonably conclude from it, or what the agent produces without the skill.
- State the observable the criterion should rest on instead.
