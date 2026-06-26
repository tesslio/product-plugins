# API Scaffolder Skill

## When to use this skill
Use this skill when a user asks to create, scaffold, or bootstrap a new REST API endpoint or service.

## Steps

1. Ask (or infer from context) the resource name, HTTP methods needed, and whether auth is required.
2. Create the route handler file at `src/routes/<resource>.ts`.
3. Define request and response types in `src/types/<resource>.ts`.
4. Add the route to the main router in `src/router.ts`.
5. Write a brief integration test at `tests/<resource>.test.ts` that covers at least GET and POST.
6. Update `README.md` with a one-line entry in the "Endpoints" table.

## Important notes
- Use the project's existing HTTP framework (Express, Fastify, Flask, Gin — detect from dependencies).
- Always validate incoming request bodies using the project's existing validation library.
- Return standard HTTP status codes: 200 for success, 201 for created, 400 for bad input, 404 for not found, 500 for unexpected errors.
- Never store credentials or secrets in route handlers — read from environment variables.
- If the resource name conflicts with an existing route, warn the user before proceeding.
