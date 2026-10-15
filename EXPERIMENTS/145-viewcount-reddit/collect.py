#!/usr/bin/env python3
"""E145 — View-Count Principle on Reddit: Data Collection"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Reddit API helper (public read-only endpoints, no authentication)
REDDIT_API = "https://www.reddit.com"

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
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "reddit", "post", "comment", "thread", "subreddit",
}


def reddit_api_get(path: str, limit: int = 0, timeout: int = 30) -> Optional[Dict]:
    """Make unauthenticated Reddit API request."""
    url = f"{REDDIT_API}{path}.json"
    if limit > 0:
        url = f"{url}?limit={limit}"
    try:
        result = subprocess.run(
            ["curl", "-s", "-A", "think-free-experiment/1.0", url],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        # Reddit API returns [listing, metadata]; take first element
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data
    except Exception as e:
        print(f"   API error for {url}: {e}")
        return None


def fetch_subreddit_posts(subreddit: str, limit: int = 50, sort: str = "hot") -> List[Dict]:
    """Fetch posts from a subreddit."""
    path = f"/r/{subreddit}/{sort}"
    data = reddit_api_get(path, limit=limit)
    if data is None:
        print(f"   Failed to fetch r/{subreddit}/{sort}")
        return []
    posts = []
    for item in data.get("data", {}).get("children", []):
        post_data = item.get("data", {})
        posts.append({
            "id": post_data.get("id", ""),
            "title": post_data.get("title", ""),
            "score": post_data.get("score", 0),
            "num_comments": post_data.get("num_comments", 0),
            "url": post_data.get("url", ""),
        })
    return posts


def classify_post(title: str) -> str:
    """Classify a post as need-related or random based on title."""
    title_lower = title.lower()
    
    # Check for generic terms - if present, classify as random
    for gw in GENERIC_TERMS:
        if gw in title_lower:
            return "random"
    
    # Check for need indicators
    for kw in NEED_INDICATORS:
        if kw in title_lower:
            return "need-related"
    
    # Default to random if no indicators found
    return "random"


def run_experiment(subreddits=None, posts_per_subreddit: int = 50):
    """Run the view-count principle experiment on Reddit."""
    
    if subreddits is None:
        subreddits = ["programming", "learnpython", "webdev", "django", "python"]
    
    print("=" * 60)
    print("E145 — View-Count Principle on Reddit")
    print("=" * 60)
    print(f"\nSubreddits: {', '.join(subreddits)}")
    print(f"Posts per subreddit: {posts_per_subreddit}")
    print()
    
    all_posts = []
    
    # Step 1: Fetch posts from each subreddit
    for subreddit in subreddits:
        print(f"Fetching r/{subreddit} (hot, limit={posts_per_subreddit})...")
        posts = fetch_subreddit_posts(subreddit, limit=posts_per_subreddit, sort="hot")
        print(f"  Fetched {len(posts)} posts")
        for post in posts:
            classified = classify_post(post["title"])
            post["classified"] = classified
            all_posts.append(post)
        # Rate limit courtesy sleep
        time.sleep(2)
    
    # Step 2: Gate assessment
    print("\n" + "=" * 60)
    print("Step 2: Gate assessment")
    print("=" * 60)
    
    # G1: Retrieval
    print(f"\nG1: Retrieval — Total posts = {len(all_posts)} (need: ≥50)")
    g1_pass = len(all_posts) >= 50
    print(f"   G1: {'PASS' if g1_pass else 'FAIL'}")
    
    if not g1_pass:
        print("   Insufficient posts for G1. Experiment terminated.")
        results = {"error": "g1_failed", "total_posts": len(all_posts)}
        output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/145-viewcount-reddit/results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        return results
    
    # Separate classified posts
    need_related_posts = [p for p in all_posts if p["classified"] == "need-related"]
    random_posts = [p for p in all_posts if p["classified"] == "random"]
    
    print(f"   Need-related classified: {len(need_related_posts)}")
    print(f"   Random classified: {len(random_posts)}")
    
    # G4: Arrival field (both categories represented)
    g4_pass = len(need_related_posts) > 0 and len(random_posts) > 0
    print(f"\nG4: Arrival field — need-related: {len(need_related_posts) > 0}, random: {len(random_posts) > 0}")
    print(f"   G4: {'PASS' if g4_pass else 'FAIL'}")
    
    if not g4_pass:
        print("   Both categories not represented. Experiment terminated.")
        results = {"error": "g4_failed", "need_related": len(need_related_posts), "random": len(random_posts)}
        output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/145-viewcount-reddit/results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, indent=2))
        return results
    
    # G2 + G3: Separation and effect magnitude
    need_scores = [p["score"] for p in need_related_posts if p["score"] is not None and p["score"] > 0]
    random_scores = [p["score"] for p in random_posts if p["score"] is not None and p["score"] > 0]
    
    print(f"\nG2/V: Separation and effect magnitude")
    print(f"   Need-related posts with score > 0: {len(need_scores)}")
    print(f"   Random posts with score > 0: {len(random_scores)}")
    
    if not need_scores or not random_scores:
        print("   G3: FAIL (insufficient data for effect size)")
        g2_pass = False
        g3_pass = False
    else:
        # Cliff's δ computation
        greater = sum(1 for x in need_scores for y in random_scores if x > y)
        ties = sum(1 for x in need_scores for y in random_scores if x == y)
        less = len(need_scores) * len(random_scores) - greater - ties
        
        cliff_d = (greater - less) / (len(need_scores) * len(random_scores)) if len(need_scores) * len(random_scores) > 0 else 0
        print(f"   Cliff's δ: {cliff_d:.4f} (need: >0.147)")
        g2_pass = cliff_d > 0.147
        print(f"   G2: {'PASS' if g2_pass else 'FAIL'}")
        
        # Proportion of need-related above random median
        random_median = sorted(random_scores)[len(random_scores) // 2]
        above_random = sum(1 for s in need_scores if s > random_median)
        prop_above = above_random / len(need_scores) if need_scores else 0
        
        print(f"   Random median score: {random_median}")
        print(f"   Need-related above random median: {above_random}/{len(need_scores)} = {prop_above:.4f}")
        g3_pass = prop_above > 0.60
        print(f"   G3: {'PASS' if g3_pass else 'FAIL'} (proportion above random median > 0.60)")
    
    # Step 3: Write results
    results = {
        "experiment": "E145",
        "title": "View-Count Principle on Reddit",
        "subreddits": subreddits,
        "posts_fetched": len(all_posts),
        "g1_retrieval_pass": g1_pass,
        "g2_separation": g2_pass,
        "g3_effect_magnitude": g3_pass,
        "g4_arrival_field": g4_pass,
        "need_related_classified": len(need_related_posts),
        "random_classified": len(random_posts),
        "conclusion": "ALL_PASS" if all([g1_pass, g2_pass, g3_pass, g4_pass]) else "GATE_CLOSED",
        "domain": "reddit",
        "timestamp": "2026-10-15"
    }
    
    output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/145-viewcount-reddit/results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults written to {output_path}")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == "__main__":
    results = run_experiment()
    if results.get("conclusion") == "ALL_PASS":
        print("\n✓ All gates passed — view-count principle supported on Reddit")
    else:
        print("\n✗ Gates failed — view-count principle does not generalize to Reddit")