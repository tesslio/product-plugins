# Code Quality Reviewer Plugin

## Problem Description

Your team maintains a library of internal Tessl skills that are periodically reviewed for quality. The standard review process covers general description and content quality, but your team has noticed a gap: the existing evaluation doesn't measure whether skills include good code examples. Engineering leads have requested a dedicated reviewer plugin that specifically assesses whether code snippets in a skill are executable, well-commented, and realistic — not pseudocode or placeholder fragments.

You've been asked to build a reviewer plugin called `code-quality-reviewer` that extends the standard evaluation approach. The plugin should retain the existing judges for description quality and content quality, but add a new dedicated judge for code example quality. The code example judge should carry roughly 30% of the total score, reflecting how important executable, well-structured code is to the team. The remaining weight should be shared among the other judges and the validation check, adjusted to make room for the new judge.

The skill files needed to build the plugin are available at `inputs/create-review-plugin/references/`. Use these as the starting point for your plugin.

## Output Specification

Produce the complete plugin directory at `./code-quality-reviewer/` with all necessary files so the plugin could be loaded and run against a skill. The plugin must be a valid Tessl reviewer plugin.

Write a brief `setup-notes.txt` file at the root of the output directory describing the weight distribution you chose and why.
