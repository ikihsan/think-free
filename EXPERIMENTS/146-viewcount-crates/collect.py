#!/usr/bin/env python3
"""E146 — View-Count Principle on crates.io: Data Collection"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

CRATES_IO_API = "https://crates.io/api/v1"

NEED_INDICATORS = {
    "web", "api", "http", "client", "server", "framework",
    "database", "sql", "postgres", "mysql", "redis", "mongo",
    "json", "parser", "auth", "oauth", "jwt", "session", "cookie",
    "cache", "queue", "worker", "job", "background", "async",
    "test", "mock", "fixture", "benchmark", "profile",
    "config", "settings", "env", "environment", "secret",
    "logger", "logging", "telemetry", "metrics", "tracing",
    "email", "mail", "smtp", "notification", "push",
    "file", "storage", "upload", "download", "archive",
    "image", "video", "audio", "media", "thumbnail",
    "search", "index", "elasticsearch", "fulltext",
    "graphql", "grpc", "websocket", "realtime", "pubsub",
    "crypto", "hash", "encrypt", "decrypt", "sign", "verify",
    "validate", "validator", "schema", "contract",
    "template", "render", "view", "html", "css", "asset",
    "router", "routing", "dispatch", "handler", "middleware",
    "dependency", "injection", "container", "provider",
    "cli", "command", "argument", "flag", "option",
    "migration", "seed", "factory",
    "excel", "pdf", "docx",
    "timex", "chrono", "decimal", "money", "currency", "exchange",
    "uuid", "nanoid", "slug", "parameterize",
    "async", "await", "future", "poll", "select",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "rust", "crate", "cargo", "",
}


def crates_request(path: str, timeout: int = 30) -> Optional[Dict]:
    """Make unauthenticated crates.io API request."""
    url = f"{CRATES_IO_API}{path}"
    try:
        result = subprocess.run(
            ["curl", "-s", "-A", "think-free-experiment/1.0", url],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            print(f"   API error (curl): {result.stderr[:200]}")
            return None
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        print(f"   API error: {e}")
        return None


def get_crate_info(crate_name: str) -> Optional[Dict]:
    """Fetch info for a single crate."""
    data = crates_request(f"/crates/{crate_name}")
    if data and "crate" in data:
        return data["crate"]
    return None


def classify_crate(name: str, description: str) -> str:
    """Classify a crate as need-related or random based on name/description."""
    name_lower = name.lower()
    desc_lower = description.lower() if description else ""
    
    # Check for generic terms - if present, classify as random
    for gw in GENERIC_TERMS:
        if gw in name_lower or gw in desc_lower:
            return "random"
    
    # Check for need indicators
    for kw in NEED_INDICATORS:
        if kw in name_lower or kw in desc_lower:
            return "need-related"
    
    # Default to random if no indicators found
    return "random"


def fetch_crates(limit: int = 100) -> List[Dict]:
    """Fetch crates from crates.io API."""
    data = crates_request(f"/crates?per_page={limit}")
    if data is None:
        return []
    crates = data.get("crates", [])
    return crates


def run_experiment(crate_limit: int = 100):
    """Run the view-count principle experiment on crates.io."""
    
    print("=" * 60)
    print("E146 — View-Count Principle on crates.io")
    print("=" * 60)
    print(f"\nFetching {crate_limit} crates from crates.io...")
    print()
    
    # Step 1: Fetch crates
    crates = fetch_crates(limit=crate_limit)
    print(f"Fetched {len(crates)} crates")
    
    if len(crates) < 30:
        print("   WARNING: Less than 30 crates retrieved, may not pass G1")
    
    # Step 2: Classify and collect data
    all_crates = []
    
    for crate in crates:
        name = crate.get("name", "")
        description = crate.get("description", "")
        downloads = crate.get("downloads", 0)
        recent_downloads = crate.get("recent_downloads", 0)
        
        classified = classify_crate(name, description)
        
        all_crates.append({
            "name": name,
            "description": description,
            "downloads": downloads,
            "recent_downloads": recent_downloads,
            "classified": classified,
        })
    
    # Step 3: Gate assessment
    print("\n" + "=" * 60)
    print("Step 2: Gate assessment")
    print("=" * 60)
    
    # G1: Retrieval
    print(f"\nG1: Retrieval — Total crates = {len(all_crates)} (need: ≥50)")
    g1_pass = len(all_crates) >= 50
    print(f"   G1: {'PASS' if g1_pass else 'FAIL'}")
    
    if not g1_pass:
        print("   Insufficient crates for G1. Experiment terminated.")
        results = {"error": "g1_failed", "total_crates": len(all_crates)}
        output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/146-viewcount-crates/results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        return results
    
    # Separate classified crates
    need_related = [c for c in all_crates if c["classified"] == "need-related"]
    random_crates = [c for c in all_crates if c["classified"] == "random"]
    
    print(f"   Need-related classified: {len(need_related)}")
    print(f"   Random classified: {len(random_crates)}")
    
    # G4: Both categories represented
    g4_pass = len(need_related) > 0 and len(random_crates) > 0
    print(f"\nG4: Arrival field — need-related: {len(need_related) > 0}, random: {len(random_crates) > 0}")
    print(f"   G4: {'PASS' if g4_pass else 'FAIL'}")
    
    if not g4_pass:
        print("   Both categories not represented. Experiment terminated.")
        results = {"error": "g4_failed", "need_related": len(need_related), "random": len(random_crates)}
        output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/146-viewcount-crates/results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        return results
    
    # G2 + G3: Separation and effect magnitude
    need_active = sum(1 for c in need_related if c["downloads"] > 0)
    random_active = sum(1 for c in random_crates if c["downloads"] > 0)
    
    need_rate = need_active / len(need_related) if need_related else 0
    random_rate = random_active / len(random_crates) if random_crates else 0
    
    print(f"\nG2: Separation")
    print(f"   Need-related active (downloads > 0): {need_active}/{len(need_related)} = {need_rate:.4f}")
    print(f"   Random active (downloads > 0): {random_active}/{len(random_crates)} = {random_rate:.4f}")
    
    # Cliff's δ computation
    need_scores = [c["downloads"] for c in need_related if c["downloads"] > 0]
    random_scores = [c["downloads"] for c in random_crates if c["downloads"] > 0]
    
    if need_scores and random_scores:
        greater = sum(1 for x in need_scores for y in random_scores if x > y)
        ties = sum(1 for x in need_scores for y in random_scores if x == y)
        less = len(need_scores) * len(random_scores) - greater - ties
        
        cliff_d = (greater - less) / (len(need_scores) * len(random_scores)) if len(need_scores) * len(random_scores) > 0 else 0
        print(f"   Cliff's δ: {cliff_d:.4f} (need: >0.147)")
        g2_pass = cliff_d > 0.147
        print(f"   G2: {'PASS' if g2_pass else 'FAIL'}")
        
        # Proportion above random median
        random_median = sorted(random_scores)[len(random_scores) // 2]
        above_random = sum(1 for s in need_scores if s > random_median)
        prop_above = above_random / len(need_scores) if need_scores else 0
        
        print(f"   Random median downloads: {random_median}")
        print(f"   Need-related above random median: {above_random}/{len(need_scores)} = {prop_above:.4f}")
        g3_pass = prop_above > 0.60
        print(f"   G3: {'PASS' if g3_pass else 'FAIL'} (proportion above random median > 0.60)")
    else:
        print("   G2: SKIP (insufficient data for effect size)")
        print("   G3: SKIP (insufficient data for effect size)")
        g2_pass = False
        g3_pass = False
    
    # Step 4: Write results
    results = {
        "experiment": "E146",
        "title": "View-Count Principle on crates.io",
        "crates_fetched": len(all_crates),
        "g1_retrieval_pass": g1_pass,
        "g2_separation": g2_pass,
        "g3_effect_magnitude": g3_pass,
        "g4_arrival_field": g4_pass,
        "need_related_classified": len(need_related),
        "random_classified": len(random_crates),
        "need_active_rate": need_active / len(need_related) if need_related else 0,
        "random_active_rate": random_active / len(random_crates) if random_crates else 0,
        "conclusion": "ALL_PASS" if all([g1_pass, g2_pass, g3_pass, g4_pass]) else "GATE_CLOSED",
        "domain": "crates.io",
        "timestamp": "2026-10-15"
    }
    
    output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/146-viewcount-crates/results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults written to {output_path}")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == "__main__":
    results = run_experiment()
    if results.get("conclusion") == "ALL_PASS":
        print("\n✓ All gates passed — view-count principle supported on crates.io")
    else:
        print("\n✗ Gates failed — view-count principle does not generalize to crates.io")