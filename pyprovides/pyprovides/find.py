#!/usr/bin/env python3
"""Query-time reverse lookup: find which distribution provides a module."""

import time
from typing import Optional

from .constants import (KNOWN_ALIASES, STDLIB_MODULES, RANKED_CACHE,
                        RANKED_LOCAL, ResolveError)
from .core import provides


def _load_ranked_projects(cache_path=RANKED_CACHE, max_age_seconds=86400):
    """Load top PyPI projects by download count, from cache or local reference."""
    import json
    import os
    # Check cache freshness
    if os.path.exists(cache_path):
        try:
            stat = os.stat(cache_path)
            if time.time() - stat.st_mtime < max_age_seconds:
                with open(cache_path) as fh:
                    return json.load(fh)
        except (OSError, json.JSONDecodeError):
            pass
    # Load from local reference file (from E090 experiment)
    if os.path.exists(RANKED_LOCAL):
        try:
            with open(RANKED_LOCAL) as fh:
                data = json.load(fh)
            os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
            with open(cache_path, "w") as fh:
                json.dump(data, fh)
            return data
        except (OSError, json.JSONDecodeError):
            pass
    # Return empty structure on failure
    return {"rows": []}


def ranked_project_names(limit: Optional[int] = None, cache_path=RANKED_CACHE):
    """Return list of project names, ranked by download count (highest first)."""
    data = _load_ranked_projects(cache_path)
    names = [r["project"] for r in data.get("rows", [])]
    if limit:
        return names[:limit]
    return names


def find_provider(module: str, max_checks: int = 500, cache: bool = True,
                  cache_dir: str = None, timeout: int = 30):
    """Find which distribution provides a module, by checking top PyPI projects.

    This is a query-time reverse lookup: instead of building a full index,
    we check candidate distributions on demand until we find one that provides
    the module, or we exhaust our budget.

    Resolution order:
    1. Standard library check (instant)
    2. Known aliases table (instant, covers common cross-name cases)
    3. Exact-name match (check if a distribution with the same name provides it)
    4. Top-N search (check top PyPI distributions' wheels)

    Args:
        module: The module name to find a provider for (e.g., "sklearn")
        max_checks: Maximum number of distributions to check in step 4 (default 500)
        cache: Whether to use the wheel metadata cache
        cache_dir: Cache directory for wheel metadata
        timeout: HTTP timeout per request

    Returns:
        (status, matches, detail)
        status: 'found' | 'stdlib' | 'not-found' | 'error'
        matches: List of (distribution_name, modules_set, detail_dict) for providers
        detail: Dict with 'checked', 'provider', 'elapsed_seconds', 'method'
    """
    from .constants import CACHE_DIR as DEFAULT_CACHE_DIR
    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR
    
    t0 = time.time()
    
    # Step 1: Standard library check
    top_module = module.split(".")[0]
    if top_module in STDLIB_MODULES:
        elapsed = time.time() - t0
        return "stdlib", [], {"checked": 0, "provider": "stdlib", "elapsed_seconds": round(elapsed, 6), "method": "stdlib"}
    
    # Step 2: Known aliases table
    if module in KNOWN_ALIASES:
        dist_name = KNOWN_ALIASES[module]
        try:
            status, mods, detail = provides(dist_name, cache=cache, cache_dir=cache_dir, timeout=timeout)
            if status == "ok" and module in mods:
                elapsed = time.time() - t0
                return "found", [(dist_name, mods, detail)], {"checked": 1, "provider": dist_name, "elapsed_seconds": round(elapsed, 3), "method": "alias"}
        except Exception:
            pass  # Fall through to search
    
    # Step 3: Exact-name match (distribution named the same as module)
    try:
        status, mods, detail = provides(module, cache=cache, cache_dir=cache_dir, timeout=timeout)
        if status == "ok" and module in mods:
            elapsed = time.time() - t0
            return "found", [(module, mods, detail)], {"checked": 1, "provider": module, "elapsed_seconds": round(elapsed, 3), "method": "exact"}
    except Exception:
        pass  # Fall through to search
    
    # Step 4: Top-N search
    checked = 0
    matches = []

    for dist_name in ranked_project_names(limit=max_checks):
        checked += 1
        try:
            status, mods, detail = provides(dist_name, cache=cache, cache_dir=cache_dir, timeout=timeout)
            if status == "ok" and module in mods:
                matches.append((dist_name, mods, detail))
                # For now, return on first match; could collect all
                break
        except Exception:
            # Skip distributions that error, continue checking
            continue

    elapsed = time.time() - t0
    if matches:
        return "found", matches, {"checked": checked + 2, "provider": matches[0][0], "elapsed_seconds": round(elapsed, 3), "method": "search"}
    return "not-found", [], {"checked": checked + 2, "provider": None, "elapsed_seconds": round(elapsed, 3), "method": "search"}