"""
Hounslow ingestion: downloads Article 4 Direction press notices, extracts the
SCHEDULE section (what's restricted) and the "Direction applies to..." sentence
(where it applies). Hounslow's format differs from Ealing's — one SCHEDULE
heading, not FIRST/SECOND — so this gets its own extraction logic.
"""

import json
import re
from pathlib import Path

import pdfplumber
import requests

PDF_URLS = {
    "hounslow-a4d-brentford-dock-2023": "https://forms2.hounslow.gov.uk/download/downloads/id/3787/notice.pdf",
}

OUTPUT_PATH = Path("/data/processed/hounslow_article4.jsonl")


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


def extract_restriction_and_area(text: str) -> tuple[str, str]:
    # restriction: everything under the single "SCHEDULE" heading, up to the signature block
    restriction_match = re.search(r"\bSCHEDULE\s*\n(.*?)Dated this", text, re.DOTALL)
    restriction = restriction_match.group(1).strip() if restriction_match else ""

    # area: pulled from the "Direction applies to X" sentence in the body
    area_match = re.search(r"[Dd]irection (?:applies to|relates to)\s+(.*?)(?:,| and)", text)
    area = area_match.group(1).strip() if area_match else ""

    restriction = re.sub(r"\s+", " ", restriction)
    area = re.sub(r"\s+", " ", area)
    return restriction, area


def normalize(record_id: str, source_url: str, restriction: str, area: str) -> dict:
    return {
        "id": record_id,
        "nation": "england",
        "authority": "hounslow",
        "level": "local",
        "topic": "article-4",
        "status": "active",
        "section_ref": record_id,
        "text": f"Restricts: {restriction} Applies to: {area}",
        "source_url": source_url,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path("/tmp/hounslow_pdfs")
    tmp_dir.mkdir(exist_ok=True)

    records = []
    for record_id, url in PDF_URLS.items():
        pdf_path = tmp_dir / f"{record_id}.pdf"
        download_pdf(url, pdf_path)
        text = extract_text(pdf_path)
        restriction, area = extract_restriction_and_area(text)
        records.append(normalize(record_id, url, restriction, area))

    with OUTPUT_PATH.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"[ingestion] wrote {len(records)} Hounslow records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()