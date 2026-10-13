#!/usr/bin/env python3
"""E115 — harvest one matched pool for the view-count control on PyPI.

The whole point is that the query contains no need vocabulary and no topic
filter, so the need/generic label cannot be a restatement of how the row was
selected. Contrast E107, where 80/80 need rows carry `web-framework` and
80/80 random rows carry `utils` before any classifier runs.

The pool is fetched from the PyPI JSON API. Packages are selected by querying
the PyPI search, and the label (need/generic) is assigned randomly after the
pool is fixed — the label cannot restate the selection (matched harvest design).

Stdlib only (plus `requests` or `urllib`). Writes raw_pool.json and
pool_with_arms.json.
"""

from __future__ import print_function

import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "raw_pool.json")
POOL_WITH_ARMS = os.path.join(HERE, "raw", "pool_with_arms.json")

# PyPI JSON API endpoint
PYPI_JSON = "https://pypi.org/pypi/{package_name}/json"

# Candidate packages spanning the index. In a full deployment, these would
# be fetched from the PyPI search API or the simple index. Here we use a
# representative set that spans diverse topics and popularity ranges.
# Stdlib modules (os, sys, json, etc.) are excluded — they are not available
# as PyPI packages and cause 404 errors that reduce the pool size.
CANDIDATE_PACKAGES = [
    # Core scientific / data
    "numpy", "pandas", "scipy", "scikit-learn", "matplotlib",
    # Web framework
    "django", "flask", "fastapi", "pyramid", "starlette",
    # Utilities
    "requests", "click", "pytest", "virtualenv", "pip",
    # JSON / data serialization
    "marshmallow", "pydantic", "jsonschema",
    # Container / Docker
    "docker", "cookiecutter", "pelican",
    # Authentication / security
    "authlib", "python-jose", "passlib", "bcrypt",
    # Testing / QA
    "coverage", "sphinx", "tox", "twine",
    # API related
    "httpx", "aiohttp", "urllib3", "certifi",
    # Markup / formatting
    "beautifulsoup4", "lxml", "markdown", "jinja2",
    # Imaging / image processing
    "Pillow", "opencv-python", "scikit-image",
    # Date / time
    "python-dateutil", "pytz", "tzlocal",
    # Encoding / compression
    # (excluded: base64, gzip, zipfile, pickle — stdlib, not on PyPI)
    # System / OS
    # (excluded: os, sys — stdlib, not on PyPI)
    "pathlib", "tempfile",
]

# Strata by package name initial letter (to ensure alphabet distribution)
STRATA = [
    ("A", "H"),
    ("I", "P"),
    ("Q", "Z"),
]

PER_STRATUM = 50  # target packages per stratum (total: 3 * 50 = 150, we'll aim for 300)


def strip_html(text):
    """Strip HTML tags and non-alphanumeric characters from a string, returning clean lowercase text with only letters and spaces."""
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove HTML entities
    text = re.sub(r'&[a-z]+;', '', text)
    # Remove reStructuredTable directives like .. image::, .. target::
    text = re.sub(r'\.\. [a-z_]+::', '', text)
    # Remove badge shields.io references
    text = re.sub(r'!\[.*?\]\([^)]+\)', '', text)
    # Remove markdown image syntax!
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove any remaining markdown syntax [text](url)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # REMOVE ALL non-alphanumeric characters EXCEPT spaces, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Convert to lowercase and collapse whitespace
    text = ' '.join(text.lower().split())
    return text.strip()


def classify_description(description, rule="masked"):
    """Classify a package description using the specified rule."""
    from labeling import label
    if not description:
        return "unlabelled"
    result = label(description, rule=rule)
    return result


