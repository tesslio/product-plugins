# Routing Health Report for content-tools Plugin

## Problem Description

The content-tools plugin has three skills: `markdown-formatter`, `citation-generator`, and `link-checker`. The team recently ran a quick eval run to check whether each skill is getting activated when it should be, and the results are concerning. Several scenarios produced no skill activation at all, and the team isn't sure whether those are gaps in how the skills describe themselves or whether the scenarios are simply out of scope for the plugin.

The plugin has also had scored evals run previously, so there's comparison data available to help distinguish routing problems from out-of-scope tasks. The team wants a complete routing health report they can act on, including concrete suggestions for fixing any description mismatches they find.

## Output Specification

Produce a file called `routing-health-report.md` containing:

1. A routing table showing which skill fired for each scenario (or `–` if none fired)
2. A skill coverage summary identifying any skills that never fired across all scenarios
3. For each zero-activation scenario (`–`), an analysis of whether it represents a routing gap or an out-of-scope task for this plugin
4. For each scenario identified as a routing gap, a specific proposed description rewrite for the affected skill — presented as a diff or before/after comparison
5. A summary section listing all proposed description changes together

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/activation-results.json ===============
{
  "eval_run_id": "act-run-881",
  "skipForcedContextActivation": true,
  "plugin": "content-tools",
  "scenarios": [
    {
      "name": "format-markdown-table",
      "task_summary": "Convert a CSV dataset into a well-formatted Markdown table with aligned columns",
      "activated_skills": ["markdown-formatter"]
    },
    {
      "name": "add-apa-citations",
      "task_summary": "Add APA-style citations to a research summary document",
      "activated_skills": ["citation-generator"]
    },
    {
      "name": "audit-broken-links",
      "task_summary": "Scan a docs site and report any broken hyperlinks or anchor references",
      "activated_skills": ["link-checker"]
    },
    {
      "name": "rewrite-intro-paragraph",
      "task_summary": "Rewrite the introduction paragraph of a blog post for clarity and conciseness",
      "activated_skills": []
    },
    {
      "name": "generate-bibliography",
      "task_summary": "Produce a bibliography from a list of academic sources in IEEE format",
      "activated_skills": []
    },
    {
      "name": "fix-heading-hierarchy",
      "task_summary": "Correct the heading levels in a Markdown document so H1 through H4 nest properly",
      "activated_skills": []
    }
  ]
}

=============== FILE: inputs/scored-eval-results.json ===============
{
  "eval_run_id": "scored-run-445",
  "skipForcedContextActivation": false,
  "plugin": "content-tools",
  "scenarios": [
    {
      "name": "rewrite-intro-paragraph",
      "baseline_score_pct": 88,
      "with_context_score_pct": 87,
      "delta": -1
    },
    {
      "name": "generate-bibliography",
      "baseline_score_pct": 31,
      "with_context_score_pct": 29,
      "delta": -2
    },
    {
      "name": "fix-heading-hierarchy",
      "baseline_score_pct": 22,
      "with_context_score_pct": 67,
      "delta": 45
    }
  ]
}

=============== FILE: inputs/skills/markdown-formatter/SKILL.md ===============
---
name: markdown-formatter
description: Format and clean up Markdown documents. Use when fixing Markdown syntax, aligning table columns, or correcting code block formatting.
---

# Markdown Formatter

Applies consistent Markdown style: table alignment, heading normalization, code block language tagging, and list indentation.

=============== FILE: inputs/skills/citation-generator/SKILL.md ===============
---
name: citation-generator
description: Generate citations and references. Use when creating APA, MLA, or Chicago-style citations from source metadata.
---

# Citation Generator

Produces correctly formatted citations from DOI, URL, or manual metadata input.

=============== FILE: inputs/skills/link-checker/SKILL.md ===============
---
name: link-checker
description: Check hyperlinks in documents. Use when verifying URLs are reachable or finding broken links in a webpage.
---

# Link Checker

Scans documents for hyperlinks and reports broken or unreachable ones.
