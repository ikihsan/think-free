"""Effect-size and significance helpers, split out of the measuring script.

Standard-library statistics shared by the view-count experiments: Cliff's
delta, the Mann-Whitney U normal approximation, and the Wilson interval.
They were moved here because the caller's inline word lists had already
taken it over the 300-line cap, and these functions are the part worth
testing on its own.
"""
import math
from typing import List, Tuple

def wilson_ci(n: int, k: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denominator = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denominator
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))

def mann_whitney_u(x: List[int], y: List[int]) -> Tuple[float, float]:
    """Mann-Whitney U test. Returns (U statistic, p-value approximation)."""
    # Combine and rank
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda t: t[0])
    
    # Assign ranks (average for ties)
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2.0  # 1-indexed
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    
    # Sum ranks for group 0 (x)
    n1 = len(x)
    n2 = len(y)
    r1 = sum(ranks[i] for i in range(n1))
    
    # U statistic
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation for p-value
    if n1 * n2 == 0:
        return (0.0, 1.0)
    
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    
    if std_u == 0:
        return (u, 1.0)
    
    z = (u - mean_u) / std_u
    # Two-tailed p-value
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    
    return (u, p)
