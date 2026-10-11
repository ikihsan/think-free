#!/usr/bin/env python3
"""E107 — Harvest GitHub repositories for view-count principle experiment (search-only)"""
import json
import os
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Set

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
SEARCH_ENDPOINT = "/search/repositories"

# Need-related topics (indicating common programming needs) - high-value topics
NEED_TOPICS = [
    "web-framework", "database", "orm", "cache", "queue", "messaging",
    "authentication", "authorization", "oauth", "jwt", "security",
    "logging", "monitoring", "observability", "testing", "deployment",
    "kubernetes", "docker", "graphql", "grpc", "websocket",
    "serialization", "validation", "configuration", "secrets-management",
    "search", "elasticsearch", "machine-learning", "data-processing",
    "streaming", "load-balancing", "rate-limiting", "circuit-breaker",
    "router", "middleware", "cli", "migration", "http-client", "api-client",
]

# Generic topics (likely not need-related)
GENERIC_TOPICS = [
    "utils", "common", "core", "library", "tool", "util", "helper",
    "base", "standard", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox",
]

# Need indicators in descriptions
NEED_INDICATORS = {
    "web framework", "http server", "http client", "api client", "rest api",
    "database", "orm", "sql", "postgresql", "mysql", "redis", "mongodb",
    "cache", "caching", "queue", "messaging", "rabbitmq", "kafka",
    "authentication", "authorization", "oauth", "jwt", "session", "security",
    "logging", "monitoring", "observability", "testing", "test framework",
    "deployment", "ci/cd", "continuous integration", "continuous deployment",
    "kubernetes", "docker", "container", "microservices", "service mesh",
    "graphql", "grpc", "websocket", "real-time", "pub/sub", "message broker",
    "serialization", "json", "xml", "yaml", "protobuf", "avro",
    "validation", "schema", "configuration", "config", "secrets management",
    "email", "notification", "push", "file storage", "object storage", "s3",
    "search", "elasticsearch", "fulltext", "machine learning", "ml", "ai",
    "data processing", "etl", "streaming", "data pipeline",
    "load balancing", "rate limiting", "circuit breaker", "retry", "timeout",
    "router", "routing", "middleware", "dependency injection", "cli",
    "command line", "argument parsing", "template engine", "rendering",
    "migration", "seeding", "factory", "active record",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package", "tool", "util", "helper",
    "base", "standard", "stdlib", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox", "toy",
    "sample", "proof of concept", "poc", "prototype", "experiment",
}

TARGET_PER_GROUP = 80  # Aim high to account for ambiguous classifications
MAX_PAGES_PER_QUERY = 2
REQUEST_DELAY = 2.0  # seconds between requests to be gentle


def make_request(url: str) -> Dict[str, Any]:
    """Make a GitHub API request with rate limit handling."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "origin-mission-E107",
            "Accept": "application/vnd.github.v3+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining")
            reset = resp.headers.get("X-RateLimit-Reset")
            if remaining is not None:
                rem = int(remaining)
                print(f"  Rate limit remaining: {rem}")
                if rem < 3:
                    if reset:
                        wait_time = max(0, int(reset) - int(time.time()) + 10)
                        if wait_time > 0:
                            print(f"  Rate limit low, waiting {wait_time}s...")
                            time.sleep(wait_time)
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            reset = e.headers.get("X-RateLimit-Reset")
            if reset:
                wait_time = max(0, int(reset) - int(time.time()) + 10)
                if wait_time > 0:
                    print(f"  Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    return make_request(url)  # Retry once
        print(f"  HTTP Error {e.code}: {e.reason}")
        return {}
    except Exception as e:
        print(f"  Error: {e}")
        return {}


def search_repositories(query: str, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
    """Search GitHub repositories."""
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
        "page": page,
    }
    url = f"{GITHUB_API_BASE}{SEARCH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = make_request(url)
    return data.get("items", [])


def classify_repository(repo: Dict[str, Any]) -> str:
    """Classify repository as need-related, random, or ambiguous."""
    topics = set(t.lower() for t in repo.get("topics", []))
    description = (repo.get("description") or "").lower()
    
    has_generic_topic = any(t in GENERIC_TOPICS for t in topics)
    has_need_topic = any(t in NEED_TOPICS for t in topics)
    has_need_desc = any(ind in description for ind in NEED_INDICATORS)
    has_generic_desc = any(term in description for term in GENERIC_TERMS)
    
    # Classification logic
    if has_need_topic and not has_generic_topic:
        return "need-related"
    if has_need_desc and not (has_generic_topic or has_generic_desc):
        return "need-related"
    if has_generic_topic and not has_need_topic:
        return "random"
    if has_generic_desc and not (has_need_topic or has_need_desc):
        return "random"
    return "ambiguous"


def harvest_group(topics: List[str], group_name: str, target: int) -> List[Dict[str, Any]]:
    """Harvest repositories for a group using topic searches (search API only)."""
    print(f"\n=== Harvesting {group_name} repositories ===")
    repos = []
    seen_full_names: Set[str] = set()
    
    for topic in topics:
        if len(repos) >= target:
            break
        
        print(f"  Searching topic: {topic}")
        query = f"topic:{topic}"
        
        for page in range(1, MAX_PAGES_PER_QUERY + 1):
            if len(repos) >= target:
                break
            
            items = search_repositories(query, page=page)
            if not items:
                break
            
            for item in items:
                full_name = item["full_name"]
                if full_name in seen_full_names:
                    continue
                seen_full_names.add(full_name)
                
                # Use search result directly - it has all fields we need:
                # stargazers_count, forks_count, open_issues_count, pushed_at, topics, description
                repos.append(item)
                if len(repos) % 10 == 0:
                    print(f"    Collected {len(repos)} repositories...")
                
                if len(repos) >= target:
                    break
            
            time.sleep(REQUEST_DELAY)
        
        time.sleep(REQUEST_DELAY)
    
    print(f"  Finished {group_name}: {len(repos)} repositories")
    return repos


def main():
    print("=== E107 — GitHub Repositories View-Count Principle Harvest (search-only) ===")
    print(f"Target: {TARGET_PER_GROUP} repositories per group")
    
    # Harvest need-related repositories
    need_repos = harvest_group(NEED_TOPICS, "need-related", TARGET_PER_GROUP)
    
    # Harvest random repositories
    random_repos = harvest_group(GENERIC_TOPICS, "random", TARGET_PER_GROUP)
    
    # Classify all repositories
    print("\n=== Classifying repositories ===")
    all_repos = []
    
    for repo in need_repos:
        classification = classify_repository(repo)
        repo["classification"] = classification
        repo["classification_intended"] = "need-related"
        all_repos.append(repo)
    
    for repo in random_repos:
        classification = classify_repository(repo)
        repo["classification"] = classification
        repo["classification_intended"] = "random"
        all_repos.append(repo)
    
    # Count classifications
    class_counts = {}
    for repo in all_repos:
        cls = repo["classification"]
        class_counts[cls] = class_counts.get(cls, 0) + 1
    
    print(f"\nClassification results:")
    for cls, count in sorted(class_counts.items()):
        print(f"  {cls}: {count}")
    
    # Save raw data
    os.makedirs("EXPERIMENTS/107-github-repos-viewcount", exist_ok=True)
    with open("EXPERIMENTS/107-github-repos-viewcount/raw_data.json", "w") as f:
        json.dump(all_repos, f, indent=2)
    
    print(f"\nRaw data saved to EXPERIMENTS/107-github-repos-viewcount/raw_data.json")
    print(f"Total repositories: {len(all_repos)}")
    
    return all_repos


if __name__ == "__main__":
    main()