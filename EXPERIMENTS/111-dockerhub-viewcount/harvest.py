#!/usr/bin/env python3
"""
E111 — Harvest Docker Hub repository data for view-count principle experiment.

Simplified version without problematic rate limit handling.
"""

import json
import time
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path


SEARCH_URL = "https://hub.docker.com/v2/search/repositories/"

# Need-related search queries - infrastructure/deployment needs
NEED_QUERIES = [
    "nginx", "postgres", "mysql", "redis", "mongo", "rabbitmq", "kafka",
    "prometheus", "grafana", "jenkins", "gitlab", "kubernetes", "docker",
    "terraform", "ansible", "vault", "consul", "traefik", "kong",
    "elasticsearch", "influxdb", "minio", "cert-manager", "keycloak",
    "etcd", "zookeeper", "haproxy", "caddy", "envoy", "istio",
]

# Random/control queries - generic base images, not systematically need-related
RANDOM_QUERIES = [
    "ubuntu", "debian", "alpine", "busybox", "centos", "fedora",
    "archlinux", "opensuse", "amazonlinux", "rockylinux", "almalinux",
    "hello-world", "scratch", "distroless",
    "myapp", "test-app", "sample-app", "demo-app", "example-app",
    "myimage", "testimage", "custom-image", "personal-image",
    "internal-app", "private-app", "company-app", "team-app",
    "project-a", "project-b", "service-a", "service-b",
]

BROAD_QUERIES = [""]


def fetch_page(query, page=1, page_size=100):
    """Fetch a single page of search results."""
    url = f"{SEARCH_URL}?query={query}&page_size={page_size}&page={page}"
    req = Request(url, headers={"User-Agent": "E111-DockerHub-Experiment/1.0"})

    try:
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except HTTPError as e:
        if e.code == 429:
            retry_after = int(e.headers.get("Retry-After", 60))
            print(f"  Rate limited (429), waiting {retry_after}s...")
            time.sleep(retry_after)
            return fetch_page(query, page, page_size)
        else:
            print(f"  HTTP error {e.code} for query '{query}': {e.reason}")
            return None
    except URLError as e:
        print(f"  URL error for query '{query}': {e.reason}")
        return None
    except Exception as e:
        print(f"  Unexpected error for query '{query}': {e}")
        return None


def search_query(query, max_pages=1, page_size=100):
    """Search all pages for a query."""
    all_results = []
    for page in range(1, max_pages + 1):
        print(f"  Fetching page {page} for '{query}'...")
        data = fetch_page(query, page, page_size)
        if not data or "results" not in data:
            break
        results = data["results"]
        if not results:
            break
        all_results.extend(results)
        if len(results) < page_size:
            break
        time.sleep(0.5)  # Be nice to the API
    return all_results


def harvest_all():
    """Harvest data for all queries."""
    all_repos = []
    seen = set()

    # Harvest need-related
    print("Harvesting need-related queries...")
    for query in NEED_QUERIES:
        results = search_query(query, max_pages=1, page_size=100)
        for repo in results:
            key = repo.get("repo_name", "")
            if key and key not in seen:
                repo["_query_type"] = "need"
                repo["_query"] = query
                all_repos.append(repo)
                seen.add(key)
        print(f"  '{query}': {len(results)} results, total unique: {len(all_repos)}")

    # Harvest random
    print("\nHarvesting random queries...")
    for query in RANDOM_QUERIES:
        results = search_query(query, max_pages=1, page_size=100)
        for repo in results:
            key = repo.get("repo_name", "")
            if key and key not in seen:
                repo["_query_type"] = "random"
                repo["_query"] = query
                all_repos.append(repo)
                seen.add(key)
        print(f"  '{query}': {len(results)} results, total unique: {len(all_repos)}")

    # Also get some broad popular images
    print("\nHarvesting broad/popular images...")
    for query in BROAD_QUERIES:
        results = search_query(query, max_pages=1, page_size=100)
        for repo in results:
            key = repo.get("repo_name", "")
            if key and key not in seen:
                repo["_query_type"] = "broad"
                repo["_query"] = query
                all_repos.append(repo)
                seen.add(key)
        print(f"  broad: {len(results)} results, total unique: {len(all_repos)}")

    print(f"\nTotal unique repositories harvested: {len(all_repos)}")
    return all_repos


def main():
    print("E111 — Docker Hub harvest")
    print("=" * 50)

    repos = harvest_all()

    # Save raw data
    output = {
        "harvested_at": time.time(),
        "total_count": len(repos),
        "repositories": repos,
    }

    out_path = Path(__file__).parent / "raw_data.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved raw data to {out_path}")
    print(f"Total repositories: {len(repos)}")

    # Quick stats
    need_count = sum(1 for r in repos if r.get("_query_type") == "need")
    random_count = sum(1 for r in repos if r.get("_query_type") == "random")
    broad_count = sum(1 for r in repos if r.get("_query_type") == "broad")
    official_count = sum(1 for r in repos if r.get("is_official"))
    automated_count = sum(1 for r in repos if r.get("is_automated"))

    print(f"  Need queries: {need_count}")
    print(f"  Random queries: {random_count}")
    print(f"  Broad queries: {broad_count}")
    print(f"  Official images: {official_count}")
    print(f"  Automated builds: {automated_count}")

    # Pull count stats
    pulls = [r.get("pull_count", 0) for r in repos if r.get("pull_count", 0) > 0]
    if pulls:
        pulls.sort()
        print(f"  Pull count range: {pulls[0]} - {pulls[-1]}")
        print(f"  Pull count median: {pulls[len(pulls)//2]}")


if __name__ == "__main__":
    main()