# Evidence manifest

Cutoff: 2026-08-31. Window: 2 completed review rounds on 2 pull requests. Older
history and incident records were unavailable. Review bodies, replies, actor
kinds, reviewed head SHAs, and dispositions are included.

- PR 101, round 1, head `a111`, Tessl reviewer: `src/generated/payments-client.ts`
  logs a response body. Human reply: the file header names
  `tools/codegen/templates/client.ts` as its source, so the generated copy is
  overwritten and the template is the reviewable source. Refuted on `a111`.
- PR 108, round 1, head `b211`, Tessl reviewer: `src/generated/orders-client.ts`
  logs a response body. Human reply: this file carries the same generated
  header and is overwritten from `tools/codegen/templates/client.ts`; the
  template was reviewed instead. Refuted on `b211`.
