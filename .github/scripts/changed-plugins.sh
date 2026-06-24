#!/usr/bin/env bash
# Print the top-level plugin directories whose files changed between two refs.
#
# A "plugin directory" is any top-level directory that contains a
# .tessl-plugin/plugin.json manifest. Both the publish-on-merge workflow and
# the PR version-check workflow depend on this, so the definition of "a
# plugin" and "what changed" lives in exactly one place.
#
# Usage: changed-plugins.sh <base-ref> <head-ref>
set -euo pipefail

base_ref="${1:?usage: changed-plugins.sh <base-ref> <head-ref>}"
head_ref="${2:?usage: changed-plugins.sh <base-ref> <head-ref>}"

# Top-level directory of every changed path, deduped, one per line. Paths with
# no slash are repo-root files (e.g. README.md) and are skipped. A while-read
# loop (not `for dir in $changed_dirs`) keeps directory names with whitespace
# intact instead of word-splitting them.
while IFS= read -r dir; do
  [ -z "$dir" ] && continue
  # Keep only directories that are plugins at the head ref.
  if git cat-file -e "${head_ref}:${dir}/.tessl-plugin/plugin.json" 2>/dev/null; then
    echo "$dir"
  fi
done < <(
  git diff --name-only "$base_ref" "$head_ref" \
    | awk -F/ 'NF > 1 { print $1 }' \
    | sort -u
)