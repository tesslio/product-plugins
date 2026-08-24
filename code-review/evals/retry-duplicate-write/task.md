# Review a retrying payment worker diff

Use the code-review lens suite in this plugin to review the diff. Write only actionable findings to `review.md`.

The job runner retries failed jobs with the same `job.id`. The payment provider charges immediately and may return a network error after accepting the charge.

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
+  await payments.charge({
+    customerId: invoice.customerId,
+    amountCents: invoice.amountCents,
+  });

   await invoices.markPaid(invoice.id);
 }
```
