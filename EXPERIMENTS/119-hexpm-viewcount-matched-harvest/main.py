#!/usr/bin/env python3
"""E119 — Hex.pm view-count matched-harvest experiment main entry point."""

import sys
from classify import main as classify_main

if __name__ == "__main__":
    sys.exit(classify_main())