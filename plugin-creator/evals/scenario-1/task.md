# Refactor a Sprawling Database Admin Skill

## Problem Description

The platform team at Fieldstone Technologies has been maintaining a single monolithic skill file that covers everything related to database administration — schema migrations, backups, health monitoring, and user access management. Over time this file has grown unwieldy: it has four clearly distinct responsibility areas with different triggers, different audiences, and different risk profiles. A junior engineer recently ran the backup steps when they meant to run the monitoring steps, causing unnecessary downtime.

The team lead has decided it is time to split the skill into focused, independently maintainable units. The skill file lives at `inputs/SKILL.md`. There is no other infrastructure to set up; all the context you need is in that file.

Your job is to analyze the existing skill, propose and execute a decomposition into a well-structured multi-skill plugin, and produce the resulting file structure on disk.

## Output Specification

Produce the following in your working directory:

1. **A decomposed plugin directory** — a folder named `database-admin-plugin/` containing a proper plugin manifest and one sub-folder per focused skill, each with its own skill file. Organize shared material appropriately so it is not duplicated across skills.

2. **`decomposition-rationale.md`** — a short document (a page or less) explaining:
   - Why you decomposed the skill the way you did and what the agent gains from this structure
   - The proposed structure: list each resulting skill, its name, and when it fires
   - What happens next — any recommendations for the team after the restructure is in place

Do not preserve the monolithic structure. The goal is a clean multi-skill plugin where each unit can stand alone.
