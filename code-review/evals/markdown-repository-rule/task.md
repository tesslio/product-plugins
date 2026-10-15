# Review a new deployment guide

Review this pull request and flag any findings that should be addressed. Write only actionable findings to `review.md`.

This repository is an application, not an agent plugin. Its root `AGENTS.md`, unchanged by this pull request, includes:

```markdown
## Guides

Every guide under `docs/guides/` starts with a `## Prerequisites` section that
lists the access and tools a reader needs before step 1.
```

`scripts/deploy.sh`, unchanged by this pull request, begins:

```bash
#!/usr/bin/env bash
# Usage: scripts/deploy.sh --target <staging|production>
```

```diff
diff --git a/docs/guides/deploy.md b/docs/guides/deploy.md
new file mode 100644
--- /dev/null
+++ b/docs/guides/deploy.md
@@ -0,0 +1,12 @@
+# Deploying
+
+1. Merge your pull request to `main`.
+2. Wait for the `build` workflow on `main` to pass. If it fails, fix it on a
+   new pull request before going on.
+3. Deploy to staging:
+
+   ```sh
+   scripts/deploy.sh --env staging
+   ```
+
+4. Check the staging site, then repeat step 3 with `production`.
```
