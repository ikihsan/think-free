#!/usr/bin/env python3
"""NPM platform search module."""

import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


NPM_SEARCH_URL = "https://registry.npmjs.org/-/v1/search"
NPM_PACKAGE_URL = "https://registry.npmjs.org/{name}"


def search_packages(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search NPM for packages matching query."""
    params = {"text": query, "size": max_results, "from": 0}
    url = f"{NPM_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  NPM search error: {e}")
        return []
    
    results = []
    for pkg in data.get("objects", [])[:max_results]:
        p = pkg.get("package", {})
        results.append({
            "name": p.get("name", ""),
            "summary": p.get("description", ""),
            "description": p.get("description", ""),
            "version": p.get("version", ""),
            "platform": "npm",
            "url": f"https://www.npmjs.com/package/{p.get('name', '')}/",
            "score": pkg.get("score", {}).get("final", 0),
        })
    
    return results


def get_package_details(name: str) -> Optional[Dict[str, Any]]:
    """Get detailed package metadata including download stats."""
    url = NPM_PACKAGE_URL.format(name=urllib.parse.quote(name))
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  NPM detail error for {name}: {e}")
        return None
    
    # NPM API returns flat structure
    dist_tags = data.get("dist-tags", {})
    latest_version = dist_tags.get("latest", "")
    latest = data.get("versions", {}).get(latest_version, {})
    
    # Compute activity score from metadata (E072 approach)
    activity_score = 0
    if dist_tags:
        activity_score += 1
    if data.get("homepage"):
        activity_score += 5
    repo = data.get("repository")
    if repo and isinstance(repo, dict) and repo.get("url"):
        activity_score += 2
    keywords = data.get("keywords")
    if keywords and isinstance(keywords, list) and len(keywords) > 0:
        activity_score += 1
    
    return {
        "name": data.get("name", name),
        "summary": data.get("description", ""),
        "description": data.get("readme", "")[:2000] if data.get("readme") else data.get("description", ""),
        "version": latest_version,
        "author": data.get("author", {}).get("name", "") if isinstance(data.get("author"), dict) else str(data.get("author", "")),
        "license": data.get("license", ""),
        "homepage": data.get("homepage", ""),
        "repository": data.get("repository", {}),
        "keywords": data.get("keywords", []),
        "activity_score": activity_score,
        "platform": "npm",
        "url": f"https://www.npmjs.com/package/{name}/",
    }


def enrich_results(results: List[Dict[str, Any]], max_detail: int = 10) -> List[Dict[str, Any]]:
    """Enrich search results with detailed metadata and activity scores."""
    enriched = []
    
    for i, pkg in enumerate(results):
        if i >= max_detail:
            pkg["activity_score"] = 0
            enriched.append(pkg)
            continue
        
        details = get_package_details(pkg["name"])
        if details:
            pkg.update(details)
            # Activity score from metadata (E072)
            pkg["activity_score"] = pkg.get("activity_score", 0)
        else:
            pkg["activity_score"] = 0
        
        enriched.append(pkg)
        time.sleep(0.1)
    
    return enriched


if __name__ == "__main__":
    # Test
    results = search_packages("react state management")
    print(f"Found {len(results)} packages")
    enriched = enrich_results(results[:5])
    for r in enriched:
        print(f"  {r['name']}: {r.get('summary', '')[:60]} (activity: {r.get('activity_score', 0)})")