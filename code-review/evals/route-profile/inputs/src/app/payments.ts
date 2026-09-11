export async function chargeCard(orderId: string, amountCents: number) {
  const response = await fetch('https://payments.example.com/charges', {
    method: 'POST',
    body: JSON.stringify({ orderId, amountCents }),
  });
  return (await response.json()) as { id: string };
}
