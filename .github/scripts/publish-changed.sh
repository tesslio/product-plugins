#!/usr/bin/env bash
# Publish every plugin whose files changed in the pushed commit range.
#
# Usage: publish-changed.sh <before-ref> <after-ref>
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
before_ref="${1:?usage: publish-changed.sh <before-ref> <after-ref>}"
after_ref="${2:?usage: publish-changed.sh <before-ref> <after-ref>}"

# GitHub sends an all-zero SHA for the first push to a ref (no prior commit to
# diff against); fall back to the parent of the pushed commit.
if [ -z "$before_ref" ] ||
  [ "$before_ref" = "0000000000000000000000000000000000000000" ]; then
  before_ref="${after_ref}^"
fi

changed_plugins=$("$script_dir/changed-plugins.sh" "$before_ref" "$after_ref")

if [ -z "$changed_plugins" ]; then
  echo "No plugin directories changed; nothing to publish."
  exit 0
fi

while IFS= read -r dir; do
  [ -z "$dir" ] && continue
  echo "::group::Publishing $dir"
  tessl plugin publish "$dir"
  echo "::endgroup::"
done <<< "$changed_plugins"