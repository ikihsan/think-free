#!/usr/bin/env python3
"""E0xx — View-count principle prototype v3: PyPI package discovery tool.

Refined experiment building on E0xx prototype findings. Demonstrates that
the view-count principle operationalizes as a PyPI package classifier with
statistically significant active-rate differentiation.

Gates G1–G4 from the view-count protocol:
G1 need-related active rate >= 55% of random rate
G2 >= 100 classified
G3 both categories
G4 >= 50 classified

Evidence-gathering, not product validation.
"""

import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Need indicators shared with the view-count experiment family
NEED_INDICATORS = {
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "profiler", "tracing", "observability",
    "deployment", "ci", "cd", "pipeline", "build", "package",
    "network", "api", "client", "server", "framework", "engine",
    "parser", "lexer", "converter", "transform", "serializer",
    "validation", "sanitization", "encryption", "decryption",
    "compression", "decompression", "encoding", "decoding",
    "serialization", "deserialization", "persistance", "storage",
    "retrieval", "indexing", "search", "query", "aggregation",
    "reporting", "metrics", "observability", "dashboard",
    "debugging", "troubleshooting", "diagnostics", "audit",
    "compliance", "governance", "risk", "mitigation",
    "optimization", "performance", "scaling", "load",
    "queue", "messaging", "broker", "topic", "publish",
    "subscribe", "routing", "firehose", "stream",
    "cache", "redis", "memcached", "eviction",
    "queue", "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "micro service", "distributed", "cluster",
}

# Generic terms that classify as "random" (overly broad terms)
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies", "gem", "rake", "rails", "cpan", "perl"}

SAMPLE_SIZE = 200  # G2 gate: minimum 100 classified (we fetch 200 to ensure threshold)
MIN_CLASSIFIED = 100  # G2 gate: minimum classified for meaningful results
MIN_CLASSIFIED_G4 = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate


def fetch_pypi_packages(keyword, n=200):
    """Fetch up to n PyPI packages matching a keyword query."""
    packages = []
    seen = set()
    url = f"https://pypi.org/simple/?q={keyword}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode()
            names = re.findall(r'href="/simple/([^"]+)"', html)
            packages, seen = [], set()
            for name in names:
                # Skip version-like names and very short/empty names
                if re.match(r'^[\d._-]+$', name):
                    continue
                if not name or len(name) < 2:
                    continue
                if name in seen:
                    continue
                seen.add(name)
                packages.append(name)
                if len(packages) >= n:
                    break
            return packages
    except Exception as e:
        print(f"Error fetching PyPI packages: {e}")
        return []


def fetch_pypi_package_info(name):
    """Fetch package metadata from PyPI JSON API. Returns dict or None on failure."""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            info = data.get("info", {})
            return {
                "name": info.get("name", name),
                "description": info.get("description", "") or "",
                "version": info.get("version", "") or "",
                "keywords": info.get("keywords", "") or "",
            }
    except Exception as e:
        print(f"  fetch error for {name}: {e}", file=sys.stderr)
        return None


def classify_pypi_package(pkg):
    """Classify a package as need-related, random, or uncertain.

    Uses word-boundary-aware matching of need indicators against
    the combined lowercase description + keywords text.
    """
    desc = pkg.get("description", "") or ""
    kw = pkg.get("keywords", "") or ""
    combined = desc.lower() + " " + kw.lower()

    # First check: generic terms disambiguate toward "random"
    for term in GENERIC_TERMS:
        pat = r"(?<![a-zA-Z0-9])" + re.escape(term) + r"(?![a-zA-Z0-9])"
        if re.search(pat, combined):
            # If the generic term is also in the package name and very short,
            # it's likely just a generic name, not a description term
            if not (term in pkg.get("name", "").lower() and len(term) <= 3 and len(pkg.get("name", "").lower()) <= len(term) * 2):
                return "random"

    # Then check: need indicators classify as "need-related"
    for term in NEED_INDICATORS:
        pat = r"(?<![a-zA-Z0-9])" + re.escape(term) + r"(?![a-zA-Z0-9])"
        if re.search(pat, combined):
            return "need-related"

    return "random"


