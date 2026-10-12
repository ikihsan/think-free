#!/usr/bin/env python3
"""NuGet platform search module."""

import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


NUGET_SEARCH_URL = "https://azuresearch-usnc.nuget.org/query"
NUGET_PACKAGE_URL = "https://api.nuget.org/v3-flatcontainer/{name}/{version}/{name}.nuspec"


def search_packages(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search NuGet for packages matching query."""
    params = {
        "q": query,
        "take": max_results,
        "prerelease": "false",
    }
    url = f"{NUGET_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  NuGet search error: {e}")
        return []
    
    results = []
    for pkg in data.get("data", [])[:max_results]:
        results.append({
            "name": pkg.get("id", ""),
            "summary": pkg.get("description", "") or "",
            "description": pkg.get("description", "") or "",
            "version": pkg.get("version", ""),
            "total_downloads": pkg.get("totalDownloads", 0),
            "tags": pkg.get("tags", []),
            "title": pkg.get("title", ""),
            "authors": pkg.get("authors", ""),
            "platform": "nuget",
            "url": f"https://www.nuget.org/packages/{pkg.get('id', '')}/",
        })
    
    return results


def get_package_details(name: str, version: str = None) -> Optional[Dict[str, Any]]:
    """Get detailed package metadata."""
    # First, search for the package to get latest version if not provided
    if not version:
        search_results = search_packages(f"id:{name}", max_results=1)
        if search_results:
            version = search_results[0].get("version", "")
    
    if not version:
        return None
    
    # Fetch nuspec for detailed metadata
    url = NUGET_PACKAGE_URL.format(name=urllib.parse.quote(name), version=version)
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/xml"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            nuspec = resp.read().decode()
    except Exception as e:
        print(f"  NuGet detail error for {name}: {e}")
        return None
    
    # Parse nuspec XML (simplified)
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(nuspec)
        ns = {"ns": "http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd"}
        
        metadata = root.find("ns:metadata", ns)
        if metadata is None:
            metadata = root.find("metadata")
        
        if metadata is not None:
            description = metadata.find("ns:description", ns)
            if description is None:
                description = metadata.find("description")
            
            authors = metadata.find("ns:authors", ns)
            if authors is None:
                authors = metadata.find("authors")
            
            project_url = metadata.find("ns:projectUrl", ns)
            if project_url is None:
                project_url = metadata.find("projectUrl")
            
            license_url = metadata.find("ns:licenseUrl", ns)
            if license_url is None:
                license_url = metadata.find("licenseUrl")
            
            tags = metadata.find("ns:tags", ns)
            if tags is None:
                tags = metadata.find("tags")
            
            return {
                "name": name,
                "summary": description.text if description is not None else "",
                "description": description.text if description is not None else "",
                "version": version,
                "authors": authors.text if authors is not None else "",
                "project_url": project_url.text if project_url is not None else "",
                "license_url": license_url.text if license_url is not None else "",
                "tags": tags.text.split() if tags is not None and tags.text else [],
                "platform": "nuget",
                "url": f"https://www.nuget.org/packages/{name}/",
            }
    except Exception as e:
        print(f"  NuGet nuspec parse error for {name}: {e}")
    
    return None


def enrich_results(results: List[Dict[str, Any]], max_detail: int = 10) -> List[Dict[str, Any]]:
    """Enrich search results with detailed metadata."""
    enriched = []
    
    for i, pkg in enumerate(results):
        if i >= max_detail:
            pkg["activity_score"] = pkg.get("total_downloads", 0)
            enriched.append(pkg)
            continue
        
        details = get_package_details(pkg["name"], pkg.get("version"))
        if details:
            pkg.update(details)
        pkg["activity_score"] = pkg.get("total_downloads", 0)
        
        enriched.append(pkg)
        time.sleep(0.1)
    
    return enriched


if __name__ == "__main__":
    # Test
    results = search_packages("json serializer")
    print(f"Found {len(results)} packages")
    enriched = enrich_results(results[:5])
    for r in enriched:
        print(f"  {r['name']}: {r.get('summary', '')[:60]} (downloads: {r.get('total_downloads', 0)})")