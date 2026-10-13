"""Gate evaluation and results.json writing for the E0xx prototype.

Moved verbatim out of `experiment.py`: the G1-G4 verdict block was the
last block over the 300-line cap in `docs/policy/doc-standards.md`, and
the thresholds and JSON keys here are the experiment's contract.
"""
import json
import os
import time

from vocabulary import THRESHOLD_RATIO


def evaluate_and_report(keyword, packages, final_classified, final_active,
                        classified_count, failures, priority_entries, out_dir=None):
    """Evaluate G1-G4 and write results.json. Returns a process exit code.

    Split out of `main()`, which had passed the 300-line cap in
    `docs/policy/doc-standards.md`. Gate thresholds, printed lines and
    JSON keys are unchanged: this is a move, not a rewrite.
    """
    # Step 3: Evaluate gates
    print("\n=== Gate Evaluation ===")
    
    # G2: sample size >= 100
    g2_pass = classified_count >= 100
    print(f"  G2 gate (classified >= 100): {'PASS' if g2_pass else 'FAIL'} (classified: {classified_count})")
    
    # G4: classified >= 50
    g4_pass = classified_count >= 50
    print(f"  G4 gate (classified >= 50): {'PASS' if g4_pass else 'FAIL'} (classified: {classified_count})")
    
    # G1: need-related active rate >= 55% of random active rate
    if final_classified["need-related"] > 0 and final_classified["random"] > 0:
        need_rate = final_active["need-related"] / final_classified["need-related"]
        random_rate = final_active["random"] / final_classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= THRESHOLD_RATIO
        print(f"  G1 gate (need/random active ratio >= {THRESHOLD_RATIO*100:.0f}%): {'PASS' if g1_pass else 'FAIL'}")
        print(f"    need-related active rate: {need_rate*100:.1f}%")
        print(f"    random active rate: {random_rate*100:.1f}%")
        print(f"    ratio: {ratio*100:.1f}%")
    else:
        g1_pass = False
        print(f"  G1 gate: SKIPPED (insufficient classification: need-related={final_classified['need-related']}, random={final_classified['random']})")
    
    # G3: both categories represented
    g3_pass = final_classified["need-related"] > 0 and final_classified["random"] > 0
    print(f"  G3 gate (both categories represented): {'PASS' if g3_pass else 'FAIL'} (need-related: {final_classified['need-related']}, random: {final_classified['random']})")
    
    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n  Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'}")
    
    # Step 4: Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "keyword": keyword,
        "sample_size": len(packages),
        "classified": final_classified,
        "active": final_active,
        "active_rates": {
            "need-related": final_active["need-related"] / final_classified["need-related"] if final_classified["need-related"] > 0 else 0,
            "random": final_active["random"] / final_classified["random"] if final_classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "conclusion": "pending",
        "experiment_description": "View-count principle prototype v3: PyPI package discovery tool",
        "prioritized_packages": [
            {
                "name": p["name"],
                "priority_score": p["priority_score"],
                "indicator_count": p["indicator_count"],
                "active": p["active"],
            }
            for p in priority_entries[:20]
        ],
    }
    
    if out_dir is None:
        out_dir = os.path.join("EXPERIMENTS", "0xx-viewcount-prototype")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-viewcount-prototype/results.json ===")
    
    return 0 if all_pass else 2
