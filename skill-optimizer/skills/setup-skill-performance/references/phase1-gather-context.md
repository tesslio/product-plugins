# Phase 1: Find the Plugin

## 1.1 Find what to evaluate

Exclude `.tessl/` (installed plugin copies) and `node_modules/` everywhere below.

1. **Inside a plugin?** Look for `.tessl-plugin/plugin.json` or `tile.json` in the current directory and its parents, up to the repository root. If you find one, that directory is the plugin. Use it.
2. **At a repository root, or not in a plugin?** Look below the current directory for `SKILL.md` files and plugin manifests. Use your judgement about what is a real candidate. Skip test fixtures, examples and copies that agent tools install (for example `.claude/skills/`).
   - **One clear candidate:** use it. Tell the user its path.
   - **A few:** ask which one to evaluate. Describe each by path and what the skill does. Do not ask the user whether it is a plugin or a skill.
   - **Many, or no clear choice:** do not list them all. Ask the user which skill they want to evaluate, by name or path, and find it from their answer.
   - **None:** tell the user that evals need a `SKILL.md`, and suggest `tessl skill new` to write one.

If the chosen candidate is a skill with no plugin manifest in its directory or a parent, import it before you continue:
```bash
tessl skill import <skill-dir>
```
Tell the user that this adds only `<skill-dir>/.tessl-plugin/plugin.json`. From here on, `<skill-dir>` is the plugin path.

If you cannot ask the user (a non-interactive run), continue only with one clear candidate, importing it first if needed. Otherwise stop, and tell the user to run again from the skill's directory or to name the skill.

If the user provides a path inside a `.tessl/plugins/` directory (an installed plugin cache), stop and warn them: that path is Tessl's local install cache — running evals from there won't work and changes would be overwritten on the next `tessl install`. Offer two options: point to the original plugin source, or copy the plugin out of `.tessl/plugins/` to a new location (`cp -r .tessl/plugins/<workspace>/<plugin> ./<plugin>`).

## 1.2 Verify login

```bash
tessl whoami
```

If not logged in, ask the user to run `tessl login` before continuing.

## 1.3 Check for existing scenarios

Check if scenarios already exist in the plugin's `evals/` directory:
```bash
ls <plugin-dir>/evals/*/task.md 2>/dev/null
```

If scenarios exist, warn the user:

> "You already have scenarios in `evals/`. Options:
> 1. **Add more** — generate new scenarios alongside existing ones
> 2. **Replace all** — generate new scenarios and replace existing ones
> 3. **Skip generation** — just run evals on existing scenarios
>
> What would you prefer?"
