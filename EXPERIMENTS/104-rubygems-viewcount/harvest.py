#!/usr/bin/env python3
"""
E104 — View-count principle on RubyGems — Data Collection

Fetches need-related and random gems from RubyGems, collecting
name, description (from info field), and download counts.
"""

import urllib.request, json, time, sys
from collections import Counter

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
    "broadcast", "channel", "presence",
    "rake", "gem", "bundler", "rails", "rack", "sinatra",
    "active_record", "action_view", "action_controller",
    "rspec", "minitest", "test_unit",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "rubygem", "ruby", "rails", "rack"
}


def classify_gem(description):
    """Classify a gem as need-related, random, or ambiguous based on its description."""
    if description is None:
        return "ambiguous"
    desc_lower = str(description).lower()
    has_need = any(term in desc_lower for term in NEED_INDICATORS)
    has_generic = any(term in desc_lower for term in GENERIC_TERMS)
    if has_need and not has_generic:
        return "need-related"
    elif not has_need and has_generic:
        return "random"
    else:
        # Ambiguous: check which side has more matches
        need_count = sum(1 for term in NEED_INDICATORS if term in desc_lower)
        generic_count = sum(1 for term in GENERIC_TERMS if term in desc_lower)
        if need_count > generic_count:
            return "need-related"
        elif generic_count > need_count:
            return "random"
        else:
            return "ambiguous"


def fetch_need_related(max_count=100):
    """Fetch need-related gems via keyword search."""
    collected = set()
    keywords = [
        "web framework", "http client", "database", "auth", "cache",
        "json", "logger", "config", "test", "rails", "gem"
    ]
    
    for kw in keywords:
        if len(collected) >= max_count:
            break
        try:
            encoded = urllib.request.quote(kw, safe='')
            url = f'https://rubygems.org/api/v1/search.json?query={encoded}&sort=downloads&page=1'
            r = urllib.request.urlopen(url, timeout=15)
            data = json.loads(r.read().decode())
            for gem in data:
                name = gem.get('name', '')
                if name and name not in collected:
                    collected.add(name)
        except Exception as e:
            print(f'Error searching keyword "{kw}": {e}', file=sys.stderr)
        time.sleep(0.5)
    
    # Also try individual shorter keywords if we don't have enough
    short_keywords = ["web", "api", "http", "db", "cache", "json", "auth", "test", "ruby", "gem"]
    for kw in short_keywords:
        if len(collected) >= max_count:
            break
        try:
            encoded = urllib.request.quote(kw, safe='')
            url = f'https://rubygems.org/api/v1/search.json?query={encoded}&sort=downloads&page=1'
            r = urllib.request.urlopen(url, timeout=15)
            data = json.loads(r.read().decode())
            for gem in data:
                name = gem.get('name', '')
                if name and name not in collected:
                    collected.add(name)
        except Exception as e:
            print(f'Error searching short keyword "{kw}": {e}', file=sys.stderr)
        time.sleep(0.5)
    
    return collected


def fetch_random(max_count=100):
    """Fetch random gems from the default listing via search with broad terms."""
    collected = set()
    # Use broad search queries to get random-ish results
    broad_queries = ["ruby", "programming", "software", "development", "code"]
    for query in broad_queries:
        if len(collected) >= max_count:
            break
        try:
            encoded = urllib.request.quote(query, safe='')
            url = f'https://rubygems.org/api/v1/search.json?query={encoded}&sort=downloads&page=1'
            r = urllib.request.urlopen(url, timeout=15)
            data = json.loads(r.read().decode())
            for gem in data:
                name = gem.get('name', '')
                if name and name not in collected:
                    collected.add(name)
        except Exception as e:
            print(f'Error searching broad query "{query}": {e}', file=sys.stderr)
        time.sleep(0.5)
    
    # If still not enough, paginate
    page = 2
    while len(collected) < max_count and page <= 20:
        try:
            url = f'https://rubygems.org/api/v1/search.json?query=&sort=downloads&page={page}'
            r = urllib.request.urlopen(url, timeout=15)
            data = json.loads(r.read().decode())
            if not data:
                break
            for gem in data:
                name = gem.get('name', '')
                if name and name not in collected:
                    collected.add(name)
        except Exception as e:
            print(f'Error fetching random page {page}: {e}', file=sys.stderr)
        page += 1
        time.sleep(0.5)
    
    return collected


