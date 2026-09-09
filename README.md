# book-partnership-data

Compare ongoing commercial partner programs and payout obligations.

Status: **local source pilot**, version 0.1.0. Six manually invoked official
public partner pages run through the shared bounded capture and lake replay lane.
There is no scheduler, hosted API, consumer integration or application action.
The CLI still provides a machine-readable JSON contract and searches synthetic
examples; capture never falls back from live data to fixtures.

## Users and boundary

For people and small teams discovering commercial partnerships.
Durable commercial relationships; one-off referral promotions belong to deal and creator eligibility to creator-program.

Subcategories: affiliate, reseller, channel-partner, distribution, integration-partner, licensing.

Domain-specific terms: `partner_model`, `commission_basis`, `exclusivity_required`, `settlement_terms`.
Each record represents one program/offer intake window. A repeat intake receives
a distinct source record ID. Cross-domain packages use `related_records` rather
than copying the same award into several products.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
book-partnership-data contract
book-partnership-data demo --open-only
book-partnership-data demo --query "affiliate"
book-partnership-data validate src/book_partnership_data/demo.json
python -m unittest discover -s tests -v
```

With dependencies already available, use `PYTHONPATH=src python3 -m book_partnership_data`.
`demo` uses the fixed synthetic clock 2026-09-07T00:00:00Z unless `--as-of` is
provided. `--open-only` excludes closed, unknown-deadline, expired, stale (72h
default), and future-checked records. This is an availability filter; it does
not assert personal eligibility, selection probability, or a guaranteed payout.

Contract: `src/book_partnership_data/schema.json` (`partnership.v1`).
Unknown amounts, currencies, eligibility and deadlines remain unknown. Cash,
credit, discount, in-kind benefits and access are different value kinds. Never
sum them as cash income. Queries and validation are read-only and do not persist
provided files. The `live` label requires captured lineage, but validation alone
does not verify that referenced lake objects exist or prove source truth.

## Data ownership and source policy

Owner: bookchaowalit. Public program metadata only; no applications, personal
screening answers, financial credentials, cookies, or private transcripts.
See `sources.json` and the source policy JSON files under
`src/book_partnership_data/`: Stripe, HubSpot, Microsoft, AWS, Shopify and
Apple public partner overviews are enabled for bounded metadata only. Exact
source permission and retention are reviewed before network ingestion. No
login, partner application, agreement acceptance or messaging is performed.

Implemented flow: approved source pull → immutable landing bytes
and checksum → Bronze Parquet and manifest through the shared lake runtime →
versioned read-only contract → consumer pull. Each product owns its source
adapters and lake prefix. Producers never write into another app's database,
CRM, tasks, application tracker, or notification system.

## Remaining implementation gates

1. Expand commission and settlement extraction without inferring a commercial
   agreement or payout.
2. Package the local shared capture runtime for independent deployment.
3. Add retention/access controls and runtime monitoring.
4. Connect a read-only consumer. Eligibility, ranking, deadlines and agreement
   application workflow belong to consumers with separate private storage.

## Official source pilots

Sources: [Stripe Partner Ecosystem](https://stripe.com/partners/become-a-partner),
[HubSpot Affiliate Program](https://www.hubspot.com/partners/affiliates),
[Microsoft Cloud Solution Provider](https://microsoftpartners.microsoft.com/csp/),
[AWS Marketplace Channel](https://aws.amazon.com/marketplace/partners),
[Shopify Partner Program](https://www.shopify.com/partners), and
[Apple MFi Program](https://mfi.apple.com/). The adapter captures bounded
partner-track metadata and keeps commission, exclusivity, settlement, approval,
certification and timing terms unknown until the relevant agreement is reviewed.

```bash
export SOLO_EMPIRE_ROOT=/home/bookchaowalit/book/solo-empire
PYTHONPATH=src "$SOLO_EMPIRE_ROOT/infra/.venv-datalake/bin/python" -m book_partnership_data.capture acquire --lake "$PWD/data/lake" --state-dir "$PWD/data/control"
PYTHONPATH=src "$SOLO_EMPIRE_ROOT/infra/.venv-datalake/bin/python" -m book_partnership_data.capture records --lake "$PWD/data/lake" --state-dir "$PWD/data/control"
```

No runtime port is reserved. The former `opportunity.v1` is archival; `job.v1` remains a separate job-data contract.
Breaking contract changes require a new version and a consumer migration.
There is no production deployment to roll back; discard demo output or restore
the previous contract version locally. Source permission, live availability,
lake replay and real eligibility are **unverified**, not passing gates.
