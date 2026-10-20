"""preflight — three checks on the instrument that produces an evaluation rate.

    from preflight import concordance, alternate_form_fp, control_arm, render

The package has no dependencies outside the standard library and no knowledge of
any particular domain. A caller supplies rows, labels and predicates; this code
measures the join, the false-positive rate on correct output, and whether a
declared negative arm is negative. It reports the measurements and withholds the
rate when one of them fails.

Typical usage:

    from preflight import concordance, alternate_form_fp, control_arm, render

    checks = [
        concordance(key_rows, output_rows),                      # C1
        alternate_form_fp(control_items, flagger, fp_ceiling=0.02),  # C2
        control_arm(control_rows, is_positive, premise=0.0),     # C3
    ]
    text, code = render(checks, rate=recall)   # code 3 and the rate withheld

Exit 3 means an instrument check failed and the rate is not printed. `--anyway`
in the CLI prints the number *and* says the checks failed, so a caller who wants
an unvouched rate has to say so.

Adapter modules are in ``preflight.adapters`` and can be imported directly:

    from preflight.adapters.jsonl_adapter import adapt_jsonl
    from preflight.adapters.csv_adapter import adapt_csv
    from preflight.adapters.yaml_adapter import adapt_yaml
    from preflight.adapters.xml_adapter import adapt_xml

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
    "VERSION",
]

VERSION = "0.1"