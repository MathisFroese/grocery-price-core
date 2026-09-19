"""Deterministic price comparison without fabricating missing information.

All currency amounts use ``Decimal``. This library performs no scraping, API calls,
location lookup, or inference about whether a pickup price equals an in-store price.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class PriceKind(str, Enum):
    REGULAR = "regular"
    OFFER = "offer"
    LAST_PAID = "last_paid"
    ESTIMATE = "estimate"


class SalesChannel(str, Enum):
    IN_STORE = "in_store"
    ONLINE = "online"
    PICKUP = "pickup"


class Unit(str, Enum):
    G = "g"
    KG = "kg"
    ML = "ml"
    L = "l"
    PIECE = "piece"


class Availability(str, Enum):
    COMPARABLE = "comparable"
    UNKNOWN_PRICE = "unknown_price"
    INCOMPATIBLE_UNIT = "incompatible_unit"
    DIFFERENT_CHANNEL = "different_channel"
    INACTIVE_OFFER = "inactive_offer"
    NOT_VERIFIED = "not_verified"


def _positive(value: Decimal, field: str) -> None:
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise ValueError(f"{field} must be a finite positive Decimal")


@dataclass(frozen=True)
class PriceObservation:
    """A source-backed price for a package, not necessarily a shelf price.

    ``price=None`` represents a genuinely unknown price. Estimates and historical
    purchases are retained for display but excluded from verified comparisons.
    """

    product: str
    price: Optional[Decimal]
    quantity: Decimal
    unit: Unit
    kind: Optional[PriceKind]
    channel: SalesChannel
    source: str
    observed_on: date
    store_id: Optional[str] = None
    offer_from: Optional[date] = None
    offer_through: Optional[date] = None

    def __post_init__(self) -> None:
        if not self.product.strip():
            raise ValueError("product must not be empty")
        if not self.source.strip():
            raise ValueError("source must not be empty")
        _positive(self.quantity, "quantity")
        if self.price is None:
            if self.kind is not None:
                raise ValueError("unknown prices must have kind=None")
        else:
            _positive(self.price, "price")
            if self.kind is None:
                raise ValueError("known prices must have a kind")
        if self.offer_from or self.offer_through:
            if self.kind is not PriceKind.OFFER:
                raise ValueError("validity dates are permitted only for offers")
            if not self.offer_from or not self.offer_through:
                raise ValueError("an offer requires both validity dates")
            if self.offer_from > self.offer_through:
                raise ValueError("offer_from must not be after offer_through")
        if self.kind is PriceKind.OFFER and (not self.offer_from or not self.offer_through):
            raise ValueError("offers require explicit validity dates")


def normalize_unit_price(observation: PriceObservation) -> Optional[tuple[Decimal, str]]:
    """Price per kilogram, litre, or piece; unknown stays unknown.

    Values are exact Decimal divisions and are not rounded until presentation.
    """
    if observation.price is None:
        return None
    per = {
        Unit.G: (Decimal("1000"), "kg"),
        Unit.KG: (Decimal("1"), "kg"),
        Unit.ML: (Decimal("1000"), "l"),
        Unit.L: (Decimal("1"), "l"),
        Unit.PIECE: (Decimal("1"), "piece"),
    }
    multiplier, base_unit = per[observation.unit]
    return observation.price * multiplier / observation.quantity, base_unit


def effective_price(
    observation: PriceObservation,
    *,
    on: date,
    allow_estimates: bool = False,
) -> tuple[Availability, Optional[tuple[Decimal, str]]]:
    """Validate whether a price can be used for the specified date.

    Historical/estimated values are never silently promoted to verified prices.
    """
    if observation.price is None:
        return Availability.UNKNOWN_PRICE, None
    if observation.kind in (PriceKind.ESTIMATE, PriceKind.LAST_PAID) and not allow_estimates:
        return Availability.NOT_VERIFIED, None
    if observation.kind is PriceKind.OFFER and not (
        observation.offer_from <= on <= observation.offer_through
    ):
        return Availability.INACTIVE_OFFER, None
    return Availability.COMPARABLE, normalize_unit_price(observation)


@dataclass(frozen=True)
class UnitComparison:
    status: Availability
    left_per_unit: Optional[Decimal] = None
    right_per_unit: Optional[Decimal] = None
    base_unit: Optional[str] = None
    cheaper: Optional[str] = None
    savings_per_unit: Optional[Decimal] = None


def compare_unit_prices(
    left: PriceObservation,
    right: PriceObservation,
    *,
    on: date,
    allow_estimates: bool = False,
    allow_cross_channel: bool = False,
) -> UnitComparison:
    """Compare equivalent goods only; caller must check product equivalence.

    A different sales channel requires explicit opt-in. Missing prices, expired
    offers and incompatible units return a status rather than invented savings.
    """
    a_status, a = effective_price(left, on=on, allow_estimates=allow_estimates)
    b_status, b = effective_price(right, on=on, allow_estimates=allow_estimates)
    if a_status is not Availability.COMPARABLE:
        return UnitComparison(a_status)
    if b_status is not Availability.COMPARABLE:
        return UnitComparison(b_status)
    if not allow_cross_channel and left.channel is not right.channel:
        return UnitComparison(Availability.DIFFERENT_CHANNEL)
    if a[1] != b[1]:
        return UnitComparison(Availability.INCOMPATIBLE_UNIT)
    cheaper = "left" if a[0] < b[0] else "right" if b[0] < a[0] else "equal"
    return UnitComparison(
        status=Availability.COMPARABLE,
        left_per_unit=a[0],
        right_per_unit=b[0],
        base_unit=a[1],
        cheaper=cheaper,
        savings_per_unit=abs(a[0] - b[0]),
    )
