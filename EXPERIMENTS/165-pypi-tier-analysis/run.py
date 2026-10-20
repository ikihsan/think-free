#!/usr/bin/env python3
"""
E165 — PyPI View-Count Principle Tier Analysis (main entry point).

Tests whether the view-count principle's G1 activity advantage varies across:
- Popularity tiers (by number of releases)
- Package age tiers (by first release year)

Imports vocabulary, PyPI client, and gate computation from local modules.
"""

import json
import os
import time
from typing import Dict, List, Any

from vocab import (
    classify_package, classify_by_keywords, is_active,
    NEED_INDICATORS, GENERIC_TERMS,
)
from pypi_client import fetch_simple_index, search_packages, fetch_pypi_package, extract_package_info
from gates import compute_gates_for_packages, assign_tiers, popularity_key, age_key


# ---------------------------------------------------------------------------
# Keywords for diverse package set
# ---------------------------------------------------------------------------

SEARCH_KEYWORDS = [
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "api", "client", "server", "framework",
    "parser", "serializer", "validation", "compression", "encryption",
    "queue", "messaging", "container", "docker", "kubernetes",
    "web", "http", "rest", "graphql", "cli", "async", "config",
    "utils", "tools", "helpers", "extensions", "plugins",
]


def fetch_packages(keywords: List[str], all_names: List[str], max_per_keyword: int = 20) -> List[Dict]:
    """Fetch packages from PyPI using keyword searches against cached index."""
    all_packages = []
    seen_names = set()

    for kw in keywords:
        print(f"  Searching for '{kw}'...")
        names = search_packages(kw, all_names, max_per_keyword)
        for name in names:
            if name in seen_names:
                continue
            pkg_data = fetch_pypi_package(name)
            if pkg_data is None:
                continue
            pkg_info = extract_package_info(pkg_data)
            pkg_info["_search_keyword"] = kw
            all_packages.append(pkg_info)
            seen_names.add(name)

    print(f"  Fetched {len(all_packages)} unique packages")
    return all_packages


