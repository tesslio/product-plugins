# Skill Optimization Automation

## Problem Description

A developer advocacy team maintains a library of SKILL.md files and wants to set up a repeatable process for improving them one at a time. Currently the team does this manually and inconsistently — some developers skip the review step, some apply changes without validating syntax, and no one compares scores before and after. The team lead wants to standardize the process with an automated script.

Create a shell script that automates the skill optimization workflow. The script should accept a path to a SKILL.md file and walk through the improvement process programmatically, capturing review output before and after changes, running validations, and producing a summary of the improvement.

## Output Specification

Produce the following files:
- `optimize_skill.sh` — the automation script
- `README.md` — brief usage instructions explaining how to run the script and what it does at each step

The script does not need to make actual edits to the SKILL.md (it can leave that step as a placeholder or interactive step), but it should handle all the evaluation and validation steps programmatically.
