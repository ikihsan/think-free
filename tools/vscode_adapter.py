"""VS Code Extension Marketplace adapter for the view-count principle.

Adapted from the PyPI registry adapter in tools/viewcount_core.py.
The VS Code Extension Marketplace uses client-side rendering with no simple
public JSON API available from this environment. This module documents
the fetch barrier and provides a classification framework.

See E161 (session 2026-10-15-012) for the synthesis and proposal.
"""

import re
import json
import os
import time
import urllib.request
import urllib.parse


# ---------------------------------------------------------------------------
# Need-indicator classifier (adapted from tools/viewcount_core.py)
# ---------------------------------------------------------------------------

# Strong keywords that single-handedly classify an extension as need-related
STRONG_KEYWORDS = {
    "fix", "solution", "helper", "tool", "library", "framework", "bug",
    "crash", "debug", "troubleshoot", "problem", "issue", "install",
    "import", "automation", "script", "resolver", "validator", "parser",
    "converter", "player", "viewer", "manager", "controller", "driver",
    "automate", "automated", "wrapper", "tutorial", "guide",
}

# Secondary keywords — need-related if ≥2 appear
SECONDARY_KEYWORDS = {
    "how", "why", "calculate", "compute", "setup", "configure",
    "conflict", "conflict resolution", "conflict management",
    "conflict handling", "conflict de", "conflict resolve",
    "conflict manage", "conflict handle",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "extension",
    "snippet", "boilerplate", "template", "skeleton",
}


def _matches_word_boundary(desc_lower, term):
    """Check if *term* appears as a whole word in *desc_lower* (regex \b)."""
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_extension_description(description):
    """Classify a VS Code extension description as 'need-related' or 'random'.

    Classification logic (adapted from E148/GitHub repos pattern):

    - If any **strong keyword** appears as a whole word → need-related
    - If ≥2 **secondary keywords** appear → need-related
    - If any **generic term** appears as a whole word → random
    - Otherwise → random (default, lowest-confidence)
    """
    if not description:
        return "random"
    desc_lower = description.lower()

    # 1) Strong keyword single-match → need-related
    for term in STRONG_KEYWORDS:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"

    # 2) ≥2 secondary keywords → need-related
    secondary_count = 0
    for term in SECONDARY_KEYWORDS:
        if _matches_word_boundary(desc_lower, term):
            secondary_count += 1
    if secondary_count >= 2:
        return "need-related"

    # 3) Generic term → random
    for term in GENERIC_TERMS:
        if _matches_word_boundary(desc_lower, term):
            return "random"

    # 4) Default → random
    return "random"


def is_active(package_info):
    """Check if an extension has activity metadata (non-empty description).

    For VS Code extensions, presence of a non-empty description is the
    analogue of "has version + description" on PyPI."""
    desc = package_info.get("description", "") or ""
    return len(desc.strip()) > 0


def classify_by_keywords(package_info):
    """Supplementary classification using extension metadata fields.

    Checks the extension name and other available text fields for need
    indicators. Returns 'need-related', 'random', or None if insufficient.
    """
    name = (package_info.get("name", "") or "").lower()
    desc = (package_info.get("description", "") or "").lower()

    # Check name for strong keywords
    for term in STRONG_KEYWORDS:
        if _matches_word_boundary(name, term):
            return "need-related"

    # Check name for generic terms
    for term in GENERIC_TERMS:
        if _matches_word_boundary(name, term):
            return "random"

    # Fall through to description-level classification
    return None


# ---------------------------------------------------------------------------
# Registry adapter — VS Code Extension Marketplace
# ---------------------------------------------------------------------------

# The VS Code Extension Marketplace does not expose a simple public JSON API
# from the current environment. Access requires either:
#
# 1) The `vsce` tool with published extension data
# 2) Reverse-engineered undocumented API endpoints (blocked by CSP/rendering)
# 3) The Open VS Code Marketplace API (limited, requires authentication)
#
# This adapter documents the barrier and provides a fallback corpus of
# well-known extensions for framework validation.
# ---------------------------------------------------------------------------

