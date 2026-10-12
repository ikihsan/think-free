#!/usr/bin/env python3
"""Hex.pm platform search module."""

import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


HEX_SEARCH_URL = "https://hex.pm/api/packages"
HEX_PACKAGE_URL = "https://hex.pm/api/packages/{name}"


def search_packages(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search Hex.pm for packages matching query."""
    params = {
        "search": query,
        "sort": "downloads",
        "page": 1,
    }
    url = f"{HEX_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Hex.pm search error: {e}")
        return []
    
    results = []
    for pkg in data[:max_results]:
        downloads = pkg.get("downloads", {})
        results.append({
            "name": pkg.get("name", ""),
            "summary": pkg.get("meta", {}).get("description", "") or "",
            "description": pkg.get("meta", {}).get("description", "") or "",
            "version": pkg.get("meta", {}).get("version", "") or "",
            "downloads_all": downloads.get("all", 0),
            "downloads_recent": downloads.get("recent", 0),  # 30-day
            "downloads_week": downloads.get("week", 0),
            "downloads_day": downloads.get("day", 0),
            "platform": "hex",
            "url": f"https://hex.pm/packages/{pkg.get('name', '')}",
        })
    
    return results


def get_package_details(name: str) -> Optional[Dict[str, Any]]:
    """Get detailed package metadata."""
    url = HEX_PACKAGE_URL.format(name=urllib.parse.quote(name))
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Hex.pm detail error for {name}: {e}")
        return None
    
    meta = data.get("meta", {})
    downloads = data.get("downloads", {})
    releases = data.get("releases", [])
    
    latest_version = ""
    if releases:
        latest_version = releases[-1].get("version", "")
    
    return {
        "name": name,
        "summary": meta.get("description", "") or "",
        "description": meta.get("description", "") or "",
        "version": latest_version,
        "license": meta.get("license", {}).get("name", "") if isinstance(meta.get("license"), dict) else str(meta.get("license", "")),
        "links": meta.get("links", {}),
        "downloads_all": downloads.get("all", 0),
        "downloads_recent": downloads.get("recent", 0),
        "downloads_week": downloads.get("week", 0),
        "downloads_day": downloads.get("day", 0),
        "platform": "hex",
        "url": f"https://hex.pm/packages/{name}",
    }


def enrich_results(results: List[Dict[str, Any]], max_detail: int = 10) -> List[Dict[str, Any]]:
    """Enrich search results with detailed metadata."""
    enriched = []
    
    for i, pkg in enumerate(results):
        if i >= max_detail:
            pkg["activity_score"] = pkg.get("downloads_recent", 0)
            enriched.append(pkg)
            continue
        
        details = get_package_details(pkg["name"])
        if details:
            pkg.update(details)
        pkg["activity_score"] = pkg.get("downloads_recent", 0)
        
        enriched.append(pkg)
        time.sleep(0.1)
    
    return enriched


if __name__ == "__main__":
    # Test
    results = search_packages("web framework")
    print(f"Found {len(results)} packages")
    enriched = enrich_results(results[:5])
    for r in enriched:
        print(f"  {r['name']}: {r.get('summary', '')[:60]} (recent downloads: {r.get('downloads_recent', 0)})")