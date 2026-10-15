"""E165 — Gate computation and tier analysis utilities.

Split from run.py to stay within the 300-line cap.
"""

from typing import Dict, List, Optional, Any


# ---------------------------------------------------------------------------
# Gate computation
# ---------------------------------------------------------------------------

def compute_gates(classified: Dict[str, int], active: Dict[str, int],
                  total_classified: int, min_classified: int = 50) -> Dict[str, Any]:
    g1_pass = g2_pass = g3_pass = g4_pass = False
    need_rate = random_rate = ratio = 0.0

    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55

    g2_pass = total_classified >= 100
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    g4_pass = total_classified >= min_classified

    return {
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "g1_ratio": ratio,
        "g1_need_rate": need_rate,
        "g1_random_rate": random_rate,
        "classified_total": total_classified,
        "need_related_count": classified["need-related"],
        "random_count": classified["random"],
        "need_related_active": active["need-related"],
        "random_active": active["random"],
        "active_rates": {"need-related": need_rate, "random": random_rate},
    }


def compute_gates_for_packages(packages: List[Dict], classify_fn, active_fn) -> Dict[str, Any]:
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    for pkg in packages:
        cls = classify_fn(pkg)
        act = active_fn(pkg)
        classified[cls] += 1
        if act:
            active[cls] += 1
    return compute_gates(classified, active, sum(classified.values()))


# ---------------------------------------------------------------------------
# Tier analysis
# ---------------------------------------------------------------------------

def assign_tiers(packages: List[Dict], key_func, n_tiers: int = 3) -> Dict[int, List[Dict]]:
    valid = [p for p in packages if key_func(p) is not None]
    if not valid:
        return {}
    valid.sort(key=key_func)
    n = len(valid)
    tier_size = n // n_tiers
    remainder = n % n_tiers
    tiers = {}
    start = 0
    for i in range(n_tiers):
        size = tier_size + (1 if i < remainder else 0)
        tiers[i] = valid[start:start + size]
        start += size
    return tiers


def popularity_key(pkg: Dict) -> Optional[int]:
    return pkg.get("num_releases")


def age_key(pkg: Dict) -> Optional[int]:
    fr = pkg.get("first_release")
    if fr:
        try:
            return int(fr[:4])
        except (ValueError, IndexError):
            pass
    return None