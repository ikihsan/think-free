#!/usr/bin/env python3
"""Statistical utilities for view-count principle experiments. Stdlib only."""

import math
from typing import List, Tuple


def cliffs_delta(x: List[float], y: List[float]) -> float:
    """Compute Cliff's delta (effect size). Positive = x > y."""
    if not x or not y:
        return 0.0
    n_x, n_y = len(x), len(y)
    greater = 0
    less = 0
    for xi in x:
        for yj in y:
            if xi > yj:
                greater += 1
            elif xi < yj:
                less += 1
    return (greater - less) / (n_x * n_y)


def mann_whitney_u(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Mann-Whitney U test. Returns (U, p-value approximation)."""
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

    r_x = sum(ranks[idx] for idx, (_, g) in enumerate(combined) if g == 0)
    n_x, n_y = len(x), len(y)

    u_x = r_x - n_x * (n_x + 1) / 2
    u_y = n_x * n_y - u_x
    u = min(u_x, u_y)

    mean_u = n_x * n_y / 2
    std_u = (n_x * n_y * (n_x + n_y + 1) / 12) ** 0.5
    if std_u == 0:
        return u, 1.0
    z = (u - mean_u) / std_u
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u, p