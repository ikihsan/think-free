"""E0xx — View-count principle on Packagist (PHP packages)"""
import json
import os
import urllib.request
import time
import random
import re
from html import unescape

# Configuration
NEED_INDICATORS = {
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "performance", "api", "client", "server",
    "framework", "engine", "core", "utility", "helper",
    "parser", "lexer", "converter", "transform", "serializer",
    "validation", "sanitization", "encryption", "decryption",
    "compression", "decompression", "encoding", "decoding",
    "serialization", "deserialization", "persistance", "storage",
    "retrieval", "indexing", "search", "query", "aggregation",
    "reporting", "metrics", "dashboard", "debugging", "troubleshooting",
    "diagnostics", "audit", "compliance", "governance", "risk", "mitigation",
    "optimization", "scaling", "load", "queue", "messaging", "broker",
    "topic", "publish", "subscribe", "routing", "firehose", "stream",
    "cache", "redis", "memcached", "eviction",
    "queue", "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "micro service", "distributed", "cluster",
    "cms", "content", "theme", "plugin", "extension",
    "rest", "soap", "graphql", "json", "xml", "http",
    "mvc", "orm", "api gateway", "service mesh",
}

# Too-generic terms that always classify as "random"
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies", "gem", "rake", "rails", "bundle", "assets"}

SAMPLE_SIZE = 100  # G2 gate: minimum 100 packages
MIN_CLASSIFIED = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate


def fetch_packages(keyword, page=1, per_page=20):
    """Fetch PHP packages from Packagist by search keyword."""
    url = f"https://packagist.org/search.json?q={keyword}&limit={per_page}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except Exception as e:
        print(f"Error fetching packages for keyword '{keyword}': {e}")
        return []


def fetch_package_details(package_name):
    """Fetch detailed info for a specific PHP package."""
    url = f"https://packagist.org/packages/{package_name}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("package", {})
    except Exception as e:
        print(f"Error fetching package {package_name}: {e}")
        return None


def classify_package(package_info):
    """Classify a PHP package as need-related or random."""
    desc = package_info.get("description", "") or ""
    name = package_info.get("name", "").lower()
    desc_lower = desc.lower()
    
    # Check for generic terms - if present in description (but not just the package name), classify as random
    found_generic = False
    for term in GENERIC_TERMS:
        # Only flag if term appears in desc and not as the main package name
        if term in desc_lower and (term not in name or len(term) > len(name)):
            found_generic = True
            break
    
    if found_generic:
        return "random"
    
    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        if term in desc_lower:
            found_need = True
            break
    
    if found_need:
        return "need-related"
    
    # If description is very short, classify as random
    if len(desc.strip()) < 10:
        return "random"
    
    # Default to random
    return "random"


def is_active(package_info):
    """Check if a package has significant activity metadata (the 'active' signal).
    Following E071/E072 precedent adapted for Packagist: 'active' = having non-empty
    description AND version releases present. On Packagist, the `keywords` field is often
    absent, so we treat the active signal as description + version presence.
    
    On Packagist:
    - Description = the package description field (non-empty = active)
    - Version metadata = the package has release versions (non-empty dict = active)
    - Keywords are supportive but not required (often absent on Packagist)
    """
    desc = package_info.get("description", "") or ""
    # Version: check if package has releases (versions is a dict keyed by version)
    versions = package_info.get("versions", {})
    version_active = versions is not None and isinstance(versions, dict) and len(versions) > 0
    
    # Description must be non-empty
    desc_active = len(desc.strip()) > 0
    
    # Keywords are supportive but not required on Packagist
    # (many legitimate packages don't have keywords declared)
    keywords_active = True  # Conservative: assume ok if desc+version present
    
    return desc_active and keywords_active and version_active


def main():
    print("=== E0xx — View-count principle on Packagist (PHP packages) ===")
    print()
    
    # Step 1: Search for packages across need-related keywords
    print("Step 1: Searching Packagist across need-related keywords...")
    
    all_packages = []
    seen_names = set()
    
    # Keyword groups to search
    keyword_groups = [
        "database", "cache", "auth", "security", "logging", "monitoring",
        "testing", "benchmark", "performance", "api", "framework",
    ]
    
    for keyword in keyword_groups:
        results = fetch_packages(keyword, per_page=15)
        for pkg in results:
            name = pkg.get("name", "")
            if name and name not in seen_names:
                seen_names.add(name)
                all_packages.append(pkg)
                if len(all_packages) >= 200:
                    break
        if len(all_packages) >= 200:
            break
        time.sleep(0.3)
    
    print(f"  Found {len(all_packages)} unique packages across {len(keyword_groups)} keywords")
    time.sleep(0.5)
    
    # Step 2: Fetch details for each package and classify
    print(f"Step 2: Fetching details for {len(all_packages)} packages...")
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    
    for i, pkg in enumerate(all_packages):
        package_name = pkg.get("name", "")
        if not package_name:
            continue
        
        # Fetch detailed info
        details = fetch_package_details(package_name)
        if details is None:
            continue
        
        cls = classify_package(details)
        active_flag = is_active(details)
        
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        classified_count += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{len(all_packages)} packages...")
        
        time.sleep(0.15)  # Rate limiting - be respectful to Packagist API
    
    print(f"\nStep 2 complete: Classified {classified_count} packages")
    
    # Step 3: Print classification results
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")
    
    print(f"  Total classified: {classified_count} / {len(all_packages)}")
    
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
    
    # Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "sample_size": len(all_packages),
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
        "experiment_description": "View-count principle on Packagist (PHP packages)",
    }
    
    os.makedirs("EXPERIMENTS/0xx-packagist-viewcount", exist_ok=True)
    with open("EXPERIMENTS/0xx-packagist-viewcount/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-packagist-viewcount/results.json ===")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())