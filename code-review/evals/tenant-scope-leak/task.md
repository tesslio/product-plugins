# Review a tenant-scoped API diff

Use the code-review lens suite in this plugin to review the diff. Write only actionable findings to `review.md`.

The service stores projects for multiple workspaces. Every request has `request.auth.workspaceId`, and callers may only see projects in their own workspace.

```diff
diff --git a/src/routes/projects.ts b/src/routes/projects.ts
@@
 app.get('/projects/:projectId', async (request, reply) => {
   const { projectId } = request.params;
-  const project = await db.project.findFirst({
-    where: {
-      id: projectId,
-      workspaceId: request.auth.workspaceId,
-    },
-  });
+  const project = await db.project.findUnique({
+    where: { id: projectId },
+  });

   if (!project) {
     return reply.code(404).send({ error: 'not found' });
   }

   return reply.send({
     id: project.id,
     name: project.name,
     billingEmail: project.billingEmail,
   });
 });
```
