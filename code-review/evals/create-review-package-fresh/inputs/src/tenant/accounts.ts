export async function getAccount(context: { tenantId: string }, id: string) {
  return database.accounts.find({ tenantId: context.tenantId, id });
}
