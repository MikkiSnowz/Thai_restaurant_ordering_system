"""Money and order-total calculations.

All money is stored as integer cents so totals are exact
(the original app stored floats like 107.406).
"""
from dataclasses import dataclass


def percent_of(cents: int, percent: int) -> int:
    """percent% of cents, rounded half-up to the nearest cent."""
    if cents < 0 or percent < 0:
        raise ValueError("cents and percent must be non-negative")
    return (cents * percent + 50) // 100


def format_money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100:,}.{cents % 100:02d}"


@dataclass(frozen=True)
class Totals:
    subtotal: int
    discount: int
    surcharge: int
    total: int


def calculate_totals(
    lines,
    discount_applied: bool,
    surcharge_applied: bool,
    discount_percent: int,
    surcharge_percent: int,
) -> Totals:
    """lines: iterable of (unit_price_cents, quantity).

    The discount is taken off the subtotal once; the surcharge is then added
    once on the discounted amount. Neither can be stacked.
    """
    subtotal = 0
    for unit_price, qty in lines:
        if unit_price < 0 or qty < 0:
            raise ValueError("price and quantity must be non-negative")
        subtotal += unit_price * qty
    discount = percent_of(subtotal, discount_percent) if discount_applied else 0
    after_discount = subtotal - discount
    surcharge = percent_of(after_discount, surcharge_percent) if surcharge_applied else 0
    return Totals(subtotal, discount, surcharge, after_discount + surcharge)
