# Grocery Price Core v0.1.0

First public source release of the standalone, MIT-licensed Python library.

## Included

- Explicit regular, offer, estimate, last-paid and unknown price semantics.
- Exact `Decimal` unit-price normalization for mass, volume and pieces.
- Date-bounded offers and explicit in-store, online and pickup channels.
- Status-based comparisons that do not invent savings from missing or incompatible prices.
- Dependency-free runtime, synthetic examples, documentation and automated tests on Python 3.10 and 3.12.

## Scope and limitations

This release contains **only Grocery Price Core**. It does not publish or license the separate private Kühlschrank application, its Git history, retailer integrations or private datasets.

The caller is responsible for verifying product equivalence and choosing acceptable source freshness. No live shelf-price coverage or external adoption is claimed. This release is not a PyPI publication.

See [README.md](README.md) and [LICENSING_DECISION.md](LICENSING_DECISION.md).
