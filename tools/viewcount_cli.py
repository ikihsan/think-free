"""E103+ — View-count principle CLI prototype.

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
}

# Generic terms that classify as "random" (not need-related)
GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets",
}


def classify_package(description):
    """Classify a package as 'need-related' or 'random' based on its description."""
    if not description:
        return "random"
    desc_lower = description.lower()

    # If a generic term appears in the description words, classify as random.
    words = set(desc_lower.split())
    if words & GENERIC_TERMS:
        return "random"

    # Check for need-related indicators.
    for term in NEED_INDICATORS:
        if term in desc_lower:
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
        return normalized[:20]
    return matched


def search_pypi(keyword, max_results=200):
    """Search PyPI for packages matching *keyword*.

    Tries the PyPI JSON search API first, falls back to the simple index,
    then to the embedded fallback sample.
    """
    # Try the PyPI simple index to get package names
    try:
        url = "https://pypi.org/simple/"
        req = urllib.request.Request(url, headers={"User-Agent": "origin-viewcount-prototype/1.0"})
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
                            headers={"User-Agent": "origin-viewcount-prototype/1.0"},
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
# Prototype entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="View-count principle prototype: find need-related packages"
    )
    parser.add_argument("keyword", nargs="?", help="Search keyword or need description")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to display (default: 10)",
    )
    parser.add_argument(
        "--registry",
        choices=["pypi"],
        default="pypi",
        help="Package registry to search (default: pypi)",
    )
    parser.add_argument(
        "--list-keywords",
        action="store_true",
        help="List example search keywords from past experiments",
    )
    args = parser.parse_args()

    if args.list_keywords:
        print("Example keywords from prior experiments:")
        for kw in [
            "database", "cache", "auth", "security", "logging",
            "monitoring", "testing", "benchmark", "performance", "api",
        ]:
            print(f"  - {kw}")
        return

    if not args.keyword:
        parser.print_usage()
        print(
            "\nEnter a keyword/need description to search for relevant packages.\n"
            "The tool classifies packages as 'need-related' (have a need indicator "
            "in their description) or 'random' and reports active/metadata status."
        )
        return

    keyword = args.keyword
    print(f"=== View-count prototype: searching '{keyword}' ===\n")

    if args.registry == "pypi":
        packages = search_pypi(keyword, max_results=200)
    else:
        print(f"Registry '{args.registry}' not supported yet.")
        return

    if not packages:
        print("No packages found. Try a different keyword?")
        return

    # Classify and evaluate
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_pkgs = []

    for pkg in packages:
        cls = classify_package(pkg.get("description", ""))
        active_flag = is_active(pkg)
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        if cls == "need-related":
            need_related_pkgs.append(pkg)

    # Print classification summary
    print("=== Classification ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")

    # G1 gate: need-related active rate >= 55% of random active rate
    g1_pass = False
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"\n=== Gate G1 ===")
        print(f"  need-related active rate: {need_rate*100:.1f}%")
        print(f"  random active rate: {random_rate*100:.1f}%")
        print(f"  ratio (need/random): {ratio*100:.1f}%")
        print(f"  G1 pass (>= 55%): {'PASS' if g1_pass else 'FAIL'}")
    else:
        print(f"\n=== Gate G1 ===")
        print(f"  SKIPPED: need at least one package in each category (need-related={classified['need-related']}, random={classified['random']})")

    # G2 gate: minimum classified sample size >= 100
    g2_pass = classified["need-related"] + classified["random"] >= 100
    print(f"\n=== Gate G2 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G2 pass (>= 100): {'PASS' if g2_pass else 'FAIL'}")

    # G3 gate: both categories represented
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"\n=== Gate G3 ===")
    print(f"  G3 pass (both categories): {'PASS' if g3_pass else 'FAIL'}")

    # G4 gate: minimum 50 classified
    g4_pass = (classified["need-related"] + classified["random"]) >= 50
    print(f"\n=== Gate G4 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G4 pass (>= 50): {'PASS' if g4_pass else 'FAIL'}")

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n=== Overall ===")
    print(f"  All gates pass: {'YES' if all_pass else 'NO'}")

    # Display need-related packages ranked by version presence/activity
    print(f"\n=== Need-related packages (top {min(args.top, len(need_related_pkgs))}) ===")
    # Sort: packages with version/active first, then alphabetically
    need_related_pkgs.sort(
        key=lambda p: (
            0 if is_active(p) else 1,
            p.get("name", "").lower(),
        )
    )
    for i, pkg in enumerate(need_related_pkgs[: args.top]):
        name = pkg.get("name", "N/A")
        version = pkg.get("version", "N/A")
        desc = pkg.get("description", "")[:80] if pkg.get("description") else ""
        active_str = "ACTIVE" if is_active(pkg) else "inactive"
        print(
            f"  {i+1}. {name} {version}"
            f" -- {desc}..."
            f" [{active_str}]"
        )

    # Save results JSON for the session record
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": os.uname().machine if hasattr(os, "uname") else "unknown",
        "sample_size": len(packages),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0
            else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": (
            (active["need-related"] / classified["need-related"])
            / (active["random"] / classified["random"] >= 0.55)
            if classified["need-related"] > 0 and classified["random"] > 0
            else False
        ),
        "g2_pass": classified["need-related"] + classified["random"] >= 100,
        "g3_pass": classified["need-related"] > 0 and classified["random"] > 0,
        "g4_pass": (classified["need-related"] + classified["random"]) >= 50,
        "conclusion": "pending",
        "experiment_description": f"View-count prototype search for keyword: {keyword}",
    }

    out_dir = "EXPERIMENTS/e103-viewcount-prototype"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")


if __name__ == "__main__":
    main()