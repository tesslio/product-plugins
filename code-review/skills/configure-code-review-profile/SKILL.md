---
name: configure-code-review-profile
description: Decides what a repository's Tessl Code Review reviews and writes the `.tessl-code-review.yml` profile that says so, covering which lenses run, which paths each lens sees, which paths are excluded from every lens, how hard reviewers think, and which findings request changes. Use when someone wants a lens routed at part of a repository, wants generated code, lockfiles, snapshots, or vendored directories kept out of reviews, wants to add a lens to what a repository already runs, wants reviews to stop blocking on minor findings, or asks where the Code Review config file lives and what it can say. Not for installing Code Review on a repository, and not for writing the lens itself.
---

# Configure a repository's Code Review profile

A repository decides what its reviews do in one file: `.tessl-code-review.yml`
at the repository root. The profile names the lenses the review runs, routes
each one at the paths it is good for, excludes the paths no lens should read,
and sets how hard the reviewers think and which findings request changes.

The Tessl Review GitHub App, the supported way Code Review runs on a
repository, discovers that file at that path on its own. Nothing has to select
it. A profile kept anywhere else, or under any other name, is read by nobody on
the App path. The CLI and the unsupported GitHub Action both take the path
explicitly instead, which
[references/profile-schema.md](references/profile-schema.md) covers.

This skill writes and changes that file. It does not install Code Review on a
repository, and it does not author lenses: a new lens is
`create-code-review-lens`, and this skill is where the finished lens is
selected and routed.

## Before anything else: a lens list is the whole review

`lenses` is the complete ordered set for the run, not an addition to a default
set. A profile that names one lens runs that lens and nothing else. There is no
merge with the four published defaults, and no warning that they stopped
running. This is the same trap `--skill` has on the command line, and it is the
most expensive mistake available here, because the review that results still
looks like a review: it arrives, it grades findings, it approves pull requests,
and the classes of bug the defaults used to catch simply stop being mentioned.

So adding a lens means writing out every lens the review should run, each one
pinned, with the new one among them. Leaving the profile out entirely is what
keeps the defaults.

## Procedure

### 1. Read the repository before deciding anything

The profile is a claim about a specific repository's shape, so gather the shape
first. Worth knowing before any key is written:

- **The top-level layout**, and which directories hold code a reviewer should
  read as opposed to content, fixtures, or configuration.
- **The languages and ecosystems present**, which decide what the generated and
  vendored paths are called here.
- **What changes.** The paths that appear most often in recent history are the
  paths the profile actually governs; a carefully routed lens over a directory
  nobody touches costs nothing and does nothing.
- **An existing profile.** If `.tessl-code-review.yml` is already there, this is
  a change to a running policy rather than a fresh one. Read what it selects
  now, and carry through anything the request does not ask you to change.
- **Lenses the repository keeps locally**, usually under a directory such as
  `review-lenses/`, which a profile references by path.

Do not interview the user about facts the repository answers. Ask only about the
things it cannot: whether a concern is worth a lens of its own, and how hard the
team wants reviews to push back.

### 2. Decide the lens set

Start from the four published defaults and change the set deliberately:

- Keep a default unless there is a reason to drop it. Dropping one is a decision
  to stop reviewing a dimension, and it should be stated as such to the user.
- Pin every registry reference. An unpinned ref resolves to whatever is
  published latest, which means the review's own instructions change without
  anyone editing the profile.
- Reference a local lens by a path relative to the profile, and keep it inside
  the repository.
- Count the lenses that will have work to do. Only lenses with at least one
  selected file in a given change count, and eight is the supported ceiling per
  run.

### 3. Route each lens with globs

A lens without `globs` reviews the whole change. Give a lens globs when it is
genuinely specialized: a lens about database migrations reads migrations, and
pointing it at the frontend spends a reviewer pass on files it has nothing to
say about.

Routing is honest about what a lens can see: each lens receives only its
selected files in its prompt and its diff tools, and it cannot reach the files
routed to another lens through those tools. So a lens whose judgment depends on
reading a caller must have the caller's path in its globs too.

The pattern rules, including ordered evaluation and what happens to a renamed
file, are in [references/profile-schema.md](references/profile-schema.md).

### 4. Bound the profile with `ignore`

`ignore` is the profile's exclusion list, and it is the half of a profile most
often left out. It is what keeps every lens off generated output, lockfiles,
snapshots, and vendored code, in one place, instead of each lens carrying its
own negations and one of them forgetting.

