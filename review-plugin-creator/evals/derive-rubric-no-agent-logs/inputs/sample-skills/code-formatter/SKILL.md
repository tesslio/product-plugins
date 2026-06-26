# Code Formatter Skill

## When to use this skill
Use this skill whenever a user asks to format, lint, or clean up source code files.

## Steps

1. Identify the language of the code files provided.
2. Apply the project's formatting rules (from `.editorconfig` or `.prettierrc` if present).
3. Run the formatter with `--write` to apply changes in-place.
4. Report which files were changed and how many lines were modified.

## Important notes
- Always preserve semantic meaning — never alter logic while formatting.
- For TypeScript and JavaScript, use Prettier. For Python, use black. For Go, use gofmt.
- If no config file is present, use 2-space indentation for JS/TS, 4-space for Python.
- Do not format generated files (e.g., files in `dist/`, `build/`, or `__generated__/`).
