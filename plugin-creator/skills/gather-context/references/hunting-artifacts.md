# Hunting for artifacts

When the user wants you to find the material yourself rather than hand it over ("look at my PRs and tell me what's worth a skill"), mine two evidence streams. This mirrors how `derive-review-rubrics` (in the `review-plugin-creator` plugin) grounds its work in real evidence.

## PR review feedback

Invoke `/find-optimizations` over a PR window (a PR number, or a period like "the last 2 weeks"), scoped to recurring review comments. Repeated corrections are the strongest signal that reusable context is missing. Each finding has a type, a summary, and evidence (PR numbers and the specific comments).

## Agent logs (optional)

`tessl agent-logs view --json --since <ISO timestamp>` (add `--provider` to narrow). Look for tasks where the agent needed correction, or where a skill that should have fired did not. Empty entries mean no local history (e.g. a cloud sandbox), say so and proceed on PR evidence. Do not invent log evidence you do not have.

## Turn evidence into candidates

Cluster recurring patterns. Each cluster is a candidate: "the agent keeps getting X wrong, context teaching Y would fix it." Rank by how often and how severely each recurred, present the top few with their evidence, and let the user choose. Feed the chosen candidate back into the problem understanding. If the evidence is thin, say so rather than manufacturing a candidate.
