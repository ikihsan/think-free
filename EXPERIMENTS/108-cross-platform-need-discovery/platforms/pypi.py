#!/usr/bin/env python3
"""PyPI platform search module.

Note: PyPI's search endpoint (https://pypi.org/search/) requires JavaScript and blocks
automated requests. This module uses alternative approaches:
1. Known package database for common needs
2. GitHub search as proxy (many PyPI packages have GitHub repos)
3. Direct package detail API for known package names
"""

import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional


PYPI_PACKAGE_URL = "https://pypi.org/pypi/{name}/json"
PYPI_STATS_URL = "https://pypistats.org/api/packages/{name}/recent"

# Curated known packages for common need categories (fallback when search unavailable)
KNOWN_PACKAGES = {
    "web": ["django", "flask", "fastapi", "starlette", "sanic", "tornado", "bottle", "falcon"],
    "http": ["requests", "httpx", "aiohttp", "urllib3", "httpcore", "httplib2"],
    "async": ["aiohttp", "httpx", "asyncio", "trio", "anyio", "curio"],
    "database": ["sqlalchemy", "django-orm", "peewee", "tortoise-orm", "databases", "asyncpg", "psycopg2"],
    "orm": ["sqlalchemy", "tortoise-orm", "peewee", "django-orm", "ponyorm"],
    "redis": ["redis", "aredis", "aioredis", "redis-py-cluster"],
    "cache": ["redis", "memcached", "pymemcache", "aiocache", "diskcache"],
    "queue": ["celery", "rq", "dramatiq", "huey", "arq", "asyncio-queue"],
    "auth": ["authlib", "python-jose", "pyjwt", "passlib", "bcrypt", "argon2"],
    "oauth": ["authlib", "requests-oauthlib", "oauthlib", "social-auth-core"],
    "jwt": ["pyjwt", "python-jose", "authlib"],
    "security": ["cryptography", "pycryptodome", "bcrypt", "argon2", "passlib"],
    "config": ["pydantic", "python-dotenv", "dynaconf", "configparser", "toml"],
    "logging": ["loguru", "structlog", "logging", "python-json-logger"],
    "testing": ["pytest", "unittest", "hypothesis", "faker", "factory-boy"],
    "cli": ["click", "typer", "argparse", "fire", "cliff", "cement"],
    "serialization": ["pydantic", "marshmallow", "attrs", "dataclasses-json", "orjson", "ujson"],
    "validation": ["pydantic", "cerberus", "voluptuous", "marshmallow", "jsonschema"],
    "email": ["emails", "yagmail", "smtplib", "mailgun", "sendgrid"],
    "file": ["pathlib", "pathlib2", "watchdog", "python-magic", "mimetypes"],
    "search": ["elasticsearch-py", "opensearch-py", "whoosh", "xapian"],
    "graphql": ["graphene", "strawberry", "ariadne", "gql"],
    "grpc": ["grpcio", "grpcio-tools", "grpclib"],
    "websocket": ["websockets", "autobahn", "aiohttp-ws", "starlette-websockets"],
    "template": ["jinja2", "mako", "chameleon", "templite"],
    "router": ["starlette", "fastapi", "aiohttp", "sanic"],
    "middleware": ["starlette", "fastapi", "aiohttp"],
    "dependency": ["fastapi", "dependency-injector", "python-dependency-injector"],
    "migration": ["alembic", "django-migrations", "yoyo-migrations"],
    "monitoring": ["prometheus-client", "opentelemetry", "datadog", "sentry-sdk"],
    "metrics": ["prometheus-client", "statsd", "opentelemetry"],
    "tracing": ["opentelemetry", "jaeger-client", "zipkin"],
}


def search_packages(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search for PyPI packages using known package database as fallback."""
    terms = query.lower().split()
    
    # Find matching known packages
    matched = set()
    for term in terms:
        if term in KNOWN_PACKAGES:
            matched.update(KNOWN_PACKAGES[term])
    
    # Also check for partial matches
    for category, packages in KNOWN_PACKAGES.items():
        for term in terms:
            if term in category or category in term:
                matched.update(packages)
    
    results = []
    for name in list(matched)[:max_results]:
        results.append({
            "name": name,
            "summary": f"Known package for {query}",
            "description": "",
            "version": "",
            "platform": "pypi",
            "url": f"https://pypi.org/project/{name}/",
            "from_known": True,
        })
    
    return results


def get_package_details(name: str) -> Optional[Dict[str, Any]]:
    """Get detailed package metadata including downloads."""
    url = PYPI_PACKAGE_URL.format(name=urllib.parse.quote(name))
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  PyPI detail error for {name}: {e}")
        return None
    
    info = data.get("info", {})
    
    # Get download stats from pypistats
    downloads = get_download_stats(name)
    
    return {
        "name": info.get("name", name),
        "summary": info.get("summary", ""),
        "description": info.get("description", ""),
        "version": info.get("version", ""),
        "author": info.get("author", ""),
        "license": info.get("license", ""),
        "home_page": info.get("home_page", ""),
        "project_urls": info.get("project_urls", {}),
        "classifiers": info.get("classifiers", []),
        "requires_python": info.get("requires_python", ""),
        "keywords": info.get("keywords", ""),
        "downloads_last_month": downloads.get("last_month", 0),
        "downloads_last_week": downloads.get("last_week", 0),
        "downloads_last_day": downloads.get("last_day", 0),
        "platform": "pypi",
        "url": f"https://pypi.org/project/{name}/",
    }


def get_download_stats(name: str) -> Dict[str, int]:
    """Get download statistics from pypistats.org."""
    url = PYPI_STATS_URL.format(name=urllib.parse.quote(name))
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "needfind/1.0", "Accept": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        total = 0
        last_month = 0
        last_week = 0
        last_day = 0
        
        for entry in data.get("data", []):
            if entry.get("category") == "without_mirrors":
                total = entry.get("downloads", 0)
            elif entry.get("category") == "last_month":
                last_month = entry.get("downloads", 0)
            elif entry.get("category") == "last_week":
                last_week = entry.get("downloads", 0)
            elif entry.get("category") == "last_day":
                last_day = entry.get("downloads", 0)
        
        return {
            "total": total,
            "last_month": last_month,
            "last_week": last_week,
            "last_day": last_day,
        }
    except Exception:
        return {"total": 0, "last_month": 0, "last_week": 0, "last_day": 0}


def enrich_results(results: List[Dict[str, Any]], max_detail: int = 10) -> List[Dict[str, Any]]:
    """Enrich search results with detailed metadata and download stats."""
    enriched = []
    
    for i, pkg in enumerate(results):
        if i >= max_detail:
            pkg["downloads_last_month"] = 0
            pkg["activity_score"] = 0
            enriched.append(pkg)
            continue
        
        details = get_package_details(pkg["name"])
        if details:
            pkg.update(details)
            pkg["activity_score"] = pkg.get("downloads_last_month", 0)
        else:
            pkg["downloads_last_month"] = 0
            pkg["activity_score"] = 0
        
        enriched.append(pkg)
        time.sleep(0.1)
    
    return enriched


if __name__ == "__main__":
    # Test
    results = search_packages("async http client")
    print(f"Found {len(results)} packages from known database")
    enriched = enrich_results(results[:5])
    for r in enriched:
        print(f"  {r['name']}: {r.get('summary', '')[:60]} (downloads/month: {r.get('downloads_last_month', 0)})")