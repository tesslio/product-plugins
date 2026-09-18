# product-plugins

Official Tessl plugins published to the [`tessl` workspace](https://tessl.io/registry/tessl/) on the Tessl registry. Each top-level directory containing a `.tessl-plugin/plugin.json` is one plugin.

Read this file before adding, moving, or renaming any file in this repository.

## This repository is public

Everything committed here is world-readable, including git history. Assume anything you add will be read by customers, competitors, and search engines.

Never commit:

- Draft notes, review requests, or working documents written for colleagues.
- Names of Tessl staff, or instructions addressed to a named individual.
- Links to any internal tool or document, such as an issue tracker, wiki, chat workspace, or shared drive.
- Issue or ticket identifiers, outside a commit message.
- Roadmap, pricing, customer names, or anything about unreleased work.
- Credentials, API keys, or workspace tokens.

Internal working documents belong in an internal repository or document store. To get feedback on a draft plugin, share a branch or a local path. Do not commit the instructions for the person reviewing it.

**`.tesslignore` does not make a file private.** It controls only what `tessl publish` uploads to the registry. A file listed in `.tesslignore` is still committed to this public repository and still visible on GitHub. These are two separate exposure surfaces, and this repository is the wider one. Excluding a file from the published bundle is not a reason to commit it.

## Every plugin here is customer-facing

These plugins ship to users under the Tessl name, and merging to `main` publishes them. A plugin is not ready to merge until it meets the bar:

- **Reviewed.** Score it with `tessl review run <plugin> --workspace tessl` and act on the findings. Do not publish a plugin you have not reviewed.
- **Evaluated.** Every plugin needs eval scenarios under `<plugin>/evals/`, and they need to pass. Scores are published as a badge on the registry listing, so a weak plugin is weak in public.
- **Documented.** Every plugin needs a `README.md` written for a user who has never seen it, plus a row in the root `README.md` table carrying its version and eval badges.
- **Versioned.** Bump the version in `<plugin>/.tessl-plugin/plugin.json` for any change to that plugin. CI blocks the merge otherwise.

A plugin that is still a draft does not belong on `main`. Keep it on a branch until it clears the bar.

## Layout

| Path | Purpose |
| --- | --- |
| `<plugin>/.tessl-plugin/plugin.json` | Plugin manifest. Holds the published name and version. |
| `<plugin>/skills/<skill>/SKILL.md` | The skills the plugin provides. |
| `<plugin>/evals/<scenario>/` | Eval scenarios (`task.md`, `criteria.json`, `scenario.json`). |
| `<plugin>/README.md` | User-facing documentation for that plugin. |
| `<plugin>/tessl.json` | Local development project file. Not published. |
| `<plugin>/.tesslignore` | Files excluded from `tessl publish`. See the warning above. |
| `.tessl-code-review.yml` | Code Review profile for this repository: the lens set and the paths each lens reviews. |
| `review-lenses/<lens>/SKILL.md` | A review lens this repository runs on its own pull requests. Not a plugin, and not published. |

## CI

- `version-check` fails a pull request that changes a plugin without bumping that plugin's version.
- `publish` publishes every changed plugin when a commit lands on `main`. Merging is publishing. There is no separate release step.
- `tessl-code-review` reviews a pull request when it is opened, reopened, or marked ready for review, and again when an owner, member, or collaborator comments `@tessl-code-review` on it as a whole word. An opened draft is not reviewed until it is marked ready, though a mention on a draft is. Pushing commits does not start a review. Changes requested fails the `Tessl Code Review` check, so a blocked pull request needs a fresh review against the new head before it can merge.

The lenses in `review-lenses/` and the profile that routes them are instructions that later run with a reviewer's authority. Review a change to either with the same care as a change to a published skill.

A review reads them from the pull-request head, which is the branch under review. A change that narrows the profile's routing, or weakens a lens, therefore takes effect on the review of the change that makes it. Nothing in the workflow can catch that, so it is a reviewer's job: read a change to `.tessl-code-review.yml` or `review-lenses/` as a change to the gate itself. Contributions arriving as fork pull requests are not reviewed at all, so this reaches only branches pushed by someone who already has write access.

## Before opening a pull request

Check every file you added against one question: could a customer read this without surprise? If a file exists to communicate with someone at Tessl, it does not belong in this repository.
