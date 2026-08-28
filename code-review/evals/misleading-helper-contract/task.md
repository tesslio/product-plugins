# Review a workspace settings PR

Review this PR and flag any findings that should be addressed. Write only actionable findings to `review.md`.

This PR changes the workspace access helper and updates the settings route that calls it. The route also introduces a local `workspaceId` variable.

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
-  await settings.update(request.params.workspaceId, request.body);
+  const { workspaceId } = request.params;
+  assertWorkspaceAccess(request.auth.userId, workspaceId);
+  await settings.update(workspaceId, request.body);
   return reply.code(204).send();
 });
```