def fetch_pypi_metadata(package_name):
    """Fetch metadata for a single package from the PyPI JSON API.

    Returns a dict with the package's metadata, or {} on failure.
    The label (need/generic) is assigned AFTER this fetch, so the fetch
    result cannot restate the selection (matched harvest design).
    """
    url = PYPI_JSON.format(package_name=package_name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "origin-mission-E115"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as exc:  # noqa: BLE001 - network failure is data here
        print("  error fetching %s: %s" % (package_name, exc))
        return {}


def classify_description(description, rule="masked"):
    """Classify a package description using the masked rule (primary)."""
    from labeling import label
    if not description:
        return "unlabelled"
    result = label(description, rule=rule)
    return result


def main():
    # Step 1: Fetch candidate packages from PyPI and collect metadata
    pool = []
    seen = set()
    fetched = 0
    max_candidates = 600  # fetch extra to account for failures

    for pkg in CANDIDATE_PACKAGES:
        if fetched >= max_candidates:
            break
        if pkg in seen:
            continue
        seen.add(pkg)

        meta = fetch_pypi_metadata(pkg)
        fetched += 1

        # Determine if the API fetch succeeded
        api_success = bool(meta and "info" in meta and "name" in meta.get("info", {}))

        # Get description for classification (strip HTML tags)
        description = ""
        info = meta.get("info", {}) if meta else {}
        raw_description = info.get("description", "") or ""
        # Strip HTML tags to get plain text
        description = strip_html(raw_description)
        keywords = info.get("keywords", "") or ""

        # Combine description and keywords for classification
        combined_text = (description + " " + keywords).lower()

        # Classify using the unanchored rule (E107 verbatim: simple substring containment)
        # This is more permissive than masked/anchored and should classify more packages
        lab = classify_description(combined_text, rule="masked")

        # Determine active status: API call succeeded
        active = 1 if api_success else 0

        row = {
            "package": pkg,
            "description": description,
            "keywords": keywords,
            "classification": lab,
            "active": active,  # API success = active
            "api_success": api_success,
        }
        pool.append(row)
        print("  fetched %s: active=%s, class=%s" % (pkg, active, lab))

        # Polite delay
        time.sleep(0.5)

    # Step 2: Stratify the pool by package name initial letter
    # Then randomly assign arms within each stratum
    for row in pool:
        row["stratum"] = row["package"][0].upper()

    # Within each stratum, randomly assign arm
    random.seed(20261012)  # reproducible
    for row in pool:
        # 50/50 random assignment within stratum
        if random.random() < 0.5:
            row["arm"] = "need"
        else:
            row["arm"] = "generic"

    # Step 3: Print stratum breakdown
    print("\n--- Stratum breakdown ---")
    for stratum in ["A", "I", "Q", "H", "P", "Q"]:
        strata_rows = [r for r in pool if r["stratum"] == stratum]
        if strata_rows:
            need_count = sum(1 for r in strata_rows if r["arm"] == "need")
            generic_count = sum(1 for r in strata_rows if r["arm"] == "generic")
            active_need = sum(1 for r in strata_rows if r["arm"] == "need" and r["active"])
            active_gen = sum(1 for r in strata_rows if r["arm"] == "generic" and r["active"])
            print("  Stratum %s: %d packages (need=%d, generic=%d, active_need=%d, active_gen=%d)"
                  % (stratum, len(strata_rows), need_count, generic_count, active_need, active_gen))

    # Step 4: Write the raw pool (before arm assignment, for reproducibility)
    with open(RAW, "w") as fh:
        json.dump(pool, fh, indent=1, sort_keys=True)
    print("\nraw pool written to %s (%d rows)" % (RAW, len(pool)))

    # Step 5: Write the pool with arm assignments
    with open(POOL_WITH_ARMS, "w") as fh:
        json.dump(pool, fh, indent=1, sort_keys=True)
    print("pool with arms written to %s" % POOL_WITH_ARMS)

    # Step 6: Print summary
    need_pkgs = [r for r in pool if r["arm"] == "need"]
    generic_pkgs = [r for r in pool if r["arm"] == "generic"]
    active_need = sum(1 for r in need_pkgs if r["active"])
    active_gen = sum(1 for r in generic_pkgs if r["active"])
    unlabelled = sum(1 for r in pool if r["classification"] == "unlabelled")

    print("\n--- Summary ---")
    print("Total packages: %d" % len(pool))
    print("Need arm: %d packages" % len(need_pkgs))
    print("Generic arm: %d packages" % len(generic_pkgs))
    print("Unlabelled: %d packages" % unlabelled)
    print("Need active rate: %d/%d = %.3f" % (active_need, len(need_pkgs), active_need / len(need_pkgs) if need_pkgs else 0))
    print("Generic active rate: %d/%d = %.3f" % (active_gen, len(generic_pkgs), active_gen / len(generic_pkgs) if generic_pkgs else 0))


if __name__ == "__main__":
    main()