"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
"""

import bristol
import cardiff
import ealing
import gwynedd
import hounslow


def main() -> None:
    bristol.main()
    ealing.main()
    hounslow.main()
    gwynedd.main()
    cardiff.main()


if __name__ == "__main__":
    main()