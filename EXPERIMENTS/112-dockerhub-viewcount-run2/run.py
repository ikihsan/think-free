#!/usr/bin/env python3
"""
Docker Hub View-Count Principle Test
Tests whether need-related images have higher pull activity than random images.
"""

import argparse
import json
import random
import sys
import time

from dockerhub_lib import (
    Image,
    run_gates,
    sample_need_related,
    sample_random,
)


def main():
    parser = argparse.ArgumentParser(description="Docker Hub View-Count Principle Test")
    parser.add_argument("--gate", action="store_true", help="Run gates and exit with code")
    parser.add_argument("--need", type=int, default=60, help="Target need-related sample size")
    parser.add_argument("--random", type=int, default=60, help="Target random sample size")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    print("Fetching need-related images...", file=sys.stderr)
    need_imgs = sample_need_related(args.need)
    print(f"  Got {len(need_imgs)} need-related images", file=sys.stderr)
    
    print("Fetching random images...", file=sys.stderr)
    random_imgs = sample_random(args.random)
    print(f"  Got {len(random_imgs)} random images", file=sys.stderr)
    
    gates = run_gates(need_imgs, random_imgs)
    
    # Prepare results
    results = {
        "experiment": "112-dockerhub-viewcount-run2",
        "protocol": "PROTOCOL.md",
        "seed": args.seed,
        "need_images": [img.__dict__ for img in need_imgs],
        "random_images": [img.__dict__ for img in random_imgs],
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