#!/usr/bin/env python3
"""
E072 — view-count prototype on NPM: classify need statements.

Prototype that applies the view-count principle using NPM JSON API metadata:
  For each need statement, query NPM and compute an activity score.
  Classify the need as 'served' if the package has sufficient activity metadata
  (indicating independent arrivals at the need), 'unserved' otherwise.

This is an evidence-gathering prototype, not product validation. It tests whether
the view-count principle (shown conclusive in E071 on PyPI) can classify needs
in practice on NPM.

Rubric (adapted from E071/E072):
  - active: activity_score >= 6  (homepage + repository + keywords + version presence)
  - inactive: 0 < activity_score < 6
  - missing: activity_score <= 0

Usage:
    python3 view_count_prototype.py need-statements.jsonl
"""
import json
import sys
import urllib.request

HERE = "/home/ubuntu/think-free/EXPERIMENTS/072-npm-view-count-prototype"


def compute_activity_score(info):
    """Compute activity score from NPM JSON API metadata.

    The NPM API response is flat — fields are at the top level, not nested
    under "info" as in PyPI.
    """
    if "error" in info:
        return -1  # missing

    score = 0
    # 1. Package existence / version presence (1 point)
    # Check dist-tags for latest tag presence
    dist_tags = info.get("dist-tags")
    if dist_tags and isinstance(dist_tags, dict) and "latest" in dist_tags:
        score += 1
    # 2. Has Homepage URL (5 points)
    if info.get("homepage"):
        score += 5
    # 3. Has Repository URL (2 points)
    pu = info.get("repository")
    if pu and isinstance(pu, dict) and pu.get("url"):
        score += 2
    # 4. Has Keywords (1 point)
    kw = info.get("keywords")
    if kw and isinstance(kw, list) and len(kw) > 0:
        score += 1

    return score


def classify_activity(score):
    """Classify activity score into category."""
    if score >= 6:
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


def query_npm(package_name):
    """Query NPM JSON API for a package and return the info dict."""
    try:
        url = "https://registry.npmjs.org/" + package_name
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        return data
    except Exception:
        return {"error": "api_error", "name": package_name}


def classify_need(need_text):
    """Classify a need statement based on NPM metadata.

    Extracts potential package names from the need text and checks if
    any of them have sufficient activity metadata on NPM.
    """
    import re

    # Known important NPM packages from the E072 experiment
    important_packages = [
        "react", "lodash", "express", "angular", "vue", "webpack",
        "babel", "moment", "jquery", "node-fetch", "nodemon",
        "pm2", "sequelize", "mongoose", "dotenv", "passport",
        "jsonwebtoken", "bcryptjs", "swagger-ui",
    ]

    # Extract words from the need text
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9]*", need_text.lower())

    # Check important packages first
    for pkg in important_packages:
        if pkg in words:
            info = query_npm(pkg)
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
        if word_lower in {"react", "lodash", "express", "angular", "vue", "webpack",
                          "babel", "moment", "jquery", "node-fetch", "nodemon",
                          "pm2", "sequelize", "mongoose", "dotenv", "passport",
                          "jsonwebtoken", "bcryptjs", "swagger-ui",
                          "npm", "node", "javascript", "typescript"}:
            info = query_npm(word_lower)
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

    print("E072 View-count Prototype on NPM")
    print("=" * 60)
    print("Classifying need statements based on NPM activity metadata")
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
    active_pct = active_count / len(results) * 100 if len(results) > 0 else 0
    inactive_pct = inactive_count / len(results) * 100 if len(results) > 0 else 0
    missing_pct = missing_count / len(results) * 100 if len(results) > 0 else 0
    print("  Active (package found with sufficient metadata): %d (%.1f%%)" % (active_count, active_pct))
    print("  Inactive (package found but low activity): %d (%.1f%%)" % (inactive_count, inactive_pct))
    print("  Missing (no package found on NPM): %d (%.1f%%)" % (missing_count, missing_pct))

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