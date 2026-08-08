"""
Ealing ingestion: downloads press notice PDFs, extracts the FIRST SCHEDULE
(what's restricted) and SECOND SCHEDULE (where it applies) sections,
normalizes into the standard schema.
"""

import json
import re
from pathlib import Path

import pdfplumber
import requests

PDF_URLS = {
    "ealing-a4d-nonimmediate": "https://www.ealing.gov.uk/download/downloads/id/20189/article_4_direction_non-immediate_press_notice.pdf",
    "ealing-a4d-immediate-perivale": "https://www.ealing.gov.uk/download/downloads/id/20552/article_4_direction_immediate_perivale_ward_press_notice_confirmed_11_april_2025.pdf",
}

OUTPUT_PATH = Path("/data/processed/ealing_article4.jsonl")


def download_pdf(url: str, dest: Path) -> None:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    dest.write_bytes(resp.content)


def extract_text(pdf_path: Path) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_schedules(text: str) -> tuple[str, str]:
    first_match = re.search(r"FIRST SCHEDULE(.*?)SECOND SCHEDULE", text, re.DOTALL)
    second_match = re.search(
        r"SECOND SCHEDULE(.*?)(?:A copy of the direction|Made under the Common Seal|DocuSign|$)",
        text,
        re.DOTALL,
    )

    first = first_match.group(1).strip() if first_match else ""
    second = second_match.group(1).strip() if second_match else ""

    first = re.sub(r"\s+", " ", first)
    second = re.sub(r"\s+", " ", second)

    # strip any residual unmapped-glyph junk (cid codes from unembedded fonts)
    first = re.sub(r"\(cid:\d+\)", "", first)
    second = re.sub(r"\(cid:\d+\)", "", second)

    return first, second


def normalize(record_id: str, source_url: str, restriction: str, area: str) -> dict:
    return {
        "id": record_id,
        "nation": "england",
        "authority": "ealing",
        "level": "local",
        "topic": "article-4",
        "status": "active",
        "section_ref": record_id,
        "text": f"Restricts: {restriction} Applies to: {area}",
        "source_url": source_url,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path("/tmp/ealing_pdfs")
    tmp_dir.mkdir(exist_ok=True)

    records = []
    for record_id, url in PDF_URLS.items():
        pdf_path = tmp_dir / f"{record_id}.pdf"
        download_pdf(url, pdf_path)
        text = extract_text(pdf_path)
        restriction, area = extract_schedules(text)
        records.append(normalize(record_id, url, restriction, area))

    with OUTPUT_PATH.open("w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"[ingestion] wrote {len(records)} Ealing records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()