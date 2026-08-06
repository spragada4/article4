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
  - Gotcha: **not every London borough publishes here.** Several boroughs (Ealing, Wandsworth,
    Islington, Hounslow, and others) keep Article 4 data on their own council sites instead.
    Always check the borough's own planning pages as a fallback.
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

## Pilot local authorities

| Authority | Nation | Source | Notes |
|---|---|---|---|
| Ealing | England (London) | Local only — ealing.gov.uk, not on planning.data.gov.uk | Two Article 4 Directions made 30 Oct 2024, removing PD rights for C3→C4 (HMO) conversion in Perivale ward. Published as PDFs. Good concrete demo case. |
| TODO | England (London) | TODO | pick 1-2 more boroughs — check planning.data.gov.uk first, fall back to council site |
| Bristol OR Manchester | England | TODO | non-London English authority — check for open data portal first |
| Cardiff | Wales | TODO | check cardiff.gov.uk planning pages |
| Gwynedd | Wales | TODO | Article 4 second-homes case — check gwynedd.llyw.cymru planning pages |

## Schema every source gets normalized into

\`\`\`json
{
  "id": "string",
  "nation": "england | wales",
  "authority": "national | ealing | gwynedd | ...",
  "level": "national | local",
  "topic": "permitted-development | article-4 | building-regs | local-plan",
  "section_ref": "string",
  "text": "string",
  "source_url": "string"
}
\`\`\`