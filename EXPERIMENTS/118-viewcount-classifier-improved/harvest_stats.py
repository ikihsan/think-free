"""Statistics and the matched harvest for E118's classifier, split out.

Lifted verbatim so `e118_classifier.py` fits the 300-line cap in
`docs/policy/doc-standards.md`. The vocabulary it classifies with moved to
`e118_vocabulary.json`; the classifier itself stayed in the caller.
"""
import math
from typing import Dict, List, Tuple


def make_matched_harvest(
    all_packages: List[Dict],
    n_need: int,
    n_random: int,
) -> Tuple[List[Dict], List[Dict]]:
    """Split packages into need and random arms using matched harvest design.

    Both arms come from the SAME pool of packages, divided by classification
    rather than drawn from different topics/queries sorted by the outcome metric.
    We stratify by download count (popularity) so that each stratum has a
    comparable mix of high/low popularity packages in both arms.

    Returns (need_arm, random_arm) lists of package dicts.
    """
    # Sort all packages by recent downloads (popularity)
    sorted_pkgs = sorted(all_packages, key=lambda p: p.get("downloads_recent", 0), reverse=True)

    # Stratify into popularity strata (e.g., quartiles)
    n = len(sorted_pkgs)
    n_strata = min(4, max(2, n // 50))  # ~50 packages per stratum
    stratum_size = n // n_strata
    remaining = n % n_strata

    # Assign each package to a stratum
    strata: List[List[Dict]] = []
    idx = 0
    for i in range(n_strata):
        # Give the first `remaining` strata one extra package
        size = stratum_size + (1 if i < remaining else 0)
        stratum = sorted_pkgs[idx:idx + size]
        strata.append(stratum)
        idx += size

    # Within each stratum, classify packages and split between arms
    need_arm: List[Dict] = []
    random_arm: List[Dict] = []

    for stratum in strata:
        # Classify each package in the stratum
        classified: List[Tuple[Dict, str]] = []  # (pkg, "need"|"random"|"unclassified")
        for pkg in stratum:
            classification = classify_package_keyword(pkg)
            classified.append((pkg, classification))

        # Separate into need and random/unclassified groups
        need_in_stratum = [p for p, c in classified if c == "need-related"]
        other_in_stratum = [p for p, c in classified if c != "need-related"]

        # Distribute need packages evenly between arms
        # The "matched" part: same pool, different classification
        need_mid = len(need_in_stratum) // 2

        need_arm.extend(need_in_stratum[:need_mid])
        need_arm.extend(need_in_stratum[need_mid:])  # rest also go to need arm for balance

        # Other packages (random or unclassified) go to random arm
        random_arm.extend(other_in_stratum)

    # Trim to requested sizes
    need_arm = need_arm[:n_need]
    random_arm = random_arm[:n_random]

    return need_arm, random_arm

def mann_whitney_u(need_vals: List[int], random_vals: List[int]) -> Tuple[float, float, float]:
    """Mann-Whitney U test. Returns (U, p_value, cliff_delta)."""
    combined = [(v, "need") for v in need_vals] + [(v, "random") for v in random_vals]
    combined.sort(key=lambda x: x[0])

    # Assign ranks (average for ties)
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, min(j, len(ranks) + 1)):
            ranks[k] = avg_rank
        i = j

    # Sum ranks for need group
    n1 = len(need_vals)
    n2 = len(random_vals)
    r1 = sum(ranks[i] for i in range(min(n1, len(ranks))))

    # U statistic
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    # Normal approximation for p-value
    if n1 * n2 == 0:
        return u, 1.0, 0.0
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if std_u == 0:
        return u, 1.0, 0.0
    z = (u - mean_u) / std_u

    # Two-tailed p-value using normal approximation
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / math.sqrt(2))))

    # Cliff's delta
    greater = sum(1 for nv in need_vals for rv in random_vals if nv > rv)
    less = sum(1 for nv in need_vals for rv in random_vals if nv < rv)
    cliff_delta = (greater - less) / (n1 * n2) if n1 * n2 > 0 else 0.0

    return u, p, cliff_delta

def wilson_ci95_lower(x: int, n: int) -> float:
    """Wilson CI95 lower bound for proportion x/n."""
    if n == 0:
        return 0.0
    z = 1.96
    phat = x / n
    denominator = 1 + z**2 / n
    centre = phat + z**2 / (2 * n)
    margin = z * math.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    return max(0, (centre - margin) / denominator)
