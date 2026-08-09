"""
Cardiff ingestion.

NOTE: Cardiff's dedicated conservation-area document pages
(cardiff.gov.uk/.../Conservation/Documents/...) have moved or been
restructured since being indexed — direct PDF links there now 404.
The reliable working source instead is Cardiff's council meeting archive
(moderngov), which is more stable. This one Cabinet report covers TWO
Article 4(2) Directions at once (Llandaff and Cardiff Road conservation
areas), both restricting demolition of gates/fences/walls.

Document type differs again from the other pilot authorities: this is a
Cabinet committee report (numbered paragraphs), not a press notice or
single-schedule notice — so it gets its own, simpler extraction.
"""

import json
import re
from pathlib import Path

import pdfplumber
import requests

PDF_URL = "https://cardiff.moderngov.co.uk/documents/s25638/Cabinet%2015%20November%202018%20Llandaff%20Article%204%202%20directions.pdf"
OUTPUT_PATH = Path("/data/processed/cardiff_article4.jsonl")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def download_pdf(url: str, dest: Path) -> None:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    dest.write_bytes(resp.content)


def extract_text(pdf_path: Path) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_restriction(text: str) -> str:
    match = re.search(r"Reason for this Report\s*\n?1\.(.*?)Background", text, re.DOTALL)
    restriction = match.group(1).strip() if match else ""
    return re.sub(r"\s+", " ", restriction)


def normalize(restriction: str) -> list[dict]:
    # One Cabinet report, two separate conservation areas — split into two records
    areas = ["Llandaff Conservation Area", "Cardiff Road Conservation Area"]
    return [
        {
            "id": f"cardiff-a4d-{area.lower().replace(' ', '-')}",
            "nation": "wales",
            "authority": "cardiff",
            "level": "local",
            "topic": "article-4",
            "status": "active",
            "section_ref": f"cardiff-a4d-{area.lower().replace(' ', '-')}",
            "text": f"Restricts: {restriction} Applies to: {area}",
            "source_url": PDF_URL,
        }
        for area in areas
    ]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path("/tmp/cardiff_pdfs")
    tmp_dir.mkdir(exist_ok=True)
    pdf_path = tmp_dir / "cardiff.pdf"

    download_pdf(PDF_URL, pdf_path)
    text = extract_text(pdf_path)
    restriction = extract_restriction(text)
    records = normalize(restriction)

    with OUTPUT_PATH.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"[ingestion] wrote {len(records)} Cardiff records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()