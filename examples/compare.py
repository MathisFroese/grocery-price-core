"""Runnable synthetic example; does not claim any current grocery price."""
from datetime import date
from decimal import Decimal

from grocery_price_core import (
    PriceKind, PriceObservation, SalesChannel, Unit, compare_unit_prices,
)

on = date(2026, 9, 19)
common = dict(
    product="synthetic oats", quantity=Decimal("500"), unit=Unit.G,
    channel=SalesChannel.IN_STORE, source="synthetic example", observed_on=on,
)
regular = PriceObservation(price=Decimal("1.50"), kind=PriceKind.REGULAR, **common)
offer = PriceObservation(
    price=Decimal("1.25"), kind=PriceKind.OFFER,
    offer_from=on, offer_through=on, **common,
)
result = compare_unit_prices(offer, regular, on=on)
print(result.status.value, result.cheaper, result.savings_per_unit, result.base_unit)
