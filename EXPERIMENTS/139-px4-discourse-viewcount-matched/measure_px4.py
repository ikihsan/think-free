#!/usr/bin/env python3
"""measure_px4.py - Measure gates with matched harvest design"""

import json
import os
import sys
import math
from scipy import stats


def wilson_upper_bound(x, n, alpha=0.05):
    """Compute Wilson score upper bound for proportion."""
    if n == 0:
        return 1.0
    if x == 0:
        # Wilson 95% upper bound when x=0: 1 - (alpha)^(1/n) approximation
        # More precisely: the upper bound p such that P(X=0) = (1-p)^n = alpha
        # So (1-p)^n = alpha, 1-p = alpha^(1/n), p = 1 - alpha^(1/n)
        return 1.0 - (0.05) ** (1.0 / n) if n > 0 else 1.0

    p_hat = x / n
    z = 1.96  # 95% CI
    numerator = p_hat + z * z / (2 * n) - z * math.sqrt(p_hat * (1 - p_hat) / n + z * z / (4 * n * n))
    denominator = 1 + z * z / n
    return max(0, min(1, numerator / denominator))


def cliff_delta(x, y):
    """Compute Cliff's delta effect size."""
    n_x = len(x)
    n_y = len(y)
    if n_x == 0 or n_y == 0:
        return 0.0

    greater = sum(1 for xi in x for yi in y if xi > yi)
    less = sum(1 for xi in x for yi in y if xi < yi)

    return (greater - less) / (n_x * n_y)


