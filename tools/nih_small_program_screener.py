#!/usr/bin/env python3
"""
NIH SBIR Small-Program Accessibility Screener

Deprecated: Use tools.nih_sbir_metrics and tools.nih_sbir_screener instead.
This file is retained for backward compatibility; it delegates to the
modular implementation split across two files to comply with the 300-line cap.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis) and the spending category screen from E204.
"""

import sys
import os

# Ensure the tools directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from nih_sbir_screener import run_screener


def main():
    """Run the screener (delegates to modular implementation)."""
    # Parse command-line arguments
    args = sys.argv[1:]
    
    # Handle --multi flag
    if '--multi' in args:
        # Remove --multi from args and pass remaining as category_codes
        args = [a for a in args if a != '--multi']
        run_screener(args, multi_mode=True)
    else:
        # Default behavior: screen provided categories (or all three)
        if not args:
            args = ['101', '108', '176']
        run_screener(args)


if __name__ == '__main__':
    main()