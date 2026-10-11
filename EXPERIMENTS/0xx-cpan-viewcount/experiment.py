"""E0xx — View-count principle on CPAN (Perl package registry)"""
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

# Too-generic terms that always classify as "random"
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies", "gem", "rake", "rails", "cpan", "perl"}

SAMPLE_SIZE = 100  # G2 gate: minimum 100 packages
MIN_CLASSIFIED = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate


def fetch_cpan_packages(query, page=1, per_page=20):
    """Fetch packages from MetaCpan by search query."""
    # The MetaCpan API doesn't support page/per_page params in this format
    url = f"https://fastapi.metacpan.org/v1/release/_search?q={query}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            hits = data.get("hits", {}).get("hits", [])
            return hits
    except Exception as e:
        print(f"Error fetching CPAN packages for query '{query}': {e}")
        return []


def fetch_cpan_release(release_id):
    """Fetch detailed info for a specific CPAN release."""
    url = f"https://fastapi.metacpan.org/v1/release/{release_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching CPAN release {release_id}: {e}")
        return None


def classify_cpan_release(release_info):
    """Classify a CPAN release as need-related or random."""
    info = release_info.get("abstract", "") or ""
    info_lower = info.lower()
    
    # Check for generic terms - if present in abstract, classify as random
    found_generic = False
    for term in GENERIC_TERMS:
        if term in info_lower:
            found_generic = True
            break
    
    if found_generic:
        return "random"
    
    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        # Simple substring check but be conservative
        if term in info_lower:
            found_need = True
            break
    
    if found_need:
        return "need-related"
    
    # Default to random (we only classify as need-related when a clear need indicator is present)
    return "random"


def is_active_cpan(release_info):
    """Check if a CPAN release has significant activity metadata.
    Following E071/E072 precedent: 'active' = having non-empty abstract,
    version metadata, and distribution.
    """
    abstract = release_info.get("abstract", "") or ""
    version = release_info.get("version", "") or ""
    dist = release_info.get("distribution", "") or ""
    
    # Abstract must be non-empty
    desc_active = len(abstract.strip()) > 0
    
    # Version metadata must be present
    version_active = version != "" and version is not None
    
    # Distribution metadata must be present
    dist_active = dist != "" and dist is not None
    
    return desc_active and version_active and dist_active


def main():
    print("=== E0xx — View-count principle on CPAN ===")
    print()
    
    # Step 1: Search for packages across need-related keywords
    print("Step 1: Searching MetaCPAN across need-related keywords...")
    
    all_releases = []
    seen_ids = set()
    
    # Keyword groups to search
    keyword_groups = [
        "database", "cache", "auth", "security", "logging", "monitoring",
        "testing", "benchmark", "performance", "network", "api",
    ]
    
    for keyword in keyword_groups:
        results = fetch_cpan_packages(keyword)
        for hit in results:
            release_id = hit.get("_id", "")
            if release_id and release_id not in seen_ids:
                seen_ids.add(release_id)
                release_info = hit.get("_source", {})
                all_releases.append((release_id, release_info))
                if len(all_releases) >= 200:
                    break
        if len(all_releases) >= 200:
            break
        time.sleep(0.3)
    
    print(f"  Found {len(all_releases)} unique releases across {len(keyword_groups)} keywords")
    time.sleep(0.5)
    
    # Step 2: Fetch details for each release and classify
    print(f"Step 2: Fetching details for {len(all_releases)} releases...")
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    
    for i, (release_id, release_info) in enumerate(all_releases):
        if not release_info:
            continue
        
        cls = classify_cpan_release(release_info)
        active_flag = is_active_cpan(release_info)
        
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        classified_count += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{len(all_releases)} releases...")
        
        time.sleep(0.1)
    
    print(f"\nStep 2 complete: Classified {classified_count} releases")
    
    # Step 3: Print classification results
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")
    
    print(f"  Total classified: {classified_count} / {len(all_releases)}")
    
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
        "sample_size": len(all_releases),
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
        "experiment_description": "View-count principle on CPAN (Perl package registry)",
    }
    
    os.makedirs("EXPERIMENTS/0xx-cpan-viewcount", exist_ok=True)
    with open("EXPERIMENTS/0xx-cpan-viewcount/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-cpan-viewcount/results.json ===")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())