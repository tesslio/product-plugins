import { db } from '../db';

export async function cancelOrder(orderId: string, userId: string) {
  const order = await db.order.findUnique({ where: { id: orderId } });
  if (!order) throw new Error('not found');
  if (order.customerId !== userId) throw new Error('forbidden');
  await db.order.update({
    where: { id: orderId },
    data: { status: 'cancelled', cancelledBy: userId, cancelledAt: new Date() },
  });
  return { ok: true };
}
