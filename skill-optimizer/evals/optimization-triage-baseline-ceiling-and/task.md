# Optimization Decision Point for pull-request-reviewer Tile

## Problem Description

The ML platform team at Crescendo has finished the initial eval setup for their `pull-request-reviewer` tile and has received the first batch of results. Before jumping into improvements, the engineering lead wants a structured triage document that analyzes the results and recommends what to do next.

The team is time-constrained — they don't want to spend hours writing tile improvements only to discover the real problem is something structural. They need someone to read the results critically and flag any issues that should be addressed before diving into content edits.

## Output Specification

Produce a `triage-report.md` that:
1. Summarizes the key findings from the eval results
2. Identifies and prioritizes any critical issues that must be resolved first
3. Recommends specific next steps in priority order
4. Explains what each recommended action is meant to address

## Input Files

The following files are provided as inputs. Extract them before beginning.

=============== FILE: inputs/eval-results.json ===============
{
  "tile": "pull-request-reviewer",
  "eval_run_id": "eval-run-3391",
  "scenarios": [
    {
      "name": "security-review",
      "description": "Review a pull request for security vulnerabilities and flag risky patterns",
      "baseline_score_pct": 84,
      "with_context_score_pct": 79,
      "delta": -5,
      "criteria": [
        { "name": "flags_injection_risks", "baseline": 9, "with_context": 7, "max": 10 },
        { "name": "checks_auth_bypass", "baseline": 8, "with_context": 6, "max": 10 },
        { "name": "identifies_hardcoded_secrets", "baseline": 9, "with_context": 9, "max": 10 },
        { "name": "structured_summary", "baseline": 10, "with_context": 10, "max": 10 },
        { "name": "severity_labels", "baseline": 10, "with_context": 9, "max": 10 },
        { "name": "references_cwe", "baseline": 7, "with_context": 5, "max": 10 },
        { "name": "pr_scope_respected", "baseline": 8, "with_context": 7, "max": 10 },
        { "name": "no_false_positives", "baseline": 7, "with_context": 6, "max": 10 }
      ]
    },
    {
      "name": "style-and-clarity",
      "description": "Review a PR for code style issues, naming clarity, and documentation completeness",
      "baseline_score_pct": 87,
      "with_context_score_pct": 91,
      "delta": 4,
      "criteria": [
        { "name": "naming_conventions", "baseline": 9, "with_context": 10, "max": 10 },
        { "name": "doc_completeness", "baseline": 8, "with_context": 9, "max": 10 },
        { "name": "inline_comment_quality", "baseline": 8, "with_context": 9, "max": 10 },
        { "name": "consistent_formatting", "baseline": 9, "with_context": 9, "max": 10 },
        { "name": "unused_imports_flagged", "baseline": 9, "with_context": 9, "max": 10 }
      ]
    },
    {
      "name": "performance-analysis",
      "description": "Identify performance bottlenecks, unnecessary allocations, and inefficient patterns in a PR",
      "baseline_score_pct": 82,
      "with_context_score_pct": 85,
      "delta": 3,
      "criteria": [
        { "name": "loop_complexity", "baseline": 9, "with_context": 9, "max": 10 },
        { "name": "memory_allocation", "baseline": 8, "with_context": 9, "max": 10 },
        { "name": "db_query_patterns", "baseline": 7, "with_context": 8, "max": 10 },
        { "name": "caching_opportunities", "baseline": 9, "with_context": 9, "max": 10 },
        { "name": "algorithm_choice", "baseline": 7, "with_context": 8, "max": 10 }
      ]
    }
  ]
}
