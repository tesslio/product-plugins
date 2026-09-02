export function formatPrice(cents: number, symbol: string): string {
  const units = cents / 100;
  return `${symbol}${units}`;
}
