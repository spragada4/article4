"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
"""

import bristol
import ealing
import hounslow


def main() -> None:
    bristol.main()
    ealing.main()
    hounslow.main()


if __name__ == "__main__":
    main()