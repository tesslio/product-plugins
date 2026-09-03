# PR 58: Round discounted line totals to whole cents

Line totals after a discount were carrying fractional cents into the invoice.
This change adds `roundCents` and applies it in `applyDiscount`. Nothing else
in the cart module is in scope; tax rounding has its own ticket.
