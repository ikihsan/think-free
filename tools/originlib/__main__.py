"""Allow `python3 -m originlib` from anywhere inside the repository."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())