def run_experiment() -> Dict[str, Any]:
    print("=== E165: PyPI View-Count Principle Tier Analysis ===")
    print(f"Search keywords: {len(SEARCH_KEYWORDS)}")
    print()

    # Step 1: Fetch simple index once
    print("[1] Loading PyPI simple index...")
    all_names = fetch_simple_index()
    if not all_names:
        return {"error": "Failed to load simple index"}

    # Step 2: Fetch package details
    print("[2] Fetching package details...")
    packages = fetch_packages(SEARCH_KEYWORDS, all_names, max_per_keyword=15)
    if not packages:
        return {"error": "No packages fetched"}

    # Step 3: Classify all packages
    print("[3] Classifying packages...")
    for pkg in packages:
        cls = classify_by_keywords(pkg)
        if cls is None:
            cls = classify_package(pkg.get("description", ""))
        pkg["classification"] = cls
        pkg["active"] = is_active(pkg)

    need_related = [p for p in packages if p["classification"] == "need-related"]
    random_pkgs = [p for p in packages if p["classification"] == "random"]
    print(f"  Need-related: {len(need_related)}")
    print(f"  Random: {len(random_pkgs)}")
    print()

    # Step 4: Overall gates
    print("[4] Computing overall gates...")
    overall_gates = compute_gates_for_packages(packages, classify_by_keywords, is_active)
    print(f"  G1 (ratio >= 55%): {'PASS' if overall_gates['g1_pass'] else 'FAIL'} (ratio={overall_gates['g1_ratio']*100:.1f}%)")
    print(f"  G2 (total >= 100): {'PASS' if overall_gates['g2_pass'] else 'FAIL'} (total={overall_gates['classified_total']})")
    print(f"  G3 (both categories): {'PASS' if overall_gates['g3_pass'] else 'FAIL'}")
    print(f"  G4 (total >= 50): {'PASS' if overall_gates['g4_pass'] else 'FAIL'}")
    print()

    # Step 5: Popularity tier analysis
    print("[5] Popularity tier analysis (by number of releases)...")
    pop_tiers = assign_tiers(packages, popularity_key, 3)
    pop_results = {}
    tier_names_pop = ["bottom", "middle", "top"]
    for tier_idx in [0, 1, 2]:
        tier_pkgs = pop_tiers.get(tier_idx, [])
        if not tier_pkgs:
            continue
        gates = compute_gates_for_packages(tier_pkgs, classify_by_keywords, is_active)
        tier_name = tier_names_pop[tier_idx]
        min_rel = min(p["num_releases"] for p in tier_pkgs)
        max_rel = max(p["num_releases"] for p in tier_pkgs)
        pop_results[tier_name] = {
            "tier_index": tier_idx,
            "package_count": len(tier_pkgs),
            "release_range": f"{min_rel}-{max_rel}",
            "gates": gates,
        }
        print(f"  {tier_name.capitalize()} tier ({min_rel}-{max_rel} releases, n={len(tier_pkgs)}):")
        print(f"    G1: {'PASS' if gates['g1_pass'] else 'FAIL'} (ratio={gates['g1_ratio']*100:.1f}%, need_rate={gates['g1_need_rate']*100:.1f}%, random_rate={gates['g1_random_rate']*100:.1f}%)")
        print(f"    G2: {'PASS' if gates['g2_pass'] else 'FAIL'} (total={gates['classified_total']})")
        print(f"    G3: {'PASS' if gates['g3_pass'] else 'FAIL'}")
        print(f"    G4: {'PASS' if gates['g4_pass'] else 'FAIL'}")
    print()

    # Step 6: Age tier analysis
    print("[6] Age tier analysis (by first release year)...")
    age_tiers = assign_tiers(packages, age_key, 3)
    age_results = {}
    tier_names_age = ["oldest", "middle", "newest"]
    for tier_idx in [0, 1, 2]:
        tier_pkgs = age_tiers.get(tier_idx, [])
        if not tier_pkgs:
            continue
        gates = compute_gates_for_packages(tier_pkgs, classify_by_keywords, is_active)
        tier_name = tier_names_age[tier_idx]
        years = [int(p["first_release"][:4]) for p in tier_pkgs if p.get("first_release")]
        min_year = min(years) if years else 0
        max_year = max(years) if years else 0
        age_results[tier_name] = {
            "tier_index": tier_idx,
            "package_count": len(tier_pkgs),
            "year_range": f"{min_year}-{max_year}",
            "gates": gates,
        }
        print(f"  {tier_name.capitalize()} tier ({min_year}-{max_year}, n={len(tier_pkgs)}):")
        print(f"    G1: {'PASS' if gates['g1_pass'] else 'FAIL'} (ratio={gates['g1_ratio']*100:.1f}%, need_rate={gates['g1_need_rate']*100:.1f}%, random_rate={gates['g1_random_rate']*100:.1f}%)")
        print(f"    G2: {'PASS' if gates['g2_pass'] else 'FAIL'} (total={gates['classified_total']})")
        print(f"    G3: {'PASS' if gates['g3_pass'] else 'FAIL'}")
        print(f"    G4: {'PASS' if gates['g4_pass'] else 'FAIL'}")
    print()

    # Step 7: Cross-tabulation
    print("[7] Cross-tabulation (popularity x age)...")
    cross_results = {}
    for pop_i, pop_name in enumerate(tier_names_pop):
        for age_i, age_name in enumerate(tier_names_age):
            pop_pkgs = pop_tiers.get(pop_i, [])
            age_pkgs = age_tiers.get(age_i, [])
            cross_pkgs = [p for p in pop_pkgs if p in age_pkgs]
            if len(cross_pkgs) < 10:
                continue
            gates = compute_gates_for_packages(cross_pkgs, classify_by_keywords, is_active)
            cross_results[f"{pop_name}_x_{age_name}"] = {
                "package_count": len(cross_pkgs),
                "gates": gates,
            }
            print(f"  {pop_name} x {age_name} (n={len(cross_pkgs)}): G1={'PASS' if gates['g1_pass'] else 'FAIL'} (ratio={gates['g1_ratio']*100:.1f}%)")
    print()

    # Build final results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "experiment": "E165-pypi-tier-analysis",
        "platform": "PyPI",
        "sample_size": len(packages),
        "overall": {
            "classified": {
                "need-related": len(need_related),
                "random": len(random_pkgs),
            },
            "gates": overall_gates,
        },
        "popularity_tiers": pop_results,
        "age_tiers": age_results,
        "cross_tiers": cross_results,
        "conclusion": "pending",
    }

    # Determine conclusion
    overall = overall_gates
    if overall["g1_pass"] and overall["g2_pass"] and overall["g3_pass"] and overall["g4_pass"]:
        results["conclusion"] = "gates_all_pass"
    elif not overall["g1_pass"] and not overall["g2_pass"]:
        results["conclusion"] = "g1_and_g2_fail"
    elif not overall["g1_pass"]:
        results["conclusion"] = "g1_fail"
    elif not overall["g2_pass"]:
        results["conclusion"] = "g2_fail"
    else:
        results["conclusion"] = "partial"

    return results


def main():
    results = run_experiment()

    out_dir = "/home/ubuntu/think-free/EXPERIMENTS/165-pypi-tier-analysis"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")

    print(f"\n=== SUMMARY ===")
    print(f"Experiment: {results.get('experiment')}")
    print(f"Platform: {results.get('platform')}")
    print(f"Sample size: {results.get('sample_size')}")
    print(f"Overall conclusion: {results.get('conclusion')}")
    og = results['overall']['gates']
    print(f"Overall G1: {'PASS' if og['g1_pass'] else 'FAIL'} (ratio={og['g1_ratio']*100:.1f}%)")
    print(f"Overall G2: {'PASS' if og['g2_pass'] else 'FAIL'} (total={og['classified_total']})")
    for tier_name, tier_data in results.get("popularity_tiers", {}).items():
        g = tier_data["gates"]
        print(f"  Pop {tier_name}: G1={'PASS' if g['g1_pass'] else 'FAIL'} (ratio={g['g1_ratio']*100:.1f}%, n={tier_data['package_count']})")
    for tier_name, tier_data in results.get("age_tiers", {}).items():
        g = tier_data["gates"]
        print(f"  Age {tier_name}: G1={'PASS' if g['g1_pass'] else 'FAIL'} (ratio={g['g1_ratio']*100:.1f}%, n={tier_data['package_count']})")


if __name__ == "__main__":
    main()