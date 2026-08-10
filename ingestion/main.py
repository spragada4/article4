"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
"""

import bristol
import cardiff
import ealing
import gwynedd
import hounslow
import national_seed


def main() -> None:
    national_seed.main()
    bristol.main()
    ealing.main()
    hounslow.main()
    gwynedd.main()
    cardiff.main()