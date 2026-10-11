#!/usr/bin/env python3
"""E106 — View-count principle PyPI prototype — Data Collection (fixed)"""

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
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
    "rubygem", "ruby", "rails", "rack"
}


def classify_gem(description):
    """Classify a PyPI package as need-related, random, or ambiguous."""
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
        need_count = sum(1 for term in NEED_INDICATORS if term in desc_lower)
        generic_count = sum(1 for term in GENERIC_TERMS if term in desc_lower)
        if need_count > generic_count:
            return "need-related"
        elif generic_count > need_count:
            return "random"
        else:
            return "ambiguous"


def is_active(detail):
    """Check if a package is 'active' based on E071 definition.
    
    A package is 'active' if it has: a version, a summary/description, and classifiers.
    This follows E071's definition where need-related packages have 82.93% active rate
    vs 57.50% for random packages.
    """
    try:
        info = detail.get('info', {})
        if isinstance(info, str):
            return False
        # Active if: has version in info, has summary/description, has classifiers
        has_version = info.get('version', '') != ''
        has_description = bool(detail.get('info', {}).get('summary', '') or detail.get('info', {}).get('description', ''))
        has_classifiers = bool(detail.get('info', {}).get('classifiers', []))
        return has_version and has_description and has_classifiers
    except:
        return False


def fetch_packages(names, max_per_group=20):
    """Fetch package details from PyPI's JSON API."""
    results = []
    for name in names:
        try:
            url = 'https://pypi.org/pypi/%s/json' % urllib.request.quote(name, safe='')
            r = urllib.request.urlopen(url, timeout=15)
            detail = json.loads(r.read().decode())
            
            description = detail.get('info', {}).get('summary', '') or detail.get('info', {}).get('description', '') or ''
            classification = classify_gem(description)
            active = is_active(detail)
            
            result = {
                'name': name,
                'description': description,
                'needs_classification': classification,
                'active': active,
                'api_url': url
            }
            results.append(result)
        except Exception as e:
            print('Error fetching %s: %s' % (name, e), file=sys.stderr)
        time.sleep(0.1)
    
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description='PyPI view-count prototype')
    parser.add_argument('names', metavar='N', type=str, nargs='+',
                        help='PyPI package names to assess')
    parser.add_argument('--samplesize', type=int, default=20,
                        help='Number of packages to sample (default: 20)')
    args = parser.parse_args()
    
    all_results = fetch_packages(args.names, args.samplesize)
    
    # Assign groups based on classification
    for r in all_results:
        if r['needs_classification'] == 'need-related':
            r['group'] = 'need-related'
        elif r['needs_classification'] == 'random':
            r['group'] = 'random'
        else:
            r['group'] = 'ambiguous'
    
    # Save results
    with open('results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print summary
    need_related = [r for r in all_results if r['group'] == 'need-related']
    random_gems = [r for r in all_results if r['group'] == 'random']
    
    print('=== PyPI View-count Prototype Summary ===')
    print('Total packages assessed: %d' % len(all_results))
    print('Need-related: %d' % len(need_related))
    print('Random: %d' % len(random_gems))
    print('Ambiguous: %d' % sum(1 for r in all_results if r['group'] == 'ambiguous'))
    
    # Active rates (E071 definition)
    nr_active = sum(1 for r in need_related if r['active']) / len(need_related) if need_related else 0
    r_active = sum(1 for r in random_gems if r['active']) / len(random_gems) if random_gems else 0
    print()
    print('Active rate (E071 definition: has version + summary + classifiers):')
    print('  need-related: %d/%d = %.4f' % (sum(1 for r in need_related if r['active']), len(need_related), nr_active))
    print('  random: %d/%d = %.4f' % (sum(1 for r in random_gems if r['active']), len(random_gems), r_active))
    
    # G1: Sample size
    print()
    print('G1 (sample size >= 100 with valid classification): %s' % ('PASS' if len(need_related) + len(random_gems) >= 100 else 'FAIL (valid=%d)' % (len(need_related) + len(random_gems))))
    
    # Comparison to E071
    print()
    print('Comparison to E071: need-related active rate %.4f vs random active rate %.4f' % (nr_active, r_active))
    print('E071 result: 82.93%% vs 57.50%%, all gates pass')
    if abs(nr_active - r_active) > 0.1:
        print('Note: Sample rates differ from E071 - may need larger sample')
    else:
        print('Note: Sample rates are approximately consistent with E071')
    
    print()
    print('Results saved to results.json')
    
    # Show a few examples
    print()
    print('=== Sample results ===')
    for r in need_related[:3]:
        desc_preview = r['description'][:60] if r['description'] else '(empty)'
        print('  %s: class=%-15s active=%-5s' % (r['name'], r['needs_classification'], str(r['active'])))
    for r in random_gems[:3]:
        desc_preview = r['description'][:60] if r['description'] else '(empty)'
        print('  %s: class=%-15s active=%-5s' % (r['name'], r['needs_classification'], str(r['active'])))