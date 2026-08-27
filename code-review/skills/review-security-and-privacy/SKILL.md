---
name: review-security-and-privacy
description: Review a code change for trust-boundary, authorization, injection, secret-handling, logging, and privacy disclosure risks. Use when reviewing for security, privacy, vulnerabilities, auth bugs, secrets in logs, sensitive-data exposure, or PII disclosure.
---

# Review lens: Security and Privacy

Review changes at trust boundaries: places where data, code, or authority moves between components, users, or systems.

## Scope

- **Security** Who can reach what, and what an untrusted input can do once it lands.
- **Privacy** What the change discloses, and to whom.

## Method

Start from the boundaries the change touches rather than reading the diff in file order. Trace untrusted input to the operations it can influence, including indirectly executed code.

Follow the data outward as well: what each new field, log line, error message, or response body reveals, and who becomes able to see it.

Do not report a security smell without an exploit path through the changed code. Name the actor, the input or authority they control, and the sink or disclosure they can reach.

## Threshold

Report a finding when an untrusted input can reach a sensitive operation, or when data can be disclosed to a party that is not entitled to receive it.

Do not report hypothetical risks without a plausible path through the changed code.

## Reporting

- Name the untrusted input or controlled authority, the sink or disclosure it reaches, and the impact, in one or two sentences.
- State the concrete fix: validate at this boundary, parameterize this query, escape this output, move this secret to config. Not generic advice.
- If coverage is warranted, name the exact actor, resource, or data boundary case to test rather than asking generally for more security tests.
