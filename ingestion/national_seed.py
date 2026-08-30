"""
National baseline seed data — permitted development rights that apply across
England and Wales by default, before any local Article 4 override is applied.

Hand-curated rather than scraped: this is a small, stable rule set (verified
current as of 2026 — no PD rule changes in 2026 per Planning Portal/gov.uk
guidance), and it's the missing "national" tier that Phase 3's ingestion
never populated (Phase 3 only pulled local Article 4 overrides).
"""

import json
from pathlib import Path

OUTPUT_PATH = Path("/data/processed/national_baseline.jsonl")

RECORDS = [
    {
        "id": "national-pd-class-a-extensions",
        "nation": "england",
        "authority": "national",
        "level": "national",
        "topic": "permitted-development",
        "status": "active",
        "section_ref": "GPDO Schedule 2, Part 1, Class A",
        "text": (
            "Rear extensions are permitted development up to 3m deep for terraced "
            "and semi-detached houses, or 4m for detached houses (extendable to 6m "
            "and 8m respectively under the prior approval / neighbour consultation "
            "scheme). Extensions and outbuildings combined must not cover more than "
            "50% of the curtilage of the original house."
        ),
        "source_url": "https://www.planningportal.co.uk/permission/common-projects/house-extensions/planning-permission",
    },
    {
        "id": "national-pd-class-b-loft",
        "nation": "england",
        "authority": "national",
        "level": "national",
        "topic": "permitted-development",
        "status": "active",
        "section_ref": "GPDO Schedule 2, Part 1, Class B",
        "text": (
            "Loft conversions are permitted development up to a volume allowance of "
            "40 cubic metres for terraced houses or 50 cubic metres for detached and "
            "semi-detached houses. The enlargement must not exceed the height of the "
            "existing roof, and on the principal elevation must not extend beyond the "
            "existing roof slope. Side-facing windows must be obscure-glazed."
        ),
        "source_url": "https://www.planningportal.co.uk/permission/common-projects/loft-conversion/planning-permission",
    },
    {
        "id": "national-pd-class-e-outbuildings",
        "nation": "england",
        "authority": "national",
        "level": "national",
        "topic": "permitted-development",
        "status": "active",
        "section_ref": "GPDO Schedule 2, Part 1, Class E",
        "text": (
            "Outbuildings (sheds, garden rooms, garages, home offices, etc.) are "
            "permitted development provided they are single storey, with a maximum "
            "eaves height of 2.5m and overall height of 4m (dual-pitched roof) or 3m "
            "otherwise. No outbuilding is permitted forward of the principal "
            "elevation, and height is limited to 2.5m within 2m of a boundary."
        ),
        "source_url": "https://www.greatercambridgeplanning.org/the-planning-application-process-and-advice/pre-application-advice/householder-and-small-business-advice/advice-for-householders",
    },
    {
        "id": "national-pd-class-l-hmo",
        "nation": "england",
        "authority": "national",
        "level": "national",
        "topic": "permitted-development",
        "status": "active",
        "section_ref": "GPDO Schedule 2, Part 3, Class L",
        "text": (
            "Change of use from a dwellinghouse (Use Class C3) to a small house in "
            "multiple occupation (Use Class C4, up to 6 unrelated occupants) is "
            "permitted development by default. This is the specific right that "
            "local Article 4 Directions most commonly withdraw — see local "
            "authority overrides for whether it still applies at a given address."
        ),
        "source_url": "https://www.planningportal.co.uk/",
    },
    {
        "id": "national-pd-general-note",
        "nation": "england",
        "authority": "national",
        "level": "national",
        "topic": "permitted-development",
        "status": "active",
        "section_ref": "GPDO Schedule 2, general",
        "text": (
            "Permitted development rights apply only to houses and bungalows, not "
            "flats, maisonettes, or mobile homes. Rights can be withdrawn locally by "
            "an Article 4 Direction, and additional restrictions apply automatically "
            "in conservation areas, National Parks, and World Heritage Sites. Always "
            "check local overrides in addition to the national baseline."
        ),
        "source_url": "https://reigate-banstead.gov.uk/info/20243/before_you_apply/149/permitted_development",
    },
]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w") as f:
        for record in RECORDS:
            f.write(json.dumps(record) + "\n")
    print(f"[ingestion] wrote {len(RECORDS)} national baseline records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()