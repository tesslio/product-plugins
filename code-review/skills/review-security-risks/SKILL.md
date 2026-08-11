---
name: review-security-risks
description: Review a diff for security risks across auth/authz, untrusted input, injection, output encoding, secrets, crypto, sensitive logging, file and network access, webhooks, and dependency or build-script changes. Use when reviewing a pull request, diff, or code change for security issues or vulnerabilities, as a security review lens in `tessl change review` or a GitHub Actions review workflow. Reports high-confidence, file-anchored findings and complements scanners (CodeQL, Snyk, Dependabot) rather than duplicating them.
---

# Review Security Risks

A security review lens for `tessl change review`. Review the diff for the risks
below and report concrete, actionable findings.

## Stance

- Review the diff first. Read surrounding code only when a line in the diff
  forces a security judgement you cannot make from the hunk alone.
- Keep findings high-confidence. Report a risk when you can name the untrusted
  input, the sink it reaches, and the impact.
- Complement scanners. Skip generic dependency-version or lint-style findings
  that CodeQL, Snyk, or Dependabot already cover; focus on logic and design
  risks a scanner misses.
- If you find no security issues, say so in one line.

## What to look for

1. **Auth and authz** — added endpoints, routes, jobs, or actions missing an
   authentication or authorization check; checks that trust a client-supplied
   identity, role, or tenant id; privilege boundaries widened.
2. **Untrusted input** — request bodies, query params, headers, CLI args, env
   vars, file contents, or webhook payloads used without validation before
   reaching a sink.
3. **Injection** — untrusted input concatenated into SQL, shell commands,
   file paths, URLs, template strings, or `eval`-like calls.
4. **Output encoding** — untrusted data rendered into HTML, logs, or responses
   without escaping; reflected or stored content that can carry script.
5. **Secrets** — credentials, tokens, or keys added to source, committed
   config, fixtures, or error messages; secrets passed where they can be
   logged.
6. **Crypto** — weak or home-grown algorithms, hardcoded keys or IVs, predictable
   randomness for security values, missing signature or token verification.
7. **Sensitive logging** — passwords, tokens, PII, or full request bodies
   written to logs or telemetry.
8. **File and network access** — path traversal from user input, writes outside
   an intended directory, SSRF from a user-controlled URL, overly broad file or
   network permissions.
9. **Webhooks** — inbound webhook handlers that skip signature or origin
   verification, or trust payload fields without checks.
10. **Dependency and build-script changes** — new or changed `postinstall` and
    build scripts, lockfile edits pulling unexpected sources, or CI steps that
    execute untrusted code or expose secrets.

## How to report

- Anchor each finding to the changed line that introduces the risk.
- Name the untrusted input, the sink, and the impact in one or two sentences.
- Prefix with a severity cue where helpful (e.g. "high:", "medium:").
- State the concrete fix (validate at this boundary, parameterize this query,
  move this secret to config), not generic advice.
