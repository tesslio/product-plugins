# Post-Fix Validation for database-migrator Plugin

## Problem Description

A developer at Ironwood Systems has been iteratively improving the `database-migrator` plugin based on eval feedback. Over the last few hours, they've made three separate edits to the plugin's `SKILL.md`: adding a detailed rollback procedure with step-by-step instructions, expanding the error handling section with a comprehensive list of failure modes and recovery steps, and adding a rules section containing 40 lines of migration pre-checks.

The developer is concerned that these additions, while accurate, may have significantly increased the number of tokens loaded into every agent context that uses this plugin — even for simple tasks that don't need the rollback details or the full pre-check list. They want a script that validates the plugin after each of these three change sets and flags whether the token footprint has grown to a point where restructuring is needed.

The plugin is at `./database-migrator/`.

## Output Specification

Produce two files:

1. `validate-plugin.sh` — a shell script that runs plugin validation after each of the three change sets. The script should:
   - Validate the plugin after each set of edits
   - Check for token cost changes
   - Output a recommendation if front-loaded token costs have increased significantly

2. `validation-notes.md` — a short explanation of:
   - What command was used for validation and why
   - What a significant increase in front-loaded tokens should trigger
   - Your recommended approach for handling content that is causing token bloat
