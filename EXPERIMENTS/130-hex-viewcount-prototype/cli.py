#!/usr/bin/env python3
"""E130 — Hex.pm View-Count Prototype CLI.

Command-line interface for fetching Hex.pm packages, classifying them
using the view-count principle's NEED_INDICATORS/GENERIC_TERMS framework,
and evaluating gates G1–G4.
"""

import argparse
import json
import math
import sys
import time
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional


# --- Classification framework from E103 ---

NEED_INDICATORS = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "database", "orm", "sql", "postgres", "mysql", "redis", "mongo",
    "json", "xml", "yaml", "parser", "serializer", "encoder", "decoder",
    "auth", "oauth", "jwt", "session", "cookie", "security",
    "cache", "queue", "worker", "job", "background", "async",
    "test", "mock", "fixture", "benchmark", "profile",
    "config", "settings", "env", "environment", "secret",
    "logger", "logging", "telemetry", "metrics", "tracing",
    "email", "mail", "smtp", "notification", "push",
    "file", "storage", "upload", "download", "archive",
    "image", "video", "audio", "media", "thumbnail",
    "search", "index", "elasticsearch", "fulltext",
    "graphql", "grpc", "websocket", "realtime", "pubsub",
    "crypto", "hash", "encrypt", "decrypt", "sign", "verify",
    "validate", "validator", "schema", "contract",
    "template", "render", "view", "html", "css", "asset",
    "router", "routing", "dispatch", "handler", "middleware",
    "dependency", "injection", "container", "provider",
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "pubsub", "broadcast", "channel", "presence",
    "ecto", "phoenix", "plug", "absinthe", "tesla", "finch",
    "httpoison", "jason", "poison", "comeonin", "bcrypt",
    "guardian", "ueberauth", "pow", "coherence",
    "exq", "oban", "quantum", "cron", "scheduler",
    "broadway", "genstage", "flow", "stream",
    "nimble", "csv", "excel", "pdf", "docx",
    "timex", "calendar", "tzdata", "chrono",
    "decimal", "money", "currency", "exchange",
    "uuid", "ulid", "nanoid", "slug", "parameterize"
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental"
}


def classify_need(desc: str) -> str:
    """Classify package description as need-related or random."""
    if not desc:
        return "random"
    desc_lower = desc.lower()

    # Generic terms -> random (take priority)
    for term in GENERIC_TERMS:
        if term in desc_lower:
            return "random"

    # Need indicators -> need-related
    for term in NEED_INDICATORS:
        if term in desc_lower:
            return "need-related"

    return "random"


# --- Hex.pm API helpers ---

HEADERS = {"User-Agent": "E130-prototype/1.0"}


