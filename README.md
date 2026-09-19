# Grocery Price Core

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, **independent MIT-licensed Python library** for price comparisons that do not turn offers, estimates, unknown prices, or pickup prices into verified in-store regular prices. Its goal is a reusable foundation for trustworthy grocery and accessibility-focused shopping applications.

**Status:** initial standalone library (`0.1.0`); not yet published to PyPI and with no claimed external adoption. The private Kühlschrank application, its code, scraping integrations, product catalogs, personal information, and Git history are **not** included or licensed here.

## What it does

- Compares unit prices per kg, litre, or piece using `Decimal` arithmetic.
- Keeps regular, offer, estimate, last-paid, and unknown price semantics distinct.
- Checks offer validity dates and explicitly tracks sales channels.
- Refuses to manufacture savings figures from incomplete evidence.
- Has zero runtime dependencies and makes no network requests.

## Run the tests

Requires Python 3.10+; no external services, accounts, keys or retailer data required:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Try the self-contained synthetic example with `PYTHONPATH=src python examples/compare.py`.

To install the package in an environment with setuptools available:

```bash
python -m pip install .
```

## Example — synthetic prices only

```python
from datetime import date
from decimal import Decimal
from grocery_price_core import PriceObservation, PriceKind, SalesChannel, Unit, compare_unit_prices

common = dict(product="oats", quantity=Decimal("500"), unit=Unit.G,
              kind=PriceKind.REGULAR, channel=SalesChannel.IN_STORE,
              source="synthetic example", observed_on=date(2026, 9, 19))
left = PriceObservation(price=Decimal("1.25"), **common)
right = PriceObservation(price=Decimal("1.50"), **common)
result = compare_unit_prices(left, right, on=date(2026, 9, 19))
print(result.status.value, result.cheaper, result.savings_per_unit, result.base_unit)
# comparable left 0.50 kg
```

The caller must establish that goods are genuinely equivalent. This package does not infer product identity from names or brands, check retailer coverage, guarantee current shelf prices, or round non-terminating divisions for display. A price's source and observation date are recorded; the caller must decide whether a non-offer observation is fresh enough for the intended use.

## The wider vision: from pantry to plate

> **Do not ask people to become better organizers; reduce how much organizing they have to do.**

Grocery Price Core is one small, reusable building block for a future **360-degree food-planning experience**. An application built around that vision could:

1. Scan barcodes to help record what is in the fridge and pantry, with an easy way to correct missing or uncertain information.
2. Track quantities and best-before dates, highlighting food that could be used soon.
3. Suggest recipes based on what is already available, dietary needs and available energy.
4. Turn flexible meal plans into a shopping list for what is missing.
5. Compare verified local regular prices and offers, with clear sources, dates and store/channel distinctions.
6. Update the inventory after shopping and help people resume when plans change.

The aim is to connect these steps so that people do not have to coordinate multiple apps, remember every item or repeatedly calculate prices by hand. This may be particularly valuable for some disabled people, including people on the autism spectrum and people with ADHD, while remaining useful to anyone.

**Scope boundary:** This is a product vision, **not a list of features implemented in Grocery Price Core**. The public library currently handles price observations and comparison primitives only. It does not scan barcodes, maintain a pantry, suggest recipes, plan meals or provide a finished accessible app. A separate application can remain private; its code and commercial future are not licensed by this repository.

## Project and public value

**Accessibility and disability inclusion are core motivations.** People on the autism spectrum (including those who use the term Asperger's) and people with ADHD may face additional effort in planning, comparing prices, switching tasks and handling unexpected changes. Clear distinctions between regular prices, offers, estimates and unknowns can help developers build more predictable, lower-effort grocery and budgeting experiences. This library is useful for everyone and does not require anyone to disclose a diagnosis. Its possible benefits are **design goals, not measured clinical or accessibility outcomes**. No third-party usage, reviews or download numbers are claimed.

Read [Accessibility and public benefit](ACCESSIBILITY_AND_PUBLIC_BENEFIT.md) for concrete examples, limitations and responsible evaluation.

For contribution guidelines, security reports, license scope and maintenance goals see [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [LICENSING_DECISION.md](LICENSING_DECISION.md) and [MAINTAINER_PLAN.md](MAINTAINER_PLAN.md).

## License

[MIT](LICENSE) applies to the code in **this separate repository only**. It grants no rights to external trademarks, retailer catalogs or the separate private Kühlschrank app.