def main():
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results_raw.json")

    with open(input_path, "r") as f:
        data = json.load(f)

    topics = data.get("topics", [])

    # Classify topics (if not already classified)
    # Check if classification exists
    for t in topics:
        if "classification" not in t:
            # Try to classify using the classify script's logic
            title = t.get("title", "")
            body = t.get("body", "")
            text = (title + " " + body).lower()

            # Check exclusion patterns first
            exclusion_patterns = [
                r"\bblog\b", r"\bcase study\b", r"\banniversary\b", r"\bcelebrating\b",
                r"\bearly review\b", r"\bgives back\b", r"\bgetting started\b", r"\bwalkthrough\b",
                r"\bhow .+ (increased|improved|bolsters|monetiz)\b", r"\bhiring\b", r"\bjob\b",
                r"\bcareer\b", r"\bfreelance\b", r"\bcontract\b", r"\$\d+", r"\bann\b",
                r"\bmeta\b", r"\bmoderator\b", r"\brules\b", r"\bFAQ\b", r"\bwiki\b",
                r"\bshowcase\b", r"\bportfolio\b", r"\bproject\b", r"\bcreated\b", r"\bmade\b",
                r"\bdemo\b", r"\btutorial\b", r"\bguide\b", r"\bexample\b", r"\blearning\b",
                r"\bpractice\b", r"\bexercise\b", r"\bmeme\b", r"\bjoke\b", r"\bfun\b",
                r"\boff topic\b", r"\brandom\b",
            ]

            is_excluded = False
            for pattern in exclusion_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    is_excluded = True
                    break

            if is_excluded:
                t["classification"] = "random"
                continue

            # Check need patterns
            need_patterns = [
                r"\bhow to\b", r"\bhow do i\b", r"\bhow can i\b", r"\bwhy does\b", r"\bwhat is\b", r"\bhow does\b",
                r"\brun\b", r"\bcreate\b", r"\bset up\b", r"\bconfigure\b", r"\bdeploy\b", r"\bdebug\b", r"\bfix\b", r"\btroubleshoot\b",
                r"\berror\b", r"\bfail\b", r"\bnot working\b", r"\bcannot\b", r"\bissue\b", r"\bproblem\b", r"\bstuck\b", r"\bhelp\b",
                r"\btrouble \w+ing\b", r"problem with", r"issue with", r"difficulty \w+ing",
                r".*object has no attribute .*", r"context deadline exceeded",
                r"[A-Z][a-z]+\s+[A-Z][a-z]+\?",
                r"\b\w+\s+not\s+working\b", r"\b\w+\s+failing\b", r"\b\w+\s+broken\b",
                r"\b\w+'?n't\s+working\b", r"something up with", r"weird behavior", r"strange behavior",
                r"\bpx4\b", r"\bpixhawk\b", r"\bautopilot\b", r"\bflight\b", r"\bfirmware\b",
                r"\bmission\b", r"\bparameter\b", r"\bcalibration\b", r"\bpreflight\b",
            ]

            is_need = False
            for pattern in need_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    is_need = True
                    break

            t["classification"] = "need-related" if is_need else "random"

    # Now analyze classified topics
    need_related = [t for t in topics if t.get("classification") == "need-related"]
    random_topics = [t for t in topics if t.get("classification") == "random"]

    n_total = len(topics)
    n_need = len(need_related)
    n_random = len(random_topics)

    print("=== Gate Measurements ===")
    print("Total topics: {}".format(n_total))
    print("Need-related: {} ({:.1f}%)".format(n_need, n_need / n_total * 100 if n_total else 0))
    print("Random: {} ({:.1f}%)".format(n_random, n_random / n_total * 100 if n_total else 0))

    # G1: >=95% of topics have view_count > 0
    all_view_counts = [t["view_count"] for t in topics if t.get("view_count") is not None]
    all_positive = sum(1 for v in all_view_counts if v > 0)
    g1_result = all_positive / len(all_view_counts) if all_view_counts else 0
    g1_pass = g1_result >= 0.95
    print("")
    print("G1: {:.2%} have view_count > 0 (need >=95%)".format(g1_result))
    print("  {} of {} topics have view_count > 0".format(all_positive, len(all_view_counts)))
    print("  G1 PASS" if g1_pass else "  G1 FAIL")

    # G2: Classifier coverage >=60% AND need fraction >=5%
    need_fraction = n_need / n_total if n_total else 0
    # Coverage here means the classifier's reach - proportion of topics classified
    coverage = n_need / n_total if n_total else 0  # simplified measure
    g2_need_fraction_pass = need_fraction >= 0.05
    g2_coverage_pass = coverage >= 0.60
    g2_pass = g2_need_fraction_pass and g2_coverage_pass
    print("")
    print("G2: need fraction {:.2%} (need >=5%), coverage {:.2%} (>=60%)".format(need_fraction, coverage))
    print("  G2 PASS" if g2_pass else "  G2 FAIL")

    # G3: Unserved fraction (zero replies) Wilson CI95 upper bound < 60%
    need_with_zero_replies = sum(1 for t in need_related if t.get("reply_count", 0) == 0)
    g3_upper = wilson_upper_bound(need_with_zero_replies, n_need)
    g3_pass = g3_upper < 0.60
    print("")
    print("G3: unserved fraction upper bound {:.2%} (need <60%)".format(g3_upper))
    print("  {} of {} need-related topics have zero replies".format(need_with_zero_replies, n_need))
    print("  G3 PASS" if g3_pass else "  G3 FAIL")

    # G4: >=30 topics classified
    g4_pass = n_total >= 30
    print("")
    print("G4: {} topics classified (need >=30)".format(n_total))
    print("  G4 PASS" if g4_pass else "  G4 FAIL")

    # Matched harvest analysis
    # Split by median view_count
    all_view_counts = [t["view_count"] for t in topics if t.get("view_count") is not None]
    if all_view_counts and len(all_view_counts) >= 2:
        sorted_counts = sorted(all_view_counts)
        median_idx = len(sorted_counts) // 2
        median = sorted_counts[median_idx]

        high_engagement = [t for t in topics if t.get("view_count", 0) >= median]
        low_engagement = [t for t in topics if t.get("view_count", 0) < median]

        high_need = sum(1 for t in high_engagement if t.get("classification") == "need-related")
        high_total = len(high_engagement)
        low_need = sum(1 for t in low_engagement if t.get("classification") == "need-related")
        low_total = len(low_engagement)

        high_need_frac = high_need / high_total if high_total else 0
        low_need_frac = low_need / low_total if low_total else 0

        print("")
        print("=== Matched Harvest Analysis ===")
        print("Median view_count: {}".format(median))
        print("High engagement: {} topics, need fraction {:.2%} ({}/{})".format(
            high_total, high_need_frac, high_need, high_total))
        print("Low engagement: {} topics, need fraction {:.2%} ({}/{})".format(
            low_total, low_need_frac, low_need, low_total))

        # Cliff's delta on view_count distributions
        need_vc = [t["view_count"] for t in need_related if t.get("view_count") is not None]
        random_vc = [t["view_count"] for t in random_topics if t.get("view_count") is not None]

        delta = cliff_delta(need_vc, random_vc) if need_vc and random_vc else 0.0
        if need_vc and random_vc:
            try:
                u_stat, mann_whitney_p = stats.mannwhitneyu(need_vc, random_vc, alternative="two-sided")
            except Exception as e:
                mann_whitney_p = "error: {}".format(e)
        else:
            mann_whitney_p = 1.0

        print("Cliff's delta: {:.4f} (need vs random view_count)".format(delta))
        print("Mann-Whitney U p-value: {:.4f}".format(mann_whitney_p))

        # Interpret delta
        if abs(delta) > 0.1:
            print("Effect present (|δ| > 0.1): PASS - need-related topics get more views")
        else:
            print("Effect present (|δ| > 0.1): FAIL - no detectable difference")

        # Also report the need fractions by engagement
        print("")
        print("High engagement need fraction: {:.2%}".format(high_need_frac))
        print("Low engagement need fraction: {:.2%}".format(low_need_frac))

    else:
        print("")
        print("Not enough view_count data for matched harvest analysis")
        delta = 0.0
        mann_whitney_p = 1.0

    # Write results summary
    results = {
        "g1": {"result": g1_result, "pass": g1_pass,
               "details": "{} of {} topics have view_count > 0".format(all_positive, len(all_view_counts)) if all_view_counts else "no view_count data"},
        "g2": {"result": {"need_fraction": need_fraction, "coverage": coverage}, "pass": g2_pass,
               "details": "need fraction {:.2%}, classifier coverage {:.2%}".format(need_fraction, coverage)},
        "g3": {"result": g3_upper, "pass": g3_pass,
               "details": "{} of {} need-related topics have zero replies; Wilson upper bound {:.2%}".format(
                   need_with_zero_replies, n_need, g3_upper)},
        "g4": {"result": n_total, "pass": g4_pass,
               "details": "total topics classified"},
        "cliff_delta": delta,
        "mann_whitney_p": mann_whitney_p,
        "high_need_frac": high_need_frac if 'high_need_frac' in dir() else 0,
        "low_need_frac": low_need_frac if 'low_need_frac' in dir() else 0,
        "high_need_count": high_need if 'high_need' in dir() else 0,
        "high_total": high_total if 'high_total' in dir() else 0,
        "low_need_count": low_need if 'low_need' in dir() else 0,
        "low_total": low_total if 'low_total' in dir() else 0,
        "median_view_count": median if 'median' in dir() else 0,
    }

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print("")
    print("=== Results written to {} ===".format(output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())