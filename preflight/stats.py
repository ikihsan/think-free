"""Wilson score interval, and the small stats the three checks share.

The interval is used for a reason that is not statistical fashion: every verdict
this package emits is a claim that a rate is low or high, and a rate reported
without an interval cannot be told apart from a rate measured on nine items.
"""

import math


def wilson(k, n, z=1.959963985):
    """Wilson score interval for a binomial proportion.

    Returns (lower, upper) in [0, 1]. Degenerate cells (n == 0, or every
    trial the same way) return (0.0, 0.0) or (1.0, 1.0) rather than NaN, so a
    caller can compare them without a special case.
    """
    if n == 0:
        return (0.0, 0.0)
    p = float(k) / float(n)
    denom = 1.0 + z * z / n
    centre = p + z * z / (2.0 * n)
    half = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n)
    return (max(0.0, (centre - half) / denom), min(1.0, (centre + half) / denom))


def fmt_interval(k, n, digits=4):
    lo, hi = wilson(k, n)
    return "%d/%d = %.4f CI95 [%.4f, %.4f]" % (k, n, (float(k) / n) if n else 0.0, lo, hi)