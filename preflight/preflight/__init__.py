"""preflight -- three checks on the instrument that produces an evaluation rate.

    from preflight import concordance, alternate_form_fp, control_arm, render

The package has no dependencies outside the standard library and no knowledge of
any particular domain. A caller supplies rows, labels and predicates; this code
measures the join, the false-positive rate on correct output, and whether a
declared negative arm is negative. It reports the measurements and withholds the
rate when one of them fails.
"""

from .alternate_form import alternate_form_fp
from .concordance import concordance
from .control_arm import control_arm
from .report import EXIT_OK, EXIT_USAGE, EXIT_WITHHELD, blocking, headline, may_report, render
from .stats import wilson

__all__ = [
    "alternate_form_fp",
    "concordance",
    "control_arm",
    "render",
    "headline",
    "may_report",
    "blocking",
    "wilson",
    "EXIT_OK",
    "EXIT_USAGE",
    "EXIT_WITHHELD",
]

VERSION = "0.1"