"""
Gwynedd ingestion.

NOTE: as of this writing, gwynedd.llyw.cymru has a broken redirect —
requests to the /en/Residents/.../Article-4-Direction.aspx path get
301-redirected by the server itself to /en-gb/planning-and-building-control/
planning/article-4-direction, which 404s. This is a bug on the council's
site, not our request (confirmed: same failure with full browser headers).

The text below was directly verified against the live page before the
redirect broke (confirmed working URL is in SOURCE_URL). Re-check
SOURCE_URL periodically (e.g. via the weekly ingestion cron) and switch
back to live fetching once the council fixes their redirect.

This is also the pilot authority that proves the `status` field matters:
the direction was confirmed, then quashed by the High Court, with the
council's final appeal refused in Feb 2026 — so it is definitively NOT
in force.
"""

import json
import re
from pathlib import Path

SOURCE_URL = "https://www.gwynedd.llyw.cymru/en/Residents/Planning-and-building-control/Planning/Article-4-Direction.aspx"
OUTPUT_PATH = Path("/data/processed/gwynedd_article4.jsonl")

# Verified directly against the live page. See module docstring for why
# this is static rather than live-fetched.
CONFIRMED_TEXT = """
On 27 November 2025, during a High Court hearing and following his previous judgment,
the judge (Justice Eyre) confirmed an order to quash Cyngor Gwynedd Cabinet's decision
on 16 July 2024 to confirm the Article 4 Direction. The Council submitted a written
application to request permission to appeal to the Court of Appeal and the Rt. Hon
Justice Lewisam refused the request on 6 February 2026. As a result, as the 16 July
2024 decision is quashed, the Article 4 Direction is not in force within the Gwynedd
Local Planning Authority Area. Following the quashing of the decision to confirm the
Article 4 Direction, material changes of use that were restricted by the Article 4
Direction now have permitted development right. Therefore, it is not necessary to
receive planning permission to undertake these material changes of use. The changes
of use which now have permitted development rights can be examined within the Town
and Country Planning (General Permitted Development) Order 1995 (as amended). The
ruling to refuse the request to appeal brings the litigation process to an end.
"""


def normalize(text: str) -> dict:
    return {
        "id": "gwynedd-a4d-second-homes",
        "nation": "wales",
        "authority": "gwynedd",
        "level": "local",
        "topic": "article-4",
        "status": "quashed",
        "section_ref": "gwynedd-a4d-second-homes",
        "text": re.sub(r"\s+", " ", text).strip(),
        "source_url": SOURCE_URL,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = normalize(CONFIRMED_TEXT)

    with OUTPUT_PATH.open("w") as f:
        f.write(json.dumps(record) + "\n")

    print(f"[ingestion] wrote 1 Gwynedd record to {OUTPUT_PATH} (static fallback — see module docstring)")


if __name__ == "__main__":
    main()