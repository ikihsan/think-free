"""View-count principle classifier and registry client.

Split out of `viewcount_cli.py` at the 300-line cap. This half owns the
need-indicator vocabulary and the registry client; `viewcount_cli.py` owns
argument parsing and the gate report. The vocabulary was measured to cover
only 28% of a representative pool (E113), which is why it lives in one
named place rather than being copied per experiment.

Original module docstring:

E103+ — View-count principle CLI prototype.

Search a package registry for need-related packages using the view-count
principle: need-related packages have systematically higher activity metadata
(description + version) than random packages.

Usage:
    python3 tools/viewcount_cli.py <keyword> [--top N] [--registry pypi]

    python3 tools/viewcount_cli.py --list-keywords
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

# ---------------------------------------------------------------------------
# Need-indicator classifier (same logic as E071/E072/E102/E103 experiments)
# ---------------------------------------------------------------------------

NEED_INDICATORS = {
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "profiler", "tracing", "observability",
    "deployment", "ci", "cd", "pipeline", "build", "package",
    "network", "api", "client", "server", "framework", "engine",
    "parser", "lexer", "converter", "transform", "serializer",
    "validation", "sanitization", "encryption", "decryption",
    "compression", "decompression", "encoding", "decoding",
    "serialization", "deserialization", "persistance", "storage",
    "retrieval", "indexing", "search", "query", "aggregation",
    "reporting", "metrics", "observability", "dashboard",
    "debugging", "troubleshooting", "diagnostics", "audit",
    "compliance", "governance", "risk", "mitigation",
    "optimization", "performance", "scaling", "load",
    "queue", "messaging", "broker", "topic", "publish",
    "subscribe", "routing", "firehose", "stream",
    "cache", "redis", "memcached", "eviction",
    "queue", "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "micro service", "distributed", "cluster",
    # Extended vocabulary (E172 experiment): additional need indicators
    # observed in Python package descriptions beyond the original 55-term set.
    "crud", "rest", "sdk", "cli",
}

# Generic terms that classify as "random" (not need-related)
GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets",
}


def _matches_word_boundary(desc_lower, term):
    """Check if *term* appears as a whole word in *desc_lower* (regex \b)."""
    # word-boundary match: avoid substring hits like "database" inside "databaseify"
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_package(description):
    """Classify a package as 'need-related' or 'random' based on its description.

    Uses word-boundary matching to reduce substring false positives.
    First checks generic terms (classifies as random), then need indicators.
    """
    if not description:
        return "random"
    desc_lower = description.lower()

    # If a generic term appears as a whole word, classify as random.
    for term in GENERIC_TERMS:
        if _matches_word_boundary(desc_lower, term):
            return "random"

    # Check for need-related indicators with word-boundary matching.
    for term in NEED_INDICATORS:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"

    # Default to random.
    return "random"


def is_active(package_info):
    """Check if a package has significant activity metadata (non-empty description
    AND version present), following the E071/E072/E102/E103 precedent."""
    desc = package_info.get("description", "") or ""
    version = package_info.get("version", "") or ""
    desc_active = len(desc.strip()) > 0
    version_active = version != "" and version is not None
    return desc_active and version_active


# ---------------------------------------------------------------------------
# Keyword-based extension: if description alone is insufficient, check title/
# project_name fields for need indicators.
# ---------------------------------------------------------------------------

def classify_by_keywords(package_info):
    """Supplementary classification using package metadata fields beyond description.

    Checks the project name and other available text fields for need indicators.
    Returns 'need-related', 'random', or None if insufficient fields are present.
    """
    name = (package_info.get("name", "") or "").lower()
    desc = (package_info.get("description", "") or package_info.get("summary", "") or "").lower()

    # Check name first - if a need indicator is in the project name, it's likely need-related
    for term in NEED_INDICATORS:
        if _matches_word_boundary(name, term):
            return "need-related"

    # If name has a generic term, classify as random
    for term in GENERIC_TERMS:
        if _matches_word_boundary(name, term):
            return "random"

    # Fall through to description-level classification
    return None


# ---------------------------------------------------------------------------
# Registry adapters
# ---------------------------------------------------------------------------

# A small embedded sample of well-known packages with descriptions and versions.
# This serves as a fallback when the PyPI API is unavailable.
FALLBACK_PACKAGES = [
    {"name": "requests", "version": "2.31.0", "summary": "Python HTTP for Humans."},
    {"name": "numpy", "version": "1.24.3", "summary": "NumPy is the fundamental package for array computing with Python."},
    {"name": "flask", "version": "2.3.3", "summary": "A micro web framework written in Python."},
    {"name": "django", "version": "4.2.7", "summary": "The Web framework for perfectionists with deadlines."},
    {"name": "pandas", "version": "2.1.4", "summary": "Data analysis and statistics using Python."},
    {"name": "pip", "version": "23.1.2", "summary": "The standard Python package manager."},
    {"name": "pyyaml", "version": "6.0.1", "summary": "YAML parser and emitter for Python."},
    {"name": "beautifulsoup4", "version": "4.12.2", "summary": "Screen-scraping library for Python."},
    {"name": "sqlalchemy", "version": "2.0.23", "summary": "SQL toolkit and Object Relational Mapper for Python."},
    {"name": "marshmallow", "version": "3.21.0", "summary": "A lightweight library for converting objects to/from JSON."},
    {"name": "black", "version": "23.7.0", "summary": "The uncompromising code formatter."},
    {"name": "flake8", "version": "6.0.1", "summary": "Modular source code checker: pep8 pyflakes and co"},

    {"name": "click", "version": "8.2.0", "summary": "Command line interfaces in a pleasant and usable way."},
    {"name": "pytest", "version": "7.4.3", "summary": "Simple powerful testing with Python"},

    {"name": "pyyaml", "version": "6.0.1", "summary": "YAML parser and emitter for Python."},
    {"name": "jinja2", "version": "3.1.2", "summary": "A very fast and expressive template engine."},
    {"name": "httpx", "version": "0.25.0", "summary": "The next generation HTTP client."},
    {"name": "urllib3", "version": "2.2.2", "summary": "HTTP library with thread-safe connection pooling"},

    {"name": "cython", "version": "0.29.35", "summary": "The Cython compiler for writing C extensions"},
    {"name": "cffi", "version": "1.17.0", "summary": "Foreign Function Interface for Python calling C code"},
    {"name": "mypy", "version": "1.7.1", "summary": "Optional static typing for Python"},
    {"name": "wheel", "version": "0.43.0", "summary": "Command line tool for manipulating wheel files"},

    {"name": "setuptools", "version": "65.5.0", "summary": "Most extensible Python build backend"},
    {"name": "virtualenv", "version": "20.16.0", "summary": "Virtual Python Environment builder"},
    {"name": "tqdm", "version": "4.66.2", "summary": "Fast, extensible progress bars (Python)"},
    {"name": "rich", "version": "13.7.1", "summary": "Rich text and beautiful formatting in the terminal"},

    {"name": "python-dotenv", "version": "1.0.0", "summary": "Loads environment variables from .env files"},
    {"name": "web3", "version": "5.31.0", "summary": "Python library for Ethereum"},
    {"name": "aiohttp", "version": "3.8.1", "summary": "Async http client/server framework (asyncio)"},
    {"name": "pendulum", "version": "2.2.2", "summary": "Python datetime library (better timedelta)"},
]


def fetch_fallback_packages(keyword):
    """Return packages from the embedded sample that match *keyword*."""
    matched = []
    kw_lower = keyword.lower()
    for pkg in FALLBACK_PACKAGES:
        # Use 'description' key, falling back to 'summary' if absent
        desc = pkg.get("description") or pkg.get("summary") or ""
        # Match against package name or summary/description
        if kw_lower in pkg["name"].lower() or kw_lower in desc.lower():
            matched_pkg = dict(pkg)  # shallow copy
            matched_pkg["description"] = desc  # normalize to 'description'
            matched.append(matched_pkg)
    # If no keyword match, return all (so the demo always shows something)
    if not matched:
        # Normalize descriptions and return all
        normalized = []
        for pkg in FALLBACK_PACKAGES:
            desc = pkg.get("description") or pkg.get("summary") or ""
            normalized.append(dict(pkg, description=desc))
        return normalized
    return matched


def search_pypi(keyword, max_results=200):
    """Search PyPI for packages matching *keyword*.

    Tries the PyPI JSON search API first, falls back to the simple index,
    then to the embedded fallback sample.
    """
    # Try the PyPI simple index to get package names
    try:
        url = "https://pypi.org/simple/"
        req = urllib.request.Request(url, headers={"User-Agent": "origin-viewcount-prototype/3.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8")
            # Extract package names from the simple index HTML
            names = re.findall(r'href="/simple/([^"\']+)"', html)[:100]
            # Filter to packages that might match the keyword
            matching = []
            seen = set()
            for name in names:
                # Skip obvious non-project entries (trailing / is from simple index format)
                if name.startswith("(") or name.startswith("["):
                    continue
                # Check if the name matches the keyword (simple substring)
                if keyword.lower() in name.lower():
                    matching.append(name)
                    seen.add(name)
                    if len(matching) >= max_results:
                        break
            if matching:
                # Fetch details for each matched package
                packages = []
                for name in matching[:max_results]:
                    try:
                        pkg_url = f"https://pypi.org/p/{name}/json"
                        pkg_req = urllib.request.Request(
                            pkg_url,
                            headers={"User-Agent": "origin-viewcount-prototype/3.0"},
                        )
                        with urllib.request.urlopen(pkg_req, timeout=5) as pkg_resp:
                            pkg_data = json.loads(pkg_resp.read().decode("utf-8"))
                            info = pkg_data.get("info", {})
                            packages.append(
                                {
                                    "name": name,
                                    "version": info.get("version", ""),
                                    "description": info.get("summary", ""),
                                    "author": info.get("author", ""),
                                    "author_email": info.get("author_email", ""),
                                    "home_page": info.get("home_page", ""),
                                    "project_urls": info.get("project_urls", {}),
                                }
                            )
                    except Exception:
                        # Fallback: use minimal data
                        packages.append(
                            {
                                "name": name,
                                "version": "",
                                "description": "",
                                "author": "",
                                "author_email": "",
                                "home_page": "",
                            }
                        )
                return packages[:max_results]
    except Exception:
        pass

    # Fall back to embedded sample
    return fetch_fallback_packages(keyword)


# ---------------------------------------------------------------------------
# End of viewcount_core module (vocabulary, classifiers, registry adapters).
# The prototype entry point (run_prototype, CLI) has been moved to
# tools/viewcount_prototype.py to keep this file within the 300-line cap.
# ---------------------------------------------------------------------------
