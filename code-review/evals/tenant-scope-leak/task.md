# Review a project lookup PR

Review this PR and flag any findings that should be addressed. Write only actionable findings to `review.md`.

Projects are stored by workspace, and each request carries `request.auth.workspaceId`. This PR switches the lookup helper used by the route and also trims project names before returning them.

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
-    name: project.name,
+    name: project.name.trim(),
     billingEmail: project.billingEmail,
   });
 });
```
