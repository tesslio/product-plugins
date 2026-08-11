# Legibility anti-patterns

Each pattern fails the cold-reader test, the from-scratch test, or both. The fix
is always a code change, never a comment.

## Names

- **Names that mislead.** A name reflects intent at writing time, not current
  behaviour, so names lie as code evolves. Examples: a function scoped to one
  subject, later widened but still named for the original subject; a translator
  whose name doesn't say which direction it converts. If a reader must read the
  body to learn the name was wrong, the name failed. Fix: rename or restructure.
- **Dressed-up old concepts.** When a refactor removes a concept, the new code
  shouldn't carry a renamed version of it. Ask whether the distinction is still
  meaningful, or whether you are just relabeling the old design.
- **Names describing history, not behaviour.** `oldFooHandler` or `legacyFoo` is
  only acceptable when a current `foo` exists alongside it. A lone `legacyFoo`
  with no `foo` is just `foo`.
- **Change-relative comments and names.** Anything only a reader of the diff,
  the git history, or this ticket can decode: past-shape references ("same as
  the previous shape"), change-relative framing ("the new scheme", "now that…",
  "previously", "no longer"), and planning labels ("V2", "phase N", "the
  migration"). This is a test, not a word list — ask whether the term would mean
  anything to someone who never saw this change. Fix: describe what the code
  does now; context about the change belongs in the PR description.
- **Comments naming distant code.** A comment in one file that names a symbol in
  another. The named symbol gets renamed or deleted; the comment doesn't. Fix:
  describe the behaviour without naming the distant symbol, or delete the
  comment.

## Types and signatures

- **Opaque collection types.** `Record<string, X>`, `Map<string, Y>`, or plain
  string-tuple arrays hide what the key means and what an entry represents. Fix:
  name the types (`type FixtureName = string`), wrap the relationship in a
  struct so the key has a name, or eliminate the helper that produced the opaque
  shape so the caller iterates the keyed structure where the key's role is
  obvious.
- **Signatures whose meaning depends on the caller.** A signature should
  constrain intent. If a reader must know which caller passed the arguments to
  interpret them, the signature is too loose — e.g. `process(input, mode)` where
  `mode` is an untyped tag, or a function returning a generic map tagged with a
  `source` flag the caller re-branches on. Fix: narrow parameter types to a
  literal union, split the function so each branch has a precise name, or push
  the work into the caller so the context lives in the loop.

## Structure

- **Information round-trips.** A helper flattens a structure and erases source
  information; the caller immediately recovers it via a flag on each entry. Fix:
  dissolve the helper and let the caller iterate each source in its own loop —
  the loop context is the source marker.
- **Single-consumer helpers nobody can read in isolation.** A helper file used
  by exactly one caller, named after internal mechanics. `lib/` means shared,
  not "where this file ended up": one consumer means colocate, multiple
  consumers means a shared module is right. Fix: inline; if the caller's body
  gets unwieldy, use a file-local private helper named in the caller's
  vocabulary rather than a separate module.
- **Inscrutable function bodies.** A long body with no internal structure where
  the reader must hold the whole sequence in their head. Fix: split into named
  local functions that show the phases. Counter-rule: don't over-extract — a
  short block doing one thing is fine inline. The test is "would a reader
  skimming need to slow down here?", not line count.
- **Vestigial abstractions.** Function pairs, split modules, or wrapper-and-core
  kept because of a distinction that no longer matters (`doThingInternal` vs
  `doThing` when the wrapper is gone; an interface with one implementation and
  no other planned). If the reason for the split is gone, collapse it.
- **A new general mechanism that doesn't absorb its special cases.** Adding a
  capability that overlaps existing behaviour invites bolting the new path on
  beside the old one, leaving two paths that build the same artifact and can
  diverge. Triggers: the same output type produced by two paths; a "default"
  written as separate code when it is a special case of the new mechanism; more
  than one way to specify the same concept. Fix: check whether the new primitive
  subsumes the old, and if so delete the old path.
- **Files whose exports don't say what the file is for.** A file's exports
  should describe the file's job; an internal helper named in the eventual
  caller's vocabulary muddies the file's surface. Fix: rename the helper to fit
  the file's frame, or inline it so the caller's domain words stay at the call
  site.

## Validation

- **Validate at the layer where it's possible.** Pre-validation that pretends to
  check something it cannot (runtime state, downstream resolution, content not
  yet present) is worse than none — it misleads readers and gives false comfort.
  Fix: move the check to the layer that owns the necessary context.

## Legitimate exceptions

Opacity is fundamental, not sediment, in a few cases — do not flag these:

- Generic library code: a `Result<T, E>` is opaque on purpose.
- Tight inner loops: three lines inlined can be clearer than a named function.
- Pure mathematical primitives: `dot(a, b)` need not spell out its arguments.
