# Review a pull request that adds a skill to a plugin

Review this pull request and flag any findings that should be addressed. Write only actionable findings to `review.md`.

`plugins/notes/` is an agent plugin: it holds `.tessl-plugin/plugin.json`, whose `skills` field is `"./skills/"`. Users install it, and an agent runs its skills on the user's machine. The plugin already has eval scenarios under `plugins/notes/evals/`.

The plugin's skills drive `notes-cli`. Its help output, unchanged by this pull request:

```text
$ notes-cli export --help
Usage: notes-cli export <title> [--output-format md|html] [--out <dir>]
```

```diff
diff --git a/plugins/notes/skills/share-note/SKILL.md b/plugins/notes/skills/share-note/SKILL.md
new file mode 100644
--- /dev/null
+++ b/plugins/notes/skills/share-note/SKILL.md
@@ -0,0 +1,19 @@
+---
+name: share-note
+description: Share one of the project's notes as a Markdown file. Use when the user asks to share, send, or export a note.
+---
+
+# Share a note
+
+1. Ask the user for the note's title, and use it exactly as they typed it.
+2. Export it:
+
+   ```sh
+   notes-cli export "<title>" --format md --out shared/
+   ```
+
+3. Run `scripts/stamp.sh "<title>"` to add the sharing date to the exported file.
+4. Tell the user the path of the file in `shared/`.
+
+If the user asks to share every note, repeat steps 2 and 3 for each title in
+`notes-cli list`.
diff --git a/plugins/notes/skills/share-note/scripts/stamp.sh b/plugins/notes/skills/share-note/scripts/stamp.sh
new file mode 100755
--- /dev/null
+++ b/plugins/notes/skills/share-note/scripts/stamp.sh
@@ -0,0 +1,6 @@
+#!/usr/bin/env bash
+set -e
+for f in shared/*.md; do
+  test -f "$f" || continue
+done
+eval "echo 'Shared on $(date +%F)' >> shared/$1.md"
```
