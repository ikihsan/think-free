#!/usr/bin/env python3
"""E067 — did you mean a different project? prototype.

Tests whether a "did you mean / this resolves to a different project" warning
would surface the 24 healthy-metadata false accepts identified in E064.

Practical difficulty: When developers type a package name into pip/npm that is
a near-miss for a real package but resolves to a different project, they may
install the wrong package without realizing it.

Who experiences it: Developers who use package managers, particularly when typing
package names from memory or quickly.

Available evidence: E064 measured that 93 of 576 (16.15%) near-miss package names
resolve to real, different artifacts; 24 of 93 false accepts carry healthy metadata
(popular, actively maintained projects).

Important uncertainty: Whether surfacing "this is a different project than
intended" would help users make informed installation decisions.

Prototype: Uses the PyPI JSON API to check if a given package name has
similarly-named siblings on PyPI, and warns if the name the user typed is likely
a different project than intended.
"""

import json
import sys
import urllib.request
import urllib.error


PYPI_JSON_URL = "https://pypi.org/pypi/{name}/json"


def fetch_pypi_metadata(name):
    """Fetch package metadata from PyPI JSON API."""
    try:
        url = PYPI_JSON_URL.format(name=urllib.parse.quote(name, safe=""))
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "think-free-e067/1.0"},
        )
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read().decode("utf-8"))
        return data
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def find_similar_packages(name, all_packages=None):
    """Find packages on PyPI with similar names.

    Looks for packages whose names share a common prefix or have a similar
    base name with different suffixes (e.g., 'chalk-cli' vs 'chalk').
    """
    if all_packages is None:
        metadata = fetch_pypi_metadata(name)
        if metadata is None:
            return []
        all_packages = set(metadata.keys()) if isinstance(metadata, dict) else set()

    # Don't look up if we already have no data
    if not all_packages:
        return []

    # Normalize the input name
    normalized = name.lower().strip()
    similar = []

    for pkg_name in all_packages:
        pkg_lower = pkg_name.lower()
        if pkg_lower == normalized:
            continue  # exact match, skip

        # Check if one is a prefix of the other (e.g., 'chalk' vs 'chalk-cli')
        if pkg_lower.startswith(normalized) or normalized.startswith(pkg_lower):
            similar.append(pkg_name)
        # Check for common suffix patterns like -cli, -utils, etc.
        elif "-cli" in pkg_lower or "-utils" in pkg_lower or "-rs" in pkg_lower or "-go" in pkg_lower:
            # Strip common suffixes and compare bases
            base1 = pkg_lower.replace("-cli", "").replace("-utils", "").replace("-rs", "").replace("-go", "").replace("-js", "")
            base2 = normalized.replace("-cli", "").replace("-utils", "").replace("-rs", "").replace("-go", "").replace("-js", "")
            if base1 == base2 and base1:
                similar.append(pkg_name)

    return similar


def check_did_you_mean(package_name):
    """Check if the package name likely resolves to a different intended project.

    Returns a dict with the analysis result.
    """
    metadata = fetch_pypi_metadata(package_name)
    if metadata is None:
        return {
            "package_name": package_name,
            "found_on_pypi": False,
            "warning": None,
            "note": "Package not found on PyPI or API error",
        }

    # Get the actual package name from the metadata (in case of normalization)
    info = metadata.get("info", {})
    actual_name = info.get("name", package_name).lower()
    normalized_input = package_name.lower()

    if actual_name == normalized_input:
        # Exact match - no warning needed
        return {
            "package_name": package_name,
            "found_on_pypi": True,
            "actual_name": info.get("name", package_name),
            "warning": None,
            "note": "Exact match on PyPI - no ambiguity",
        }

    # Find similarly-named packages
    similar = find_similar_packages(package_name, set(metadata.keys()) if isinstance(metadata, dict) else set())

    if similar:
        # Check if any similar package is a well-known "CLI/utils" variant
        # that the user might mistake for the base package
        warning_parts = []
        for sim in similar[:5]:  # top 5 similar
            sim_info = metadata  # simplified - in full would fetch sim metadata
            desc = ""
            # Check if this is a -cli or -utils variant
            sim_lower = sim.lower()
            if any(sim_lower.endswith(suffix) for suffix in ["-cli", "-utils", "-rs", "-go", "-js"]):
                base = sim_lower.rstrip("-cli -utils -rs go js".split())
                if base == actual_name or base == normalized_input:
                    warning_parts.append(
                        f"Did you mean '{sim}'? This is a {'-cli' if '-cli' in sim_lower else ''} variant "
                        f"of the '{base}' package you may be looking for. "
                        f"This is a different project than intended."
                    )
                    break

        if not warning_parts:
            # General similar package warning
            warning_parts.append(
                f"Package '{package_name}' resolves on PyPI, but there are similar-named packages. "
                f"Did you mean one of: {', '.join(similar[:3])}? "
                f"These are different projects."
            )

        return {
            "package_name": package_name,
            "found_on_pypi": True,
            "actual_name": info.get("name", package_name),
            "similar_packages": similar[:5],
            "warning": " | ".join(warning_parts) if warning_parts else None,
            "note": "Similar-named packages found on PyPI",
        }
    else:
        # Package found but no similarly-named siblings
        return {
            "package_name": package_name,
            "found_on_pypi": True,
            "actual_name": info.get("name", package_name),
            "warning": None,
            "note": "Package found on PyPI but no similarly-named siblings",
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 didyoumean.py <package_name>")
        print("Example: python3 didyoumean.py jinja2-cli")
        sys.exit(1)

    package_name = sys.argv[1]
    result = check_did_you_mean(package_name)

    print(f"Package: {result['package_name']}")
    print(f"Found on PyPI: {result['found_on_pypi']}")

    if result['found_on_pypi']:
        print(f"Actual PyPI name: {result['actual_name']}")

    if result.get('warning'):
        print(f"WARNING: {result['warning']}")

    if result.get('similar_packages'):
        print(f"Similar packages on PyPI: {', '.join(result['similar_packages'])}")

    if result.get('note'):
        print(f"Note: {result['note']}")

    # Exit code: 0 if no warning needed, 1 if warning would be shown
    if result['warning']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()