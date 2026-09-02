export type Cart = { lines: Line[]; currency: string };
export type Line = { sku: string; unitCents: number; quantity: number };
export type Discount = { kind: 'percent' | 'fixed'; value: number };

export function roundCents(value: number): number {
  return Math.round(value);
}

export function lineTotal(line: Line, discount: Discount): number {
  const gross = line.unitCents * line.quantity;
  if (discount.kind === 'fixed') {
    return roundCents(Math.max(0, gross - discount.value));
  }
  return roundCents(gross * (1 - discount.value / 100));
}

export function applyDiscount(cart: Cart, discount: Discount): Cart {
  return {
    ...cart,
    lines: cart.lines.map((line) => ({ ...line, unitCents: lineTotal(line, discount) / line.quantity })),
  };
}
