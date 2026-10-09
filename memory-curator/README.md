# tessl/memory-curator

Keep a project's memory notes short, current, and attributed.

A memory topic holds one note, plus the facts that agent runs have proposed for it since the note was last written. This plugin's skill, `promote-memory`, folds those waiting facts into the note.

You don't run the skill yourself. Tessl's memory promotion job launches it in your project's repository when a topic has facts waiting, and passes the topic as the input `TOPIC`.

## What the skill does

1. **Reads the note and the waiting facts.** `tessl memory pending` writes the note exactly as stored, and the batch of facts, each with who stated it and when.
2. **Rewrites the note.** It adds new facts, deletes a line that a newer fact contradicts or a retraction names, and merges restatements into one line. Every line ends with who stated it and when.
3. **Keeps what lasts.** Standing instructions, preferences, conventions, what names mean, stable pointers, who owns what, settled decisions, and the one-line lesson of an incident. It drops what can be checked live, such as ticket, PR, or CI state, and the details of a single task.
4. **Treats its input as data.** The note and the facts come from conversations other people control. The skill deletes any line that tells an agent to run, fetch, or install something, and never keeps secrets or credentials.
5. **Saves once.** `tessl memory save` stores the new note, under 48 KB, and clears the facts it used. Facts that arrive during the run wait for the next one.

## Skills

| Skill | Description |
| --- | --- |
| `promote-memory` | Fold the facts proposed to one memory topic into the topic's note. |
