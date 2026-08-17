---
name: setup-code-review
description: Install or update Tessl Code Review in a GitHub repository by writing a thin caller workflow that invokes the Tessl Code Review Action at a pinned commit SHA. Inspects existing workflows and any Code Review caller already present, asks when reviews should run and whether findings should block the merge, proposes the change, and only writes after explicit approval. Use when someone wants to add, set up, enable, configure, update, or remove Tessl Code Review, AI code review, or automated pull-request review in a repository, or wants to switch it between advisory and gate mode.
---

# Set up Tessl Code Review

Tessl Code Review runs as a GitHub Action. The Action owns everything about
running a review: pull-request resolution, checkout of the exact head, Tessl CLI
setup, review publication, the check run it reports on the reviewed head,
stale-head protection, idempotent retries, failure notices, and result
artifacts.

The repository owns a thin caller workflow: triggers, concurrency, runner,
timeout, permissions, the token secret, and the review policy inputs.

This skill installs or updates that caller workflow. It never reimplements review
or publication logic, and it never adds a second execution path.

## The Action repository

The supported Action is `tesslio/code-review-action`.

This is the only place that name is decided; it is written in several. Everywhere
else in this skill, "the Action repository" means that repository, and the
templates carry it on their `uses:` lines. If the name ever changes, update it
here, on the templates' `uses:` lines, and on the `uses:` line of any workflow
already installed in a repository. The repository path is what changes; the
pinned commit SHA stays, unless the selected release changes too. Nothing else
about the setup changes.

## Procedure

Work through these phases in order. Do not write any file before phase 4.

### 1. Detect

Read the repository before asking anything. Gather:

- **Workflow conventions.** List `.github/workflows/`. Note the naming style
  (`kebab-case.yml` against `Title Case.yaml`), the runner label other workflows
  use, whether they set `timeout-minutes`, and whether they pin third-party
  actions to commit SHAs.
- **An existing Code Review caller.** Search the workflow directory for the
  Action repository. If one exists, record its file path, the pinned
  revision, its triggers, its concurrency group, its permissions block, and its
  `mode`, `profile`, and `lenses` inputs. This is an update, not a fresh install.
- **Restricted overrides on an existing caller.** If the existing caller sets
  `model` or `effort`, leave both exactly as they are and name them in phase 3
  as restricted overrides this setup does not manage. Do not describe them as
  supported configuration, and do not offer to change them.
- **Conflicting or duplicate callers.** More than one workflow invoking the
  Action, or another reviewer bot on the same triggers, is a conflict. Surface
  it in phase 3 rather than overwriting either one.
- **The token secret.** Check whether a `TESSL_TOKEN` repository secret exists
  (`gh secret list` if the GitHub CLI is authenticated). You cannot read its
  value, only whether the name is present. Listing secrets needs admin rights,
  so treat a `403` as unknown rather than as missing.
- **Fork traffic.** If the repository takes pull requests from forks, note it.
  The Action rejects cross-repository pull requests before it runs a review, so
  those pull requests are not reviewed on any trigger. Say so in phase 3 rather
  than installing something that silently never fires.
- **The default branch.** A comment mentioning `@tessl-code-review` runs the copy
  of the workflow on the default branch, not the copy on the pull-request branch.
  The mention trigger does nothing until this change is merged. Tell the user in
  phase 6.
- **Branch protection.** If gate mode is a live option, note which checks are
  currently required on the default branch.

Infer everything you can from this. Only the two questions below are genuinely
unanswerable from the repository.

### 2. Interview

Ask the two questions in [references/interview.md](references/interview.md):
when reviews run, and whether findings block. They are orthogonal choices, and
every pairing of them is installable. Present the trade-offs briefly, state the
default, and let the user take the default in one word.

If the user picks gate, read "What gate mode enforces" in
[references/interview.md](references/interview.md) first. The Action reports its
own check run on the head it reviewed, so a gate enforces on every cadence. What
the cadence decides is when a fresh verdict arrives, which changes what a blocked
pull request has to do to become unblocked.

Do not ask about the executor, the harness, the backend endpoint, the CLI
channel, or telemetry. Do not offer the model or the reasoning effort either:
they are not part of this setup, the templates never set them, and the selected
profile decides both.

### 3. Propose

Show the user, before writing:

- the exact file path you will create or modify;
- the full workflow contents you propose, or a diff against the existing caller;
- the pinned Action revision you will use, and which release it came from;
- who may request a mention-driven round, as a choice rather than a silent
  default (see **The mention guard** below);
- anything you found that needs a human decision: a conflicting caller, fork
  traffic, a missing `TESSL_TOKEN` secret, an unsafe existing trigger, a `model`
  or `effort` override already present;
- for gate mode, the branch-protection and repository-settings changes the user
  has to make themselves, because a workflow file cannot make them.

Ask for explicit approval. Do not proceed on silence or on a vague reply.

**Pinning.** The `uses:` line must carry a full 40-character commit SHA. A tag or
a branch is a moving reference, and every mention round hands the repository's
`TESSL_TOKEN` to whatever that reference currently points at, so resolve the SHA
yourself rather than trusting a name.

Resolve it at setup time, against the current supported release of the Action
repository:

