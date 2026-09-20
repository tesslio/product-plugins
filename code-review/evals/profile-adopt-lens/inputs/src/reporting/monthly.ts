import { db } from '../db.js';

export async function monthlyTotals(accountIds: string[]) {
  const totals = [];
  for (const accountId of accountIds) {
    const rows = await db.query('SELECT sum(total_cents) FROM orders WHERE account_id = $1', [
      accountId,
    ]);
    totals.push({ accountId, total: rows[0].sum });
  }
  return totals;
}
