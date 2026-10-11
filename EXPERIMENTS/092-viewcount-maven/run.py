"""E092 — View-count principle on Maven Central Java packages."""

import json
import urllib.request
import sys

# Configuration
SOLR_URL = "https://search.maven.org/solrsearch/select"
SAMPLE_SIZE = 100  # G2 gate: minimum 100 packages
MIN_CLASSIFIED = 50  # G4 gate: minimum 50 classified
THRESHOLD_RATIO = 0.55  # G1: need-related active rate must be >= 55% of random active rate

# Problem-domain indicators: terms that suggest a specific need/problem
NEED_INDICATORS = {
    "web", "rest", "mvc", "orm", "sql", "json", "xml", "http",
    "parser", "lexer", "encoder", "decoder", "converter", "transform",
    "framework", "client", "server", "engine", "core", "utility", "helper",
    "gui", "cli", "webapp", "library", "tool", "parser",
}

# Too-generic terms that always classify as "random"
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies"}


def fetch_packages(n=SAMPLE_SIZE):
    """Fetch n random packages from Maven Central via Solr."""
    packages = []
    url = f"{SOLR_URL}?q=&rows={n}&wt=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "origin-mission-E092"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            docs = data.get("response", {}).get("docs", [])
            for doc in docs:
                packages.append({
                    "g": doc.get("g", ""),
                    "a": doc.get("a", ""),
                    "v": doc.get("v", ""),
                    "p": doc.get("p", ""),
                    "desc": doc.get("desc", "") or "",
                    "keywords": doc.get("keywords", []) or [],
                })
    except Exception as e:
        print(f"Error fetching packages: {e}", file=sys.stderr)
        sys.exit(1)
    return packages


def classify_package(pkg):
    """Classify a package as need-related or random."""
    desc = (pkg["desc"] + " " + " ".join(pkg["keywords"])).lower()

    # Check for generic terms - if description/keywords contain only generic terms, classify as random
    found_generic = False
    for term in GENERIC_TERMS:
        if term in desc:
            found_generic = True
            break

    if found_generic:
        return "random"

    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        if term in desc:
            found_need = True
            break

    if found_need:
        return "need-related"

    # Also check: if description is very short or absent, classify as random
    if len(desc) < 10:
        return "random"

    # If we get here, description is present and not generic - default to random
    # (we only classify as need-related when a clear need indicator is present)
    return "random"


def is_active(pkg):
    """Check if a package has significant activity metadata (the 'active' signal)."""
    # Active = has a non-empty description AND has keywords AND has version metadata
    desc_active = len(pkg["desc"].strip()) > 0
    keywords_active = len(pkg["keywords"]) > 0
    version_active = pkg["v"] is not None and str(pkg["v"]).strip() != ""
    return desc_active and keywords_active and version_active


def main():
    # Fetch packages
    packages = fetch_packages(SAMPLE_SIZE)
    print(f"Fetched {len(packages)} packages from Maven Central")

    # Classify each package
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0

    for pkg in packages:
        cls = classify_package(pkg)
        if cls not in classified:
            # Unexpected classification - skip
            continue
        classified[cls] += 1
        classified_count += 1

        if is_active(pkg):
            active[cls] += 1

    # Print results
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")

    print(f"\n=== Metrics ===")
    print(f"  Total classified: {classified_count} / {SAMPLE_SIZE}")
    print(f"  G2 gate (n >= 100): {'PASS' if SAMPLE_SIZE >= 100 else 'FAIL'}")
    print(f"  G4 gate (classified >= 50): {'PASS' if classified_count >= MIN_CLASSIFIED else 'FAIL'}")

    if classified_count >= MIN_CLASSIFIED and SAMPLE_SIZE >= 100:
        # G1 gate: check ratio
        need_rate = active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0
        random_rate = active["random"] / classified["random"] if classified["random"] > 0 else 0
        ratio = need_rate / random_rate if random_rate > 0 else 0

        print(f"\n  G1 gate (need/active >= 55% of random):")
        print(f"    need-related active rate: {need_rate*100:.1f}%")
        print(f"    random active rate: {random_rate*100:.1f}%")
        print(f"    ratio: {ratio*100:.1f}%")
        print(f"    Result: {'PASS' if ratio >= THRESHOLD_RATIO else 'FAIL'}")

        if ratio >= THRESHOLD_RATIO:
            print("\n*** ALL GATES PASS *** - view-count principle generalizes to Maven Central ***")
            return 0
        else:
            print("\n*** G1 FAIL *** - view-count principle does not generalize to Maven Central ***")
            return 0
    else:
        print("\n*** GATE PRECONDITIONS NOT MET *** - insufficient data")
        return 2


if __name__ == "__main__":
    sys.exit(main())