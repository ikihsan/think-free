"""E103+ — View-count principle CLI prototype.

Search a package registry for need-related packages using the view-count
principle: need-related packages have systematically higher activity metadata
(description + version) than random packages.

Usage:
    python3 tools/viewcount_cli.py <keyword> [--top N] [--registry pypi]

    python3 tools/viewcount_cli.py --list-keywords
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse

from viewcount_core import (  # noqa: E402
    FALLBACK_PACKAGES,
    GENERIC_TERMS,
    NEED_INDICATORS,
    classify_package,
    fetch_fallback_packages,
    is_active,
    search_pypi,
)


# ---------------------------------------------------------------------------
# Prototype entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="View-count principle prototype: find need-related packages"
    )
    parser.add_argument("keyword", nargs="?", help="Search keyword or need description")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to display (default: 10)",
    )
    parser.add_argument(
        "--registry",
        choices=["pypi"],
        default="pypi",
        help="Package registry to search (default: pypi)",
    )
    parser.add_argument(
        "--list-keywords",
        action="store_true",
        help="List example search keywords from past experiments",
    )
    args = parser.parse_args()

    if args.list_keywords:
        print("Example keywords from prior experiments:")
        for kw in [
            "database", "cache", "auth", "security", "logging",
            "monitoring", "testing", "benchmark", "performance", "api",
        ]:
            print(f"  - {kw}")
        return

    if not args.keyword:
        parser.print_usage()
        print(
            "\nEnter a keyword/need description to search for relevant packages.\n"
            "The tool classifies packages as 'need-related' (have a need indicator "
            "in their description) or 'random' and reports active/metadata status."
        )
        return

    keyword = args.keyword
    print(f"=== View-count prototype: searching '{keyword}' ===\n")

    if args.registry == "pypi":
        packages = search_pypi(keyword, max_results=200)
    else:
        print(f"Registry '{args.registry}' not supported yet.")
        return

    if not packages:
        print("No packages found. Try a different keyword?")
        return

    # Classify and evaluate
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_pkgs = []

    for pkg in packages:
        cls = classify_package(pkg.get("description", ""))
        active_flag = is_active(pkg)
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        if cls == "need-related":
            need_related_pkgs.append(pkg)

    # Print classification summary
    print("=== Classification ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")

    # G1 gate: need-related active rate >= 55% of random active rate
    g1_pass = False
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"\n=== Gate G1 ===")
        print(f"  need-related active rate: {need_rate*100:.1f}%")
        print(f"  random active rate: {random_rate*100:.1f}%")
        print(f"  ratio (need/random): {ratio*100:.1f}%")
        print(f"  G1 pass (>= 55%): {'PASS' if g1_pass else 'FAIL'}")
    else:
        print(f"\n=== Gate G1 ===")
        print(f"  SKIPPED: need at least one package in each category (need-related={classified['need-related']}, random={classified['random']})")

    # G2 gate: minimum classified sample size >= 100
    g2_pass = classified["need-related"] + classified["random"] >= 100
    print(f"\n=== Gate G2 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G2 pass (>= 100): {'PASS' if g2_pass else 'FAIL'}")

    # G3 gate: both categories represented
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"\n=== Gate G3 ===")
    print(f"  G3 pass (both categories): {'PASS' if g3_pass else 'FAIL'}")

    # G4 gate: minimum 50 classified
    g4_pass = (classified["need-related"] + classified["random"]) >= 50
    print(f"\n=== Gate G4 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G4 pass (>= 50): {'PASS' if g4_pass else 'FAIL'}")

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n=== Overall ===")
    print(f"  All gates pass: {'YES' if all_pass else 'NO'}")

    # Display need-related packages ranked by version presence/activity
    print(f"\n=== Need-related packages (top {min(args.top, len(need_related_pkgs))}) ===")
    # Sort: packages with version/active first, then alphabetically
    need_related_pkgs.sort(
        key=lambda p: (
            0 if is_active(p) else 1,
            p.get("name", "").lower(),
        )
    )
    for i, pkg in enumerate(need_related_pkgs[: args.top]):
        name = pkg.get("name", "N/A")
        version = pkg.get("version", "N/A")
        desc = pkg.get("description", "")[:80] if pkg.get("description") else ""
        active_str = "ACTIVE" if is_active(pkg) else "inactive"
        print(
            f"  {i+1}. {name} {version}"
            f" -- {desc}..."
            f" [{active_str}]"
        )

    # Save results JSON for the session record
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": os.uname().machine if hasattr(os, "uname") else "unknown",
        "sample_size": len(packages),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0
            else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": (
            (active["need-related"] / classified["need-related"])
            / (active["random"] / classified["random"] >= 0.55)
            if classified["need-related"] > 0 and classified["random"] > 0
            else False
        ),
        "g2_pass": classified["need-related"] + classified["random"] >= 100,
        "g3_pass": classified["need-related"] > 0 and classified["random"] > 0,
        "g4_pass": (classified["need-related"] + classified["random"]) >= 50,
        "conclusion": "pending",
        "experiment_description": f"View-count prototype search for keyword: {keyword}",
    }

    out_dir = "EXPERIMENTS/e103-viewcount-prototype"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")


if __name__ == "__main__":
    main()