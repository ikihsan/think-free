#!/usr/bin/env python3
"""E108 — Collect Packagist package data for view-count principle test."""

import json
import time
import urllib.request
import urllib.parse
import random
from typing import Any, Dict, List, Optional, Set

# Need indicators and generic terms from PROTOCOL.md
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
    # PHP-specific terms
    "laravel", "symfony", "laminas", "zend", "slim", "lumen",
    "doctrine", "eloquent", "propel", "atlas",
    "guzzle", "httplug", "php-http", "buzz",
    "monolog", "psr/log", "psr/cache", "psr/container",
    "phpunit", "mockery", "phpspec", "behat",
    "twig", "blade", "latte", "smarty",
    "composer", "packagist", "satis",
    "flysystem", "league", "spatie",
    "carbon", "nesbot", "brick",
    "ramsey", "uuid", "ulid",
    "vlucas", "phpdotenv", "dotenv",
    "swiftmailer", "mailer", "sendmail",
    "fzaninotto", "faker", "factory",
    "sebastian", "code-coverage", "php-code-coverage",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "demo", "example", "sample", "test", "testing",
    "skeleton", "boilerplate", "starter", "template",
}

SEARCH_QUERIES = [
    "web framework",
    "http client",
    "database driver",
    "auth authentication",
    "cache redis",
    "queue worker",
    "json parser",
    "logger logging",
    "config settings",
    "test mock",
    "email mail",
    "file storage",
    "search elasticsearch",
    "graphql api",
    "websocket realtime",
    "crypto encrypt",
    "validate schema",
    "template render",
    "router routing",
    "dependency injection",
    "cli command",
    "migration seed",
    "pubsub broadcast",
    "laravel symfony",
    "doctrine orm",
    "guzzle http",
    "monolog psr",
    "phpunit mockery",
    "twig blade",
    "flysystem league",
    "carbon date",
    "ramsey uuid",
    "vlucas dotenv",
    "swiftmailer mail",
    "faker factory",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (E108 experiment)"}


def fetch(url: str) -> Optional[Dict[str, Any]]:
    """Fetch JSON from URL with error handling."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def classify_need(desc: str) -> str:
    """Classify package as need-related or random."""
    if not desc:
        return "random"
    desc_lower = desc.lower()

    # Generic terms -> random
    for term in GENERIC_TERMS:
        if term in desc_lower:
            return "random"

    # Need indicators -> need-related
    for term in NEED_INDICATORS:
        if term in desc_lower:
            return "need-related"

    return "random"


def collect_need_related(max_packages: int = 100) -> List[Dict[str, Any]]:
    """Collect need-related packages via keyword searches."""
    packages = []
    seen: Set[str] = set()

    for query in SEARCH_QUERIES:
        if len(packages) >= max_packages:
            break

        print(f"Searching: {query}")
        url = f"https://packagist.org/search.json?q={urllib.parse.quote(query)}"
        data = fetch(url)
        if not data or "results" not in data:
            continue

        for pkg in data["results"]:
            if len(packages) >= max_packages:
                break
            name = pkg.get("name")
            if name in seen:
                continue
            seen.add(name)

            desc = pkg.get("description", "")
            classification = classify_need(desc)
            if classification == "need-related":
                # Get detailed info including downloads
                detail_url = f"https://packagist.org/packages/{name}.json"
                detail = fetch(detail_url)
                if not detail or "package" not in detail:
                    continue
                pkg_detail = detail["package"]
                downloads = pkg_detail.get("downloads", {})
                packages.append({
                    "name": name,
                    "description": desc,
                    "downloads_total": downloads.get("total", 0),
                    "downloads_monthly": downloads.get("monthly", 0),
                    "downloads_daily": downloads.get("daily", 0),
                    "classification": "need-related",
                    "source_query": query,
                })
        time.sleep(0.3)  # Be polite

    return packages


def collect_random(max_packages: int = 100) -> List[Dict[str, Any]]:
    """Collect random packages from the full package list."""
    print("Fetching full package list...")
    list_data = fetch("https://packagist.org/packages/list.json")
    if not list_data or "packageNames" not in list_data:
        print("  Failed to fetch package list")
        return []

    all_names = list_data["packageNames"]
    print(f"  Total packages available: {len(all_names)}")

    # Randomly sample from the list
    random.seed(42)  # Reproducible sampling
    sampled_names = random.sample(all_names, min(len(all_names), max_packages * 3))

    packages = []
    seen: Set[str] = set()

    for name in sampled_names:
        if len(packages) >= max_packages:
            break
        if name in seen:
            continue
        seen.add(name)

        print(f"Fetching detail for random: {name}")
        detail_url = f"https://packagist.org/packages/{name}.json"
        detail = fetch(detail_url)
        if not detail or "package" not in detail:
            continue

        pkg_detail = detail["package"]
        desc = pkg_detail.get("description", "")
        classification = classify_need(desc)
        if classification == "random":
            downloads = pkg_detail.get("downloads", {})
            packages.append({
                "name": name,
                "description": desc,
                "downloads_total": downloads.get("total", 0),
                "downloads_monthly": downloads.get("monthly", 0),
                "downloads_daily": downloads.get("daily", 0),
                "classification": "random",
                "source_query": "random_sample",
            })
        time.sleep(0.2)

    return packages


def main():
    print("=== E108 Packagist View-Count Data Collection ===\n")

    # Collect need-related
    print("Collecting need-related packages...")
    need_packages = collect_need_related(100)
    print(f"  Collected {len(need_packages)} need-related packages\n")

    # Collect random
    print("Collecting random packages...")
    random_packages = collect_random(100)
    print(f"  Collected {len(random_packages)} random packages\n")

    # Combine and save
    all_packages = need_packages + random_packages

    output = {
        "experiment": "E108",
        "platform": "Packagist",
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "need_related_count": len(need_packages),
        "random_count": len(random_packages),
        "packages": all_packages,
    }

    import os
    os.makedirs("raw", exist_ok=True)
    with open("raw/collected.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Total packages: {len(all_packages)}")
    print(f"Need-related: {len(need_packages)}")
    print(f"Random: {len(random_packages)}")
    print("Saved to raw/collected.json")


if __name__ == "__main__":
    main()