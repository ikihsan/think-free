"""PyPI fetch helpers, split out of the prototype's measuring script.

The API calls lived inline in `experiment.py`, whose inline word lists had
already taken it over the 300-line cap in `docs/policy/doc-standards.md`.
Lifted verbatim; the retry wrapper keeps its own call to `time.sleep`.
"""

import json
import time
import urllib.request

def fetch_pypi_packages(keyword, n=200):
    """Fetch packages from PyPI simple index matching a keyword."""
    url = f"https://pypi.org/simple/?q={keyword}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode()
            names = re.findall(r'href="/simple/([^"]+)"', html)
            packages = []
            seen = set()
            for name in names:
                if re.match(r'^[\d._-]+$', name):
                    continue
                if not name or len(name) < 2:
                    continue
                if name in seen:
                    continue
                seen.add(name)
                packages.append(name)
                if len(packages) >= n:
                    break
            return packages
    except Exception as e:
        print(f"Error fetching PyPI packages for keyword '{keyword}': {e}")
        return []

def fetch_pypi_package_info_with_retry(name, max_retries=3):
    """Fetch package metadata from PyPI JSON API with retry logic."""
    url = f"https://pypi.org/pypi/{name}/json"
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E0xx'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                info = data.get("info", {})
                return {
                    "name": name,
                    "description": info.get("description", "") or "",
                    "version": info.get("version", "") or "",
                    "keywords": info.get("keywords", "") or "",
                }
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 0.5 * (2 ** attempt)
                print(f"  Retry {attempt+1}/{max_retries} for {name} in {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                print(f"  Failed to fetch {name} after {max_retries} attempts: {e}")
                return None
