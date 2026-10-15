#!/usr/bin/env python3
"""E110 — Collect RubyGems package data for view-count principle test."""

import json
import time
import urllib.request
import urllib.parse
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
    # Ruby-specific terms
    "rails", "sinatra", "hanami", "padrino", "roda", "cuba",
    "activerecord", "sequel", "rom", "datamapper",
    "sidekiq", "resque", "delayed_job", "que", "good_job",
    "devise", "warden", "omniauth", "clearance", "authlogic",
    "pundit", "cancancan", "rolify",
    "rspec", "minitest", "cucumber", "capybara", "factory_bot",
    "pry", "byebug", "debug",
    "rubocop", "reek", "flog", "flay",
    "capistrano", "mina", "vlad",
    "whenever", "rufus-scheduler", "clockwork",
    "paperclip", "carrierwave", "shrine", "activestorage",
    "kaminari", "will_paginate", "pagy",
    "redis", "redis-namespace", "connection_pool",
    "pg", "mysql2", "sqlite3", "trilogy",
    "httparty", "faraday", "excon", "typhoeus",
    "oj", "yajl", "multi_json",
    "nokogiri", "oga", "sax-machine",
    "sidekiq", "celluloid", "concurrent-ruby",
    "dry-", "rom-", "hanami-", "trailblazer",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "demo", "example", "sample", "test", "testing",
    "skeleton", "boilerplate", "starter", "template",
    "fork", "mirror", "copy", "clone",
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
    "rails activerecord",
    "sinatra framework",
    "sidekiq background",
    "devise auth",
    "rspec test",
    "httparty faraday",
    "nokogiri xml",
    "kaminari paginate",
    "paperclip attachment",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (E110 experiment)"}


def fetch(url: str) -> Optional[Dict[str, Any]]:
    """Fetch JSON from URL with error handling."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def fetch_package_detail(name: str) -> Optional[Dict[str, Any]]:
    """Fetch detailed package info including version_downloads."""
    url = f"https://rubygems.org/api/v1/gems/{urllib.parse.quote(name)}.json"
    return fetch(url)


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
        url = f"https://rubygems.org/api/v1/search.json?query={urllib.parse.quote(query)}"
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

            desc = pkg.get("info", "")
            classification = classify_need(desc)
            if classification == "need-related":
                # Fetch detailed info for version_downloads
                detail = fetch_package_detail(name)
                if detail:
                    version_downloads = detail.get("version_downloads", 0)
                    total_downloads = detail.get("downloads", 0)
                else:
                    version_downloads = pkg.get("version_downloads", 0)
                    total_downloads = pkg.get("downloads", 0)

                packages.append({
                    "name": name,
                    "description": desc,
                    "downloads_total": total_downloads,
                    "downloads_version": version_downloads,
                    "classification": "need-related",
                    "source_query": query,
                })
        time.sleep(0.2)  # Be polite

    return packages


def collect_random(max_packages: int = 100) -> List[Dict[str, Any]]:
    """Collect random packages from search with generic terms."""
    packages = []
    seen = set()

    # Use search with generic terms that are unlikely to match need indicators
    # but are broad enough to get a variety of packages
    generic_queries = ["a", "the", "ruby", "code", "program", "script", "gem", "lib",
                       "module", "class", "function", "file", "string", "hash",
                       "array", "hash", "hash", "data", "info", "doc", "wiki"]

    for query in generic_queries:
        if len(packages) >= max_packages:
            break
        print(f"Fetching random search: {query}")
        url = f"https://rubygems.org/api/v1/search.json?query={urllib.parse.quote(query)}"
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

            desc = pkg.get("info", "")
            classification = classify_need(desc)
            if classification == "random":
                # Fetch detailed info for version_downloads
                detail = fetch_package_detail(name)
                if detail:
                    version_downloads = detail.get("version_downloads", 0)
                    total_downloads = detail.get("downloads", 0)
                else:
                    version_downloads = pkg.get("version_downloads", 0)
                    total_downloads = pkg.get("downloads", 0)

                packages.append({
                    "name": name,
                    "description": desc,
                    "downloads_total": total_downloads,
                    "downloads_version": version_downloads,
                    "classification": "random",
                    "source_query": f"random_search_{query}",
                })
        time.sleep(0.2)

    return packages


def main():
    print("=== E110 RubyGems View-Count Data Collection ===\n")

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
        "experiment": "E110",
        "platform": "RubyGems",
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
    import os
    os.makedirs("raw", exist_ok=True)
    main()