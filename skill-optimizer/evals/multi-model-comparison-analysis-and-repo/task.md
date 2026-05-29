# Model Benchmark Comparison Report

## Problem Description

The quality team at a software tooling company has completed a multi-model benchmark run against their `workflow-tile` and needs a structured comparison report for an upcoming stakeholder review. The raw output from three separate eval runs has been collected and is provided below. The team lead needs a clear, decision-ready analysis: how do the three Claude models compare, where is the tile's skill making a real difference, and what should be fixed before the tile is published to the internal registry.

Produce a comprehensive comparison report in `comparison_report.md` that stakeholders can use to understand the current state of the tile across all models and make an informed decision about publishing. The eval-improve skill is available for addressing identified gaps.

## Output Specification

Produce one file:

- `comparison_report.md` — A structured report containing:
  - An overall model comparison table (aggregate scores across all scenarios)
  - A per-scenario breakdown with scores per model
  - A per-criterion breakdown with scores per model for each individual criterion
  - Interpretation of what the baseline (without-skill) scores reveal
  - Diagnosis of any failing criteria, including what type of failure each represents
  - A model-by-model recommendation summary
  - Recommended next steps based on the results

## Input Files

The following raw eval run outputs are provided as inputs. Extract them before beginning.

=============== FILE: inputs/run-haiku.txt ===============
=== EVAL RUN: run-abc123 ===
Agent: claude:claude-haiku-4-5
Tile: ./workflow-tile
Status: Completed

--- Scenario: scenario-0 ---
Description: setup workflow initialization

  Without Skill Score: 30%
  With Skill Score:    46%

  Criteria (with skill):
    dependency_check    (max 30pts):   6 pts   (20%)
    config_output       (max 40pts):  40 pts  (100%)
    logging_format      (max 30pts):   0 pts    (0%)

--- Scenario: scenario-1 ---
Description: error handling and recovery

  Without Skill Score: 60%
  With Skill Score:    50%

  Criteria (with skill):
    error_detection     (max 40pts):  32 pts   (80%)
    fallback_logic      (max 30pts):  12 pts   (40%)
    retry_behavior      (max 30pts):   6 pts   (20%)

Overall: Without Skill 45% | With Skill 48% | Delta +3pp
=============== END FILE ===============

=============== FILE: inputs/run-sonnet.txt ===============
=== EVAL RUN: run-def456 ===
Agent: claude:claude-sonnet-4-6
Tile: ./workflow-tile
Status: Completed

--- Scenario: scenario-0 ---
Description: setup workflow initialization

  Without Skill Score: 55%
  With Skill Score:    75%

  Criteria (with skill):
    dependency_check    (max 30pts):   8 pts   (27%)
    config_output       (max 40pts):  40 pts  (100%)
    logging_format      (max 30pts):  27 pts   (90%)

--- Scenario: scenario-1 ---
Description: error handling and recovery

  Without Skill Score: 75%
  With Skill Score:    62%

  Criteria (with skill):
    error_detection     (max 40pts):  32 pts   (80%)
    fallback_logic      (max 30pts):  21 pts   (70%)
    retry_behavior      (max 30pts):   9 pts   (30%)

Overall: Without Skill 65% | With Skill 69% | Delta +4pp
=============== END FILE ===============

=============== FILE: inputs/run-opus.txt ===============
=== EVAL RUN: run-ghi789 ===
Agent: claude:claude-opus-4-6
Tile: ./workflow-tile
Status: Completed

--- Scenario: scenario-0 ---
Description: setup workflow initialization

  Without Skill Score: 70%
  With Skill Score:    80%

  Criteria (with skill):
    dependency_check    (max 30pts):  10 pts   (33%)
    config_output       (max 40pts):  40 pts  (100%)
    logging_format      (max 30pts):  30 pts  (100%)

--- Scenario: scenario-1 ---
Description: error handling and recovery

  Without Skill Score: 80%
  With Skill Score:    80%

  Criteria (with skill):
    error_detection     (max 40pts):  40 pts  (100%)
    fallback_logic      (max 30pts):  24 pts   (80%)
    retry_behavior      (max 30pts):  16 pts   (53%)

Overall: Without Skill 75% | With Skill 80% | Delta +5pp
=============== END FILE ===============
