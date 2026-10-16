#!/usr/bin/env python3
"""
Classify Go packages as need-related or general based on pre-declared keyword rules.
"""

import json
import re
from pathlib import Path


# Pre-declared need-related keywords (derivatives, wrappers, adapters, etc.)
NEED_KEYWORDS = [
    # Wrapper/binding/adapter patterns
    r"\bwrapper\b", r"\bwrap\b", r"\bbinding\b", r"\bbind\b",
    r"\badapter\b", r"\badaptor\b", r"\bbridge\b",

    # Client/SDK/API patterns (as derivative indicators)
    r"\bclient\b", r"\bsdk\b", r"\bapi\b",

    # Middleware/plugin/extension patterns
    r"\bmiddleware\b", r"\bplugin\b", r"\bextension\b", r"\bext\b",

    # Driver/dialect patterns
    r"\bdriver\b", r"\bdialect\b",

    # Framework/derivative patterns
    r"\bframework\b", r"\bfw\b",

    # Implementation/fork/port patterns (when not primary)
    r"\bimplementation\b", r"\bimpl\b",
    r"\bfork\b", r"\bport\b", r"\bmirror\b",

    # Major version paths suggesting derivatives (v2, v3 in path)
    r"/v[2-9]\b", r"/v[1-9]\d+\b",
]

# Pre-declared general/original keywords (primary frameworks, stdlib)
GENERAL_KEYWORDS = [
    # Primary web frameworks (original, not derivatives)
    r"\bgin\b", r"\becho\b", r"\bfiber\b", r"\bbeego\b",
    r"\biris\b", r"\brevel\b", r"\bchi\b", r"\bgorilla\b",
    r"\bhttprouter\b", r"\bmux\b", r"\bnegroni\b", r"\balice\b",

    # Core/standard library indicators
    r"\bstdlib\b", r"\bstandard\b", r"\bbuiltin\b", r"\bcore\b",
    r"^golang\.org/", r"^google\.golang\.org/",
    r"^github\.com/golang/", r"^golang\.org/x/",

    # Primary database drivers (original)
    r"^github\.com/go-sql-driver/", r"^github\.com/lib/pq\b",
    r"^github\.com/mattn/go-sqlite3\b", r"^github\.com/jackc/pgx\b",

    # Primary cloud SDKs (original)
    r"^github\.com/aws/aws-sdk-go\b", r"^cloud\.google\.com/go/",
    r"^github\.com/azure/azure-sdk-for-go\b",
]


def compile_patterns(keywords):
    """Compile regex patterns with case-insensitive flag."""
    return [re.compile(kw, re.IGNORECASE) for kw in keywords]


NEED_PATTERNS = compile_patterns(NEED_KEYWORDS)
GENERAL_PATTERNS = compile_patterns(GENERAL_KEYWORDS)


def classify_package(path, synopsis):
    # type: (str, str) -> str
    """
    Classify a package as 'need-related', 'general', or 'unclassified'.
    Rules:
    1. If any need-related keyword matches path OR synopsis -> need-related
    2. Else if any general keyword matches path OR synopsis -> general
    3. Else -> unclassified
    """
    text = f"{path} {synopsis}".lower()

    # Check need-related first
    for pattern in NEED_PATTERNS:
        if pattern.search(text):
            return "need-related"

    # Check general
    for pattern in GENERAL_PATTERNS:
        if pattern.search(text):
            return "general"

    return "unclassified"


def classify_all(input_file="raw_harvest.json", output_file="classified.json"):
    # type: (str, str) -> list
    """Classify all harvested packages."""
    with open(input_file) as f:
        packages = json.load(f)

    results = []
    counts = {"need-related": 0, "general": 0, "unclassified": 0}

    for p in packages:
        classification = classify_package(p["path"], p["synopsis"])
        p["classification"] = classification
        counts[classification] += 1
        results.append(p)

    print(f"Classification results:")
    print(f"  Need-related: {counts['need-related']}")
    print(f"  General: {counts['general']}")
    print(f"  Unclassified: {counts['unclassified']}")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    return results


def main():
    classify_all()


if __name__ == "__main__":
    main()