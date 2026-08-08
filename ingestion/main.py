"""
Ingestion service entrypoint. Runs each authority's ingestion in turn.
"""

import bristol
import ealing


def main() -> None:
    bristol.main()
    ealing.main()


if __name__ == "__main__":
    main()