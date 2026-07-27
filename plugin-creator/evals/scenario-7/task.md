# Build a Claude Code idle-notification hook

The Meridian platform team uses Claude Code and wants a local desktop notification when Claude Code emits its native `Notification` event with the `idle_prompt` notification type. The hook must run a bundled `hooks/notify-idle.sh` entrypoint. This requirement intentionally depends on an agent-specific event that is not in Tessl's generic event set.

Create a Tessl plugin named `meridian/claude-idle-notifier` under `claude-idle-notifier/`, ready for `tessl plugin lint` and `tessl plugin pack`.

Also create `hook-decision.md` in the working directory with a concise explanation of why the chosen hook tier is necessary and why the other tier cannot express this requirement. Do not modify `.claude/settings.json` directly.
