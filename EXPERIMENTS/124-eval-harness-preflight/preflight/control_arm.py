"""C3 -- is the declared negative arm actually negative?

A gate that scores a reader on a "control" arm is asserting something about the
arm, usually without writing it down: that no true positive lives there. When the
assertion is false the gate stops measuring the reader. It measures the arm, and
it does it identically for every subject, so a reader that invents and a reader
that reads correctly come out the same and the result reads as a clean finding
about the reader (F122: `G0_C_precision = 0.0`, for the incumbent detector and a
naive rule as well as for the assistant).

The check is deliberately narrow. It does not know what a "positive" is in your
domain; you supply a predicate over evidence the key does not use. What it adds
is the interval, and the refusal: an arm that holds positives is not a control,
and a gate built on it cannot separate the subjects it was built to separate.
"""

from .stats import fmt_interval, wilson


def control_arm(rows, is_positive, premise=0.0, name="control"):
    """Count the true positives inside a declared negative arm.

    `is_positive(row)` must read something outside the key -- the row's own
    evidence, a second source, a pattern in a free-text field. A predicate that
    consults the key reproduces the key and can only confirm it.

    `premise` is what the gate assumes: 0.0 for "this arm holds no positives".
    A nonzero premise is a legitimate declaration, and is measured against.
    """
    hits = [r for r in rows if is_positive(r)]
    n = len(rows)
    rate = float(len(hits)) / n if n else 0.0
    lo, hi = wilson(len(hits), n)
    verdict = "OK"
    reason = ""
    if not n:
        verdict = "NO_CONTROL_ROWS"
        reason = "the declared control arm is empty, so the gate it feeds measures nothing"
    elif lo > premise:
        verdict = "CONTROL_NOT_EMPTY"
        reason = ("%d of %d rows in the declared negative arm carry a true positive "
                  "(Wilson lower bound %.4f > premise %.4f): every subject scores "
                  "identically here, so this arm cannot separate them"
                  % (len(hits), n, lo, premise))
    return {
        "check": "C3_control_arm",
        "verdict": verdict,
        "reason": reason,
        "arm": name,
        "rows": n,
        "positives": len(hits),
        "premise": premise,
        "rate": round(rate, 4),
        "wilson": [round(lo, 4), round(hi, 4)],
        "summary": fmt_interval(len(hits), n),
        "examples": [{"id": r.get("id") or r.get("account_id") or r.get("name"), "evidence": r.get("evidence")}
                     for r in hits[:5]],
    }