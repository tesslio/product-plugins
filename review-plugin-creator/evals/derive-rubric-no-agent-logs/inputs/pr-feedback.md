# Recurring PR Review Feedback — Q2 2026

This document collects recurring review comments gathered across ~40 skill-related PRs from January to June 2026. Comments are grouped by theme.

---

## Theme 1: Vague "When to use" descriptions (appeared in 18 of 40 PRs)

- "The trigger section just says 'when the user asks' — that's too broad. What distinguishes this skill from a general assistant reply?"
- "Reviewer couldn't tell from the description alone when this skill fires vs when the agent handles it inline."
- "Trigger context is missing entirely. What keywords or request patterns are expected?"
- "This is the third PR this sprint where the skill description gave the reviewer no basis to judge fit."

**Severity**: High — caused wrong-skill invocations in staging; one incident resulted in the api-scaffolder being triggered by a formatting request.

---

## Theme 2: Steps too vague to follow reliably (appeared in 14 of 40 PRs)

- "Step 3 says 'apply the changes' — apply how? Which CLI? Which flags?"
- "The steps skip from reading the file to producing the output with nothing in between."
- "No mention of what to do when the expected config file is absent. Agent will halt or guess."
- "Steps 1–3 are fine; Steps 4–5 are placeholders. A reviewer can't certify this is implementable."

**Severity**: Medium — skills with vague steps produced inconsistent agent behavior across runs.

---

## Theme 3: Missing example invocations (appeared in 11 of 40 PRs)

- "There are no examples anywhere in this skill. How does the reviewer know what 'correct' looks like?"
- "Skill has good intent but without a worked example, the LLM interpolates wildly."
- "Every other skill in this repo has at least one before/after example. This one has none."

**Severity**: Medium — correlated with higher review score variance; graders disagree more when examples are absent.

---

## Theme 4: No cleanup or size-limit guidance for generated output (appeared in 9 of 40 PRs)

- "Skill generates a report but doesn't say anything about file size or cleanup. We've had jobs time out because 2 GB diffs were left on disk."
- "What if the formatter produces a huge unified diff? The task description says nothing about this."

**Severity**: Medium — operational risk; jobs fail when large files cause pipeline timeouts.

---

## Theme 5: Scope creep — skills doing more than stated (appeared in 7 of 40 PRs)

- "The skill says it will format files. The agent also rewrote two test files unprompted."
- "README says 'scaffold route only' but the skill's steps also modify the main router and write tests. That's three things, not one."
- "Boundaries are not enforced. The agent interpreted 'update README' as permission to reorganize the whole docs/ folder."

**Severity**: Low-Medium — caused reviewer confusion; one incident required a rollback.

---

## Theme 6: Missing frontmatter / malformed headings (appeared in 5 of 40 PRs)

- "No `# Title` at line 1."
- "H2 headings are inconsistent — some use '##', one uses '###'."
- "Title present but blank."

**Severity**: Low — purely structural; lint-catchable.

---

## Theme 7: No error-handling guidance (appeared in 6 of 40 PRs)

- "What should the agent do if the formatter exits non-zero? Skill is silent on this."
- "Missing: what happens when the target file doesn't exist? The skill assumes a happy path only."

**Severity**: Low-Medium — led to silent failures in CI.
