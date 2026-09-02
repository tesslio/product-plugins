import { processor } from '../payments';

export async function refundOrder(orderId: string, amountCents: number) {
  return processor.refund({ orderId, amountCents });
}
