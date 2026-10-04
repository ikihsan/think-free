"""The one exception a CLI handler raises for a refusal.

`cli.py` catches it and exits 1, which is the contract every caller branches
on: a refusal the fleet flow is *meant* to produce prints one line on stderr
rather than a traceback (`FAILURES.md` F014).

It lives in its own module because four handler modules need it and all four
are imported by `cli.py`: importing it from there would be a cycle, and before
this module existed three of them referenced a name they never imported, so
`raise Usage(...)` in `cli_repo`, `cli_session` and `cli_task` was a
`NameError` waiting for the one argument shape argparse cannot produce
(defect 13 in `STATE-defects.md`). A refusal that crashes instead of refusing is
the opposite of what it is for.
"""

from __future__ import annotations


class Usage(Exception):
    """Raised for a malformed invocation."""