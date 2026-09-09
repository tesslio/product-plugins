---
name: review-security-and-privacy
description: Review trust boundaries and unauthorized disclosure. Use as one lens in a code review run.
---

# Review lens: Security and Privacy

Start at changed trust boundaries and trace controlled authority to sensitive
operations.

Maintainer note: service-to-service jobs authenticate through workload identity.

Report a plausible unauthorized operation. Do not report a smell without an
actor, controlled input, and reachable sink.