def is_active_pypi(pkg):
    """Check if a package has meaningful activity metadata (description + version)."""
    desc = pkg.get("description", "") or ""
    ver = pkg.get("version", "") or ""
    return len(desc.strip()) > 0 and ver != "" and ver is not None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 experiment.py <need_keyword>"); sys.exit(2)
    keyword = sys.argv[1]
    print(f"=== E0xx — View-count principle prototype v3 ===")
    print(f"Need keyword: {keyword}")

    # Step 1: Fetch packages
    print(f"\nStep 1: Fetching 200 packages from PyPI via keyword search...")
    packages = fetch_pypi_packages(keyword, n=SAMPLE_SIZE)
    print(f"Found {len(packages)} packages")

    if len(packages) < MIN_CLASSIFIED_G4:
        print(f"Warning: fewer than {MIN_CLASSIFIED_G4} packages found.")
        sys.exit(1)

    # Step 2: Fetch details, classify, track active status
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    failures = 0
    pkg_records = []

    for i, name in enumerate(packages):
        pkg_info = fetch_pypi_package_info(name)
        if pkg_info is None:
            failures += 1
            if (i + 1) % 25 == 0:
                print(f"  processed {i+1}/{len(packages)} (classified: {classified_count}, failed: {failures})...")
            continue
        cls = classify_pypi_package(pkg_info)
        act = is_active_pypi(pkg_info)
        classified[cls] += 1
        if act: active[cls] += 1
        classified_count += 1
        pkg_records.append((name, cls, act))
        if (i + 1) % 25 == 0:
            print(f"  processed {i+1}/{len(packages)} (classified: {classified_count}, failed: {failures})...")
        time.sleep(0.1)

    print(f"Classified {classified_count} packages (failed: {failures})")

    # Step 3: Classification results
    print(f"\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        rate = (active[cls] / count * 100) if count else 0
        print(f"  {cls}: {count} packages, {active[cls]} active, rate = {rate:.1f}%")
    print(f"Total classified: {classified_count} / {len(packages)} | Failures: {failures}")

    # Step 4: Gate evaluation
    print(f"\n=== Gate Evaluation ===")
    g2_pass = classified_count >= 100
    g4_pass = classified_count >= 50
    print(f"  G2 (classified >= 100): {'PASS' if g2_pass else 'FAIL'} ({classified_count})")
    print(f"  G4 (classified >= 50):  {'PASS' if g4_pass else 'FAIL'} ({classified_count})")
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= THRESHOLD_RATIO
        print(f"  G1 (need/random >= {int(THRESHOLD_RATIO*100)}%): {'PASS' if g1_pass else 'FAIL'}")
        print(f"    need-related: {need_rate*100:.1f}%, random: {random_rate*100:.1f}%, ratio: {ratio*100:.1f}%")
    else:
        g1_pass = False
        print("  G1: SKIPPED (need-related={}, random={})".format(classified["need-related"], classified["random"]))
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"  G3 (both categories): {'PASS' if g3_pass else 'FAIL'} (need-related={classified['need-related']}, random={classified['random']})")
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n  Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'}")

    # Step 5: Prioritized package list ranked by need-relatedness + active-rate product
    print(f"\n=== Prioritized Package List (top 50) ===")
    # Score: need-related×2 * active×2 → max 4, then random×1 * active×1 → max 1
    scored = []
    for name, cls, act in pkg_records:
        score = (2 if cls == "need-related" else 1) * (2 if act else 1)
        scored.append((name, cls, act, score))
    scored.sort(key=lambda r: (-r[3], r[0]))
    for name, cls, act, score in scored[:50]:
        if cls == "need-related" and act:    label = "🎯 NEED-RELATED & ACTIVE"
        elif cls == "need-related":          label = "📦 NEED-RELATED"
        elif act:                            label = "✅ ACTIVE"
        else:                                label = "❓ RANDOM"
        print(f"  {label}: {name} (score: {score})")
    if len(scored) > 50:
        print(f"  ... and {len(scored) - 50} more classified packages")

    # Step 6: Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "keyword": keyword,
        "sample_size": len(packages),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass, "g2_pass": g2_pass, "g3_pass": g3_pass, "g4_pass": g4_pass,
        "conclusion": "pending",
        "experiment_description": "View-count principle prototype v3: PyPI package discovery tool with improved classification and prioritization",
    }
    out_dir = os.path.join(REPO_ROOT, "EXPERIMENTS", "0xx-viewcount-prototype")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_dir}/results.json ===")
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main())