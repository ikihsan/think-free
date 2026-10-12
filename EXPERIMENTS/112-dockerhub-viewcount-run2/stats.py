#!/usr/bin/env python3
"""
Statistical functions for Docker Hub View-Count Principle Test.
"""

import math
from typing import List, Tuple


def mann_whitney_u(x: List[int], y: List[int]) -> Tuple[float, float]:
    """Mann-Whitney U test (two-sided). Returns (U, p_value)."""
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda t: t[0])
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    n1 = len(x)
    n2 = len(y)
    r1 = sum(ranks[i] for i in range(len(combined)) if combined[i][1] == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if std_u == 0:
        return u, 1.0
    z = (u - mean_u) / std_u
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u, p


def cliff_delta(x: List[int], y: List[int]) -> float:
    """Cliff's delta effect size."""
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return 0.0
    greater = sum(1 for a in x for b in y if a > b)
    less = sum(1 for a in x for b in y if a < b)
    return (greater - less) / (n1 * n2)


def wilson_lower_bound(k: int, n: int, z: float = 1.96) -> float:
    """Wilson score interval lower bound."""
    if n == 0:
        return 0.0
    p = k / n
    denom = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjust = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - adjust) / denom