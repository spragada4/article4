"""
Ingestion service entrypoint.

Phase 3: pulls the national Article 4 direction bulk dataset from
planning.data.gov.uk and filters it down to Bristol as the first pilot authority.
"""

import json
from pathlib import Path

import ealing

import pandas as pd

SOURCE_URL = "https://files.planning.data.gov.uk/dataset/article-4-direction.csv"
OUTPUT_PATH = Path("/data/processed/bristol_article4.jsonl")


def fetch_article4_national() -> pd.DataFrame:
    return pd.read_csv(SOURCE_URL)


def filter_bristol(df: pd.DataFrame) -> pd.DataFrame:
    # Bristol City Council's entity ID on planning.data.gov.uk is 66
    # (confirmed via https://www.planning.data.gov.uk/entity/66)
    return df[df["organisation-entity"] == 66]

def main() -> None:
    # ... existing Bristol code ...
    ealing.main()

def normalize(row: pd.Series) -> dict:
    return {
        "id": str(row["entity"]),
        "nation": "england",
        "authority": "bristol",
        "level": "local",
        "topic": "article-4",
        "status": "active" if pd.isna(row["end-date"]) or row["end-date"] == "" else "superseded",
        "section_ref": str(row["reference"]),
        "text": row["description"] if pd.notna(row["description"]) else (row["notes"] if pd.notna(row["notes"]) else ""),
        "source_url": row["document-url"] if pd.notna(row["document-url"]) else row["documentation-url"],
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = fetch_article4_national()
    bristol_df = filter_bristol(df)

    with OUTPUT_PATH.open("w") as f:
        for _, row in bristol_df.iterrows():
            record = normalize(row)
            f.write(json.dumps(record) + "\n")

    print(f"[ingestion] wrote {len(bristol_df)} Bristol records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()