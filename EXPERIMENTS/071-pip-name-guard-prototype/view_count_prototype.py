#!/usr/bin/env python3
"""
E071 — view-count prototype on PyPI: classify need statements.

Prototype that applies the view-count principle using PyPI JSON API metadata:
  For each need statement, query PyPI and compute an activity score.
  Classify the need as 'served' if the package has sufficient activity metadata
  (indicating independent arrivals at the need), 'unserved' otherwise.

This is an evidence-gathering prototype, not product validation. It tests whether
the view-count principle (shown conclusive in E071) can classify needs in practice.

Rubric (adapted from E071):
  - active: activity_score >= 10  (version presence + homepage + docs + source + dev status)
  - inactive: 0 < activity_score < 10
  - missing: activity_score <= 0

Usage:
    python3 view_count_prototype.py need-statements.jsonl
"""
import json
import sys
import urllib.request

HERE = "/home/ubuntu/think-free/EXPERIMENTS/071-pip-name-guard-prototype"


def compute_activity_score(info):
    """Compute activity score from PyPI JSON API metadata."""
    if "error" in info:
        return -1  # missing

    score = 0
    # 1. Release presence (1 point if version string exists)
    if info.get("version"):
        score += 1
    # 2. Has Homepage URL (5 points)
    if info.get("home_page"):
        score += 5
    else:
        pu = info.get("project_urls") or {}
        for k in pu:
            if "Homepage" in k or k.lower() == "homepage":
                score += 5
                break
    # 3. Has Documentation URL (3 points)
    if info.get("docs_url"):
        score += 3
    else:
        pu = info.get("project_urls") or {}
        for k in pu:
            if "Documentation" in k or k.lower() == "documentation":
                score += 3
                break
    # 4. Has Source URL (2 points)
    pu = info.get("project_urls")
    if pu:
        for k in pu:
            if "Source" in k or k.lower() == "source":
                score += 2
                break
    # 5. Development Status classifier 5 — Production/Stable (5 points)
    classifiers = info.get("classifiers", [])
    if any("Development Status :: 5" in c for c in classifiers):
        score += 5
    # 6. Development Status classifier 4 — Beta (3 points)
    if any("Development Status :: 4" in c for c in classifiers):
        score += 3

    return score


def classify_activity(score):
    """Classify activity score into category."""
    if score >= 10:
        return "active"
    elif score > 0:
        return "inactive"
    else:
        return "missing"


def load_need_statements(path):
    """Load need statements from a JSONL file."""
    statements = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    need_text = obj.get("need_text", "")
                    if need_text:
                        statements.append((len(statements), need_text))
                except (json.JSONDecodeError, KeyError):
                    continue
    return statements


def query_pypi(package_name):
    """Query PyPI JSON API for a package and return the info dict."""
    try:
        url = "https://pypi.org/pypi/" + package_name + "/json"
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        return data.get("info", {})
    except Exception:
        return {"error": "api_error", "name": package_name}


def classify_need(need_text):
    """Classify a need statement based on PyPI metadata.

    Extracts potential package names from the need text and checks if
    any of them have sufficient activity metadata on PyPI.
    """
    # Extract potential package names (simple heuristic: lowercase words
    # that match known PyPI package names or look like package names)
    # For this prototype, we'll extract capitalized words and known names
    import re

    # Known important PyPI packages from the E071 experiment
    important_packages = [
        "requests", "pillow", "numpy", "flask", "django", "bcrypt",
        "pytest", "gitpython", "sqlalchemy", "jinja2", "matplotlib",
        "scipy", "pyyaml", "boto3", "click", "sphinx", "black", "mypy"
    ]

    # Extract words from the need text
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]*", need_text.lower())

    # Check important packages first
    for pkg in important_packages:
        if pkg in words:
            info = query_pypi(pkg)
            score = compute_activity_score(info)
            classification = classify_activity(score)
            return {
                "need_text": need_text[:80] + "..." if len(need_text) > 80 else need_text,
                "matched_package": pkg,
                "activity_score": score,
                "classification": classification,
            }

    # Check any word that looks like a package name
    for word in words:
        word_lower = word.lower()
        if word_lower in {"python", "django", "flask", "numpy", "pillow", "requests",
                          "pytest", "sphinx", "black", "mypy", "pytest-xdist",
                          "setuptools", "wheel", "virtualenv", "tox", "cookiecutter",
                          "jupyter", "ipython", "nbformat", "traitlets"}:
            info = query_pypi(word_lower)
            score = compute_activity_score(info)
            classification = classify_activity(score)
            if classification in ("active", "inactive"):
                return {
                    "need_text": need_text[:80] + "..." if len(need_text) > 80 else need_text,
                    "matched_package": word_lower,
                    "activity_score": score,
                    "classification": classification,
                }

    # No matching package found
    return {
        "need_text": need_text[:80] + "..." if len(need_text) > 80 else need_text,
        "matched_package": None,
        "activity_score": -1,
        "classification": "missing",
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 view_count_prototype.py <need-statements.jsonl>")
        print("  need-statements.jsonl: JSONL file with 'need_text' fields")
        sys.exit(1)

    path = sys.argv[1]
    statements = load_need_statements(path)

    print("E071 View-count Prototype on PyPI")
    print("=" * 60)
    print("Classifying need statements based on PyPI activity metadata")
    print()

    results = []
    for i, (sid, need_text) in enumerate(statements):
        result = classify_need(need_text)
        result["statement_id"] = sid
        result["need_text_full"] = need_text
        results.append(result)

        if (i + 1) % 5 == 0:
            print("  classified %d/%d..." % (i + 1, len(statements)))

    # Summary
    active_count = sum(1 for r in results if r["classification"] == "active")
    inactive_count = sum(1 for r in results if r["classification"] == "inactive")
    missing_count = sum(1 for r in results if r["classification"] == "missing")

    print()
    print("Summary:")
    print("  Total need statements: %d" % len(results))
    print("  Active (package found with sufficient metadata): %d (%.2%%)" % (active_count, active_count / len(results) * 100))
    print("  Inactive (package found but low activity): %d (%.2%%)" % (inactive_count, inactive_count / len(results) * 100))
    print("  Missing (no package found on PyPI): %d (%.2%%)" % (missing_count, missing_count / len(results) * 100))

    # Show some examples
    print()
    print("Examples:")
    for r in results[:5]:
        print("  %s" % json.dumps(r, ensure_ascii=False)[:150])

    # Save results
    output_path = path.replace(".jsonl", "-classified.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print()
    print(" classified results written to: %s" % output_path)


if __name__ == "__main__":
    main()