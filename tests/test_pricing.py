import unittest
from datetime import date
from decimal import Decimal

from grocery_price_core import (
    Availability, PriceObservation, PriceKind, SalesChannel, Unit,
    compare_unit_prices, effective_price, normalize_unit_price,
)

TODAY = date(2026, 9, 19)


def price(amount, quantity="500", unit=Unit.G, kind=PriceKind.REGULAR, channel=SalesChannel.IN_STORE, **kwargs):
    return PriceObservation(
        product="example oats", price=None if amount is None else Decimal(amount),
        quantity=Decimal(quantity), unit=unit, kind=kind, channel=channel,
        source="synthetic test fixture", observed_on=TODAY, **kwargs,
    )


class PricingTests(unittest.TestCase):
    def test_mass_conversion(self):
        self.assertEqual(normalize_unit_price(price("1.20")), (Decimal("2.40"), "kg"))
        self.assertEqual(normalize_unit_price(price("2.40", "1", Unit.KG)), (Decimal("2.40"), "kg"))

    def test_volume_conversion(self):
        self.assertEqual(normalize_unit_price(price("0.90", "500", Unit.ML)), (Decimal("1.80"), "l"))

    def test_unknown_stays_unknown(self):
        obs = price(None, kind=None)
        self.assertIsNone(normalize_unit_price(obs))
        self.assertEqual(compare_unit_prices(obs, price("2"), on=TODAY).status, Availability.UNKNOWN_PRICE)

    def test_offer_validity_is_inclusive(self):
        obs = price("1.49", kind=PriceKind.OFFER, offer_from=TODAY, offer_through=TODAY)
        self.assertEqual(effective_price(obs, on=TODAY)[0], Availability.COMPARABLE)
        self.assertEqual(effective_price(obs, on=date(2026, 9, 20))[0], Availability.INACTIVE_OFFER)

    def test_estimates_and_last_paid_require_opt_in(self):
        for kind in (PriceKind.ESTIMATE, PriceKind.LAST_PAID):
            obs = price("1", kind=kind)
            self.assertEqual(effective_price(obs, on=TODAY)[0], Availability.NOT_VERIFIED)
            self.assertEqual(effective_price(obs, on=TODAY, allow_estimates=True)[0], Availability.COMPARABLE)

    def test_cross_channel_not_assumed_equal(self):
        pickup = price("1.00", channel=SalesChannel.PICKUP)
        shelf = price("2.00")
        self.assertEqual(compare_unit_prices(pickup, shelf, on=TODAY).status, Availability.DIFFERENT_CHANNEL)
        self.assertEqual(compare_unit_prices(pickup, shelf, on=TODAY, allow_cross_channel=True).cheaper, "left")

    def test_mismatched_unit_is_not_compared(self):
        self.assertEqual(compare_unit_prices(price("2"), price("2", "1", Unit.PIECE), on=TODAY).status, Availability.INCOMPATIBLE_UNIT)

    def test_exact_savings_no_rounding(self):
        result = compare_unit_prices(price("1.25"), price("1.50"), on=TODAY)
        self.assertEqual(result.savings_per_unit, Decimal("0.50"))
        self.assertEqual(result.base_unit, "kg")
        self.assertEqual(result.cheaper, "left")

    def test_same_unit_price_is_equal(self):
        result = compare_unit_prices(price("1.00"), price("2.00", "1", Unit.KG), on=TODAY)
        self.assertEqual(result.cheaper, "equal")
        self.assertEqual(result.savings_per_unit, Decimal("0.00"))

    def test_invalid_amounts_rejected(self):
        for invalid in ("0", "-1", "NaN", "Infinity"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    price(invalid)
        with self.assertRaises(ValueError):
            price("1", "0")

    def test_regular_and_active_offer_can_be_compared_without_relabeling(self):
        offer = price("0.99", kind=PriceKind.OFFER, offer_from=TODAY, offer_through=TODAY)
        regular = price("1.49", kind=PriceKind.REGULAR)
        result = compare_unit_prices(offer, regular, on=TODAY)
        self.assertEqual(result.status, Availability.COMPARABLE)
        self.assertEqual(result.cheaper, "left")
        self.assertEqual(offer.kind, PriceKind.OFFER)
        self.assertEqual(regular.kind, PriceKind.REGULAR)

    def test_expired_offer_never_becomes_regular_price(self):
        old = price("0.99", kind=PriceKind.OFFER,
                    offer_from=date(2026, 9, 1), offer_through=date(2026, 9, 7))
        result = compare_unit_prices(old, price("1.49"), on=TODAY)
        self.assertEqual(result.status, Availability.INACTIVE_OFFER)
        self.assertIsNone(result.savings_per_unit)

    def test_unknown_counterpart_never_implies_savings(self):
        result = compare_unit_prices(price("1.49"), price(None, kind=None), on=TODAY)
        self.assertEqual(result.status, Availability.UNKNOWN_PRICE)
        self.assertIsNone(result.savings_per_unit)

    def test_offer_requires_dates(self):
        with self.assertRaises(ValueError):
            price("1", kind=PriceKind.OFFER)
        with self.assertRaises(ValueError):
            price("1", kind=PriceKind.REGULAR, offer_from=TODAY, offer_through=TODAY)

    def test_unknown_cannot_have_price_kind(self):
        with self.assertRaises(ValueError):
            price(None)


if __name__ == "__main__":
    unittest.main()
