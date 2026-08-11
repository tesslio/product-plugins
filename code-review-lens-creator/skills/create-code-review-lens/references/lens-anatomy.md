# Lens anatomy

What goes into a lens `SKILL.md`, and what each part is for. Only `name` and `description` frontmatter are required. Everything else here is a starting point, not a format the CLI enforces.

## How far to direct

A reviewer with no direction explores widely and lands somewhere different each time. A lens narrows what the reviewer attends to, which is what makes a review repeatable.

Push that too far and the lens becomes a checklist. It catches what it lists, every time, and nothing else in the same family.

The test: would this lens work on a codebase in another language? A lens naming `axios` or `?? []` has enumerated instances. A lens saying "trace untrusted input to the operations it can influence" has named a kind, and reaches instances nobody listed.

The same trade-off sets how many lenses to run. One lens covering everything spreads a single reviewer's attention across the whole diff. Several, each scoped to a concern but not prescriptive within it, is where coverage comes from.

## The parts

A whole lens, short enough to read in one go:

```markdown
---
name: review-migration-safety
description: Review a change for whether a schema or data migration can be undone once it has run. Use as one lens in a code review run.
---

# Review lens: Migration Safety

Review changes that alter stored data or its shape, for what happens when they have to be reversed after running in production.

## Scope

- **Reversibility** Whether the change can be undone, and what is lost if it is.
- **Deploy order** Whether old and new code can both run against the data during a rollout.

## Method

Start at the migration and work outward to the code that reads and writes the affected data, rather than reading the diff in file order. For each altered column, index, or document shape, find the readers that predate the change and still run during a rollout.

## Threshold

Report a change that cannot be undone without losing data, or that assumes every reader has already been deployed.

Do not report additive changes that leave existing readers working, or migrations on structures the same change creates.

## Reporting

- Name the altered structure, what is lost on reversal, and the readers still on the old shape.
- State the safe form: the backfill, the two-step deploy, the nullable intermediate.
```

**Frontmatter.** `name` matches the directory and is what a reference selects, so it is the lens's identity in a workflow file for as long as the lens exists. `description` is what an agent reads when deciding whether to use this skill: the review question, then what kind of thing it is. Keeping that second sentence recognizable is what stops a lens being mistaken for a review rubric.

**Title.** `# Review lens: <Subject>`.

**Scope.** What the lens covers, as bolded sub-concerns with a phrase each. Two or three related dimensions in one lens is normal. What matters is that a reader can tell what falls inside this lens and what belongs to another.

**Method.** Where to start, and what to follow from there. Not a list of things to match: that is Scope restated as conditions, and it is how a lens becomes a checklist.

**Threshold.** The bar a finding has to clear, and the cases not to report. Both halves matter. A lens without an exclusion reports everything adjacent to its subject, which is the usual reason a lens gets switched off.

**Reporting.** What a finding has to name to be worth acting on, and the shape of the fix to state.

If `tessl/code-review` is installed, its lenses are worth reading as further examples.

## What not to put in a lens

- **A severity.** The review grades findings after the lens produces them. State impact so it can be graded.
- **General review posture.** Working from the diff, preferring evidence to possibility, saying so when a change is clean: these belong to the review, not to each lens.
- **An unbounded search.** A sweep with no starting point in the diff spends the reviewer's turns and returns findings about code the change never touched.
- **Another lens's subject.** Lenses run in parallel and cannot see each other, so overlap becomes duplicate findings. When excluding something, name the lens it belongs to.
- **An output format.** How findings are rendered, tagged, or numbered is the review's business.
- **A condition the reviewer cannot resolve.** "If this path has a latency budget in the SLA" is not checkable from the repository.
- **A verdict on the change as a whole.** "The instrumentation here is weak overall" leaves the author nothing to do.
- **The incident the lens came from.** Naming precedent in your own codebase is fine. A customer identifier or an account number carried across from the evidence is not, and it leaves the repository the moment the lens is published.

## Length

The default lenses run to about 40 lines. Not a limit, but a long lens is usually one that has stopped being distinct. `SKILL.md` is capped at 80,000 bytes.

Bundle a reference file when the lens needs a catalog that would swamp the `SKILL.md`. Bundled files are preloaded along with it.
