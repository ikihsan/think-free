#!/usr/bin/env python3
"""E071 harvest: PyPI package activity measurement.

For each package in arms A (need-related) and B (random), query the
PyPI JSON API and record metadata + activity score.

Usage:
    python3 harvest.py            # harvest both arms
    python3 harvest.py --arm 1    # harvest arm A only
    python3 harvest.py --arm 2    # harvest arm B only
"""

import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Arm definitions: package names
ARM_A_PACKAGES = [
    # Need-related packages (from E062/E063 corpora context)
    "requests",
    "pillow",
    "numpy",
    "flask",
    "django",
    "bcrypt",
    "pytest",
    "gitpython",
    "sqlalchemy",
    "jinja2",
]

ARM_B_PACKAGES = [
    # Random packages not related to typical need statements
    "black",
    "mypy",
    "pytest-xdist",
    "sphinx",
    "wheel",
    "setuptools",
    "twine",
    "virtualenv",
    "tox",
    "cookiecutter",
]

# Output paths
ARM_A_RESULTS = os.path.join(HERE, "raw", "arm-a-results.jsonl")
ARM_B_RESULTS = os.path.join(HERE, "raw", "arm-b-results.jsonl")


def compute_activity_score(info):
    """Compute activity score from PyPI JSON API metadata."""
    if "error" in info:
        return -1  # missing

    score = 0
    # Release count
    rc = info.get("release_count", 0)
    if rc > 0:
        score += min(rc // 10, 10)
    # Project URLs
    pu = info.get("project_urls", {})
    if info.get("has_homepage"):
        score += 5
    if info.get("has_documentation"):
        score += 3
    if info.get("has_source"):
        score += 2
    # Classifiers
    classifiers = info.get("classifiers", [])
    if any("Development Status :: 5" in c for c in classifiers):
        score += 5
    if any("Development Status :: 4" in c for c in classifiers):
        score += 3

    return score


def harvest_arm(arm_id, packages, output_path):
    """Run one arm of the harvest."""
    print(f"=== E071 Arm {arm_id} harvest ===")
    results = []

    packages_to_use = packages[:]  # copy

    for i, name in enumerate(packages_to_use):
        # Query PyPI JSON API
        url = f"https://pypi.org/pypi/{name}/json"
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            data = {"error": str(e), "name": name}

        score = compute_activity_score(data)
        results.append({
            "statement_id": i,
            "package_name": name,
            "api_result": data,
            "activity_score": score,
        })

        if (i + 1) % 5 == 0:
            print(f"  harvested {i + 1}/{len(packages_to_use)}...")

        # Polite delay
        time.sleep(0.5)

    # Write results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(results)} results to {output_path}")
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="E071 harvest arm")
    parser.add_argument("--arm", type=int, choices=[1, 2], default=1,
                        help="Arm to harvest (1=need-related, 2=random)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max number of packages to harvest")
    args = parser.parse_args()

    if args.arm == 1:
        packages = ARM_A_PACKAGES
        output = ARM_A_RESULTS
    else:
        packages = ARM_B_PACKAGES
        output = ARM_B_RESULTS

    if args.limit is not None:
        packages = packages[:args.limit]

    results = harvest_arm(args.arm, packages, output)
    return 0


if __name__ == "__main__":
    sys.exit(main())