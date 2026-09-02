# Review comments from the last quarter, per-row calls

PR 812, `src/billing/invoice-export.ts`
> This awaits `customers.get(row.customerId)` inside `rows.map`. On the big
> tenants that is 40k calls. We have `customers.getMany` for exactly this.

PR 877, `src/notifications/digest.ts`
> `for (const user of users) { await prefs.load(user.id) }`. Preferences are
> already joinable on the user query. This is the same thing we fixed in 812.

PR 903, `src/reports/usage.ts`
> One HTTP call per workspace per day in the window. 30 days x 2k workspaces.
> The metrics API takes a list of workspace ids.

PR 915, `src/auth/session.ts`
> Not a per-row problem: this loop is over at most 3 identity providers and the
> provider API has no batch form. Fine as is. Leaving the comment so nobody
> "fixes" it.

PR 921, `src/search/index.ts`
> Style only: prefer `for...of` here. (Not related to the incidents.)
