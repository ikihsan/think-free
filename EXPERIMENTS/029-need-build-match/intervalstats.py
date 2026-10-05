#!/usr/bin/env python3
"""E029 -- the statistical primitives, kept apart from the gates that consume them.

Split out of `stats.py` while that file was at 350 lines, by invariant: this module
owns the arithmetic, `stats.py` owns the experiment's population, arms and gates. A
gate that both computes and applies its own threshold is harder to read against the
protocol than one that only applies.

Everything here is exact and checkable. `tests` assert the Wilson interval against a
figure this repository has already published (F042's 0 of 24, quoted as
CI95 [0.0, 0.138]) and assert that the identical-label case is refused rather than
reported as perfect agreement.
"""
import math
import re

DATA_SUFFIXES_NOTE = "unused; kept so the module has one clear purpose: arithmetic."

LABELS = {"addresses", "unrelated", "unclear"}


def wilson(k, n, z=1.96):
    """Wilson score interval. Returns (lo, hi), or (None, None) for an empty arm."""
    if not n:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (c - m) / d), min(1.0, (c + m) / d)


def newcombe_difference(k1, n1, k2, n2):
    """Newcombe score interval for p1 - p2, built from two Wilson intervals."""
    if not n1 or not n2:
        return None
    p1, p2 = k1 / float(n1), k2 / float(n2)
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    lower = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return {"difference": round(d, 6),
            "ci95": [round(max(-1.0, lower), 6), round(min(1.0, upper), 6)]}


def fisher_two_sided(k1, n1, k2, n2):
    """Two-sided Fisher exact p for a 2x2 table, by hypergeometric enumeration."""
    if not n1 or not n2:
        return None
    total = n1 + n2
    k = k1 + k2

    def prob(x):
        if not (0 <= x <= n1 and 0 <= k - x <= n2):
            return 0.0
        return math.comb(n1, x) * math.comb(n2, k - x) / float(math.comb(total, k))

    obs = prob(k1)
    lo, hi = max(0, k - n2), min(n1, k)
    return round(sum(prob(x) for x in range(lo, hi + 1)
                     if prob(x) <= obs * (1 + 1e-9)), 6)


def cohen_kappa(a, b):
    """Unweighted Cohen's kappa over the shared label set.

    Returns (None, table) when expected agreement is 1.0, because kappa is undefined
    there -- two readers who use one label each agree perfectly and score nothing.
    """
    cats = sorted(LABELS)
    n = len(a)
    if n == 0:
        return None, {}
    obs = {x: {y: 0 for y in cats} for x in cats}
    for x, y in zip(a, b):
        obs[x][y] += 1
    agree = sum(obs[x][x] for x in cats) / float(n)
    ra = {x: sum(obs[x].values()) / float(n) for x in cats}
    ca = {y: sum(obs[x][y] for x in cats) / float(n) for y in cats}
    exp = sum(ra[x] * ca[x] for x in cats)
    kappa = None if abs(1 - exp) < 1e-12 else (agree - exp) / (1 - exp)
    return kappa, {"observed_agreement": round(agree, 6), "expected": round(exp, 6),
                   "table": obs, "n": n}


STOP = set("""a an the is are was were be been being do does did doing have has had having
i you he she it we they them his her its their my your our this that these those there here
what which who whom when where why how all any some no not but if then than so as by for
from with without into onto about over under again more most other such only own same too
very can will just should now im ive dont doesnt isnt arent id like get got would could one
two also using use used make made get thing things way ways really something anything lot
know think want need looking look time people person way good great nice better best also
thing even still much many because while although though ever never always often sometimes
""".split())


def content_words(text):
    ws = re.findall(r"[a-z][a-z0-9+#.-]{2,}", (text or "").lower())
    return {w.strip(".-") for w in ws} - STOP


def lexical_overlap(need_text, titles):
    """Fraction of the need's content words appearing in the shipped titles.

    Feeds no gate anywhere in this experiment. E028 measured documentation coverage
    as `informative: false`, so a lexical score is a sanity reading, not a result --
    but it is the reading that exposed E029's replicate control (amendment 3).
    """
    nw = content_words(need_text)
    if not nw:
        return None
    tw = set()
    for t in titles:
        tw |= content_words(t or "")
    if not tw:
        return None
    return len(nw & tw) / float(len(nw))
