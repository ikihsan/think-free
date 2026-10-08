#!/usr/bin/env python3
"""
Resolve package versions via PyPI API for E068 spec generator.
Uses PyPI JSON API to get latest stable versions for packages.
"""

import json
import urllib.request
import urllib.error
import time
import sys
from pathlib import Path

CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")
EXTRACTED_FILE = CACHE_DIR / "extracted.json"
RESOLVED_FILE = CACHE_DIR / "resolved.json"
PYPI_CACHE_DIR = CACHE_DIR / "pypi"

PYPI_CACHE_DIR.mkdir(exist_ok=True)

# Rate limiting: be nice to PyPI
REQUEST_DELAY = 0.1  # seconds between requests

def load_extracted():
    with open(EXTRACTED_FILE) as f:
        return json.load(f)

def get_pypi_info(package):
    """Get package info from PyPI, with local caching."""
    cache_file = PYPI_CACHE_DIR / f"{package}.json"
    
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                return json.load(f)
        except Exception:
            pass
    
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'E068-spec-generator/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        time.sleep(REQUEST_DELAY)
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"  PyPI error for {package}: HTTP {e.code}")
        return None
    except Exception as e:
        print(f"  PyPI error for {package}: {e}")
        return None

def get_latest_stable_version(pypi_data):
    """Get latest stable (non-pre-release) version from PyPI data."""
    if not pypi_data or 'releases' not in pypi_data:
        return None
    
    releases = pypi_data['releases']
    # Filter out pre-releases (alpha, beta, rc, dev, etc.)
    stable_versions = []
    for ver_str in releases.keys():
        # Skip pre-releases
        if any(x in ver_str.lower() for x in ['a', 'b', 'rc', 'dev', 'pre', 'post']):
            # But allow post releases (e.g., 1.0.0.post1)
            if 'post' not in ver_str.lower():
                continue
        stable_versions.append(ver_str)
    
    if not stable_versions:
        return None
    
    # Sort versions (simple approach: use packaging if available, else string sort)
    try:
        from packaging import version
        # Filter out versions that packaging can't parse
        parsable_versions = []
        for v in stable_versions:
            try:
                version.parse(v)
                parsable_versions.append(v)
            except Exception:
                pass
        if parsable_versions:
            parsable_versions.sort(key=version.parse, reverse=True)
            return parsable_versions[0]
    except ImportError:
        pass
    
    # Fallback: tuple-based sorting
    def ver_key(v):
        parts = []
        for p in v.split('.'):
            try:
                parts.append(int(p))
            except ValueError:
                # Handle non-numeric parts
                parts.append(p)
        return parts
    stable_versions.sort(key=ver_key, reverse=True)
    
    return stable_versions[0]

def resolve_packages(packages, readme_hints=None):
    """Resolve versions for a list of packages."""
    readme_hints = readme_hints or {}
    resolved = {}
    
    for pkg in packages:
        # Check README hints first
        if pkg in readme_hints:
            # TODO: Could try to match version constraint from hint
            pass
        
        pypi_data = get_pypi_info(pkg)
        if pypi_data:
            ver = get_latest_stable_version(pypi_data)
            if ver:
                resolved[pkg] = ver
                print(f"    {pkg} -> {ver}")
            else:
                print(f"    {pkg} -> NO STABLE VERSION")
        else:
            print(f"    {pkg} -> NOT FOUND ON PYPI")
    
    return resolved

def main():
    extracted = load_extracted()
    
    all_packages = set()
    
    # Collect all unique packages from all repos
    for repo in extracted['a1_repos'] + extracted['test_repos']:
        all_packages.update(repo['requirements_packages'])
        all_packages.update(repo['pyproject_packages'])
        all_packages.update(repo['poetry_lock_packages'])
        all_packages.update(repo['imports'])
    
    # Also collect from README hints
    for repo in extracted['a1_repos'] + extracted['test_repos']:
        all_packages.update(repo['readme_hints'].keys())
    
    print(f"Total unique packages to resolve: {len(all_packages)}")
    
    # Load existing resolved cache if any
    resolved_cache = {}
    if RESOLVED_FILE.exists():
        with open(RESOLVED_FILE) as f:
            resolved_cache = json.load(f)
    
    # Resolve missing packages
    to_resolve = [p for p in sorted(all_packages) if p not in resolved_cache]
    print(f"Already cached: {len(resolved_cache)}, Need to resolve: {len(to_resolve)}")
    
    for i, pkg in enumerate(to_resolve):
        print(f"[{i+1}/{len(to_resolve)}] Resolving {pkg}...", end=" ")
        pypi_data = get_pypi_info(pkg)
        if pypi_data:
            ver = get_latest_stable_version(pypi_data)
            if ver:
                resolved_cache[pkg] = ver
                print(f"{ver}")
            else:
                resolved_cache[pkg] = None
                print("NO STABLE VERSION")
        else:
            resolved_cache[pkg] = None
            print("NOT FOUND")
        
        # Save progress periodically
        if (i + 1) % 20 == 0:
            with open(RESOLVED_FILE, 'w') as f:
                json.dump(resolved_cache, f, indent=2)
    
    # Final save
    with open(RESOLVED_FILE, 'w') as f:
        json.dump(resolved_cache, f, indent=2)
    
    # Stats
    resolved_count = sum(1 for v in resolved_cache.values() if v is not None)
    print(f"\nResolved: {resolved_count}/{len(resolved_cache)} ({resolved_count/len(resolved_cache)*100:.1f}%)")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())