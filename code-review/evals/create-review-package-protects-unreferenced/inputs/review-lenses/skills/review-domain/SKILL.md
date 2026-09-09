---
name: review-domain
description: Review domain changes for invalid state transitions. Use as one lens in a code review run.
---

# Review lens: Domain transitions

Maintainer wording: transitions are valid only through the aggregate command.

Report a changed path that writes state without the aggregate command.
