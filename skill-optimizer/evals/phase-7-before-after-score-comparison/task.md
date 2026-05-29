# Skill Optimization Results Report

## Problem Description

A developer has spent an afternoon improving their `cache-manager` skill file based on earlier recommendations. They now have two review outputs — one from before the changes and one from after — and want to document the improvement for their team. This report will be shared in a pull request description to explain why the skill changes are worth merging.

Given the two review outputs below, produce a clear score comparison report that shows what improved, by how much, and explains the significance of each dimension's change. The report should be suitable for a developer audience reviewing the skill changes.

## Output Specification

Produce a file `score_report.md` containing:
- An overall before/after comparison showing total score and delta
- A per-dimension breakdown showing old score, new score, and change for each dimension
- An explanation of which dimensions improved and why the changes made them better

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: before_review.txt ===============
=== Skill Review: cache-manager ===
Overall Score: 58%

Dimension Scores:
  Completeness:   1/3  (33%)  - Description missing "Use when" trigger clause
  Actionability:  2/3  (66%)  - Has some code examples, but they show pseudocode not real commands
  Conciseness:    2/3  (66%)  - Moderate; some known concepts explained
  Robustness:     2/3  (66%)  - Missing eviction strategy examples

Validation Issues:
  [WARNING] Description could be more specific about trigger conditions
  [WARNING] Code examples use placeholder values that may confuse
=============== END FILE ===============

=============== FILE: after_review.txt ===============
=== Skill Review: cache-manager ===
Overall Score: 89%

Dimension Scores:
  Completeness:   3/3  (100%) - Clear "Use when" clause with specific trigger conditions
  Actionability:  3/3  (100%) - Real executable commands with actual flag values
  Conciseness:    2/3  (66%)  - Still some minor verbosity
  Robustness:     3/3  (100%) - Added eviction strategy and TTL configuration examples

Validation Issues:
  (none)
=============== END FILE ===============
