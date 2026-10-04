#!/usr/bin/env python3
"""Rank statistics for the T-0059 census, tie-aware.

The synthetic cases in `tests/test_census_stats.py` decided the design. With 25
implementations of which one has any measurable use, the usage ranks collapse
into one 24-way tie, and Spearman then separates "the used project is #1 on the
leaderboard" from "the used project is #3" by 0.283 against 0.34 — it cannot
resolve the only difference that matters. So Spearman is reported but is not the
primary statistic; the primary one is where in the leaderboard the most-used
project actually sits, which separates the same two cases as 1 against 3.

Stars are also only a proxy for the question. A perfect tie in stars, or a niche
where nothing at all is used, makes any rank statistic undefined. Each measure
returns None rather than a number in that case, and the gate treats None as
uninformative instead of as zero.
"""


def ranks(values):
    """Average ranks, ascending. Equal values share a rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return out


def spearman(a, b):
    """Rank correlation, or None when either side is entirely tied."""
    ra, rb = ranks(a), ranks(b)
    n = len(ra)
    if n < 3:
        return None
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = sum((ra[i] - ma) ** 2 for i in range(n)) ** 0.5
    db = sum((rb[i] - mb) ** 2 for i in range(n)) ** 0.5
    return None if da == 0 or db == 0 else num / (da * db)


def top_k_overlap(stars, usage, k=5):
    """(overlap_count, overlap_fraction, chance_fraction) for the top k.

    `chance_fraction` is min(1, k*k/n), what a usage ordering unrelated to the
    leaderboard would produce. It reaches 1 whenever k > sqrt(n), which is the
    case here: with 25 rows and k=5 every top-5 shares its one used member, so
    the overlap carries no information and must not be read as a pass.
    """
    n = len(stars)
    k = min(k, n)
    by_star = set(sorted(range(n), key=lambda i: -stars[i])[:k])
    by_use = set(sorted(range(n), key=lambda i: -usage[i])[:k])
    hit = len(by_star & by_use)
    return hit, round(hit / float(k), 3), round(min(1.0, k * k / float(n)), 3)


def star_rank_of_most_used(stars, usage):
    """1-indexed star rank of the project with the highest measured use.

    Returns None when nothing in the niche has any measured use, or when every
    project ties on stars — both mean the question was not answered.
    """
    if not stars or max(usage) <= 0 or len(set(stars)) == 1:
        return None
    return sorted(stars, reverse=True).index(max(
        (s for s, u in zip(stars, usage) if u == max(usage)))) + 1


def used_fraction(usage, threshold=1):
    """Share of implementations at or above a download threshold."""
    if not usage:
        return None
    return round(sum(1 for u in usage if u >= threshold) / float(len(usage)), 3)