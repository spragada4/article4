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

### Bristol (England) — structured, best starting point
National bulk CSV: `https://files.planning.data.gov.uk/dataset/article-4-direction.csv`,
filtered by `organisation-entity == 66` (Bristol City Council's entity ID).
16 records, confirmed ingested end-to-end in Phase 3.

**Caveat:** several entries have only boilerplate `description` text (e.g. "Designation
made under Article 4 of the Town and Country Planning Act...") rather than a real summary
of what's restricted — the actual restriction detail lives only in the linked PDF
(`document-url`). Retrieval/LLM synthesis should cite the source link and avoid inventing
detail for these thin entries.

### Ealing (England, London)
Confirmed working PDFs (press notices, not the full legal orders):
- Non-immediate: https://www.ealing.gov.uk/download/downloads/id/20189/article_4_direction_non-immediate_press_notice.pdf
- Immediate (Perivale): https://www.ealing.gov.uk/download/downloads/id/20552/article_4_direction_immediate_perivale_ward_press_notice_confirmed_11_april_2025.pdf

2 records, ingested via pdfplumber + FIRST/SECOND SCHEDULE regex extraction in Phase 3.

**Gotcha:** use press notices, not the full "order" PDFs — orders include DocuSign
signature pages with unmapped font glyphs that pollute extracted text.

### Hounslow (England, London)
Confirmed working PDF: https://forms2.hounslow.gov.uk/download/downloads/id/3787/notice.pdf
(requires a browser-like User-Agent header — default `requests` UA gets 403'd).
1 record, ingested via pdfplumber + SCHEDULE-section regex in Phase 3.

**Note:** different document structure than Ealing — single "SCHEDULE" heading, not
FIRST/SECOND — needed its own extraction logic. There's also a 2021 Brentford Dock
direction that was later withdrawn per council records — a good status-tracking case to
add later if pursuing that thread further.

### Cardiff (Wales)
Dedicated conservation-area document pages (cardiff.gov.uk/.../Documents/...) have
moved/broken since being indexed — direct PDF links 404. Reliable working source instead:
Cardiff's council meeting archive (moderngov). Confirmed working PDF:
https://cardiff.moderngov.co.uk/documents/s25638/Cabinet%2015%20November%202018%20Llandaff%20Article%204%202%20directions.pdf
— a Cabinet report (not a press notice) covering two conservation areas at once, 2 records.

**Note:** different document type again — numbered-paragraph committee report, not a
schedule-style notice — needed its own extraction pattern.

### Gwynedd (Wales) — the status-tracking case
Authoritative source:
https://www.gwynedd.llyw.cymru/en/Residents/Planning-and-building-control/Planning/Article-4-Direction.aspx
— content verified directly, but as of this writing the site itself has a broken
server-side redirect (301s the /en/ path to a /en-gb/ path that 404s, confirmed even with
full browser headers). Ingested as a verified static fallback in Phase 3; re-check
periodically via the weekly cron and switch to live fetching once fixed.

**Status: quashed.** 2024 second-homes direction confirmed, then quashed by the High
Court (Sept/Nov 2025), council's final appeal refused 6 Feb 2026 — litigation is over,
direction is definitively not in force. This is the pilot case that proves the `status`
field in the schema is load-bearing, not decorative.

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