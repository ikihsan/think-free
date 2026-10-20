#!/usr/bin/env python3
"""
Fresh observation experiment: Wikipedia stubs vs developed articles view-count principle test.
Stdlib only: urllib, json, statistics, datetime, sys, time, random.
"""

import statistics
import sys
import time

from wiki_api import (
    get_stub_titles,
    get_random_titles,
    get_article_info,
    get_pageviews,
    SAMPLE_SIZE,
    DAYS_BACK,
)
from stats import cliffs_delta, mann_whitney_u


def main():
    print(f"Fetching {SAMPLE_SIZE} stub article titles...", file=sys.stderr)
    stub_titles = get_stub_titles(SAMPLE_SIZE)
    print(f"Got {len(stub_titles)} stub titles", file=sys.stderr)

    print(f"Fetching {SAMPLE_SIZE} random article titles...", file=sys.stderr)
    random_titles = get_random_titles(SAMPLE_SIZE)
    print(f"Got {len(random_titles)} random titles", file=sys.stderr)

    all_titles = stub_titles + random_titles
    print(f"Fetching article info for {len(all_titles)} articles...", file=sys.stderr)
    article_info = get_article_info(all_titles)

    valid_stub = [t for t in stub_titles if t in article_info and article_info[t]["length"] > 0]
    valid_random = [t for t in random_titles if t in article_info and article_info[t]["length"] > 0]

    print(f"Valid stubs: {len(valid_stub)}, Valid random: {len(valid_random)}", file=sys.stderr)

    if len(valid_stub) < 30 or len(valid_random) < 30:
        print("ERROR: Insufficient valid articles", file=sys.stderr)
        sys.exit(1)

    # Fetch pageviews
    print("Fetching pageviews...", file=sys.stderr)
    stub_views_per_byte = []
    stub_raw_views = []
    random_views_per_byte = []
    random_raw_views = []
    classifications = []

    for i, title in enumerate(valid_stub):
        if i % 20 == 0:
            print(f"  Stubs: {i}/{len(valid_stub)}...", file=sys.stderr)
        views = get_pageviews(title, DAYS_BACK)
        if views is None:
            print(f"    Skipping {title}: no pageviews data", file=sys.stderr)
            continue
        length = article_info[title]["length"]
        vp_byte = views / length if length > 0 else 0

        stub_views_per_byte.append(vp_byte)
        stub_raw_views.append(views)

        classifications.append({
            "title": title,
            "arm": "stub",
            "views": views,
            "length": length,
            "views_per_byte": vp_byte,
        })
        time.sleep(0.3)

    for i, title in enumerate(valid_random):
        if i % 20 == 0:
            print(f"  Random: {i}/{len(valid_random)}...", file=sys.stderr)
        views = get_pageviews(title, DAYS_BACK)
        if views is None:
            print(f"    Skipping {title}: no pageviews data", file=sys.stderr)
            continue
        length = article_info[title]["length"]
        vp_byte = views / length if length > 0 else 0

        random_views_per_byte.append(vp_byte)
        random_raw_views.append(views)

        classifications.append({
            "title": title,
            "arm": "developed",
            "views": views,
            "length": length,
            "views_per_byte": vp_byte,
        })
        time.sleep(0.3)

    print(f"Got pageviews for {len(stub_views_per_byte)} stubs, {len(random_views_per_byte)} developed", file=sys.stderr)

    # Compute gates (primary metric: views per byte)
    g1_pass = len(stub_views_per_byte) >= 30 and len(random_views_per_byte) >= 30
    g2_pass = len([v for v in stub_raw_views if v > 0]) / len(stub_raw_views) >= 0.8 if stub_raw_views else False
    g4_pass = len(stub_views_per_byte) / len(valid_stub) >= 0.8 and len(random_views_per_byte) / len(valid_random) >= 0.8

    delta = cliffs_delta(stub_views_per_byte, random_views_per_byte)
    u_stat, p_value = mann_whitney_u(stub_views_per_byte, random_views_per_byte)
    g3_pass = delta >= 0.147 and p_value < 0.05

    # Also compute for raw views
    delta_raw = cliffs_delta(stub_raw_views, random_raw_views)
    u_raw, p_raw = mann_whitney_u(stub_raw_views, random_raw_views)

    gates = {
        "G1_sample_size": {"pass": g1_pass, "stub_count": len(stub_views_per_byte), "developed_count": len(random_views_per_byte)},
        "G2_activity_presence": {"pass": g2_pass, "stub_with_views_pct": len([v for v in stub_raw_views if v > 0]) / len(stub_raw_views) * 100 if stub_raw_views else 0},
        "G3_differential_activity_vpbyte": {"pass": g3_pass, "cliffs_delta": delta, "p_value": p_value, "threshold": 0.147},
        "G3_differential_activity_raw": {"cliffs_delta": delta_raw, "p_value": p_raw, "note": "Raw views (secondary)"},
        "G4_metadata_universality": {"pass": g4_pass, "stub_coverage": len(stub_views_per_byte) / len(valid_stub) * 100, "developed_coverage": len(random_views_per_byte) / len(valid_random) * 100},
    }

    all_pass = all(g["pass"] for g in gates.values() if "pass" in g)

    results = {
        "experiment": "167-wikipedia-fresh-observation",
        "timestamp": time.time(),
        "stub_count": len(stub_views_per_byte),
        "developed_count": len(random_views_per_byte),
        "stub_vpbyte_stats": {
            "mean": statistics.mean(stub_views_per_byte) if stub_views_per_byte else 0,
            "median": statistics.median(stub_views_per_byte) if stub_views_per_byte else 0,
            "stdev": statistics.stdev(stub_views_per_byte) if len(stub_views_per_byte) > 1 else 0,
        },
        "developed_vpbyte_stats": {
            "mean": statistics.mean(random_views_per_byte) if random_views_per_byte else 0,
            "median": statistics.median(random_views_per_byte) if random_views_per_byte else 0,
            "stdev": statistics.stdev(random_views_per_byte) if len(random_views_per_byte) > 1 else 0,
        },
        "stub_raw_stats": {
            "mean": statistics.mean(stub_raw_views) if stub_raw_views else 0,
            "median": statistics.median(stub_raw_views) if stub_raw_views else 0,
        },
        "developed_raw_stats": {
            "mean": statistics.mean(random_raw_views) if random_raw_views else 0,
            "median": statistics.median(random_raw_views) if random_raw_views else 0,
        },
        "cliffs_delta_vpbyte": delta,
        "mann_whitney_u_vpbyte": u_stat,
        "p_value_vpbyte": p_value,
        "cliffs_delta_raw": delta_raw,
        "p_value_raw": p_raw,
        "gates": gates,
        "all_gates_pass": all_pass,
        "conclusion": "H1 supported (principle generalizes)" if all_pass else "H0 supported (principle does not generalize)",
    }

    # Write results
    with open("results.json", "w") as f:
        import json
        json.dump(results, f, indent=2)

    with open("classification.json", "w") as f:
        json.dump(classifications, f, indent=2)

    # Print summary
    print("\n=== RESULTS (views per byte) ===")
    print(f"Stubs: {len(stub_views_per_byte)} articles")
    print(f"  Mean vpbyte: {results['stub_vpbyte_stats']['mean']:.6f}")
    print(f"  Median vpbyte: {results['stub_vpbyte_stats']['median']:.6f}")
    print(f"Developed: {len(random_views_per_byte)} articles")
    print(f"  Mean vpbyte: {results['developed_vpbyte_stats']['mean']:.6f}")
    print(f"  Median vpbyte: {results['developed_vpbyte_stats']['median']:.6f}")
    print(f"Cliff's delta: {delta:.4f} (threshold: 0.147)")
    print(f"Mann-Whitney U: {u_stat:.1f}, p-value: {p_value:.4f}")
    print(f"\n=== RESULTS (raw views) ===")
    print(f"Stubs: Mean={results['stub_raw_stats']['mean']:.1f}, Median={results['stub_raw_stats']['median']:.1f}")
    print(f"Developed: Mean={results['developed_raw_stats']['mean']:.1f}, Median={results['developed_raw_stats']['median']:.1f}")
    print(f"Cliff's delta (raw): {delta_raw:.4f}")
    print(f"\nGates:")
    for name, g in gates.items():
        status = "PASS" if g.get("pass", False) else ("FAIL" if "pass" in g else "N/A")
        print(f"  {name}: {status}")
    print(f"\nOverall: {'ALL GATES PASS' if all_pass else 'KILL GATE FIRED'}")
    print(f"Conclusion: {results['conclusion']}")


if __name__ == "__main__":
    main()