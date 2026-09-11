import { chargeCard } from './payments.js';

export async function checkout(orderId: string, amountCents: number) {
  const receipt = await chargeCard(orderId, amountCents);
  return { orderId, receiptId: receipt.id };
}
