#!/usr/bin/env python3
"""
E084 — Measure gates for PX4 fault code experiment
Stdlib Python 3.8 only, no external dependencies.
"""

import json
import sys
import os
from pathlib import Path
from collections import Counter
import math

RAW_DIR = Path("raw")
CLASSIFIED_FILE = RAW_DIR / "classified_topics.jsonl"


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (centre - half, centre + half)


def load_classified():
    """Load classified topics from JSONL."""
    topics = []
    with open(CLASSIFIED_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                topics.append(json.loads(line))
    return topics


def evaluate_gates(topics):
    """Evaluate all predeclared gates."""
    print("=== Gate Evaluation ===\n")
    
    # G1: Population - need structured cases (need to fetch topic details for this)
    # For now, count qualified topics as proxy
    qualified_count = len(topics)
    print(f"G1 Population: {qualified_count} qualified topics (proxy, need structured case count)")
    g1_pass = qualified_count >= 100  # Using qualified as proxy; real G1 needs structured cases
    print(f"  Gate threshold: >= 100 structured cases")
    print(f"  Status: {'PASS (proxy)' if g1_pass else 'FAIL (proxy)'}")
    
    # G2: Fault concentration - top 10 fault types cover >= 30% of cases
    fault_counts = Counter(t["fault_type"] for t in topics)
    total = sum(fault_counts.values())
    top10_faults = fault_counts.most_common(10)
    top10_sum = sum(count for _, count in top10_faults)
    top10_pct = top10_sum / total if total > 0 else 0
    
    print(f"\nG2 Fault concentration: top 10 cover {top10_pct:.1%} of cases")
    print(f"  Top 10 fault types:")
    for ft, count in top10_faults:
        print(f"    {ft}: {count} ({count/total:.1%})")
    print(f"  Gate threshold: >= 30%")
    g2_pass = top10_pct >= 0.30
    print(f"  Status: {'PASS' if g2_pass else 'FAIL'}")
    
    # G3: Airframe coverage - >= 10 distinct airframe/FC combinations in top 10 fault types
    top10_labels = [ft for ft, _ in top10_faults]
    top10_topics = [t for t in topics if t["fault_type"] in top10_labels]
    
    # Create airframe/FC combinations
    combo_counter = Counter()
    for t in top10_topics:
        combo = (t["airframe"], t["fc_hardware"])
        combo_counter[combo] += 1
    
    distinct_combos = len(combo_counter)
    print(f"\nG3 Airframe coverage: {distinct_combos} distinct airframe/FC combinations in top 10 fault types")
    print(f"  Combinations:")
    for (af, fc), count in combo_counter.most_common():
        print(f"    {af} + {fc}: {count}")
    print(f"  Gate threshold: >= 10")
    g3_pass = distinct_combos >= 10
    print(f"  Status: {'PASS' if g3_pass else 'FAIL'}")
    
    # G4: Root cause specificity - need manual classification of 50 random structured cases
    # For now, we can't evaluate without fetching topic details
    print(f"\nG4 Root cause specificity: REQUIRES MANUAL CLASSIFICATION")
    print(f"  Need to fetch topic details for {min(50, len(topics))} random topics")
    print(f"  Gate threshold: >= 60% name specific replaceable part/parameter")
    g4_pass = None  # Unknown until manual review
    print(f"  Status: PENDING")
    
    # G5: Incumbent gap - need survey of free tools
    print(f"\nG5 Incumbent gap: REQUIRES TOOL SURVEY")
    print(f"  Gate threshold: No single free tool covers >= 50% of top 10 fault types")
    g5_pass = None  # Unknown until survey
    print(f"  Status: PENDING")
    
    # Summary
    print("\n=== Gate Summary ===")
    print(f"G1 Population (proxy): {'PASS' if g1_pass else 'FAIL'}")
    print(f"G2 Fault concentration: {'PASS' if g2_pass else 'FAIL'}")
    print(f"G3 Airframe coverage: {'PASS' if g3_pass else 'FAIL'}")
    print(f"G4 Root cause specificity: PENDING (manual)")
    print(f"G5 Incumbent gap: PENDING (survey)")
    
    all_auto_pass = g1_pass and g2_pass and g3_pass
    print(f"\nAutomated gates: {'ALL PASS' if all_auto_pass else 'SOME FAIL'}")
    
    return {
        "g1_population_proxy": g1_pass,
        "g2_fault_concentration": g2_pass,
        "g3_airframe_coverage": g3_pass,
        "g4_root_cause_specificity": g4_pass,
        "g5_incumbent_gap": g5_pass,
        "fault_distribution": dict(fault_counts),
        "top10_faults": top10_faults,
        "top10_pct": top10_pct,
        "distinct_combos": distinct_combos,
        "qualified_count": qualified_count,
    }


def main():
    if not CLASSIFIED_FILE.exists():
        print(f"Error: {CLASSIFIED_FILE} not found. Run harvest.py first.", file=sys.stderr)
        sys.exit(1)
    
    topics = load_classified()
    print(f"Loaded {len(topics)} qualified topics")
    
    results = evaluate_gates(topics)
    
    # Save results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to results.json")


if __name__ == "__main__":
    main()