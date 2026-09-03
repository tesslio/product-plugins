# PR 301 (hotfix): stop the CSV importer crashing on a trailing newline

Production incident INC-77. One-line fix in `src/import/csv.ts`. Per the hotfix
rule, tests land in the follow-up PR tracked as issue 302.
