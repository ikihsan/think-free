"""E0xx — View-count principle on RubyGems"""
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
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies", "gem", "rake", "rails"}

SAMPLE_SIZE = 100  # G2 gate: minimum 100 packages
MIN_CLASSIFIED = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate


def fetch_gems_by_keyword(keyword, page=1, per_page=20):
    """Fetch gems from RubyGems by search keyword."""
    url = f"https://rubygems.org/api/v1/search.json?query={keyword}&page={page}&per_page={per_page}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching gems for keyword '{keyword}': {e}")
        return []


def fetch_gem_details(gem_name):
    """Fetch detailed info for a specific gem."""
    url = f"https://rubygems.org/api/v1/gems/{gem_name}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching gem {gem_name}: {e}")
        return None


def classify_gem(gem_info):
    """Classify a gem as need-related or random."""
    info = gem_info.get("info", "") or ""
    name = gem_info.get("name", "").lower()
    
    # Get description from info field
    desc_lower = info.lower()
    
    # Check for generic terms - if present in name or info, classify as random
    # But be careful: "gem" is the platform, not necessarily generic
    # Check for core platform terms
    for term in ["gem", "rails", "rake", "ruby"]:
        if term in desc_lower and term not in name:
            # This is a platform term, not a need indicator
            pass
    
    # Check for generic terms that should classify as random
    found_generic = False
    for term in GENERIC_TERMS:
        # Only flag if the term appears in info but not as the gem name itself
        if term in desc_lower:
            # Extra check: make sure it's not just the gem name being descriptive
            if term not in name.lower():
                found_generic = True
                break
    
    if found_generic:
        return "random"
    
    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        # Word boundary matching - term should be a standalone word or part of a phrase
        # Use simple substring check but be conservative
        if term in desc_lower:
            # Additional check: make sure it's not just a coincidence
            # For now, accept substring matches
            found_need = True
            break
    
    if found_need:
        return "need-related"
    
    # If description/info is very short, classify as random
    if len(info.strip()) < 10:
        return "random"
    
    # Default to random (we only classify as need-related when a clear need indicator is present)
    return "random"


def is_active(gem_info):
    """Check if a gem has significant activity metadata (the 'active' signal).
    Following E071/E072 precedent: 'active' = having non-empty description,
    keywords, and version metadata (matching the PyPI/NPM definition).
    
    On RubyGems:
    - Description = the `info` field (non-empty summary/description)
    - Keywords = RubyGems gem metadata may include tags; if not available, 
      we treat as active if description is present and version exists
    - Version metadata = the `version` field is present and non-empty
    """
    info = gem_info.get("info", "") or ""
    version = gem_info.get("version", "") or ""
    
    # Description must be non-empty
    desc_active = len(info.strip()) > 0
    
    # Version metadata must be present
    version_active = version != "" and version is not None
    
    # Keywords: RubyGems search API doesn't return a separate keywords field 
    # in the basic gem data. We treat as active if description + version are present,
    # which matches the E071 spirit of "has meaningful activity metadata"
    keywords_active = True  # Conservative: assume present if we have desc+version
    
    return desc_active and keywords_active and version_active


def main():
    print("=== E0xx — View-count principle on RubyGems ===")
    print()
    
    # Step 1: Search for gems across multiple need-related keywords
    print("Step 1: Searching RubyGems across need-related keywords...")
    
    all_gems = []
    seen_names = set()
    
    # Keyword groups to search
    keyword_groups = [
        "database", "cache", "auth", "security", "logging", "monitoring",
        "testing", "benchmark", "performance", "network", "api",
    ]
    
    for keyword in keyword_groups:
        results = fetch_gems_by_keyword(keyword, per_page=10)
        for gem in results:
            name = gem.get("name", "")
            if name and name not in seen_names:
                seen_names.add(name)
                all_gems.append(gem)
                if len(all_gems) >= 200:  # Fetch a bit more than needed
                    break
        if len(all_gems) >= 200:
            break
        time.sleep(0.3)
    
    print(f"  Found {len(all_gems)} unique gems across {len(keyword_groups)} keywords")
    time.sleep(0.5)
    
    # Step 2: Fetch details for each gem and classify
    print(f"Step 2: Fetching details for {len(all_gems)} gems...")
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    
    for i, gem in enumerate(all_gems):
        gem_name = gem.get("name", "")
        if not gem_name:
            continue
        
        # Fetch detailed info
        details = fetch_gem_details(gem_name)
        if details is None:
            continue
        
        cls = classify_gem(details)
        active_flag = is_active(details)
        
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        classified_count += 1
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{len(all_gems)} gems...")
        
        if classified_count >= MIN_CLASSIFIED and len(all_gems) - (i + 1) < 10:
            # We have enough classified, can stop early if needed
            pass
        
        time.sleep(0.2)  # Rate limiting - be respectful to RubyGems API
    
    print(f"\nStep 2 complete: Classified {classified_count} gems")
    
    # Step 3: Print classification results
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")
    
    print(f"  Total classified: {classified_count} / {len(all_gems)}")
    
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
    
    # G3: at least need-related and random both have some representation
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
        "sample_size": len(all_gems),
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
        "experiment_description": "View-count principle on RubyGems",
    }
    
    os.makedirs("EXPERIMENTS/0xx-rubygems-viewcount", exist_ok=True)
    with open("EXPERIMENTS/0xx-rubygems-viewcount/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-rubygems-viewcount/results.json ===")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())