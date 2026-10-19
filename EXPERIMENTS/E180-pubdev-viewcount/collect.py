"""E180 — Collect data from Pub.dev for view-count principle experiment."""

import urllib.request, json, time, os, re, sys
from collections import Counter

# Classification vocabulary (mirrors viewcount_core.py)
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
    "crud", "rest", "sdk", "cli",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets",
}


def _matches_word_boundary(desc_lower, term):
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_description(desc):
    if not desc:
        return "random"
    desc_lower = desc.lower()
    for term in GENERIC_TERMS:
        if _matches_word_boundary(desc_lower, term):
            return "random"
    for term in NEED_INDICATORS:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"
    return "random"


def is_active(pkg):
    """Check if package has activity metadata: non-empty description AND version present."""
    desc = pkg.get('latest', {}).get('pubspec', {}).get('description', '') or ''
    version = pkg.get('latest', {}).get('version', '') or ''
    desc_active = len(desc.strip()) > 0
    version_active = version != '' and version is not None
    return desc_active and version_active


def fetch_pubdev_packages(limit=200):
    """Fetch packages from Pub.dev API."""
    packages = []
    try:
        url = f'https://pub.dev/api/packages?limit={limit}'
        req = urllib.request.Request(url, headers={"User-Agent": "origin-viewcount/3.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            packages = data.get('packages', [])
    except Exception as e:
        print(f"Error fetching Pub.dev packages: {e}", file=sys.stderr)
    return packages


def fetch_pubdev_search(keyword, limit=20):
    """Fetch packages from Pub.dev search API with a keyword."""
    packages = []
    try:
        encoded = urllib.parse.urlencode({'search term': keyword, 'limit': str(limit)})
        url = f'https://pub.dev/api/search?{encoded}'
        req = urllib.request.Request(url, headers={"User-Agent": "origin-viewcount/3.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            # Search returns package names; need to fetch details
            for p in data.get('packages', []):
                name = p.get('package')
                if name:
                    try:
                        detail_url = f'https://pub.dev/api/packages/{name}'
                        detail_req = urllib.request.Request(detail_url, headers={"User-Agent": "origin-viewcount/3.0"})
                        with urllib.request.urlopen(detail_req, timeout=10) as dresp:
                            detail = json.loads(dresp.read())
                            packages.append(detail)
                    except Exception:
                        pass
    except Exception as e:
        print(f"Error fetching Pub.dev search for '{keyword}': {e}", file=sys.stderr)
    return packages


def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "database"
    print(f"=== E180: View-count principle on Pub.dev ===")
    print(f"Keyword: {keyword}")
    print()

    # Fetch need-related packages via search
    print(f"Fetching need-related packages via search keyword: '{keyword}'")
    need_packages = fetch_pubdev_search(keyword, limit=20)
    print(f"  Retrieved {len(need_packages)} need-related packages via search")

    # Fetch random packages from the default listing
    print(f"Fetching random packages from default listing (limit=200)")
    random_packages = fetch_pubdev_packages(limit=200)
    print(f"  Retrieved {len(random_packages)} packages from default listing")

    # Classify all packages
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_pkgs = []
    random_pkgs = []

    # Classify need-related search results
    for pkg in need_packages:
        cls = classify_description(pkg.get('latest', {}).get('pubspecc', {}).get('description', '') or '') if pkg.get('latest') else "random"
        # Actually fix: pubspecc -> pubspec
        latest = pkg.get('latest', {}) or {}
        pubspec = latest.get('pubspec', {}) or {}
        desc = pubspec.get('description', '') or ''
        cls = classify_description(desc)
        classified[cls] += 1
        if is_active(pkg):
            active[cls] += 1
        if cls == "need-related":
            need_related_pkgs.append(pkg)
        else:
            random_pkgs.append(pkg)

    # Classify random packages from default listing
    seen_names = set()
    for pkg in random_packages:
        name = pkg.get('name', '') or ''
        if name in seen_names:
            continue
        seen_names.add(name)
        desc = pkg.get('latest', {}).get('pubspec', {}).get('description', '') or ''
        cls = classify_description(desc)
        classified[cls] += 1
        if is_active(pkg):
            active[cls] += 1
        if cls == "need-related":
            need_related_pkgs.append(pkg)
        else:
            random_pkgs.append(pkg)

        if len(need_related_pkgs) + len(random_pkgs) >= 200:
            break

    # Print classification summary
    print(f"\n=== Classification ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")

    # G1 gate
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
        print(f"  SKIPPED: need at least one package in each category")

    # G2 gate
    g2_pass = (classified["need-related"] + classified["random"]) >= 100
    print(f"\n=== Gate G2 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G2 pass (>= 100): {'PASS' if g2_pass else 'FAIL'}")

    # G3 gate
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"\n=== Gate G3 ===")
    print(f"  G3 pass (both categories): {'PASS' if g3_pass else 'FAIL'}")

    # G4 gate
    g4_pass = (classified["need-related"] + classified["random"]) >= 50
    print(f"\n=== Gate G4 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G4 pass (>= 50): {'PASS' if g4_pass else 'FAIL'}")

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n=== Overall ===")
    print(f"  All gates pass: {'YES' if all_pass else 'NO'}")

    # Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Pub.dev",
        "keyword": keyword,
        "sample_size": classified["need-related"] + classified["random"],
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "all_pass": all_pass,
        "conclusion": "pending",
        "experiment_description": f"View-count principle on Pub.dev for keyword: {keyword}",
    }

    out_dir = "EXPERIMENTS/E180-pubdev-viewcount"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")

    # Print some need-related packages
    print(f"\n=== Need-related packages ({len(need_related_pkgs)}) ===")
    for i, pkg in enumerate(need_related_pkgs[:10]):
        name = pkg.get('name', 'N/A')
        version = pkg.get('latest', {}).get('version', 'N/A') if pkg.get('latest') else 'N/A'
        pubspec = pkg.get('latest', {}).get('pubspec', {}) if pkg.get('latest') else {}
        desc = pubspec.get('description', '')[:80] if pubspec.get('description') else ''
        print(f"  {i+1}. {name} {version} -- {desc}")

    return results


if __name__ == "__main__":
    main()