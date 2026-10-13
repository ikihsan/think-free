"""Effect-size and significance helpers, split out of the measuring script.

Standard-library statistics shared by the view-count experiments: Cliff's
delta, the Mann-Whitney U normal approximation, and the Wilson interval.
They were moved here because the caller's inline word lists had already
taken it over the 300-line cap, and these functions are the part worth
testing on its own.
"""
import math

def cliffs_delta(group1: list, group2: list) -> float:
    """Compute Cliff's delta effect size."""
    if not group1 or not group2:
        return 0.0
    
    n1, n2 = len(group1), len(group2)
    greater = sum(1 for x in group1 for y in group2 if x > y)
    less = sum(1 for x in group1 for y in group2 if x < y)
    return (greater - less) / (n1 * n2)

def mann_whitney_u(group1: list, group2: list) -> tuple:
    """Compute Mann-Whitney U test statistic and p-value (normal approximation)."""
    import math
    
    n1, n2 = len(group1), len(group2)
    if n1 == 0 or n2 == 0:
        return 0.0, 1.0
    
    # Combine and rank
    combined = [(x, 0) for x in group1] + [(x, 1) for x in group2]
    combined.sort(key=lambda x: x[0])
    
    # Handle ties
    ranks = {}
    for i, (val, _) in enumerate(combined):
        if val not in ranks:
            ranks[val] = []
        ranks[val].append(i + 1)
    
    rank_sum1 = 0
    for val, group in combined:
        if group == 0:
            avg_rank = sum(ranks[val]) / len(ranks[val])
            rank_sum1 += avg_rank
    
    u1 = rank_sum1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    
    # Tie correction
    tie_correction = 0
    for val, positions in ranks.items():
        if len(positions) > 1:
            t = len(positions)
            tie_correction += t * (t * t - 1)
    
    if tie_correction > 0:
        std_u *= math.sqrt(1 - tie_correction / (n1 + n2) / ((n1 + n2) * (n1 + n2) - 1))
    
    if std_u == 0:
        return u, 1.0
    
    z = (u - mean_u) / std_u
    # Two-tailed p-value
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    
    return u, p

def wilson_ci(count: int, total: int, confidence: float = 0.95) -> tuple:
    """Wilson score interval for binomial proportion."""
    if total == 0:
        return (0.0, 0.0)
    
    z = 1.96  # 95% CI
    p = count / total
    denom = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / total + z**2 / (4 * total**2))
    return (centre - half, centre + half)
