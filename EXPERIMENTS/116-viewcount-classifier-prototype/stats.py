"""Pure statistics helpers for the E116 view-count classifier.

Split out of `classify.py` at the repository's 300-line cap. Everything
here is a total function over plain data: no network, no classification,
no experiment state.
"""

from math import sqrt, erfc


# ── Coverage & pool measurement ──────────────────────────────────

def compute_coverage(classifications):
    """Compute coverage rate from a list of (classification, weight, reason) tuples.

    coverage = (number classified) / (total items)
    A package is "classified" if its weight >= 0.5 (i.e., need-related or random).
    """
    total = len(classifications)
    if total == 0:
        return 0.0, 0, 0
    classified = sum(1 for c, w, r in classifications if w >= 0.5)
    return classified / total, classified, total


def compute_active_rate(packages):
    """Compute the active rate: proportion of packages with recent > 0 downloads."""
    if not packages:
        return 0.0, 0, 0
    active = sum(1 for p in packages if p.get("recent_downloads", 0) > 0)
    return active / len(packages), active, len(packages)


# ── Non-parametric effect size ──────────────────────────────────

def cliff_delta(x, y):
    """Compute Cliff's delta for two independent samples."""
    if not x or not y:
        return 0.0
    nx = len(x)
    ny = len(y)
    greater = 0
    less = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                greater += 1
            elif xi < yi:
                less += 1
    return (greater - less) / (nx * ny)


def mann_whitney_u(x, y):
    """Compute Mann-Whitney U test statistic and two-sided p-value."""
    if not x or not y:
        return 0.0, 1.0
    nx = len(x)
    ny = len(y)
    combined = sorted(x + y)
    n = len(combined)
    # Assign ranks
    rank_map = {}
    i = 0
    while i < n:
        val = combined[i]
        j = i
        while j < n and combined[j] == val:
            j += 1
        avg_rank = (i + j - 1) / 2.0 + 1  # 1-based
        for k in range(i, j):
            rank_map[combined[k]] = avg_rank
        i = j
    rx = sum(rank_map.get(v, 1) for v in x)
    ux = rx - nx * (nx + 1) / 2
    mu_u = nx * ny / 2.0
    sigma_u_sq = nx * ny * (nx + ny + 1) / 12.0
    if sigma_u_sq > 0:
        z = (ux - mu_u) / sqrt(sigma_u_sq)
        p = erfc(abs(z) / sqrt(2))
    else:
        z = 0
        p = 1.0
    return ux, p
