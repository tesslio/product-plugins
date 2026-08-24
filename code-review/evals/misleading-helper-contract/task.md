# Review an access helper diff

Use the code-review lens suite in this plugin to review the diff. Write only actionable findings to `review.md`.

In this codebase, helpers named `assert*` throw on failure. Callers do not usually inspect their return value.

```diff
diff --git a/src/auth/workspace-access.ts b/src/auth/workspace-access.ts
@@
-export async function assertWorkspaceAccess(userId: string, workspaceId: string) {
+export async function assertWorkspaceAccess(userId: string, workspaceId: string) {
   const membership = await memberships.find(userId, workspaceId);
-  if (!membership) {
-    throw new ForbiddenError('workspace access denied');
-  }
-  return membership;
+  return Boolean(membership);
 }
diff --git a/src/routes/settings.ts b/src/routes/settings.ts
@@
 app.patch('/workspaces/:workspaceId/settings', async (request, reply) => {
-  await assertWorkspaceAccess(request.auth.userId, request.params.workspaceId);
+  assertWorkspaceAccess(request.auth.userId, request.params.workspaceId);
   await settings.update(request.params.workspaceId, request.body);
   return reply.code(204).send();
 });
```
