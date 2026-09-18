# Regional package publishing

This action publishes or verifies one exact Tessl package version in `production`
(US) or `app-eu` (EU). It accepts agent-native plugins and legacy `tile.json`
packages. The caller checks out the source revision, binds a GitHub environment,
and supplies `path`, `name`, `version`, `target`, `api-url`, and `token`.

The CLI is pinned to 0.109.0. The action packs the source, checks that its identity
matches the publication plan, verifies workspace edit permission, and looks up the
exact version. Identical existing content succeeds without uploading. Different
content at the same version fails. Missing content is published through the CLI
and downloaded again for verification. A failed or timed-out upload is read back
before retrying, at most three times. Versions are never bumped or overwritten.

Comparison includes file paths and bytes, normalizing tar metadata and the
registry's documented upload transformations: unsupported extensions and hidden
basenames are excluded, and `tile.json` is compared after JSON normalization,
private-default insertion and `steering` to `rules` normalization. `.mcp.json`
is retained. The helper's constants must track the registry upload contract when
it changes. Conflicts are reported for review, never silently accepted.

Publication still invokes the CLI's normal publish-time eval behavior. Readback
verifies registry content, not completion of asynchronous reviews or evals. A CLI
failure after the content committed can therefore recover as a successful content
publication; the CLI's diagnostic output is retained in the job log.

## Repository workflow

`publish.yml` reconciles every current top-level plugin on a push to main. This
recovers missing versions after failed or superseded runs even if a subsequent
merge changes another plugin. The matrix runs US and EU independently with
`fail-fast: false`; either failure fails the workflow. Workflow concurrency
serializes runs. A selected-package dispatch reconciles that package's current
version and its reviewed historical versions.

Helpers always run from the triggering main commit. Package contents come from
the exact SHA in the plan, including historical backfills. No credentials are
available to the planning or PR-test jobs. Manual publication is restricted to
main. The `target` input selects `both`, `production`, or `app-eu`; the `package`
input selects a directory, with an empty value selecting all packages.

`publish-backfills.json` lists required historical versions with immutable source
commits. The planner checks their manifest identities and requires each commit to
be an ancestor of the trusted checkout. Entries must refer to a current package;
removed and local-only packages are never restored implicitly. Current versions
are discovered automatically. Add older versions to this manifest when supported
clients still require them, retaining the original source and version.

## Configuration and rollout

Before merging the workflow, create `registry-production` and `registry-app-eu`
GitHub environments, restricted to main. Each must define `TESSL_PUBLISH_TOKEN`
with a token issued by that registry and edit permission on the package's
workspace. Do not define a repository-level fallback under that name. Create the
workspace and publisher membership in each registry first. Missing credentials,
permissions, archived versions and inaccessible content fail the job.

Inspect the planning summary before backfilling, then dispatch on main with the
selected target and package. No dispatch means no manual backfill; merging this
workflow does reconcile the full inventory. A new destination initially requires
publication of all the required versions, not just the latest changed package.
After publication, install exact versions using fresh CLI state for each target.
The immutable source SHA appears in the plan and the content digest appears in
the publication summary.

Other repositories can consume this action at a pinned commit. They retain their
own triggers, package roots and manual-publish exclusions, and can call
`inventory.py` from the same pinned checkout to generate their package plan.

## Validation

Run from the repository root:

```sh
python3 -m unittest discover -s .github/actions/publish-plugin -p 'test_*.py' -v
python3 .github/actions/publish-plugin/inventory.py --root . --backfills .github/publish-backfills.json
```

The publishing-tests workflow also lints GitHub Actions definitions. Tests cover
content conflicts, exact identities, retry after commit, independent regional
recovery, permission errors, archive normalization, historical pins and inventory
exclusions. They do not publish to live registries.
