#!/usr/bin/env python3
"""Classify harvested reports and compute rates."""

import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classifier import classify_report, extract_module_from_error

STDLIB_MODULES = {
    'os', 'sys', 'json', 'datetime', 'time', 'math', 'random', 'collections',
    'itertools', 'functools', 'pathlib', 'glob', 're', 'subprocess', 'threading',
    'multiprocessing', 'asyncio', 'typing', 'dataclasses', 'enum', 'abc', 'io',
    'csv', 'xml', 'html', 'http', 'urllib', 'email', 'sqlite3', 'pickle', 'copy',
    'pprint', 'textwrap', 'string', 'numbers', 'fractions', 'decimal', 'statistics',
    'hashlib', 'hmac', 'secrets', 'base64', 'binascii', 'quopri', 'uu', 'zlib',
    'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'argparse',
    'getopt', 'optparse', 'shlex', 'cmd', 'readline', 'rlcompleter', 'logging',
    'logging.config', 'logging.handlers', 'traceback', 'warnings', 'contextlib',
    'weakref', 'gc', 'inspect', 'importlib', 'pkgutil', 'modulefinder', 'runpy',
    'site', 'sysconfig', 'builtins', '__main__', '__future__', 'typing_extensions'
}

def clean_html(text):
    """Remove HTML tags from text."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('<', '<').replace('>', '>').replace('&', '&')
    text = text.replace('"', '"').replace('\u2018', "'").replace('\u2019', "'")
    return text

def is_excluded(report, classification, module):
    """Check if report should be excluded from denominator."""
    if classification == 'stdlib':
        return True
    if classification == 'environment':
        return True
    if classification == 'unclear':
        return True
    if module and module in STDLIB_MODULES:
        return True
    return False

def classify_harvest(harvest_path):
    with open(harvest_path) as f:
        reports = json.load(f)

    results = []
    class_counts = {}

    for r in reports:
        title = r.get('title', '')
        body = clean_html(r.get('body', ''))

        classification = classify_report(title, body)
        module = extract_module_from_error(f"{title}\n{body}")

        excluded = is_excluded(r, classification, module)

        result = {
            'id': r['id'],
            'source': r['source'],
            'title': title[:100],
            'module': module,
            'classification': classification,
            'excluded': excluded,
            'view_count': r.get('view_count', 0) if r['source'] == 'stackoverflow' else r.get('reactions', {}).get('total_count', 0),
            'url': r.get('link', r.get('url', ''))
        }
        results.append(result)

        if not excluded:
            class_counts[classification] = class_counts.get(classification, 0) + 1

    return results, class_counts

def compute_rates(results, class_counts):
    """Compute the rates for G3."""
    total_classifiable = sum(class_counts.values())
    module_only = class_counts.get('module-only', 0)

    if total_classifiable == 0:
        return 0.0, 0, 0

    rate = module_only / total_classifiable
    return rate, module_only, total_classifiable

def wilson_ci(k, n, z=1.96):
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0, 0)
    p = k / n
    denominator = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denominator
    half = (z * ((p*(1-p)/n + z*z/(4*n*n))**0.5)) / denominator
    return (centre - half, centre + half)

if __name__ == "__main__":
    harvest_path = sys.argv[1] if len(sys.argv) > 1 else "harvest_raw.json"

    results, class_counts = classify_harvest(harvest_path)
    rate, module_only, total = compute_rates(results, class_counts)
    ci_low, ci_high = wilson_ci(module_only, total)

    print(f"Total reports harvested: {len(results)}")
    print(f"Classifiable (denominator): {total}")
    print(f"Class counts: {class_counts}")
    print(f"module-only: {module_only}")
    print(f"Rate R = {module_only}/{total} = {rate:.4f}")
    print(f"Wilson CI95: [{ci_low:.4f}, {ci_high:.4f}]")

    # G3 decision
    if rate < 0.01:
        decision = "KILL"
    elif rate < 0.05:
        decision = "HOLD"
    else:
        decision = "BUILD"
    print(f"G3 Decision: {decision} (rate {rate:.4f})")

    # G4: view_count check for module-only
    module_only_reports = [r for r in results if r['classification'] == 'module-only' and not r['excluded']]
    with_views = sum(1 for r in module_only_reports if r['view_count'] > 0)
    view_rate = with_views / len(module_only_reports) if module_only_reports else 0
    print(f"G4 view_count check: {with_views}/{len(module_only_reports)} = {view_rate:.2f} have view_count > 0")

    # Save detailed results
    output = {
        'total_harvested': len(results),
        'classifiable': total,
        'class_counts': class_counts,
        'module_only_count': module_only,
        'rate': rate,
        'wilson_ci95': [ci_low, ci_high],
        'g3_decision': decision,
        'g4_view_rate': view_rate,
        'module_only_with_views': with_views,
        'module_only_total': len(module_only_reports),
        'results': results
    }

    with open("CLASSIFICATION_RESULTS.json", "w") as f:
        json.dump(output, f, indent=1)

    print("Detailed results saved to CLASSIFICATION_RESULTS.json")