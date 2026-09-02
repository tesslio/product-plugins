# PR 214: Let customers cancel an order from the order page

Adds `cancelOrder` and wires it to `POST /orders/:id/cancel`. Cancelling sets the
status to cancelled and records who did it. Refund processing is untouched and
stays on its existing path.
