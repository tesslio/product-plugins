# schedule-setup

Create a repo-defined schedule in a project's `tessl.json` from a plain-language description.

Describe the task, cadence, and environment in plain words. The skill chooses the most readable supported schedule format, adds and validates the entry, and explains what happens on push. If you don't have a skill for the task yet, it can author a repo-local one with credential pre-flight checks.

Install it with:

```bash
tessl install tessl/schedule-setup
```
