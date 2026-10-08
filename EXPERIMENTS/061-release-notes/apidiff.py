"""apidiff — what changed between two versions of a pure-Python package.

Reads the two sdists PyPI already hosts, parses them with `ast`, and
diffs the public API: functions, classes, methods, and their
signatures. The verdict comes from the shipped bytes, not from any
changelog the package happens to write, so it can name a change the
release notes omit.

Stdlib only. Usage:

    python3 apidiff.py REQUESTS 2.31.0 2.32.3
    python3 apidiff.py NUMPY 1.26.4 2.0.0 --json

Classification is conservative: a change is *breaking* only when a
name a caller could import is gone, or a call that was valid is no
longer valid. Additions are never breaking.
"""

from apidiff.cli import main

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))