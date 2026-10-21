#!/usr/bin/env python3
"""Run fresh observation experiment: view-count principle on PyPI packages."""
import json
import os
import sys
import time
from pathlib import Path

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from viewcount_core import NEED_INDICATORS, GENERIC_TERMS, _matches_word_boundary, classify_package, is_active
from viewcount_prototype import search_pypi, run_prototype

def main():
    keyword = "database"
    print(f"Fresh observation: view-count principle on PyPI packages (keyword: {keyword})")
    print("=" * 60)

    # Fetch packages from PyPI
    packages = search_pypi(keyword, max_results=200)
    sample_size = len(packages)

    print(f"Fetched {sample_size} packages from PyPI")

    if not sample_size:
        print("No packages fetched; using embedded fallback sample")
        # The search_pypi function handles fallback internally

    # Classify packages
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_pkgs = []

    for pkg in packages:
        desc = pkg.get("description", "") or pkg.get("summary", "") or ""
        cls = classify_package(desc)
        classified[cls] += 1
        act = is_active(pkg)
        active[cls] += act
        if cls == "need-related":
            need_related_pkgs.append(pkg)

    print(f"Classification: {classified}")
    print(f"Active counts: {active}")

    # Compute gates
    g1_pass = False
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"\nG1: need-related active rate={need_rate*100:.1f}%")
        print(f"      random active rate={random_rate*100:.1f}%")
        print(f"      ratio (need/random)={ratio*100:.1f}%")
        print(f"      G1 pass (>= 55%): {'PASS' if g1_pass else 'FAIL'}")
    else:
        print("\nG1: SKIPPED - need at least one package in each category")

    # G2 gate: minimum classified sample size >= 100
    g2_pass = (classified["need-related"] + classified["random"]) >= 100
    print(f"\nG2: classified total={classified['need-related'] + classified['random']}")
    print(f"      G2 pass (>= 100): {'PASS' if g2_pass else 'FAIL'}")

    # G3 gate: both categories represented
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"\nG3: both categories present={g3_pass}")

    # G4 gate: minimum 50 classified
    g4_pass = (classified["need-related"] + classified["random"]) >= 50
    print(f"\nG4: classified total>=50={g4_pass}")

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\nAll gates pass: {'YES' if all_pass else 'NO'}")

    # Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": os.uname().machine if hasattr(os, "uname") else "unknown",
        "sample_size": sample_size,
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0
            else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "conclusion": "pending",
        "experiment_description": f"Fresh observation: view-count principle on PyPI packages (keyword: {keyword})",
    }

    out_dir = Path("results_json_out")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Print need-related packages
    print(f"\nNeed-related packages (top {min(5, len(need_related_pkgs))}):")
    for i, pkg in enumerate(need_related_pkgs[:5]):
        name = pkg.get("name", "N/A")
        version = pkg.get("version", "N/A")
        desc = pkg.get("description", "")[:80] if pkg.get("description") else ""
        active_str = "ACTIVE" if is_active(pkg) else "inactive"
        print(f"  {i+1}. {name} {version} -- {desc}... [{active_str}]")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())