# A small embedded sample of well-known VS Code extensions with descriptions.
# This serves as a fallback when the Marketplace API is unavailable.
FALLBACK_EXTENSIONS = [
    {
        "name": "vscode-remote-ssh",
        "version": "1.30.0",
        "description": "Remote - SSH allows developing on a remote machine using SSH.",
    },
    {
        "name": "python",
        "version": "1.25.0",
        "description": "Python language support for Visual Studio Code.",
    },
    {
        "name": "vscode-code-sample-explorer",
        "version": "0.2.1",
        "description": "Explore and search code samples for Visual Studio Code.",
    },
    {
        "name": "debugger",
        "version": "1.20.0",
        "description": "Debugger extension for Visual Studio Code.",
    },
    {
        "name": "material-icon-theme",
        "version": "4.5.0",
        "description": "A material design icon theme for Visual Studio Code.",
    },
    {
        "name": "vscode-test",
        "version": "1.5.0",
        "description": "Testing infrastructure for VS Code extensions.",
    },
    {
        "name": "javascript-jsx",
        "version": "1.15.0",
        "description": "JavaScript and JSX language support for Visual Studio Code.",
    },
    {
        "name": "gitlens",
        "version": "17.0.0",
        "description": "Supercharge the visual experience of editing with git.",
    },
    {
        "name": "hexeditor",
        "version": "0.3.0",
        "description": "A hex editor for Visual Studio Code.",
    },
    {
        "name": "path-intellisense",
        "version": "1.0.5",
        "description": "Intelligent path completion in Visual Studio Code.",
    },
]


def fetch_vscode_marketplace(keyword, max_results=200):
    """Attempt to fetch VS Code extensions from the Marketplace.

    Returns a list of extension dicts with 'name', 'version', 'description' keys.

    **Barrier**: The VS Code Extension Marketplace uses client-side rendering
    (React/TypeScript) with no accessible public JSON API from this environment.
    The fetch will always return the fallback corpus; the results file will
    document this barrier.
    """
    fallback = FALLBACK_EXTENSIONS[:]
    try:
        # Try the undocumented Marketplace API (search endpoint)
        # This is a best-effort attempt; the API is not guaranteed to work.
        search_url = (
            "https://marketplace.visualstudio.com/search?"
            "term=" + urllib.parse.quote(keyword) +
            "&category=All&galleries=Microsoft&vsVersion=&flags=prerelease"
        )
        req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": "origin-viewcount/3.0",
                "Accept": "application/json",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise Exception(f"HTTP {resp.status}")
            body = resp.read().decode("utf-8")
            # The response may be JSON or HTML depending on the endpoint
            try:
                data = json.loads(body)
                extensions = []
                # Parse the response structure (format varies)
                if isinstance(data, dict):
                    # Look for extension entries
                    results_key = None
                    for key in ["results", "extensionResults", "extensions"]:
                        if key in data and data[key]:
                            results_key = key
                            break
                    if results_key:
                        entries = data[results_key]
                        if isinstance(entries, list):
                            for entry in entries[:max_results]:
                                if isinstance(entry, dict):
                                    name = entry.get("name", "")
                                    version = entry.get("version", "")
                                    description = entry.get("description", "")
                                    if name and description:
                                        extensions.append({
                                            "name": name,
                                            "version": version,
                                            "description": description,
                                        })
                elif isinstance(data, list):
                    for entry in data[:max_results]:
                        if isinstance(entry, dict):
                            name = entry.get("name", "")
                            version = entry.get("version", "")
                            description = entry.get("description", "")
                            if name and description:
                                extensions.append({
                                    "name": name,
                                                    "version": version,
                                    "description": description,
                                })
                return extensions if extensions else fallback
            except json.JSONDecodeError:
                # HTML response — cannot parse as JSON from this environment
                raise Exception("HTML response, not JSON")
    except Exception:
        # Barrier documented: fall through to fallback corpus
        return fallback


# ---------------------------------------------------------------------------
# Gate module (G1-G4, adapted from E148/E161 proposal)
# ---------------------------------------------------------------------------


def compute_gates(classified, active, total_classified, min_classified=50):
    """Compute G1-G4 gate results given classification and activity data.

    G1: need-related active rate >= 55% of random active rate
    G2: total classified >= 100
    G3: both categories represented (need-related > 0 and random > 0)
    G4: total classified >= 50
    """
    g1_pass = False
    g2_pass = False
    g3_pass = False
    g4_pass = False
    need_rate = 0.0
    random_rate = 0.0
    ratio = 0.0

    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55

    g2_pass = total_classified >= 100
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    g4_pass = total_classified >= min_classified

    return {
        "g1_pass": g1_pass,
