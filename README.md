# Article4

A RAG-powered assistant for planning permission questions in England and Wales —
grounded in real national permitted development rules and local authority overrides
(Article 4 Directions, conservation area restrictions), with citations back to the
original source.

**Not legal advice.** Always verify with your local planning authority before
starting any work.

## Why "Article4"

Permitted development rights in England and Wales come from national legislation —
but a local planning authority can restrict them locally by issuing an **Article 4
Direction**. Answering "can I do X at my address" correctly means checking the
national baseline *and* any local override that applies to that specific address.
That national-default / local-override relationship is the core design of this
project — see [Architecture](#architecture) below.

## Status

🚧 **Ingestion pipeline complete. Retrieval/index layer not yet built.**

| Phase | Status |
|---|---|
| 0 — Project skeleton, Docker, CI | ✅ Done |
| 1 — Confirm data sources (`SOURCES.md`) | ✅ Done |
| 2 — Docker skeleton verified working | ✅ Done |
| 3 — Ingestion pipeline (national + 5 pilot authorities) | ✅ Done |
| 4 — Retrieval core: `TwoTierIndex`, hybrid ranking, LRU cache | ⏳ Not started |
| 5 — LLM synthesis with citations | ⏳ Not started |
| 6 — API wiring | ⏳ Stub only (`/ask` returns a placeholder) |
| 7 — UI polish | ⏳ Stub only |

The `api` and `ui` services run and talk to each other, but `/ask` currently
returns a hardcoded placeholder — no real retrieval or LLM call happens yet.
The actual data (25 real records) is sitting in `data/processed/` waiting for
Phase 4 to make use of it.

## What's actually in the data right now

Ingestion has run successfully against:

| Source | Records | Format |
|---|---|---|
| National permitted development baseline | 5 | Hand-curated seed, verified current 2026 rules |
| Bristol (England) | 16 | Structured national CSV (planning.data.gov.uk) |
| Ealing (England, London) | 2 | PDF parsing |
| Hounslow (England, London) | 1 | PDF parsing |
| Gwynedd (Wales) | 1 | HTML, static fallback — `status: quashed` |
| Cardiff (Wales) | 0 (source currently down, 503) | PDF parsing — retry later |

Full detail on every source, including known gotchas per authority, is in
[`SOURCES.md`](./SOURCES.md).

### Worth knowing: the Gwynedd case
Gwynedd's 2024 second-homes Article 4 Direction was confirmed, then quashed by
the High Court, with the council's final appeal refused in February 2026. It is
ingested with `status: "quashed"` — proof the schema needs to represent rules
that *existed* but are not currently in force, not just a flat list of active rules.

### Worth knowing: ingestion is resilient to upstream failures
Each authority's ingestion runs independently; if one source is temporarily
down (as happened live with Cardiff's council archive during development —
a genuine `503 Service Unavailable`), the pipeline logs a warning and
continues with the rest rather than failing the whole run.

## Architecture

```
ingestion/  → per-authority + national fetchers/scrapers, normalized into a
              common schema, written to data/processed/*.jsonl
shared/     → the retrieval core (Phase 4): TwoTierIndex (national baseline +
              local override), hybrid search, LRU query cache
api/        → FastAPI service exposing /ask (currently a stub)
ui/         → Streamlit chat interface (currently a stub)
```

### Data schema
Every ingested record is normalized into:
```json
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
```

## Running locally

```bash
cp .env.example .env   # fill in your API key
docker compose up --build
```

- API: http://localhost:8000 (see `/health`; `/ask` is a stub for now)
- UI: http://localhost:8501

### Running ingestion
Ingestion runs as a one-off job, not a long-running service:
```bash
docker compose --profile ingestion run --remove-orphans ingestion
```
Output lands in `data/processed/*.jsonl` (gitignored — regenerate anytime).

## Development workflow

All work happens on a feature branch, merged via PR once CI (lint + tests) passes:
```bash
git checkout main
git pull origin main
git checkout -b phase-N-whatever
# ...work, commit...
git push -u origin phase-N-whatever
# open PR on GitHub, let CI run, merge once green
```

## Roadmap

- **Phase 4**: build `TwoTierIndex` in `shared/index.py` — hand-built inverted
  index (hash map postings lists) for keyword search, BM25-style scoring,
  merged via a min-heap top-k, plus an LRU cache for repeated queries. This is
  the core DSA work the project is built around.
- **Phase 5**: wire real LLM synthesis into `/ask`, with forced citations back
  to `source_url`, and explicit handling for `status: quashed/superseded` records
  so the assistant doesn't present overturned rules as current.
- **Retry Cardiff** once their moderngov site is back up.
- **Stretch**: add the withdrawn 2021 Hounslow Brentford Dock direction as a
  second status-tracking case; expand to more pilot authorities.

## Disclaimer

This tool provides general information based on published planning data. It is
**not legal advice** and may not reflect the current status of every rule at
every address. Always confirm with your local planning authority before
starting work. 