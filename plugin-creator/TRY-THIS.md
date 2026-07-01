# Try this (Sandra)

Thanks for kicking the tyres on this draft. It's the **context/plugin creator** (working name), a set of skills that help someone turn a problem, or a messy existing skill, into well-shaped agent context. It does **not** run evals, that stays in skill-optimizer as a separate step.

What we most want from you: a read on the **workflow and UX**. Does the flow make sense? Does it meet a user where they are? Anything confusing, missing, or annoying? Tweak it freely, it's a draft and nothing here is precious.

The full rationale (and the user research behind it) is in the PRD Marc shared with you.

## The flow it runs
understand → gather → plan the composition → build → (then, separately) eval

Six skills: `create-context` (orchestrator), `gather-context`, `plan-composition`, `build-composition`, `decompose-into-skills`, `publish-plugin`.

## Set it up (about 5 minutes)
You've got a clone of the `product-plugins` repo on the `opt-plugin-creator-draft` branch. The plugin is at `plugin-creator/`. To try it, install it into a scratch project:

```bash
# note the absolute path to the plugin-creator folder in your clone:
PLUGIN=<absolute-path-to-your-clone>/plugin-creator

mkdir -p ~/pc-sandbox && cd ~/pc-sandbox
cat > tessl.json <<JSON
{ "name": "pc-sandbox", "dependencies": { "tessl/plugin-creator": { "source": "file:$PLUGIN" } } }
JSON
tessl install
```

Then open a Tessl or Claude Code session **in `~/pc-sandbox`** and try a scenario below.

## Two scenarios to try

**A - a messy existing skill (the main one).** Save this as `~/pc-sandbox/sample-messy-skill/SKILL.md`:

```markdown
---
name: backend-helper
description: Helps with backend stuff - APIs, database migrations, and deployment. Use this whenever you are doing backend work of any kind.
---

# Backend helper
This skill helps with our backend. It covers a lot.

## Writing API endpoints
All endpoints go under /v{n}. Use plural nouns. Return problem+json for errors. Validate the body. Add tests. Timestamps ISO 8601 UTC. Don't break a published schema.

## Database migrations
Migrations live in db/migrations with a timestamp. Always write a reversible down. Never edit a shipped migration. Back-fill large tables in batches.

## Deploying
Deploy to staging first, run smoke tests, tag the release, announce in #releases. Never deploy Friday afternoon. Roll back with the previous tag.
```

Then tell the agent:
> "I've got a skill at `sample-messy-skill/SKILL.md` that's a mess, it does endpoints, migrations, and deploys all in one. Help me get more out of Tessl with it."

Watch whether it understands the problem, proposes a sensible plan (it should suggest splitting into focused skills and explain why), builds it, and only *then* mentions eval, without rewriting your content unasked or dragging you into evals.

**B - from a brain-dump (no file needed).**
> "I keep re-explaining our service architecture conventions to the agent. Help me capture this. Rough notes: [add three or four bullets]."

Watch whether it gathers and probes for what's missing rather than dead-ending because you didn't hand it a finished skill.

## Tweak it
The skills are plain markdown at `plugin-creator/skills/*/SKILL.md`. Edit anything, re-run `tessl install` in `~/pc-sandbox`, and try again.

## What we'd love back
- Does the flow feel right, or does it get in the way?
- Where did it confuse you or do the wrong thing?
- Anything you'd change in how it talks to the user.

Notes in whatever form is easiest. Marc picks this up Friday.
