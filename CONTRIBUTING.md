# Contributing

This is an early independent library. Questions, bug reports, docs improvements, tests and small focused changes are welcome once its public repository is available.

1. Describe the problem, actual behavior, expected behavior and a minimal example with **synthetic prices**.
2. For behavior changes, add regression tests and run `PYTHONPATH=src python -m unittest discover -s tests -v`.
3. Preserve price provenance and explicit unknown values. Do not infer shelf prices from pickup/online prices or product equivalence from names.
4. Never submit private Kühlschrank code/history, retailer credentials, receipts, personal information, copied product catalogs or other third-party materials without rights.
5. By submitting your own code, you agree it can be distributed under this repository's MIT license; do not submit work you cannot license on those terms.

The maintainers cannot promise immediate review. Please use the private reporting guidance in [SECURITY.md](SECURITY.md) for vulnerabilities.
