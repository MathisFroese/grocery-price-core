# Instructions for maintainers and coding agents

- Keep all data synthetic in tests and documentation; never introduce private Kühlschrank code or Git history.
- Preserve price kinds and sales-channel provenance. Unknown must never be treated as free or zero.
- Never claim an online or pickup price is a verified shelf price.
- Never infer product equivalence from names alone; the caller checks product equivalence.
- For behavior changes, add tests and run `PYTHONPATH=src python -m unittest discover -s tests -v`.
- Only this independent component is MIT-licensed. Do not import or relicense code from the separate private app.
- Do not invent release adoption, users, stars, downloads or maintainer activity for award applications.