```bash
gh api repos/tesslio/code-review-action/releases/latest --jq .tag_name
gh api repos/tesslio/code-review-action/git/ref/tags/<tag> --jq '.object.sha, .object.type'
```

An annotated tag resolves to a tag object, so follow it once more
(`gh api repos/tesslio/code-review-action/git/tags/<sha> --jq .object.sha`) until you
hold a 40-character commit SHA. Pin that, and tell the user which release it came
from.

Do not substitute a tag, a branch, `main`, or `canary`, and do not invent a SHA.

If no release resolves, because the repository publishes none yet, it is not
readable from here, or there is no network access, **stop and say so**. There is
no supported revision to pin, so there is no workflow worth writing: a file
carrying a placeholder cannot run, and it reads as though setup succeeded. Tell
the user what failed and what unblocks it, which is access to the Action
repository or a released revision to pin. Write nothing.

The one case that needs no lookup is a user who names the revision they are
adopting. Pin exactly that, after checking it is 40 hexadecimal characters.

**The mention guard.** The templates restrict mention-driven rounds to commenters
whose author association is `OWNER`, `MEMBER`, or `COLLABORATOR`. That is the
recommended default, and it is a choice the user makes, not something you include
silently. Put it to them in one line, with its reason and its alternatives. When
the user has already given blanket approval for the described setup and said
nothing about the guard, install the recommended default and state the decision
and its alternatives in the proposal and the closing summary, rather than
stalling the setup on it. The line to put to them: a
mention round runs privileged and spends the repository's Tessl credits, so the
allowlist keeps arbitrary commenters from driving it; the alternatives are to
drop the condition so any commenter on a pull request can request a review, or to
query the commenter's permission level through the API, which is stricter and
costs an extra call. The trade-offs are in
[references/workflow-templates.md](references/workflow-templates.md).

The `@tessl-code-review` token itself is not a choice. It is the token the
Action's published review tells reviewers to use, so a caller that listens for
anything else installs a review that teaches a token the workflow ignores.

### 4. Write

Take the template for the chosen cadence from
[references/workflow-templates.md](references/workflow-templates.md), apply the
mode choice, and write it to `.github/workflows/tessl-code-review.yml` (or the
existing caller's path, if there is one, or a name matching the repository's
convention).

Writing is idempotent, and updating preserves user-owned choices:

- If no caller exists, write the template.
- If a caller exists, edit it in place. Change only what the interview decided,
  plus the pinned SHA when the user is adopting a new revision; an existing pin
  the user is deliberately keeping stays. Keep the user's runner label, `timeout-minutes`, job name,
  step ordering, extra steps that consume the Action's outputs, any `model` or
  `effort` input already present, and any triggers or concurrency settings that
  are compatible with the chosen cadence.
- Re-running against a repository whose caller already matches the interview and
  carries the pin the user selected changes nothing. Say that, rather than
  rewriting the file to make the run look productive.
- If the existing caller has a trigger the chosen cadence does not include, do
  not delete it silently. Name it in phase 3 and let the user decide.
- Never create a second workflow that also calls the Action. One
  caller per repository. Two callers double every review, and giving them the
  same concurrency group is not a fix: it serializes the runs, so the second
  review still happens, just afterwards.

### 5. Verify

After writing, check:

- the YAML parses, with a real parser rather than by eye
  (`python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <path>`, or
  `yq . <path>`, or any equivalent already available in the repository);
- the `uses:` line carries a full 40-character commit SHA;
- `permissions` is exactly `contents: read`, `checks: write`, `issues: write`,
  `pull-requests: write`. `checks: write` is what lets the Action report the
  `Tessl Code Review` check on the reviewed head, so a gate cannot be enforced
  without it;
- the concurrency group resolves to a pull-request number on every trigger the
  workflow declares;
- exactly one workflow in the repository calls the Action;
- `TESSL_TOKEN` exists as a repository secret, or the user has been told to
  create one.

### 6. Explain

Close with a short summary the user can act on, covering the contract they chose
(when reviews run, whether findings block, and for gate mode, that a blocked
pull request only unblocks when a fresh review runs against the new head), how to
request a round by mentioning `@tessl-code-review` in a comment and who is
allowed to, the `TESSL_TOKEN` secret, the permissions granted and why, any
branch-protection step still outstanding, and how to update or remove the setup
later.

For gate mode, the check to require in branch protection is the Action's own
check, named `Tessl Code Review`. Never the caller's job.

The details for the secret, permissions, branch protection, update, and removal
are in [references/operations.md](references/operations.md). Do not paste that
file wholesale. Pull out the parts that apply.

## Customizing the review itself

Cadence and blocking are the setup questions. What the reviewer actually looks
for is a separate concern, controlled by the `profile` and `lenses` inputs.
`profile: standard` with no `lenses` is the right starting point, and it is what
the templates install.

Once the workflow is running and the user wants to change what gets reviewed,
point them at the Action repository's README, which documents the `lenses` input
and the ordered selection it takes.

For CLI and Action reviews, a user can keep an explicitly selected YAML profile
in the repository and route lenses with globs. Read
[references/file-profiles.md](references/file-profiles.md) before explaining or
editing one. When adding a file profile to the caller workflow, explain that the
Action accepts the repository-relative path through its `profile` input.
