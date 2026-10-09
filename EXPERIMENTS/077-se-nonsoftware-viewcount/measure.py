#!/usr/bin/env python3
"""
E077 — Measurement and aggregation for Discourse forums.
"""

import json
import math
from typing import Any, Dict, List

from classify import classify_topics


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def wilson_ci95(k: int, n: int) -> tuple:
    """Wilson score interval 95%."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z = 1.96
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - half, centre + half)


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def measure_forum(classified: List[Dict], domain: str) -> Dict:
    """Full measurement pipeline for a single forum's classified topics."""
    total = len(classified)

    if total == 0:
        return {
            "domain": domain,
            "total": 0,
            "view_positive": 0,
            "need_topics": 0,
            "unserved_open_like": 0,
            "unserved_fraction": 0.0,
            "wilson_ci95": [0.0, 0.0],
            "view_counts": [],
        }

    # Count
    view_positive = sum(1 for t in classified if t.get("views", 0) > 0)
    need_topics = sum(1 for t in classified if t["is_need"])
    unserved_open_like = sum(1 for t in classified if t["is_unserved_open_like"])

    # Wilson CI95
    ci_low, ci_high = wilson_ci95(unserved_open_like, total)

    # View count distribution
    view_counts = [t.get("views", 0) for t in classified]

    print(f"  Total: {total}")
    print(f"  view_count > 0: {view_positive} ({view_positive/total*100:.1f}%)")
    print(f"  Need topics: {need_topics} ({need_topics/total*100:.1f}%)")
    print(f"  Unserved-open-like: {unserved_open_like} ({unserved_open_like/total*100:.2f}%)")
    print(f"  Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")

    return {
        "domain": domain,
        "total": total,
        "view_positive": view_positive,
        "need_topics": need_topics,
        "unserved_open_like": unserved_open_like,
        "unserved_fraction": unserved_open_like / total if total > 0 else 0.0,
        "wilson_ci95": [ci_low, ci_high],
        "view_counts": view_counts,
    }


def aggregate_results(all_results: List[Dict]) -> Dict:
    """Aggregate results across all forums."""
    total_all = sum(r["total"] for r in all_results if "error" not in r)
    view_positive_all = sum(r["view_positive"] for r in all_results if "error" not in r)
    need_topics_all = sum(r["need_topics"] for r in all_results if "error" not in r)
    unserved_all = sum(r["unserved_open_like"] for r in all_results if "error" not in r)

    ci_low, ci_high = wilson_ci95(unserved_all, total_all)

    print(f"\n=== AGGREGATE RESULTS ===")
    print(f"Total topics: {total_all}")
    if total_all > 0:
        print(f"view_count > 0: {view_positive_all} ({view_positive_all/total_all*100:.1f}%)")
        print(f"Need topics: {need_topics_all} ({need_topics_all/total_all*100:.1f}%)")
        print(f"Unserved-open-like: {unserved_all} ({unserved_all/total_all*100:.2f}%)")
        print(f"Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")
    else:
        print("No data collected")

    # Gate assessments
    print(f"\n=== GATE ASSESSMENTS ===")

    # G1: view_count validation
    vc_rate = view_positive_all / total_all if total_all > 0 else 0
    g1_pass = vc_rate >= 0.95
    print(f"G1 (view_count >= 95%): {'PASS' if g1_pass else 'FAIL'} — {vc_rate*100:.1f}%")

    # G2: need prevalence
    need_rate = need_topics_all / total_all if total_all > 0 else 0
    g2_pass = need_rate >= 0.05
    print(f"G2 (need prevalence >= 5%): {'PASS' if g2_pass else 'FAIL'} — {need_rate*100:.1f}%")

    # G3: unserved fraction measurable
    unserved_rate = unserved_all / total_all if total_all > 0 else 0
    g3_pass = unserved_rate < 0.50 and ci_high < 0.60
    print(f"G3 (unserved < 50%, CI95 upper < 60%): {'PASS' if g3_pass else 'FAIL'} — {unserved_rate*100:.1f}%, CI95=[{ci_low*100:.1f}%, {ci_high*100:.1f}%]")

    # G4: cross-forum variance
    forums_with_unserved = sum(1 for r in all_results if "error" not in r and r["unserved_open_like"] > 0)
    g4_pass = forums_with_unserved >= 3
    print(f"G4 (>= 3 forums with unserved > 0): {'PASS' if g4_pass else 'FAIL'} — {forums_with_unserved} forums")

    all_gates_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\nALL GATES: {'PASS' if all_gates_pass else 'FAIL'}")

    return {
        "total": total_all,
        "view_positive": view_positive_all,
        "need_topics": need_topics_all,
        "unserved_open_like": unserved_all,
        "unserved_fraction": unserved_rate,
        "wilson_ci95": [ci_low, ci_high],
        "gates": {
            "G1_view_count": {"pass": g1_pass, "value": vc_rate},
            "G2_need_prevalence": {"pass": g2_pass, "value": need_rate},
            "G3_unserved_fraction": {"pass": g3_pass, "value": unserved_rate, "ci95": [ci_low, ci_high]},
            "G4_cross_forum_variance": {"pass": g4_pass, "forums_with_unserved": forums_with_unserved},
        },
        "all_gates_pass": all_gates_pass,
    }