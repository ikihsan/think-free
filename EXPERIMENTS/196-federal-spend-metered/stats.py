#!/usr/bin/env python3
"""E196 statistics -- stdlib only (SciPy is absent on this host).

Two functions and a self-test. The self-test is not decoration: E177's sixth
instrument defect was a reader protocol with no control on its own arithmetic,
which left every control green while the p-value was wrong by 2,700x. So these
are checked against an **exact permutation test of the same data** -- a
different method, not a remembered constant. The first version of this file
compared against textbook figures from memory; one of them turned out to be
misremembered, which is precisely why the check was replaced rather than the
number corrected to match the code.
"""
import itertools
from math import comb
import math
import sys

_SELF_TEST = []


def gammq(a, x):
    """Regularised upper incomplete gamma Q(a, x). Abramowitz & Stegun 6.2.8/6.2.9."""
    if x < 0 or a <= 0:
        return float("nan")
    if x == 0:
        return 1.0
    eps, fp, itmax = 3e-14, 1e-300, 300
    gln = math.lgamma(a)
    if x < a + 1.0:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(itmax):
            ap += 1.0
            d *= x / ap
            s += d
            if abs(d) < abs(s) * eps:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - gln)
    b, c = x + 1.0 - a, 1.0 / fp
    d, h = 1.0 / b, 1.0 / b
    for i in range(1, itmax):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fp:
            d = fp
        c = b + an / c
        if abs(c) < fp:
            c = fp
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h * math.exp(-x + a * math.log(x) - gln)


def chi2_sf(x, df):
    """Upper tail of the chi-square distribution."""
    if df <= 0:
        return float("nan")
    if x <= 0:
        return 1.0
    return gammq(df / 2.0, x / 2.0)


def median(vals):
    s = sorted(vals)
    n = len(s)
    if not n:
        return None
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def _midranks(values, pool):
    return [sum(1 for y in pool if y < x) + 1
            + (sum(1 for y in pool if y == x) - 1) / 2.0 for x in values]


def _h_from_ranks(ranks, sizes, n):
    """H before tie correction.

    The Kruskal-Wallis statistic is `(sum of ranks in group i)^2 / n_i`
    summed over groups -- the *square of the group's rank total*, not the sum
    of squared ranks. The first version of this function computed the latter,
    which is a different statistic; it produced a negative H, and the
    self-test below is what caught it.
    """
    s = sum((sum(gr) ** 2) / float(len(gr)) for gr in ranks)
    return 12.0 / (n * (n + 1.0)) * s - 3.0 * (n + 1.0)


def kruskal_wallis(groups):
    """Tie-corrected H and its chi-square upper tail. groups: name -> list."""
    usable = {k: v for k, v in groups.items() if v}
    n = sum(len(v) for v in usable.values())
    k = len(usable)
    if k < 2 or n < 3:
        return None, None, 0, n
    pool = [x for v in usable.values() for x in v]
    ranks = [_midranks(v, pool) for v in usable.values()]
    h = _h_from_ranks(ranks, [len(v) for v in usable.values()], n)
    tie_corr = sum(c ** 3 - c for c in
                   (sum(1 for y in pool if y == v) for v in set(pool)) if c > 1)
    denom = 1.0 - tie_corr / float(n ** 3 - n)
    if denom <= 0:
        return None, None, k, n
    h /= denom
    return h, chi2_sf(h, k - 1), k, n


