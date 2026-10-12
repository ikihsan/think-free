#!/usr/bin/env python3
"""GitHub platform search module."""

import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


GITHUB_API_BASE = "https://api.github.com"
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


def search_packages(query: str, max_results: int = 20, language: str = None) -> List[Dict[str, Any]]:
    """Search GitHub repositories (alias for search_repositories for interface consistency)."""
    return search_repositories(query, max_results, language)


def search_repositories(query: str, max_results: int = 20, language: str = None) -> List[Dict[str, Any]]:
    """Search GitHub repositories."""
    search_query = query
    if language:
        search_query += f" language:{language}"
    
    params = {
        "q": search_query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(max_results, 100),
    }
    url = f"{GITHUB_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "needfind/1.0",
            "Accept": "application/vnd.github.v3+json",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining:
                rem = int(remaining)
                if rem < 5:
                    print(f"  GitHub rate limit low: {rem} remaining")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("  GitHub rate limited")
        else:
            print(f"  GitHub search error: {e}")
        return []
    except Exception as e:
        print(f"  GitHub search error: {e}")
        return []
    
    results = []
    for repo in data.get("items", [])[:max_results]:
        results.append({
            "name": repo.get("full_name", ""),
            "summary": repo.get("description", "") or "",
            "description": repo.get("description", "") or "",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "language": repo.get("language", ""),
            "topics": repo.get("topics", []),
            "pushed_at": repo.get("pushed_at", ""),
            "created_at": repo.get("created_at", ""),
            "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
            "platform": "github",
            "url": repo.get("html_url", ""),
        })
    
    return results


def get_repo_details(full_name: str) -> Optional[Dict[str, Any]]:
    """Get detailed repository metadata."""
    url = f"{GITHUB_API_BASE}/repos/{full_name}"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "needfind/1.0",
            "Accept": "application/vnd.github.v3+json",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            repo = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  GitHub detail error for {full_name}: {e}")
        return None
    
    # Activity score: stars + forks + recent activity
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    
    # Check recency
    recent = False
    pushed_at = repo.get("pushed_at", "")
    if pushed_at:
        try:
            from datetime import datetime, timezone
            pushed = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            recent = (now - pushed).days <= 365
        except Exception:
            pass
    
    activity_score = stars + forks * 2 + (100 if recent else 0)
    
    return {
        "name": repo.get("full_name", ""),
        "summary": repo.get("description", "") or "",
        "description": repo.get("description", "") or "",
        "stars": stars,
        "forks": forks,
        "open_issues": repo.get("open_issues_count", 0),
        "language": repo.get("language", ""),
        "topics": repo.get("topics", []),
        "pushed_at": pushed_at,
        "created_at": repo.get("created_at", ""),
        "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
        "activity_score": activity_score,
        "platform": "github",
        "url": repo.get("html_url", ""),
    }


def enrich_results(results: List[Dict[str, Any]], max_detail: int = 10) -> List[Dict[str, Any]]:
    """Enrich search results with detailed metadata."""
    enriched = []
    
    for i, repo in enumerate(results):
        if i >= max_detail:
            repo["activity_score"] = repo.get("stars", 0) + repo.get("forks", 0) * 2
            enriched.append(repo)
            continue
        
        details = get_repo_details(repo["name"])
        if details:
            repo.update(details)
        else:
            repo["activity_score"] = repo.get("stars", 0) + repo.get("forks", 0) * 2
        
        enriched.append(repo)
        time.sleep(0.5)  # Be respectful of rate limits
    
    return enriched


if __name__ == "__main__":
    # Test
    results = search_repositories("async http client", language="Python")
    print(f"Found {len(results)} repos")
    enriched = enrich_results(results[:5])
    for r in enriched:
        print(f"  {r['name']}: {r.get('summary', '')[:60]} (stars: {r.get('stars', 0)}, activity: {r.get('activity_score', 0)})")