---
name: review-plugin-release-readiness
description: Review a change to a published plugin for what users receive when it lands — whether the version step, the documentation, and the published bundle match the change. Use as one lens in a code review run.
---

# Review lens: Plugin Release Readiness

Merging publishes. There is no separate release step, so a change to a plugin is
a release of that plugin, and whatever is wrong about it reaches users at the
same moment it reaches the default branch. Review the change as the release it
becomes.

## Scope

- **The version step** Whether the version change reflects what actually changed for users. A bump is required by CI; whether it is the right size is not checked anywhere.
- **Documentation against shipped behavior** A plugin README or description that describes behavior this change replaced.
- **The published bundle** A file that reaches the registry and should not, or one the plugin needs at runtime that an ignore rule now excludes.

## Method

For each plugin the change touches, read its manifest, its README, its row in the
root listing, and its skills together, as one release.

Then ask what a user who installs the new version gets that the previous version
did not: a skill that triggers on different requests, a renamed or removed skill,
a changed default, a hook registered on a new event. For each such difference,
find where it is written down for that user, and confirm the version step says a
difference of that kind happened.

## Threshold

Report a change to the published surface that the version step misrepresents, a
document that contradicts the behavior being shipped, or a bundle that gains a
file it should not carry or loses one it needs.

Do not report a missing version bump, which CI already blocks. Do not report
README wording that is merely improvable, or an internal file that is correctly
excluded from the bundle.

This lens reads a document only as a statement about what a user receives.
Whether a skill's own instructions are accurate, and whether a template in one
behaves as printed, belong to Skill Instruction Integrity and Copyable Snippets.
Program logic in a script or hook the plugin bundles belongs to the correctness
and security lenses.

## Reporting

- Name the plugin, the surface that changed, and what a user who installs it experiences.
- State the version step the change calls for, or the document line that has to change with it.
- A version step has no changed line of its own to sit on. Name the manifest, the surface that moved, and the step it calls for, so the finding stands on its own away from the code.
