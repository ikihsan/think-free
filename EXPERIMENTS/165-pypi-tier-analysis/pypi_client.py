"""E165 — PyPI API client with caching.

Split from run.py to stay within the 300-line cap.
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# PyPI API client with caching
# ---------------------------------------------------------------------------

SIMPLE_INDEX_CACHE = "/tmp/pypi_simple_index.txt"
SIMPLE_INDEX_MAX_AGE = 3600  # 1 hour


def fetch_simple_index() -> List[str]:
    """Fetch or load cached PyPI simple index package names."""
    if os.path.exists(SIMPLE_INDEX_CACHE):
        age = time.time() - os.path.getmtime(SIMPLE_INDEX_CACHE)
        if age < SIMPLE_INDEX_MAX_AGE:
            print(f"  Loading simple index from cache...")
            with open(SIMPLE_INDEX_CACHE) as f:
                return [line.strip() for line in f if line.strip()]

    print("  Fetching PyPI simple index...")
    url = "https://pypi.org/simple/"
    req = urllib.request.Request(url, headers={"User-Agent": "E165-TierAnalysis/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8")
            names = re.findall(r'href="/simple/([^"\']+)"', html)
            filtered = [n for n in names if not n.startswith("(") and not n.startswith("[")]
            with open(SIMPLE_INDEX_CACHE, "w") as f:
                f.write("\n".join(filtered))
            print(f"  Fetched and cached {len(filtered)} package names")
            return filtered
    except Exception as e:
        print(f"  Simple index fetch failed: {e}")
        if os.path.exists(SIMPLE_INDEX_CACHE):
            print("  Using stale cache...")
            with open(SIMPLE_INDEX_CACHE) as f:
                return [line.strip() for line in f if line.strip()]
        return []


def search_packages(keyword: str, all_names: List[str], max_results: int = 50) -> List[str]:
    """Search for packages matching keyword in the pre-fetched name list."""
    kw_lower = keyword.lower()
    matching = [n for n in all_names if kw_lower in n.lower()]
    return matching[:max_results]


def fetch_pypi_package(name: str) -> Optional[Dict]:
    """Fetch package metadata from PyPI JSON API."""
    url = f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E165-TierAnalysis/1.0", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def extract_package_info(pkg_data: Dict) -> Dict:
    """Extract relevant info from PyPI JSON response."""
    info = pkg_data.get("info", {})
    releases = pkg_data.get("releases", {})

    first_release = None
    for ver, files in releases.items():
        for f in files:
            ut = f.get("upload_time") or f.get("upload_time_iso_8601")
            if ut:
                if first_release is None or ut < first_release:
                    first_release = ut

    num_releases = len(releases)

    return {
        "name": info.get("name", ""),
        "version": info.get("version", ""),
        "description": info.get("summary", "") or "",
        "first_release": first_release,
        "num_releases": num_releases,
    }