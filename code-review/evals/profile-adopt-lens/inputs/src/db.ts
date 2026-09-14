export const db = {
  async query(_sql: string, _params: unknown[]): Promise<{ sum: number }[]> {
    throw new Error('not implemented in this fixture');
  },
};
