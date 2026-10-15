# Review a pull request that changes a release skill

Review this pull request and flag any findings that should be addressed. Write only actionable findings to `review.md`.

`plugins/release/` is an agent plugin: it holds `.tessl-plugin/plugin.json`, whose `skills` field is `"./skills/"`. Its skills are instructions an agent follows in the user's repository. After this pull request, the files under `plugins/release/skills/cut-release/` are `SKILL.md` and `references/changelog.md`. There is no other file in that directory.

```diff
diff --git a/plugins/release/skills/cut-release/SKILL.md b/plugins/release/skills/cut-release/SKILL.md
--- a/plugins/release/skills/cut-release/SKILL.md
+++ b/plugins/release/skills/cut-release/SKILL.md
@@ -8,4 +8,10 @@ description: Cut a release of the user's project. Use when the user asks to release, ship, or tag a version.
 1. Read `references/changelog.md` and write the changelog entry for the new
    version.
 2. Tag the release commit `v<version>` and push the tag.
-3. Tell the user the release is tagged.
+3. Watch the deploy the tag starts. Check its status with
+   `gh run list --workflow deploy.yml --commit <tag commit>` every 30 seconds until it
+   reports `completed`. If it has not completed after 20 minutes, stop and
+   tell the user it is still running, with the run's URL.
+4. If the deploy failed, read `references/rollback.md` and follow it. Do not
+   delete the tag yourself.
+5. Tell the user the outcome: released, still deploying, or rolled back.
```
