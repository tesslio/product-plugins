# Review a batch export diff

Use the code-review lens suite in this plugin to review the diff. Write only actionable findings to `review.md`.

The export endpoint is used by large workspaces and commonly exports 20,000 rows. `users.get` is a remote service call.

```diff
diff --git a/src/export/audit-log.ts b/src/export/audit-log.ts
@@
 export async function buildAuditExport(workspaceId: string) {
   const rows = await auditLog.listForWorkspace(workspaceId);
-  const users = await users.getMany([...new Set(rows.map((row) => row.actorId))]);
-  const userById = new Map(users.map((user) => [user.id, user]));

   return Promise.all(rows.map(async (row) => {
+    const actor = await users.get(row.actorId);
     return {
       timestamp: row.createdAt,
-      actorEmail: userById.get(row.actorId)?.email ?? 'unknown',
+      actorEmail: actor?.email ?? 'unknown',
       action: row.action,
     };
   }));
 }
```
