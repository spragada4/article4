"""
API service entrypoint.

Phase 0/2 goal: prove this container runs and responds.
Phase 5/6 goal: wire /ask to real retrieval + LLM synthesis from shared/,
using the two-tier (national + local) index.
"""

from fastapi import FastAPI

app = FastAPI(title="Article4 API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ask")
def ask(nation: str, authority: str, q: str) -> dict:
    return {
        "nation": nation,
        "authority": authority,
        "query": q,
        "answer": "Not implemented yet — this is the Phase 0 skeleton.",
        "citations": [],
        "disclaimer": "Not legal advice. Verify with your local planning authority.",
    }