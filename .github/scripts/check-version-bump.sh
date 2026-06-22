#!/usr/bin/env bash
# Fail if any changed plugin has not had its version bumped forward.
#
# For each plugin directory changed between base and head, compare the version
# field in .tessl-plugin/plugin.json on both refs. The check passes only when
# the head version is strictly greater (semver) than the base version. A newly
# added plugin (no manifest on base) passes. This guarantees every merge that
# touches a plugin carries a publishable version bump.
#
# Usage: check-version-bump.sh <base-ref> <head-ref>
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
base_ref="${1:?usage: check-version-bump.sh <base-ref> <head-ref>}"
head_ref="${2:?usage: check-version-bump.sh <base-ref> <head-ref>}"

# Print the version from a plugin manifest at a given ref, or empty string if
# the manifest does not exist there (e.g. a newly added plugin).
manifest_version() {
  local ref="$1" dir="$2"
  git show "${ref}:${dir}/.tessl-plugin/plugin.json" 2>/dev/null \
    | jq -r '.version // ""' 2>/dev/null || true
}

# Return 0 when $1 is a strictly greater semver than $2. Versions here are
# plain X.Y.Z, which sort -V orders correctly.
version_gt() {
  [ "$1" != "$2" ] &&
    [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n1)" = "$1" ]
}

changed_plugins=$("$script_dir/changed-plugins.sh" "$base_ref" "$head_ref")

if [ -z "$changed_plugins" ]; then
  echo "No plugin directories changed; nothing to check."
  exit 0
fi

failed=0
while IFS= read -r dir; do
  [ -z "$dir" ] && continue
  base_version="$(manifest_version "$base_ref" "$dir")"
  head_version="$(manifest_version "$head_ref" "$dir")"

  if [ -z "$head_version" ]; then
    echo "❌ $dir: .tessl-plugin/plugin.json is missing a version field."
    failed=1
  elif [ -z "$base_version" ]; then
    echo "✅ $dir: new plugin at version $head_version."
  elif version_gt "$head_version" "$base_version"; then
    echo "✅ $dir: $base_version → $head_version."
  else
    echo "❌ $dir: version not bumped ($base_version → $head_version)." \
      "Bump the version in $dir/.tessl-plugin/plugin.json before merging."
    failed=1
  fi
done <<< "$changed_plugins"

exit "$failed"