def _exact_permutation_p(groups, max_draws=400_000):
    """Exact permutation p for the same statistic, by enumerating relabellings.

    Returns (p, permutations_enumerated). Returns (None, n_perm) when the
    enumeration would exceed `max_draws`, so a caller can never mistake a
    truncated enumeration for an exact answer.
    """
    usable = [list(v) for v in groups.values() if v]
    if len(usable) < 2:
        return None, 0
    n = sum(len(v) for v in usable)
    sizes = [len(v) for v in usable]
    n_perm, rem = 1, n
    for s in sizes:
        n_perm *= comb(rem, s)
        rem -= s
    if n_perm > max_draws:
        return None, n_perm
    pool = [x for v in usable for x in v]
    obs = kruskal_wallis({str(i): v for i, v in enumerate(usable)})[0]
    if obs is None:
        return None, n_perm
    hits, drawn = [0], [0]

    def rec(i, remaining, sumsq):
        """sumsq accumulates (group rank total)^2 / n_i, the same terms H uses."""
        if i == len(sizes):
            drawn[0] += 1
            hh = 12.0 / (n * (n + 1.0)) * sumsq - 3.0 * (n + 1.0)
            if hh >= obs - 1e-12:
                hits[0] += 1
            return
        for c in itertools.combinations(remaining, sizes[i]):
            sub = [pool[j] for j in c]
            r = _midranks(sub, pool)
            left = [x for x in remaining if x not in c]
            rec(i + 1, left, sumsq + (sum(r) ** 2) / float(len(sub)))

    rec(0, list(range(n)), 0.0)
    return hits[0] / float(drawn[0]) if drawn[0] else None, drawn[0]


def _selftest():
    ok = True

    def check(name, good, detail=""):
        nonlocal ok
        ok = ok and bool(good)
        _SELF_TEST.append((name, detail, good))

    check("chi2_sf(x=0) is 1", abs(chi2_sf(0.0, 5) - 1.0) < 1e-12)
    check("chi2_sf monotone decreasing in x",
          chi2_sf(1.0, 3) > chi2_sf(2.0, 3) > chi2_sf(10.0, 3))
    check("chi2_sf(3.841459, df=1) is 0.05 to 1e-5",
          abs(chi2_sf(3.841458820694124, 1) - 0.05) < 1e-5)
    check("chi2_sf(5.991465, df=2) is 0.05 to 1e-5",
          abs(chi2_sf(5.991464547107979, 2) - 0.05) < 1e-5)

    a = [1.83, 0.50, 1.62, 2.48, 2.17, 1.68, 1.88, 1.55, 3.06, 1.30]
    b = [0.878, 0.647, 0.598, 2.05, 1.06, 1.29, 1.06, 3.14, 1.29]
    h, p, k, n = kruskal_wallis({"a": a, "b": b})
    exact, drawn = _exact_permutation_p({"a": a, "b": b})
    check("asymptotic p agrees with exact permutation p (2 groups)",
          exact is not None and abs(p - exact) < 0.01,
          "asymptotic p=%.5f exact p=%.5f over %d permutations" % (p, exact or -1, drawn))
    check("H is positive and p in (0,1)", h > 0 and 0 < p < 1, "H=%.4f p=%.5f" % (h, p))

    # three groups of four: C(12,4)*C(8,4) = 34,650 permutations, enumerable
    c1 = [10, 12, 9, 14]
    c2 = [20, 22, 19, 24]
    c3 = [30, 32, 29, 34]
    h3, p3, _, _ = kruskal_wallis({"c1": c1, "c2": c2, "c3": c3})
    e3, d3 = _exact_permutation_p({"c1": c1, "c2": c2, "c3": c3})
    check("asymptotic p agrees with exact permutation p (3 groups)",
          e3 is not None and abs(p3 - e3) < 0.01,
          "asymptotic p=%.5f exact p=%.5f over %d permutations" % (p3, e3 or -1, d3))
    check("3-group H is positive", h3 > 0, "H=%.2f" % h3)

    # degenerate inputs must be loud rather than silently significant
    _, p_all_ties, _, _ = kruskal_wallis({"a": [1.0] * 4, "b": [1.0] * 4})
    check("all-ties input yields no significant p", p_all_ties is None or p_all_ties >= 0.999,
          "p=%s" % (p_all_ties,))
    _, p_one, _, _ = kruskal_wallis({"a": []})
    check("single empty group yields no p", p_one is None)
    _, p_small, _, _ = kruskal_wallis({"a": [1.0], "b": [2.0]})
    check("two singleton groups yield no p", p_small is None or p_small >= 0.999)
    return ok


if __name__ == "__main__":
    _ok = _selftest()
    for name, detail, good in _SELF_TEST:
        print("%-52s %-58s %s" % (name, detail, "PASS" if good else "FAIL"))
    print("stats self-test:", "PASS" if _ok else "FAIL")
    sys.exit(0 if _ok else 3)