def fetch_url(url: str) -> Optional[Dict[str, Any]]:
    """Fetch JSON from URL with error handling."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
        return None


def search_packages(query: str, max_packages: int = 100) -> List[Dict[str, Any]]:
    """Fetch packages from Hex.pm search API, classified as need-related or random."""
    packages = []
    seen = set()

    quoted = urllib.parse.quote(query)
    url = f"https://hex.pm/api/packages?search={quoted}&sort=downloads&page=1"
    data = fetch_url(url)
    if not data:
        return packages

    for pkg in data:
        if len(packages) >= max_packages:
            break
        name = pkg.get("name")
        if not name or name in seen:
            continue
        seen.add(name)

        desc = pkg.get("meta", {}).get("description", "")
        classification = classify_need(desc)
        if classification == "random":
            continue  # only classify need-related in search mode for efficiency

        downloads = pkg.get("downloads", {})
        packages.append({
            "name": name,
            "description": desc,
            "downloads_all": downloads.get("all", 0),
            "downloads_day": downloads.get("day", 0),
            "downloads_recent": downloads.get("recent", 0),
            "downloads_week": downloads.get("week", 0),
            "classification": "need-related",
            "source_query": query,
        })

    return packages


def random_packages(max_packages: int = 100) -> List[Dict[str, Any]]:
    """Fetch random packages from Hex.pm default listing, classified as need-related or random."""
    packages = []
    seen = set()
    page = 1

    while len(packages) < max_packages and page <= 50:
        url = f"https://hex.pm/api/packages?page={page}"
        data = fetch_url(url)
        if not data:
            break

        for pkg in data:
            if len(packages) >= max_packages:
                break
            name = pkg.get("name")
            if not name or name in seen:
                continue
            seen.add(name)

            desc = pkg.get("meta", {}).get("description", "")
            classification = classify_need(desc)

            downloads = pkg.get("downloads", {})
            packages.append({
                "name": name,
                "description": desc,
                "downloads_all": downloads.get("all", 0),
                "downloads_day": downloads.get("day", 0),
                "downloads_recent": downloads.get("recent", 0),
                "downloads_week": downloads.get("week", 0),
                "classification": classification,
                "source_query": f"random_page_{page}",
            })
        page += 1
        time.sleep(0.2)  # Be polite to the API

    return packages


# --- Statistical gates (from E103 analyze.py) ---

def mann_whitney_u(need_vals: List[int], random_vals: List[int]) -> tuple:
    """Mann-Whitney U test. Returns (U, p_value, cliff_delta)."""
    combined = [(v, "need") for v in need_vals] + [(v, "random") for v in random_vals]
    combined.sort(key=lambda x: x[0])

    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    n1 = len(need_vals)
    n2 = len(random_vals)
    r1 = sum(ranks[i] for i in range(n1))

    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if std_u == 0:
        return u, 1.0, 0.0
    z = (u - mean_u) / std_u

    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))

    greater = sum(1 for nv in need_vals for rv in random_vals if nv > rv)
    less = sum(1 for nv in need_vals for rv in random_vals if nv < rv)
    cliff_delta = (greater - less) / (n1 * n2) if n1 * n2 > 0 else 0.0

    return u, p, cliff_delta


def wilson_ci95_lower(x: int, n: int) -> float:
    """Wilson CI95 lower bound for proportion x/n."""
    if n == 0:
        return 0.0
    z = 1.96
    phat = x / n
    denominator = 1 + z**2 / n
    centre = phat + z**2 / (2 * n)
    margin = z * math.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    return max(0, (centre - margin) / denominator)


def evaluate_gates(packages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate G1–G4 gates on classified packages."""
    need_pkgs = [p for p in packages if p["classification"] == "need-related"]
    random_pkgs = [p for p in packages if p["classification"] == "random"]

    need_active = sum(1 for p in need_pkgs if p.get("downloads_recent", 0) > 0)
    random_active = sum(1 for p in random_pkgs if p.get("downloads_recent", 0) > 0)
    need_total = len(need_pkgs)
    random_total = len(random_pkgs)
    classified_total = need_total + random_total

    # G1: classified sample size >= 100
    g1_pass = classified_total >= 100

    # G2: Mann-Whitney U test p < 0.05, Cliff's delta > 0.147
    need_downloads = [p["downloads_recent"] for p in need_pkgs]
    random_downloads = [p["downloads_recent"] for p in random_pkgs]
    if need_downloads and random_downloads:
        u_stat, p_val, cliff_delta = mann_whitney_u(need_downloads, random_downloads)
    else:
        u_stat, p_val, cliff_delta = 0.0, 1.0, 0.0
    g2_pass = (p_val < 0.05) and (cliff_delta > 0.147)

    # G3: Wilson CI95 lower bound for proportion of need-related above random median > 0.60
    if random_downloads:
        random_median = sorted(random_downloads)[len(random_downloads) // 2]
    else:
        random_median = 0
    need_above_median = sum(1 for v in need_downloads if v > random_median)
    wilson_lb = wilson_ci95_lower(need_above_median, need_total)
    g3_pass = wilson_lb > 0.60

    # G4: both categories represented
    g4_pass = need_total > 0 and random_total > 0

    return {
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "all_pass": g1_pass and g2_pass and g3_pass and g4_pass,
        "statistics": {
            "classified_total": classified_total,
            "need_total": need_total,
            "random_total": random_total,
            "need_active": need_active,
            "random_active": random_active,
            "need_rate": need_active / need_total if need_total > 0 else 0,
            "random_rate": random_active / random_total if random_total > 0 else 0,
            "u_statistic": u_stat,
            "p_value": p_val,
            "cliff_delta": cliff_delta,
            "random_median": random_median,
            "need_above_median": need_above_median,
            "wilson_lb": wilson_lb,
        }
    }


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="E130 Hex.pm View-Count Prototype: classify packages and evaluate gates"
    )
    parser.add_argument(
        "--mode",
        choices=["search", "random"],
        required=True,
        help="Fetch mode: 'search' for keyword search, 'random' for default listing",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Search query (required in search mode)",
    )
    parser.add_argument(
        "--max-packages",
        type=int,
        default=100,
        help="Maximum number of packages to fetch (default: 100)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Write results JSON to file (optional)",
    )

    args = parser.parse_args()

    # Input validation
    if args.mode == "search" and not args.query:
        print("ERROR: --query is required in search mode", file=sys.stderr)
        sys.exit(1)

    # Fetch packages
    if args.mode == "search":
        packages = search_packages(args.query, args.max_packages)
    else:
        packages = random_packages(args.max_packages)

    # Classify packages (already classified during fetch, but ensure classification is set)
    for pkg in packages:
        if "classification" not in pkg:
            desc = pkg.get("description", "")
            pkg["classification"] = classify_need(desc)

    # Evaluate gates
    results = evaluate_gates(packages)

    # Print results
    stats = results["statistics"]
    print(f"=== E130 Hex.pm View-Count Prototype ===\n")
    print(f"Mode: {args.mode}")
    if args.mode == "search":
        print(f"Query: {args.query}")
    print(f"Max packages: {len(packages)}")
    print(f"\n--- Classification ---")
    print(f"  Need-related: {stats['need_total']}")
    print(f"  Random: {stats['random_total']}")
    print(f"  Total classified: {stats['classified_total']}")

    print(f"\n--- Activity (recent downloads > 0) ---")
    print(f"  Need-related active: {stats['need_active']}/{stats['need_total']} = {stats['need_rate']:.1%}")
    print(f"  Random active: {stats['random_active']}/{stats['random_total']} = {stats['random_rate']:.1%}")

    print(f"\n--- Gates ---")
    print(f"  G1 (sample >= 100): {'PASS' if results['g1_pass'] else 'FAIL'} ({stats['classified_total']})")
    print(f"  G2 (MWU p<0.05, delta>0.147): {'PASS' if results['g2_pass'] else 'FAIL'} (p={stats['p_value']:.6f}, delta={stats['cliff_delta']:.4f})")
    print(f"  G3 (Wilson LB > 0.60): {'PASS' if results['g3_pass'] else 'FAIL'} (LB={stats['wilson_lb']:.4f}, need_above_median={stats['need_above_median']}/{stats['need_total']}, random_median={stats['random_median']})")
    print(f"  G4 (both categories): {'PASS' if results['g4_pass'] else 'FAIL'}")

    print(f"\n--- Overall: {'ALL GATES PASS' if results['all_pass'] else 'SOME GATES FAILED'} ---")

    # Save results if output path specified
    if args.output:
        output = {
            "experiment": "E130",
            "platform": "Hex.pm",
            "mode": args.mode,
            "query": args.query if args.mode == "search" else None,
            "max_packages": len(packages),
            "gates": results,
            "conclusion": "view-count principle supported on Hex.pm" if results["all_pass"] else "view-count principle not supported on Hex.pm",
        }
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()