#!/usr/bin/env python3
"""E072 harvest: NPM package activity measurement.

For each package in arms A (need-related) and B (random), query the
NPM JSON API and record metadata + activity score.

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
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Arm definitions: package names
# Need-related packages: commonly used NPM packages that might appear in need statements
ARM_A_PACKAGES = [
    "react",
    "lodash",
    "express",
    "angular",
    "vue",
    "webpack",
    "babel",
    "moment",
    "jquery",
    "node-fetch",
]

# Random packages not related to typical need statements
ARM_B_PACKAGES = [
    "nodemon",
    "pm2",
    "sequelize",
    "mongoose",
    "dotenv",
    "passport",
    "jsonwebtoken",
    "bcryptjs",
    "swagger-ui",
    "lodash-cli",
]

# Output paths
ARM_A_RESULTS = os.path.join(HERE, "raw", "arm-a-results.jsonl")
ARM_B_RESULTS = os.path.join(HERE, "raw", "arm-b-results.jsonl")


def compute_activity_score(info):
    """Compute activity score from NPM JSON API metadata.

    adapts the rubric to the current NPM JSON API key layout:
    - The NPM API response has fields at the top level, not nested under "info"
    - homepage from data.homepage
    - repository from data.repository.url
    - keywords from data.keywords
    - no version field at top level; use dist-tags.latest existence as proxy
    - no classifiers available unlike PyPI
    """
    if "error" in info:
        return -1  # missing

    score = 0
    # 1. Package existence / version presence (1 point)
    # NPM API always returns data for existing packages;
    # check dist-tags for latest tag presence
    dist_tags = info.get("dist-tags")
    if dist_tags and isinstance(dist_tags, dict) and "latest" in dist_tags:
        score += 1
    # 2. Has Homepage URL (5 points)
    if info.get("homepage"):
        score += 5
    # 3. Has Repository URL (2 points)
    repo = info.get("repository")
    if repo and isinstance(repo, dict) and repo.get("url"):
        score += 2
    # 4. Has Keywords (1 point)
    keywords = info.get("keywords")
    if keywords and isinstance(keywords, list) and len(keywords) > 0:
        score += 1

    return score


def harvest_arm(arm_id, packages, output_path):
    """Run one arm of the harvest."""
    print(f"=== E072 Arm {arm_id} harvest ===")
    results = []

    packages_to_use = packages[:]  # copy

    for i, name in enumerate(packages_to_use):
        # Query NPM JSON API
        # The NPM JSON API v1 returns: https://registry.npmjs.org/{name}
        url = f"https://registry.npmjs.org/{name}"
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            data = {"error": str(e), "name": name}

        # The NPM API response is flat; fields are at the top level
        # PyPI uses data["info"], NPM uses data directly
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

    parser = argparse.ArgumentParser(description="E072 harvest arm")
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