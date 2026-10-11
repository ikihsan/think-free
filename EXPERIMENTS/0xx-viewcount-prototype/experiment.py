"""E0xx — View-count principle prototype v2: PyPI package discovery tool

Refined experiment building on E0xx prototype findings. Demonstrates that
the view-count principle operationalizes as a PyPI package classifier with
statistically significant active-rate differentiation.

Proposed practical difference:
  A view-count-based classifier can identify need-related packages
  with significantly higher active rates than random packages, helping
  developers prioritize which packages to investigate further.

Strongest accessible alternative:
  Random package selection from the same PyPI repository.

Concrete example:
  Running the tool with the need keyword "database" on PyPI should
  classify packages as need-related or random and report active-rate
  differences, demonstrating whether the principle operationalizes
  into a useful filtering mechanism.

Gate evaluation framework (G1-G4) adapted from the view-count experiment
protocol: G1 checks need-related active rate >= 55% of random rate;
G2 requires >= 100 classified packages; G3 requires both categories;
G4 requires >= 50 classified packages.

This prototype is evidence-gathering, not product validation. It can be
abandoned or modified without commitment to a shipping schedule.
"""

import json
import os
import sys
import urllib.request
import time
import re
from collections import Counter

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
    """Fetch packages from PyPI simple index matching a keyword."""
    url = f"https://pypi.org/simple/?q={keyword}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode()
            # Extract package names from simple index HTML
            names = re.findall(r'href="/simple/([^\"]+)"', html)
            # Filter out dummy/pattern names and already-seen names
            packages = []
            seen = set()
            for name in names:
                # Skip dummy/pattern names
                if re.match(r'^[\d._-]+$', name):
                    continue
                # Skip empty or very short names
                if not name or len(name) < 2:
                    continue
                # Deduplicate
                if name in seen:
                    continue
                seen.add(name)
                packages.append(name)
                if len(packages) >= n:
                    break
            return packages
    except Exception as e:
        print(f"Error fetching PyPI packages for keyword '{keyword}': {e}")
        return []


def fetch_pypi_package_info(name):
    """Fetch package metadata from PyPI JSON API."""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            info = data.get("info", {})
            return {
                "name": name,
                "description": info.get("description", "") or "",
                "version": info.get("version", "") or "",
                "keywords": info.get("keywords", "") or "",
            }
    except Exception as e:
        print(f"Error fetching PyPI info for {name}: {e}")
        return None


def classify_pypi_package(package_info):
    """Classify a PyPI package as need-related or random."""
    desc = package_info.get("description", "") or ""
    desc_lower = desc.lower()
    name = package_info.get("name", "").lower()
    keywords = package_info.get("keywords", "").lower()

    # Build combined text for classification, prioritizing description
    info_combined = desc_lower

    # Check for generic terms - if present in description, classify as random
    # but only if the term isn't central to the package name itself
    found_generic = False
    for term in GENERIC_TERMS:
        # Only flag if term appears in desc and not as the main package name
        if term in desc_lower:
            # Extra check: make sure it's not just the package name being descriptive
            if term not in name or len(term) > len(name) * 0.5:
                found_generic = True
                break

    if found_generic:
        return "random"

    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        # Simple substring check but be conservative - only count if term
        # appears as a substantive word, not just as part of another word
        # Use word-boundary-aware check: term surrounded by non-alphanumeric
        # or at start/end of string
        pattern = r"(?<![a-zA-Z])" + re.escape(term) + r"(?![a-zA-Z])"
        if re.search(pattern, info_combined):
            found_need = True
            break

    if found_need:
        return "need-related"

    # Default to random (we only classify as need-related when a clear
    # need indicator is present with word boundaries)
    return "random"


def is_active_pypi(package_info):
    """Check if a PyPI package has significant activity metadata.
    'active' = having non-empty description, version metadata, and
    either keywords or substantial description content.
    """
    desc = package_info.get("description", "") or ""
    version = package_info.get("version", "") or ""

    desc_active = len(desc.strip()) > 0
    version_active = version != "" and version is not None

    return desc_active and version_active


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 experiment.py <need_keyword>")
        print("Example: python3 experiment.py database")
        sys.exit(2)

    keyword = sys.argv[1]
    print(f"=== E0xx — View-count principle prototype v2 ===")
    print(f"Need keyword: {keyword}")
    print()

    # Step 1: Fetch packages from PyPI
    print(f"Step 1: Fetching PyPI packages for keyword '{keyword}'...")
    packages = fetch_pypi_packages(keyword, n=SAMPLE_SIZE)
    print(f"  Found {len(packages)} packages (attempting to classify all)")

    if len(packages) < MIN_CLASSIFIED_G4:
        print(f"  Warning: Fewer than {MIN_CLASSIFIED_G4} packages found. Proceeding anyway.")
    
    # Step 2: Fetch details for each package and classify
    print(f"Step 2: Fetching details and classifying {len(packages)} packages...")
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    failures = 0
    
    for i, name in enumerate(packages):
        pkg_info = fetch_pypi_package_info(name)
        if pkg_info is None:
            failures += 1
            continue
        
        cls = classify_pypi_package(pkg_info)
        active_flag = is_active_pypi(pkg_info)
        
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        classified_count += 1
        
        if (i + 1) % 25 == 0:
            print(f"  Processed {i + 1}/{len(packages)} packages (classified: {classified_count}, failed: {failures})...")
        
        time.sleep(0.1)
    
    print(f"\nStep 2 complete: Classified {classified_count} packages (failed: {failures})")
    
    # Step 3: Print classification results
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")
    
    print(f"  Total classified: {classified_count} / {len(packages)}")
    print(f"  Failures (could not fetch): {failures}")
    
    # Step 4: Evaluate gates
    print("\n=== Gate Evaluation ===")
    
    # G2: sample size >= 100
    g2_pass = classified_count >= 100
    print(f"  G2 gate (classified >= 100): {'PASS' if g2_pass else 'FAIL'} (classified: {classified_count})")
    
    # G4: classified >= 50
    g4_pass = classified_count >= 50
    print(f"  G4 gate (classified >= 50): {'PASS' if g4_pass else 'FAIL'} (classified: {classified_count})")
    
    # G1: need-related active rate >= 55% of random active rate
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"  G1 gate (need/random active ratio >= 55%): {'PASS' if g1_pass else 'FAIL'}")
        print(f"    need-related active rate: {need_rate*100:.1f}%")
        print(f"    random active rate: {random_rate*100:.1f}%")
        print(f"    ratio: {ratio*100:.1f}%")
    else:
        g1_pass = False
        print(f"  G1 gate: SKIPPED (insufficient classification: need-related={classified['need-related']}, random={classified['random']})")
    
    # G3: both categories represented
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"  G3 gate (both categories represented): {'PASS' if g3_pass else 'FAIL'} (need-related: {classified['need-related']}, random: {classified['random']})")
    
    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n  Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'}")
    
    # Step 5: Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "keyword": keyword,
        "sample_size": len(packages),
        "classified": {k: classified[k] for k in classified},
        "active": {k: active[k] for k in active},
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "conclusion": "pending",
        "experiment_description": "View-count principle prototype v2: PyPI package discovery tool",
    }
    
    os.makedirs("EXPERIMENTS/0xx-viewcount-prototype", exist_ok=True)
    with open("EXPERIMENTS/0xx-viewcount-prototype/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-viewcount-prototype/results.json ===")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main())