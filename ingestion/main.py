"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
A failure in one authority (e.g. a slow/down upstream site) shouldn't
block the others from running.
"""

import national_seed
import bristol
import ealing
import hounslow
import gwynedd
import cardiff

MODULES = [national_seed, bristol, ealing, hounslow, gwynedd, cardiff]


def main() -> None:
    for module in MODULES:
        try:
            module.main()
        except Exception as e:
            print(f"[ingestion] WARNING: {module.__name__} failed, skipping. Error: {e}")


if __name__ == "__main__":
    main()