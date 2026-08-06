# Data Sources

Track the exact source for every authority here before writing scraper code.

## National baseline (England)

- **planning.data.gov.uk** — the main source. Live per-property API for
  spot-checks, bulk downloads for actual indexing.
  - Live API (single property lookup only, no batch endpoint):
    `GET https://www.planning.data.gov.uk/entity.json?latitude=...&longitude=...&dataset=article-4-direction-area&dataset=conservation-area`
  - Dataset pages (use these for bulk ingestion — download as CSV/JSON/GeoJSON/Parquet):
    - Permitted development rights: https://www.planning.data.gov.uk/dataset/permitted-development-right
    - Article 4 direction areas: https://www.planning.data.gov.uk/dataset/article-4-direction-area
    - Article 4 direction rules: https://www.planning.data.gov.uk/dataset/article-4-direction-rule
  - Note: article-4-direction entries reference back to specific permitted-development-right
    entries they withdraw — this is the exact national/local relationship the TwoTierIndex models.
  - Gotcha: **not every local authority publishes here.** Several London boroughs (Ealing,
    Wandsworth, Islington, Hounslow, and others) keep Article 4 data on their own council
    sites instead. Always check the authority's own planning pages as a fallback.
- Planning Portal Interactive House (seed content for common homeowner projects)
  https://interactive.planningportal.co.uk/explore-house

## National baseline (Wales)

- GOV.WALES — permitted development rights for householders
  https://www.gov.wales/planning-permission-permitted-development-rights-householders
- legislation.gov.uk — Wales GPDO amendments (TODO: pin exact instrument/year)
- Planning Aid Wales guidance library
  https://planningaidwales.org.uk/about-planning/links-2/
- Note: no national structured/open-data equivalent to planning.data.gov.uk found for Wales.
  Expect to scrape gov.wales + individual council sites directly.
- Wales-specific legal mechanism: the Town and Country Planning (General Permitted
  Development etc.) (Amendment) (Wales) Order 2022 introduced three new use classes
  (main home / second home / short-term let) and gave Welsh authorities power to
  restrict changes between them via Article 4 — this is Wales-only, has no England
  equivalent, and is exactly what the Gwynedd pilot below tests.

## Pilot local authorities

| Authority | Nation | Source | Notes |
|---|---|---|---|
| Ealing | England (London) | Local only — ealing.gov.uk, PDF-based | Two Article 4 Directions made 30 Oct 2024, removing C3→C4 (HMO) rights in Perivale ward. |
| Hounslow | England (London) | Local only — hounslow.gov.uk, PDF-based | Borough-wide C3→C4 direction (in force Sept 2023) + conservation area directions + one site-specific fences/gates direction (Brentford Dock, 2023). Good variety of rule types from one authority. |
| Bristol | England | **Structured — best starting point.** planning.data.gov.uk (org ref: BST) AND Open Data Bristol portal (opendata.bristol.gov.uk), GeoJSON/CSV | Build and test the ingestion pipeline against this authority first — cleanest data of the pilot set. |
| Cardiff | Wales | Local only — caerdydd.gov.uk / cardiff.moderngov.co.uk, PDF-based | Directions are per-building/area (e.g. Stacey Hall conservation case) rather than one borough-wide dataset — more scraping-heavy, lower priority. |
| Gwynedd | Wales | Local only — gwynedd.llyw.cymru | **Status: quashed, not currently in force.** 2024 second-homes Article 4 Direction (restricting C3→C5/C6 change of use) was confirmed, then struck down by the High Court in 2025 over a procedural flaw. Forces the schema to carry a status/currency field rather than treating rules as permanently active — build this one after Bristol and one PDF-based English authority. |

## Recommended ingestion build order

1. Bristol (structured data — proves the pipeline works end to end)
2. Ealing or Hounslow (PDF-based — proves the scraper handles unstructured sources)
3. Gwynedd (forces the status/currency field before calling retrieval "done")
4. Cardiff (same PDF-scraping pattern as step 2, lower priority)

## Schema every source gets normalized into

\`\`\`json
{
  "id": "string",
  "nation": "england | wales",
  "authority": "national | bristol | ealing | hounslow | cardiff | gwynedd",
  "level": "national | local",
  "topic": "permitted-development | article-4 | building-regs | local-plan",
  "status": "active | quashed | superseded",
  "section_ref": "string",
  "text": "string",
  "source_url": "string"
}
\`\`\`