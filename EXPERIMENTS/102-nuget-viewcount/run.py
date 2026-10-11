#!/usr/bin/env python3
"""
NuGet View-Count Principle Test
Tests whether need-related packages have higher download activity than random packages.
"""

import argparse
import json
import random
import sys
import time
import urllib.parse
import urllib.request
from typing import List

from nuget_lib import (
    Package,
    classify_package,
    extract_package,
    fetch_nuget,
    run_gates,
    sample_need_related,
    sample_random,
)


def main():
    parser = argparse.ArgumentParser(description="NuGet View-Count Principle Test")
    parser.add_argument("--gate", action="store_true", help="Run gates and exit with code")
    parser.add_argument("--need", type=int, default=50, help="Target need-related sample size")
    parser.add_argument("--random", type=int, default=50, help="Target random sample size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    random.seed(args.seed)

    print("Fetching need-related packages...", file=sys.stderr)
    need_pkgs = sample_need_related(args.need)
    print(f"  Got {len(need_pkgs)} need-related packages", file=sys.stderr)

    print("Fetching random packages...", file=sys.stderr)
    random_pkgs = sample_random(args.random)
    print(f"  Got {len(random_pkgs)} random packages", file=sys.stderr)

    gates = run_gates(need_pkgs, random_pkgs)

    # Prepare results
    results = {
        "experiment": "102-nuget-viewcount",
        "protocol": "PROTOCOL.md",
        "seed": args.seed,
        "need_packages": [pkg.__dict__ for pkg in need_pkgs],
        "random_packages": [pkg.__dict__ for pkg in random_pkgs],
        "gates": gates,
        "overall_pass": all(g.get("pass", False) for g in gates.values())
    }

    # Write results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n=== GATE RESULTS ===")
    for gname, gdata in gates.items():
        status = "PASS" if gdata.get("pass", False) else "FAIL"
        print(f"  {gname}: {status} — {gdata.get('details', '')}")

    overall = "PASS" if results["overall_pass"] else "FAIL"
    print(f"\nOVERALL: {overall}")

    if args.gate:
        sys.exit(0 if results["overall_pass"] else 1)


if __name__ == "__main__":
    main()