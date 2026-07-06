# Publishing the data-pipeline-tools Plugin

## Background

You're a developer at Acme working on the `data-pipeline-tools` Tessl plugin. The plugin bundles several data pipeline authoring skills, but two of the three skills (`validate-schema` and `transform-csv`) were originally written by a colleague, Jordan, who has since moved to another team. You've been handed ownership and are now preparing the plugin for a wider release.

The plugin started as an internal tool (`private: true`) and version `0.1.0`, but the team has decided it should be shared publicly across the organization and beyond. This is the plugin's second release — you've added improvements to `write-pipeline` since the first version.

The plugin directory is at `my-plugin/`. The plugin manifest is at `my-plugin/.tessl-plugin/plugin.json`.

## Your Task

Produce a file called `publish-checklist.md` in the current directory. The checklist should walk through every step a developer needs to complete to safely and correctly publish this plugin — from pre-publish checks through to the actual publish command.

The checklist should reflect the full context: the plugin is moving from private to public, it includes skills you didn't write yourself, and this is not the first release. Write it as an actionable, numbered list that a developer could follow step by step.

Also include a short note at the bottom of `publish-checklist.md` about what to do if, after publishing, the team decides they want to take the plugin down or prevent new installs.
