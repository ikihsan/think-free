#!/usr/bin/env python3
"""Allow running pyprovides as: python3 -m pyprovides"""

import sys

from pyprovides.pyprovides_cli import main

if __name__ == "__main__":
    sys.exit(main())