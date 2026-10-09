#!/usr/bin/env python3
"""E067 outcome: reproduce the printed report from an outcome.json file.

Used to verify that the framework's output matches the expected format
from E062's outcome.py, and to print human-readable summaries.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def pct(a, b):
    """Percentage a/b, returning 0.0 when b is 0."""
    return 0.0 if not b else 100.0 * a / b


def wilson(k, n, z=1.959963985):
    """Wilson score interval lower/upper bounds."""
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(centre - half, 4), round(centre + half, 4))


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 outcome.py <outcome.json path>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as fh:
        outcome = json.load(fh)

    g1 = outcome["g1"]
    g4 = outcome["g4"]
    ua = outcome["unremedied_arrival"]
    us = outcome["unremedied_shape"]

    items_declared = g1.get("items_declared_by_api")
    requests_all_200 = g1.get("requests_all_200")
    rows_with_body = g1.get("rows_with_body")
    rows_with_outcome_fields = g1.get("rows_with_outcome_fields")
    total_count = g1.get("total_count_available_on_this_route")

    print("G1  rows=%d sites=%d api_items=%s all_200=%s with_body=%s outcome_fields=%s total_count_on_route=%s"
          % (g1["rows"], len(g1["sites"]),
             items_declared if items_declared is not None else "n/a",
             requests_all_200 if requests_all_200 is not None else "n/a",
             rows_with_body if rows_with_body is not None else "n/a",
             rows_with_outcome_fields if rows_with_outcome_fields is not None else "n/a",
             total_count if total_count is not None else "n/a"))
    print("G4  still-open share by age cohort:")
    for c in g4["cohorts"]:
        print("      %-6s n=%4d open %5.1f%%  accepted %5.1f%%"
              % (c["cohort"], c["n"], c["open_pct"], c["accepted_pct"]))
    print("      max gap %.1f points, gate(>=10)=%s, monotone=%s"
          % (g4["max_gap_points"],
             "PASS" if g4["meets_10_point_gate"] else "FAIL",
             "monotone" if g4["monotone"] else "not"))
    print("state distribution:")
    if "state_distribution" in outcome:
        for s in outcome["state_distribution"]:
            print("      %-9s n=%4d (%4.1f%%)  views median %6d p90 %7d max %8d"
                  % (s["state"], s["n"], s["share_pct"], s["median_views"],
                     s["p90_views"], s["max_views"]))
    else:
        print("  (no state distribution)")
    print(f"unremedied arrival (n={ua['n']}): %.1f%% of all views, median %d views; "
          "top row %d views unanswered %.1fy"
          % (ua["share_of_all_views_pct"],
             ua["median_views"],
             ua["top_row_views"],
             ua["top_row_unanswered_years"]))
    for k, v in sorted(ua["concentration"].items()):
        print("      %s of unremedied rows carry %s%% of ALL views"
              % (k, v["share_of_unremedied_views_pct"]))
    print(f"shape of the {ua['n']} no-remedy rows (all classified, see tsv):")
    classes = us.get("classes", {})
    for k, v in sorted(classes.items(), key=lambda x: -x[1]):
        print("      %-24s %3d  %5.1f%%" % (k, v, pct(v, ua["n"])))


if __name__ == "__main__":
    main()