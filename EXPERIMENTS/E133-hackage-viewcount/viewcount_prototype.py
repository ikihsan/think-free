#!/usr/bin/env python3
"""
E133 — view-count prototype on Hackage: Haskell packages.

Tests the view-count principle using Hackage metadata:
  For each Haskell package, compute an activity score from download counts
  and classify the package as 'need-related' or 'random' based on Hackage tags,
  then measure whether need-related packages receive more independent arrivals
  (downloads) than random ones.

This is an evidence-gathering prototype, not product validation. It tests whether
the view-count principle (shown conclusive in E071 on PyPI, E072 on NPM) can
generalize to the Haskell package ecosystem on Hackage.

Rubric:
  - active: download_count_total >= 100  (sufficient independent arrivals)
  - inactive: 0 < download_count_total < 100
  - missing: download_count_total <= 0

Need-related tag categories (packages solving practical problems):
  web, network, json, text, data, concurrency, STM, gui, parser,
  QuickCheck, test, Cabal, build, install, monad, arrow, STM,
  graphics, graphics-ui, database, SQL, regex, network, protocol,

Random/generic tag categories:
  library, bsd3, mit, gpl, haskell, deprecated, old, haskell98,
  has2010, has2021, .
"""

import json
import sys
import os
import re
import urllib.request
import urllib.parse
import time
import argparse

HACKAGE_BASE = "https://hackage.haskell.org"


# Need-related tag categories: packages that solve practical problems
NEED_TAG_CATEGORIES = {
    "web", "network", "json", "text", "data", "concurrency", "STM",
    "gui", "parser", "QuickCheck", "test", "Cabal", "build", "install",
    "monad", "arrow", "graphics", "graphics-ui", "database", "SQL",
    "regex", "protocol", "web-framework", "web-server", "cloud",
    "system", "file", "io", "utf8", "byte-string", "text",
    "network-uri", "curl", "http", "http-client", "tls", "crypto",
    "image", "graphics", "svg", "png", "jpeg", "fractal",
    "music", "sound", "audio", "wave", " midi", "osc",
    "web", "cs", "cpp", "java", "python", "ruby", "php",
}


# Tags that are generic/infrastructure and treated as "random"
RANDOM_TAG_CATEGORIES = {
    "library", "bsd3", "mit", "gpl", "haskell", "deprecated",
    "haskell98", "has2010", "has2021", "unknown", "experimental",
    "proposed", "refactoring", "utility", "helper", "tools",
    "testing", "template", "meta", "extension", "plugin",
}


def classify_by_tags(tags):
    """Classify package as 'need-related' or 'random' based on Hackage tags."""
    if not tags:
        return 'unclassified'
    
    tag_set = {t.lower().strip() for t in tags}
    
    # Check for need-related tags first
    for tag in tag_set:
        if tag in NEED_TAG_CATEGORIES:
            return 'need-related'
    
    # Check for random/generic tags
    for tag in tag_set:
        if tag in RANDOM_TAG_CATEGORIES:
            return 'random'
    
    # Default: unclassified (neither category matched)
    return 'unclassified'


def fetch_hackage_packages(num_packages=50, tag="library"):
    """Fetch a sample of Haskell packages from Hackage by tag."""
    packages = []
    seen = set()
    
    # Fetch from tag page
    tag_url = f"{HACKAGE_BASE}/packages/tag/{tag}"
    try:
        with urllib.request.urlopen(tag_url, timeout=30) as resp:
            data = resp.read().decode('utf-8')
            # Extract package names from links
            names = re.findall(r'href="/package/([^"/\?&]+)"', data)
            names = [n for n in names if n not in seen and not seen.add(n)]
            
            # Fetch each package's metadata
            for name in names[:num_packages]:
                pkg_url = f"{HACKAGE_BASE}/package/{name}"
                try:
                    with urllib.request.urlopen(pkg_url, timeout=15) as pkg_resp:
                        pkg_data = pkg_resp.read().decode('utf-8')
                        
                        # Extract download count
                        dl_match = re.search(r'Downloads</th>[^<]*<td>(\d[\d ,]*) total', pkg_data)
                        total_downloads = 0
                        if dl_match:
                            total_downloads = int(dl_match.group(1).replace(',', ''))
                        
                        # Extract tags from the package page
                        tags_match = re.findall(r'tag/([^"]+)"', pkg_data)
                        tags = tags_match if tags_match else []
                        
                        # Extract synopsis (fallback)
                        synopsis_match = re.search(
                            r'<h1>[^<]*<a[^>]*>[^<]*</a>:[^<]*<small>([^<]+)</small>', pkg_data
                        )
                        synopsis = synopsis_match.group(1) if synopsis_match else ""
                        
                        packages.append({
                            "name": name,
                            "total_downloads": total_downloads,
                            "tags": tags,
                            "synopsis": synopsis,
                        })
                        
                        # Be polite to the server
                        time.sleep(0.3)
                except Exception as e:
                    print(f"Warning: Failed to fetch {name}: {e}", file=sys.stderr)
                    continue
    except Exception as e:
        print(f"Error fetching tag page: {e}", file=sys.stderr)
    
    return packages


def compute_activity_score(total_downloads):
    """Compute activity score from total download count."""
    if total_downloads <= 0:
        return 0  # missing
    elif total_downloads < 100:
        return 1  # inactive
    else:
        return 2  # active


def classify_activity(score):
    """Classify activity score into category."""
    if score >= 2:
        return "active"
    elif score > 0:
        return "inactive"
    else:
        return "missing"


