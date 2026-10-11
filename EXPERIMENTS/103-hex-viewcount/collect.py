#!/usr/bin/env python3
"""E103 — Collect Hex.pm package data for view-count principle test."""

import json
import time
import urllib.request
from typing import Any, Dict, List, Optional

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
    "ecto phoenix",
    "plug middleware",
    "absinthe graphql",
    "tesla finch",
    "httpoison http",
    "jason json",
    "guardian jwt",
    "ueberauth oauth",
    "pow auth",
    "exq oban",
    "quantum cron",
    "broadway genstage",
    "nimble csv",
    "timex calendar",
    "decimal money",
    "uuid slug",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (E103 experiment)"}


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
    seen = set()

    for query in SEARCH_QUERIES:
        if len(packages) >= max_packages:
            break

        print(f"Searching: {query}")
        url = f"https://hex.pm/api/packages?search={urllib.parse.quote(query)}&sort=downloads&page=1"
        data = fetch(url)
        if not data:
            continue

        for pkg in data:
            if len(packages) >= max_packages:
                break
            name = pkg.get("name")
            if name in seen:
                continue
            seen.add(name)

            desc = pkg.get("meta", {}).get("description", "")
            classification = classify_need(desc)
            if classification == "need-related":
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
        time.sleep(0.2)  # Be polite

    return packages


def collect_random(max_packages: int = 100) -> List[Dict[str, Any]]:
    """Collect random packages from default listing."""
    packages = []
    seen = set()
    page = 1

    while len(packages) < max_packages and page <= 20:
        print(f"Fetching random page {page}")
        url = f"https://hex.pm/api/packages?page={page}"
        data = fetch(url)
        if not data:
            break

        for pkg in data:
            if len(packages) >= max_packages:
                break
            name = pkg.get("name")
            if name in seen:
                continue
            seen.add(name)

            desc = pkg.get("meta", {}).get("description", "")
            classification = classify_need(desc)
            if classification == "random":
                downloads = pkg.get("downloads", {})
                packages.append({
                    "name": name,
                    "description": desc,
                    "downloads_all": downloads.get("all", 0),
                    "downloads_day": downloads.get("day", 0),
                    "downloads_recent": downloads.get("recent", 0),
                    "downloads_week": downloads.get("week", 0),
                    "classification": "random",
                    "source_query": f"random_page_{page}",
                })
        page += 1
        time.sleep(0.2)

    return packages


def main():
    print("=== E103 Hex.pm View-Count Data Collection ===\n")

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
        "experiment": "E103",
        "platform": "Hex.pm",
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "need_related_count": len(need_packages),
        "random_count": len(random_packages),
        "packages": all_packages,
    }

    with open("raw/collected.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Total packages: {len(all_packages)}")
    print(f"Need-related: {len(need_packages)}")
    print(f"Random: {len(random_packages)}")
    print("Saved to raw/collected.json")


if __name__ == "__main__":
    import urllib.parse
    import os
    os.makedirs("raw", exist_ok=True)
    main()