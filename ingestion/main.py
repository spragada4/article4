"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
A failure in one authority (e.g. a slow/down upstream site) shouldn't
block the others from running.
"""

import bristol
import cardiff
import ealing
import gwynedd
import hounslow
import national_seed

MODULES = [national_seed, bristol, ealing, hounslow, gwynedd, cardiff]


def main() -> None:
    for module in MODULES:
        try:
            module.main()
        except Exception as e:  # noqa: BLE001 — intentional: one authority's
            # failure (network, parsing, upstream outage) must not block the rest
            print(f"[ingestion] WARNING: {module.__name__} failed, skipping. Error: {e}")


if __name__ == "__main__":
    main()