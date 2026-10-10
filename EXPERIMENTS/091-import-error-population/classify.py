#!/usr/bin/env python3
"""
E091 — Classify harvested import-error reports.
Determines which reports name a module but no distribution.
"""

import json
import re
from pathlib import Path

from constants import MODULE_TO_DIST, STDLIB_COMMON

HERE = Path(__file__).parent
RAW = HERE / "raw" / "api"


def extract_error_module(text):
    """
    Extract the module name from ImportError/ModuleNotFoundError messages.
    Priority order:
    1. "No module named 'X'" pattern (most specific)
    2. "cannot import name 'X' from 'Y'" pattern
    3. First import statement in traceback
    """
    # Pattern 1: No module named 'X'
    match = re.search(r"No module named\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    if match:
        mod = match.group(1).split(".")[0]
        if mod and not mod[0].isdigit():
            return mod.lower()

    # Pattern 2: cannot import name 'X' from 'Y'
    match = re.search(
        r"cannot import name\s+['\"]([^'\"]+)['\"]\s+from\s+['\"]([^'\"]+)['\"]",
        text, re.IGNORECASE
    )
    if match:
        mod = match.group(2).split(".")[0]
        if mod and not mod[0].isdigit():
            return mod.lower()

    # Pattern 3: ImportError: cannot import name 'X'
    match = re.search(r"cannot import name\s+['\"]([^'\"]+)['\"]", text, re.IGNORECASE)
    if match:
        mod = match.group(1).split(".")[0]
        if mod and not mod[0].isdigit():
            return mod.lower()

    return None


def extract_distributions(text):
    """Extract distribution names mentioned in pip install commands."""
    dists = set()
    patterns = [
        r"pip install\s+([a-zA-Z0-9_.-]+)",
        r"pip3 install\s+([a-zA-Z0-9_.-]+)",
        r"python -m pip install\s+([a-zA-Z0-9_.-]+)",
        r"conda install\s+([a-zA-Z0-9_.-]+)",
        r"poetry add\s+([a-zA-Z0-9_.-]+)",
        r"pipx install\s+([a-zA-Z0-9_.-]+)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            dists.add(match.lower())
    return dists


def is_help_seeking(text):
    """Heuristic: is the text asking a question seeking help (not just reporting a bug)?"""
    text_lower = text.lower()
    # Must have question indicators
    question_indicators = [
        "how do i", "how to", "what package", "what to install",
        "which package", "how can i", "help", "please",
        "?", "solve", "fix", "resolve", "install",
    ]
    if not any(ind in text_lower for ind in question_indicators):
        return False

    # Exclude bug reports in project's own issue tracker
    bug_indicators = [
        "bug report", "issue", "regression", "broken in",
        "fails on", "crash", "traceback", "expected behavior",
        "actual behavior", "steps to reproduce", "version:",
        "environment:", "os:", "python version:",
    ]
    if any(ind in text_lower for ind in bug_indicators):
        return False

    return True


def classify_item(title, body, venue):
    """Classify a single report."""
    full_text = f"{title}\n{body}"
    full_text_lower = full_text.lower()

    # Must be about import error
    if "importerror" not in full_text_lower and "modulenotfounderror" not in full_text_lower:
        return "not_import_error", "No ImportError/ModuleNotFoundError mentioned"

    # Extract the module from the error message (highest priority)
    error_module = extract_error_module(full_text)

    if not error_module:
        return "other", "Import error but no module name extracted from error message"

    # Skip stdlib modules
    if error_module in STDLIB_COMMON:
        return "stdlib_module", f"Error module '{error_module}' is in standard library"

    # Extract distributions mentioned in pip/conda install commands
    dists = extract_distributions(full_text)

    # Also check for explicit module->dist mentions in text
    for mod, dist in MODULE_TO_DIST.items():
        if mod.lower() in full_text_lower and dist.lower() in full_text_lower:
            dists.add(dist.lower())

    # Expected distribution for the error module
    expected_dist = MODULE_TO_DIST.get(error_module, error_module)

    # Check if expected distribution is mentioned
    if expected_dist in dists:
        return "names_both", f"Names module '{error_module}' and its distribution '{expected_dist}'"

    # Check if any distribution is mentioned (but not the right one)
    if dists:
        return "names_wrong_dist", f"Names module '{error_module}' but mentions other distribution(s): {', '.join(dists)}"

    # Check if it's a help-seeking question
    if is_help_seeking(full_text):
        return "names_module_no_dist", f"Names module '{error_module}' (needs '{expected_dist}') but no distribution mentioned"

    return "names_module_no_dist_not_question", f"Names module '{error_module}' but not a help-seeking question"


def main():
    manifest_path = RAW / "manifest.json"
    if not manifest_path.exists():
        print("Manifest not found. Run harvest.py first.")
        return 1

    with open(manifest_path) as f:
        manifest = json.load(f)

    classified = []
    total = 0
    module_no_dist = 0

    for entry in manifest:
        path = RAW / entry["file"]
        if not path.exists():
            continue
        with open(path) as f:
            data = json.load(f)

        items = data.get("items", [])
        for item in items:
            title = item.get("title", "")
            body = item.get("body", item.get("body_text", ""))
            url = item.get("link", item.get("html_url", ""))

            category, rationale = classify_item(title, body, entry["venue"])

            result = {
                "venue": entry["venue"],
                "query_class": entry.get("class", ""),
                "title": title[:200],
                "url": url,
                "category": category,
                "rationale": rationale,
            }
            classified.append(result)

            total += 1
            if category == "names_module_no_dist":
                module_no_dist += 1

    # Write classified results
    out_path = HERE / "classified.jsonl"
    with open(out_path, "w") as f:
        for item in classified:
            f.write(json.dumps(item) + "\n")

    # Summary
    rate = module_no_dist / total if total > 0 else 0
    print(f"\n=== Classification Summary ===")
    print(f"Total reports: {total}")
    print(f"Module-no-dist (help-seeking): {module_no_dist}")
    print(f"Rate: {rate:.2%}")

    # Category breakdown
    cats = {}
    for item in classified:
        cat = item["category"]
        cats[cat] = cats.get(cat, 0) + 1
    print(f"\nCategory breakdown:")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count} ({count/total:.2%})")

    # Save summary for gate evaluation
    summary = {
        "total_sampled": total,
        "module_no_dist_count": module_no_dist,
        "module_no_dist_rate": rate,
        "categories": cats,
        "classified_file": str(out_path),
    }
    with open(HERE / "results.json", "w") as f:
        json.dump(summary, f, indent=2)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())