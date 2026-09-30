# Upgrade plan — book-partnership-data

Score: 6/10 -> 7.5/10 (pass 1) -> 7.5/10 (pass 2) — solid contract/source tests, but no CI, lint drift and no policy-consistency checks.

## Backlog

- P0: Confirm the new GitHub Actions CI is green on the first push and keep it required.
- P1: `required_markers` in `source-microsoft-csp-reseller.json` includes "sign in", which also matches
  generic login/challenge pages; replace with a program-specific marker after a source review.
- P1: Extract commission basis from the HubSpot/Shopify pages instead of fixed prose.
- P1: Live-source monitoring (drift alerts) stays in the shared runtime; keep adapters pure.
- P2: Fill the PRODUCT.md acceptance-gate table only with evidence that exists (CI run link,
  replay report); do not mark gates passed without it.
- P2: Consider extracting the byte-identical `cli.py` shared by the sibling `book-*-data`
  products into one versioned package once a consumer exists (today each repo vendors it).

## Done in this pass (pass 1)

- Added `.github/workflows/ci.yml`: Python 3.10/3.12 matrix, `pip install -e ".[dev]"`,
  `ruff check .`, `pytest`, and a `contract`/`validate`/`demo` CLI smoke. Verified by
  replaying those steps in a clean Python 3.10 venv.
- Added `[project.optional-dependencies] dev`, pytest config (`pythonpath = src`) and an
  explicit ruff rule set (E4/E9/F/I/B/UP); fixed the resulting import-order/encode lint.
- Added `tests/test_policy.py`: `sources.json` ↔ `source*.json` ↔ schema category
  consistency, duplicate policy copies identical, https/no-query URLs, 6h minimum
  interval, `--source-id` traversal rejection, capture fail-closed without
  `SOLO_EMPIRE_ROOT`, CLI `validate` exit codes without echoing input, bad demo clock.
- README: documented the developer/CI commands and offline test boundary.

## Done in this pass (pass 2)

- Drift markers moved from the `REQUIRED_MARKERS` code table into `required_markers` in
  each packaged source config (same phrases), so a marker fix (e.g. the CSP "sign in" P1)
  is a reviewed config change. Configs without markers, with empty/non-string markers, or
  with an unreviewed id fail closed with `ValueError`; new test proves the config decides.
- The CSP "sign in" marker itself is unchanged: a replacement needs a reviewed live capture.
