---
name: setup-code-review
description: Install or update Tessl Code Review in a GitHub repository by writing a thin caller workflow that invokes the tesslio/code-review Action at a pinned commit SHA. Inspects existing workflows and any Code Review caller already present, asks when reviews should run and whether findings should block the merge, proposes the change, and only writes after explicit approval. Use when someone wants to add, set up, enable, configure, update, or remove Tessl Code Review, AI code review, or automated pull-request review in a repository, or wants to switch it between advisory and gate mode.
---

# Set up Tessl Code Review

Tessl Code Review runs as a GitHub Action, `tesslio/code-review`. The Action owns
everything about running a review: pull-request resolution, checkout of the exact
head, Tessl CLI setup, review publication, stale-head protection, idempotent
retries, failure notices, and result artifacts.

The repository owns a thin caller workflow: triggers, concurrency, runner,
timeout, permissions, the token secret, and the review policy inputs.

This skill installs or updates that caller workflow. It never reimplements review
or publication logic, and it never adds a second execution path.

## Procedure

Work through these phases in order. Do not write any file before phase 4.

### 1. Detect

Read the repository before asking anything. Gather:

- **Workflow conventions.** List `.github/workflows/`. Note the naming style
  (`kebab-case.yml` against `Title Case.yaml`), the runner label other workflows
  use, whether they set `timeout-minutes`, and whether they pin third-party
  actions to commit SHAs.
- **An existing Code Review caller.** Search the workflow directory for
  `tesslio/code-review`. If one exists, record its file path, the pinned
  revision, its triggers, its concurrency group, and its `mode`, `profile`,
  `lenses`, `model`, and `effort` inputs. This is an update, not a fresh install.
  Record `model` and `effort` even though the templates never set them, so that
  an update does not silently drop a value the repository chose.
- **Conflicting or duplicate callers.** More than one workflow invoking
  `tesslio/code-review`, or another reviewer bot on the same triggers, is a
  conflict. Surface it in phase 3 rather than overwriting either one.
- **The token secret.** Check whether a `TESSL_TOKEN` repository secret exists
  (`gh secret list` if the GitHub CLI is authenticated). You cannot read its
  value, only whether the name is present. Listing secrets needs admin rights,
  so treat a `403` as unknown rather than as missing.
- **Fork traffic.** If the repository takes pull requests from forks, note it.
  The Action rejects cross-repository pull requests before it runs a review, so
  those pull requests are not reviewed on any trigger. Say so in phase 3 rather
  than installing something that silently never fires.
- **The default branch.** A `/tessl-review` comment runs the copy of the workflow
  on the default branch, not the copy on the pull-request branch. The mention
  trigger does nothing until this change is merged. Tell the user in phase 6.
- **Branch protection.** If gate mode is a live option, note which checks are
  currently required on the default branch.

Infer everything you can from this. Only the two questions below are genuinely
unanswerable from the repository.

### 2. Interview

Ask the two questions in [references/interview.md](references/interview.md):
when reviews run, and whether findings block. They are orthogonal choices.
Present the trade-offs briefly, state the default, and let the user take the
default in one word.

If the user picks gate, read the enforcement constraint in
[references/interview.md](references/interview.md) before proposing anything. A
required status check is reported against the head a run was triggered for, and
only `pull_request` runs are triggered against a pull-request head. That makes
some cadence and gate pairings enforce differently from how they read, and the
user has to know which one they are choosing.

Do not ask about the executor, the harness, the backend endpoint, the CLI
channel, or telemetry. Do not ask about the model or the reasoning effort
either: the Action accepts `model` and `effort`, but these templates deliberately
leave both unset so the selected profile decides. If the user raises them, say
that rather than saying they cannot be configured.

### 3. Propose

Show the user, before writing:

- the exact file path you will create or modify;
- the full workflow contents you propose, or a diff against the existing caller;
- the pinned Action revision you will use, and where it came from;
- anything you found that needs a human decision: a conflicting caller, fork
  traffic, a missing `TESSL_TOKEN` secret, an unsafe existing trigger;
- for gate mode, the branch-protection and repository-settings changes the user
  has to make themselves, because a workflow file cannot make them.

Ask for explicit approval. Do not proceed on silence or on a vague reply.

**Pinning.** The `uses:` line must carry a full 40-character commit SHA. Take it
from the release notes of the Tessl Code Review release you are installing. Do
not substitute a tag, a branch, `main`, or `canary`, and do not invent a SHA. If
you cannot obtain one, write the workflow with the literal placeholder
`<full-commit-sha>`, tell the user the workflow will not run until they replace
it, and leave it to them.

### 4. Write

Take the template for the chosen cadence from
[references/workflow-templates.md](references/workflow-templates.md), apply the
mode choice, and write it to `.github/workflows/tessl-code-review.yml` (or the
existing caller's path, if there is one, or a name matching the repository's
convention).

Writing is idempotent, and updating preserves user-owned choices:

- If no caller exists, write the template.
- If a caller exists, edit it in place. Change only what the interview decided
  plus the pinned SHA. Keep the user's runner label, `timeout-minutes`, job name,
  step ordering, extra steps that consume the Action's outputs, any `model` or
  `effort` input they set, and any triggers or concurrency settings that are
  compatible with the chosen cadence.
- If the existing caller has a trigger the chosen cadence does not include, do
  not delete it silently. Name it in phase 3 and let the user decide.
- Never create a second workflow that also calls `tesslio/code-review`. One
  caller per repository. Two callers double every review, and giving them the
  same concurrency group is not a fix: it serializes the runs, so the second
  review still happens, just afterwards.

### 5. Verify

After writing, check:

- the YAML parses, with a real parser rather than by eye
  (`python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <path>`, or
  `yq . <path>`, or any equivalent already available in the repository);
- the `uses:` line carries a full commit SHA, or the placeholder plus a stated
  follow-up;
- `permissions` is exactly `contents: read`, `issues: write`,
  `pull-requests: write`;
- the concurrency group resolves to a pull-request number on every trigger the
  workflow declares;
- exactly one workflow in the repository calls `tesslio/code-review`;
- `TESSL_TOKEN` exists as a repository secret, or the user has been told to
  create one.

### 6. Explain

Close with a short summary the user can act on, covering the contract they chose
(when reviews run, whether findings block, and for gate mode, that a blocked
pull request only unblocks when a new round is requested), the `TESSL_TOKEN`
secret, the permissions granted and why, any branch-protection step still
outstanding, and how to update or remove the setup later.

The details for the secret, permissions, branch protection, update, and removal
are in [references/operations.md](references/operations.md). Do not paste that
file wholesale. Pull out the parts that apply.

## Customizing the review itself

Cadence and blocking are the setup questions. What the reviewer actually looks
for is a separate concern, controlled by the `profile` and `lenses` inputs.
`profile: standard` with no `lenses` is the right starting point, and it is what
the templates install.

Once the workflow is running and the user wants to change what gets reviewed,
point them at the `tessl/code-review` plugin, which documents the available
lenses and how to compose an ordered selection for the `lenses` input.
