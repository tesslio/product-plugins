# Review an invoice worker PR

Review this PR and flag any findings that should be addressed. Write only actionable findings to `review.md`.

This worker runs from a queue that retries failed jobs with the same `job.id`. `payments` is an external provider client; its request can be accepted by the provider even when the client sees a transient transport error. The PR also adds a `description` field to the payment request.

```diff
diff --git a/src/jobs/collect-invoice.ts b/src/jobs/collect-invoice.ts
@@
 export async function collectInvoice(job: InvoiceJob) {
   const invoice = await invoices.get(job.invoiceId);
   if (invoice.status === 'paid') return;

-  await payments.charge({
-    idempotencyKey: `invoice:${invoice.id}`,
-    customerId: invoice.customerId,
-    amountCents: invoice.amountCents,
-  });
+  const description = `Invoice ${invoice.number}`;
+  await payments.charge({
+    customerId: invoice.customerId,
+    amountCents: invoice.amountCents,
+    description,
+  });

   await invoices.markPaid(invoice.id);
 }
```