def fetch_gem_details(names):
    """Fetch detailed data for a list of gem names."""
    results = []
    for name in names:
        try:
            url = f'https://rubygems.org/api/v1/gems/{name}.json'
            r = urllib.request.urlopen(url, timeout=15)
            detail = json.loads(r.read().decode())
            
            # Extract description from info field (it's a string, not a dict)
            info = detail.get('info', '')
            description = str(info) if info else ''
            
            # Extract download count
            downloads = detail.get('downloads', 0)
            if not isinstance(downloads, (int, float)):
                downloads = 0
            downloads = int(downloads)
            
            classification = classify_gem(description)
            
            result = {
                'name': name,
                'description': description,
                'needs_classification': classification,
                'total_downloads': downloads,
                'group': None,  # will be set by caller
                'api_url': url
            }
            results.append(result)
        except Exception as e:
            print(f'  Error fetching {name}: {e}', file=sys.stderr)
        time.sleep(0.1)
    
    return results


def main():
    print('Fetching need-related gems...')
    need_names = fetch_need_related(100)
    print(f'Collected {len(need_names)} need-related gem names')
    
    print('Fetching random gems...')
    random_names = fetch_random(100)
    print(f'Collected {len(random_names)} random gem names')
    
    # Remove overlap
    both = need_names & random_names
    print(f'Overlap: {both} (removing...)')
    need_names = need_names - both
    random_names = random_names - both
    
    print(f'After dedup: need-related={len(need_names)}, random={len(random_names)}')
    
    # Fetch detailed data for need-related gems
    print('Fetching detailed data for need-related gems...')
    need_details = fetch_gem_details(sorted(need_names))
    
    # Fetch detailed data for random gems
    print('Fetching detailed data for random gems...')
    random_details = fetch_gem_details(sorted(random_names))
    
    # Assign group labels
    for r in need_details:
        r['group'] = 'need-related'
    for r in random_details:
        r['group'] = 'random'
    
    all_results = need_details + random_details
    
    # Save results
    with open('EXPERIMENTS/104-rubygems-viewcount/results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print summary
    print(f'\n=== Summary ===')
    print(f'Total gems: {len(all_results)}')
    print(f'Need-related: {len(need_details)}')
    print(f'Random: {len(random_details)}')
    
    # Classification summary
    nr_classified = Counter(r['needs_classification'] for r in need_details)
    r_classified = Counter(r['needs_classification'] for r in random_details)
    print(f'\nNeed-related classification: {dict(nr_classified)}')
    print(f'Random classification: {dict(r_classified)}')
    
    # Download stats
    nr_downloads = [r['total_downloads'] for r in need_details]
    r_downloads = [r['total_downloads'] for r in random_details]
    
    if nr_downloads:
        sorted_nr = sorted(nr_downloads)
        print(f'\nNeed-related downloads - median: {sorted_nr[len(sorted_nr)//2]}, min: {min(sorted_nr)}, max: {max(sorted_nr)} (n={len(nr_downloads)})')
    if r_downloads:
        sorted_r = sorted(r_downloads)
        print(f'Random downloads - median: {sorted_r[len(sorted_r)//2]}, min: {min(sorted_r)}, max: {max(sorted_r)} (n={len(r_downloads)})')
    
    # Active rates (downloads > 0)
    nr_active = sum(1 for r in need_details if r['total_downloads'] > 0) / len(need_details) if need_details else 0
    r_active = sum(1 for r in random_details if r['total_downloads'] > 0) / len(random_details) if random_details else 0
    print(f'\nActive rate (downloads > 0): need-related={nr_active:.4f}, random={r_active:.4f}')
    
    # Download stats including 0
    nr_active_count = sum(1 for r in need_details if r['total_downloads'] > 0)
    r_active_count = sum(1 for r in random_details if r['total_downloads'] > 0)
    print(f'\nNeed-related: {nr_active_count} have downloads > 0 out of {len(need_details)}')
    print(f'Random: {r_active_count} have downloads > 0 out of {len(random_details)}')
    
    # Print a few classified gems for verification
    print(f'\n=== Sample classified gems ===')
    for r in need_details[:5]:
        desc_preview = r['description'][:60] if r['description'] else '(empty)'
        print(f'  {r[\"name\"]:25s} class={r[\"needs_classification\"]:15s} desc={desc_preview} downloads={r[\"total_downloads\"]}')
    for r in random_details[:5]:
        desc_preview = r['description'][:60] if r['description'] else '(empty)'
        print(f'  {r[\"name\"]:25s} class={r[\"needs_classification\"]:15s} desc={desc_preview} downloads={r[\"total_downloads\"]}')
    
    print(f'\nResults saved to EXPERIMENTS/104-rubygems-viewcount/results.json')


if __name__ == '__main__':
    main()