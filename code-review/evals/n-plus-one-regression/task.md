# Review an audit export PR

Review this PR and flag any findings that should be addressed. Write only actionable findings to `review.md`.

The audit export is used by large workspaces. `users` is the profile-service client, `users.getMany` accepts at most 500 ids per call, and the export includes a timestamp field.

```diff
diff --git a/src/export/audit-log.ts b/src/export/audit-log.ts
@@
 export async function buildAuditExport(workspaceId: string) {
   const rows = await auditLog.listForWorkspace(workspaceId, { limit: 20_000 });
-  const actorIds = [...new Set(rows.map((row) => row.actorId))];
-  const batches = chunk(actorIds, 500);
-  const usersByBatch = await Promise.all(batches.map((ids) => users.getMany(ids)));
-  const userById = new Map(usersByBatch.flat().map((user) => [user.id, user]));

   return Promise.all(rows.map(async (row) => {
+    const actor = await users.get(row.actorId);
     return {
-      timestamp: row.createdAt,
-      actorEmail: userById.get(row.actorId)?.email ?? 'unknown',
+      timestamp: row.createdAt.toISOString(),
+      actorEmail: actor?.email ?? 'unknown',
       action: row.action,
     };
   }));
 }
```