def main():
    parser = argparse.ArgumentParser(description="E133 View-count Prototype on Hackage")
    parser.add_argument("--num-packages", type=int, default=50,
                        help="Number of packages to sample (default: 50)")
    parser.add_argument("--tag", type=str, default="library",
                        help="Hackage tag to sample from (default: library)")
    args = parser.parse_args()
    
    num_packages = args.num_packages
    tag = args.tag
    
    print(f"E133 View-count Prototype on Hackage")
    print(f"=" * 60)
    print(f"Sampling {num_packages} packages from Hackage tag: {tag}")
    print()
    
    # Fetch packages
    packages = fetch_hackage_packages(num_packages=num_packages, tag=tag)
    print(f"Fetched {len(packages)} packages")
    print()
    
    # Classify each package by tags
    results = []
    for pkg in packages:
        classification = classify_by_tags(pkg["tags"])
        activity_score = compute_activity_score(pkg["total_downloads"])
        activity_class = classify_activity(activity_score)
        
        results.append({
            "name": pkg["name"],
            "total_downloads": pkg["total_downloads"],
            "classified": classification,
            "activity_class": activity_class,
            "tags": pkg["tags"][:5] if pkg["tags"] else [],  # first 5 for display
        })
        
        if len(results) % 10 == 0:
            print(f"  classified {len(results)}/{num_packages}...")
    
    # Summary statistics
    total = len(results)
    classified = sum(1 for r in results if r["classified"] != 'unclassified')
    need_related = sum(1 for r in results if r["classified"] == 'need-related')
    random_count = sum(1 for r in results if r["classified"] == 'random')
    unclassified = total - classified
    
    coverage = classified / total if total > 0 else 0
    need_frac = need_related / classified if classified > 0 else 0
    
    # Activity breakdown
    active = sum(1 for r in results if r["activity_class"] == "active")
    inactive = sum(1 for r in results if r["activity_class"] == "inactive")
    missing = sum(1 for r in results if r["activity_class"] == "missing")
    
    # Need-related vs Random activity stats
    need_active = sum(1 for r in results if r["classified"] == 'need-related' and r["activity_class"] == "active")
    need_inactive = sum(1 for r in results if r["classified"] == 'need-related' and r["activity_class"] == "inactive")
    need_missing = sum(1 for r in results if r["classified"] == 'need-related' and r["activity_class"] == "missing")
    
    random_active = sum(1 for r in results if r["classified"] == 'random' and r["activity_class"] == "active")
    random_inactive = sum(1 for r in results if r["classified"] == 'random' and r["activity_class"] == "inactive")
    random_missing = sum(1 for r in results if r["classified"] == 'random' and r["activity_class"] == "missing")
    
    # Gate computations
    # G1: >=95% have arrival metric > 0 (activity_class != missing)
    items_with_arrival = sum(1 for r in results if r["activity_class"] != "missing")
    vc_rate = items_with_arrival / total if total > 0 else 0
    g1_pass = vc_rate >= 0.95
    
    # G2: coverage >= 60% floor AND need fraction >= 5%
    cov_met = coverage >= 0.60
    need_frac_met = need_frac >= 0.05
    g2_pass = cov_met and need_frac_met
    
    # G4: classified_total >= 30
    g4_pass = classified >= 30
    
    conclusions = []
    if not g1_pass:
        conclusions.append(f"G1 FAIL: vc_rate={vc_rate*100:.1f}% < 95%")
    if not cov_met:
        conclusions.append(f"G2 FAIL: coverage={coverage*100:.1f}% < 60% floor")
    elif not need_frac_met:
        conclusions.append(f"G2 FAIL: need fraction={need_frac*100:.1f}% < 5%")
    if not g4_pass:
        conclusions.append(f"G4 FAIL: classified_total={classified} < 30")
    if g1_pass and cov_met and need_frac_met and g4_pass:
        conclusions.append("G3: would need full unserved fraction CI computation")
    else:
        conclusions.append("G3: skipped (prerequisites not met)")
    
    print()
    print("Summary:")
    print(f"  Total packages: {total}")
    print(f"  Classified: {classified} ({coverage*100:.1f}% coverage)")
    print(f"  Need-related: {need_related} ({need_frac*100:.1f}% of classified)")
    print(f"  Random: {random_count}")
    print(f"  Unclassified: {unclassified}")
    print()
    print("Activity breakdown:")
    print(f"  Active (downloads >= 100): {active} ({active/total*100:.1f}%)")
    print(f"  Inactive (0 < downloads < 100): {inactive} ({inactive/total*100:.1f}%)")
    print(f"  Missing (0 downloads): {missing} ({missing/total*100:.1f}%)")
    print()
    print("Need-related vs Random activity:")
    print(f"  Need-related active: {need_active}")
    print(f"  Need-related inactive: {need_inactive}")
    print(f"  Need-related missing: {need_missing}")
    print(f"  Random active: {random_active}")
    print(f"  Random inactive: {random_inactive}")
    print(f"  Random missing: {random_missing}")
    print()
    print(f"G1 (vc_rate >= 95%): {'PASS' if g1_pass else 'FAIL'} (vc_rate={vc_rate*100:.1f}%)")
    print(f"G2 (cov >= 60% floor AND need_frac >= 5%): {'PASS' if g2_pass else 'FAIL'} (cov={coverage*100:.1f}%, need_frac={need_frac*100:.1f}%)")
    print(f"G4 (classified >= 30): {'PASS' if g4_pass else 'FAIL'} (classified={classified})")
    print(f"\nConclusions: {'; '.join(conclusions)}")
    print()
    
    # Save results
    output_path = f"hackage-viewcount-{tag}-{num_packages}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Results written to: {output_path}")


if __name__ == "__main__":
    main()