**Find what this repository excludes, do not paste a list.** Every candidate
pattern comes from something you observed in the repository in front of you:

- **Declared generated and vendored paths.** A `.gitattributes` file marking
  paths `linguist-generated` or `linguist-vendored` is the repository stating
  outright which files are not hand-written.
- **Codegen headers.** Search the tracked files for the banners generators
  write at the top of their output, such as a "do not edit" line or a
  `@generated` marker, and take the directories and extensions they cluster in.
- **Lockfiles**, named whatever this ecosystem names them. A lockfile diff is
  large, mechanical, and reviewed by nobody.
- **Snapshots and golden fixtures.** Snapshot directories, approved-output
  files, and `testdata` trees are expected to change whenever the thing they
  record changes, and a reviewer reading them reviews the recording rather than
  the change.
- **Vendored dependencies**, usually a directory holding third-party source
  copied into the repository.
- **Committed build output.** Only committed output is worth a pattern. Output
  that is ignored by git never appears in a change at all, so a pattern for it
  can never match anything.

Check each pattern against the repository's tracked files before writing it
down, because both ways of getting a pattern wrong are expensive and neither is
visible in a review:

- **A pattern that matches nothing is dead config.** It reads as protection,
  gets copied into the next repository, and excludes nothing.
- **A pattern that matches real source silently hides code from every lens.**
  The review still runs, still grades, and still approves. Nothing in its output
  says a file was never read. An over-broad `ignore` is therefore a way to turn
  reviews off by accident and keep the reassurance of receiving them.

The constraints the parser enforces, which shape how these patterns can be
written, are in [references/profile-schema.md](references/profile-schema.md).
The ones worth knowing before drafting: every pattern is positive and excludes
what it matches, so a leading `!` is rejected; a bare `**` is rejected; at most
64 patterns; and `ignore` applies to every lens, including one that declares no
`globs` of its own, and overrides anything a lens selected.

### 5. Check the profile

Run the checker against the file you wrote:

```bash
tessl code review check-profile
```

It costs no credits and runs no model. It reports schema errors, how many files
each lens selects, globs that match nothing, ignore patterns that match nothing,
and whether the run would end skipped because no lens matched.

Act on what it reports rather than noting it:

- **A lens selecting zero files is a defect, not a warning.** Either its globs
  are wrong, or `ignore` is subtracting the paths it was pointed at, or the lens
  does not belong in this profile. Fix the cause; do not leave a lens in the
  file that reviews nothing.
- **A pattern matching nothing asks two different questions, and only one of
  them is a defect.** A pattern that matches nothing in the repository's tracked
  files is dead config: it protects nothing, and it is a typo until proven
  otherwise, so check the spelling, the leading directory, and the case, which
  patterns are sensitive to. A pattern that merely matches nothing in the change
  being checked is ordinary and means nothing on its own, because a sound
  `node_modules/**` matches nothing whenever the change leaves `node_modules`
  alone. Read which of the two the report is telling you before changing a
  pattern, and change nothing on the second.
- **A run that would be skipped for no matching lenses** means this profile
  reviews nothing for that change. That is fine when the change is entirely
  generated output, and a mistake otherwise.

A profile that has not been checked is a draft, whatever it looks like on the
page. Say so rather than handing it over as finished.

### 6. Explain what was installed

Close by telling the user what the file now decides, in their terms: which
lenses run, what each one reads, what nothing reads, whether findings block and
at what severity, and which of the published defaults are no longer running if
any. Say where the file has to live for the App to find it, and that the profile
takes effect on the review of the pull request that changes it, so a change that
narrows routing or widens `ignore` applies to itself.

## What not to do here

- Do not put a profile anywhere but the repository root when the App is the
  consumer. A profile at another path is not an alternative layout; it is a file
  nothing reads.
- Do not write a lens here. Draft, run, and tune a lens with
  `create-code-review-lens`, then come back to select it.
- Do not use `ignore` to quiet a noisy lens. Excluding paths stops every lens
  reading them, and the lens is still noisy everywhere else. A noisy lens is a
  threshold problem, and it is fixed in the lens.
- Do not set `model`, `supervisorModel`, or `supervisorEffort` to solve a review
  quality problem. They are restricted, so a run whose profile sets them is
  refused for most accounts.
- Do not claim a profile works because it parses. Parsing says the keys are
  spelled correctly; the check says the routing selects the files you meant.
