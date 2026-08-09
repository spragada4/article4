"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
"""

import bristol
import ealing
import gwynedd
import hounslow


def main() -> None:
    bristol.main()
    ealing.main()
    hounslow.main()
    gwynedd.main()


if __name__ == "__main__":
    main()