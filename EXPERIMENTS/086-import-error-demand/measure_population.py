#!/usr/bin/env python3
"""
Population Measurement for import_error_classifier
Fetches real ImportError/ModuleNotFoundError reports from:
1. Stack Exchange API (Stack Overflow)
2. GitHub Issues API (popular Python repos)
"""

import json
import urllib.request
import urllib.error
import time
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from math import sqrt
from run_discrimination_test import import_error_classifier, wilson_ci


@dataclass
class Report:
    source: str
    report_id: str
    title: str
    body: str
    url: str
    classification: str
    tags: List[str] = None


def fetch_stackexchange_import_errors(max_pages=5, pagesize=100) -> List[Report]:
    """
    Fetch Python import error questions from Stack Overflow via Stack Exchange API.
    """
    reports = []
    base_url = "https://api.stackexchange.com/2.3/questions"
    
    # Search for questions with import error related terms
    # Using tagged=python and search terms in title
    for page in range(1, max_pages + 1):
        params = {
            'order': 'desc',
            'sort': 'votes',
            'tagged': 'python',
            'pagesize': pagesize,
            'page': page,
            'site': 'stackoverflow',
            'filter': 'withbody'  # Include body content
        }
        
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        url = f"{base_url}?{query_string}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pyprovides/0.1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            
            items = data.get('items', [])
            if not items:
                break
                
            for item in items:
                title = item.get('title', '')
                body = item.get('body', '')
                # Check if title or body mentions import error
                combined = f"{title} {body}".lower()
                if any(kw in combined for kw in ['modulenotfounderror', 'importerror', "no module named", 'cannot import']):
                    # Clean HTML from body
                    clean_body = re.sub(r'<[^>]+>', '', body)
                    clean_body = re.sub(r'\s+', ' ', clean_body).strip()[:2000]
                    
                    report = Report(
                        source='stackexchange',
                        report_id=str(item.get('question_id')),
                        title=title,
                        body=clean_body,
                        url=item.get('link', ''),
                        classification='',
                        tags=item.get('tags', [])
                    )
                    reports.append(report)
            
            # Respect rate limit (300 requests/day for no key, 10000 with key)
            time.sleep(0.1)
            
            if not data.get('has_more', False):
                break
                
        except urllib.error.HTTPError as e:
            print(f"Stack Exchange API error: {e.code} - {e.reason}")
            if e.code == 429:  # Rate limited
                time.sleep(60)
            break
        except Exception as e:
            print(f"Error fetching Stack Exchange page {page}: {e}")
            break
    
    return reports


def fetch_github_issues(repo: str, max_pages=3, pagesize=100, token: Optional[str] = None) -> List[Report]:
    """
    Fetch import error issues from a GitHub repository.
    """
    reports = []
    base_url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {'User-Agent': 'pyprovides/0.1.0', 'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    
    for page in range(1, max_pages + 1):
        params = {
            'state': 'all',
            'per_page': pagesize,
            'page': page
        }
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        url = f"{base_url}?{query_string}"
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                items = json.loads(resp.read().decode('utf-8'))
            
            if not items:
                break
                
            for item in items:
                # Skip PRs
                if 'pull_request' in item:
                    continue
                    
                title = item.get('title', '')
                body = item.get('body', '') or ''
                combined = f"{title} {body}".lower()
                
                if any(kw in combined for kw in ['modulenotfounderror', 'importerror', "no module named", 'cannot import']):
                    clean_body = re.sub(r'<[^>]+>', '', body)
                    clean_body = re.sub(r'\s+', ' ', clean_body).strip()[:2000]
                    
                    report = Report(
                        source=f'github:{repo}',
                        report_id=str(item.get('number')),
                        title=title,
                        body=clean_body,
                        url=item.get('html_url', ''),
                        classification='',
                        tags=[]  # GitHub issues don't have tags in the same way
                    )
                    reports.append(report)
            
            # Check for pagination
            link_header = resp.headers.get('Link', '')
            if 'rel="next"' not in link_header:
                break
                
            # Rate limit: 60 req/hour unauthenticated, 5000/hour authenticated
            time.sleep(1)
            
        except urllib.error.HTTPError as e:
            print(f"GitHub API error for {repo}: {e.code} - {e.reason}")
            if e.code == 403:  # Rate limited
                print("Rate limited, sleeping 60s...")
                time.sleep(60)
            break
        except Exception as e:
            print(f"Error fetching GitHub issues from {repo} page {page}: {e}")
            break
    
    return reports


def classify_reports(reports: List[Report]) -> List[Report]:
    """Classify all reports using the import_error_classifier."""
    for report in reports:
        combined = f"{report.title} {report.body}"
        report.classification = import_error_classifier(combined)
    return reports


def analyze_results(reports: List[Report]) -> Dict:
    """Analyze classification results."""
    # Filter to only import error reports (module_only + distribution_named + no_module)
    import_error_reports = [r for r in reports if r.classification in ('module_only', 'distribution_named', 'no_module')]
    
    if not import_error_reports:
        return {
            'total_reports': len(reports),
            'import_error_reports': 0,
            'module_only': 0,
            'distribution_named': 0,
            'no_module': 0,
            'module_only_rate': 0.0,
            'module_only_ci': (0.0, 0.0)
        }
    
    module_only = sum(1 for r in import_error_reports if r.classification == 'module_only')
    distribution_named = sum(1 for r in import_error_reports if r.classification == 'distribution_named')
    no_module = sum(1 for r in import_error_reports if r.classification == 'no_module')
    
    total_import_errors = len(import_error_reports)
    module_only_rate = module_only / total_import_errors if total_import_errors > 0 else 0.0
    module_only_ci = wilson_ci(module_only_rate, total_import_errors)
    
    # By source
    by_source = {}
    for source in set(r.source for r in reports):
        src_reports = [r for r in reports if r.source == source]
        src_import_errors = [r for r in src_reports if r.classification in ('module_only', 'distribution_named', 'no_module')]
        src_module_only = sum(1 for r in src_import_errors if r.classification == 'module_only')
        src_total = len(src_import_errors)
        src_rate = src_module_only / src_total if src_total > 0 else 0.0
        src_ci = wilson_ci(src_rate, src_total)
        by_source[source] = {
            'total': len(src_reports),
            'import_errors': src_total,
            'module_only': src_module_only,
            'rate': src_rate,
            'ci': src_ci
        }
    
    return {
        'total_reports': len(reports),
        'import_error_reports': total_import_errors,
        'module_only': module_only,
        'distribution_named': distribution_named,
        'no_module': no_module,
        'module_only_rate': module_only_rate,
        'module_only_ci': module_only_ci,
        'by_source': by_source
    }


def main():
    print("=" * 80)
    print("POPULATION MEASUREMENT: Real Python Import Error Reports")
    print("=" * 80)
    
    all_reports = []
    
    # 1. Stack Exchange (Stack Overflow)
    print("\n1. Fetching from Stack Exchange API (Stack Overflow)...")
    se_reports = fetch_stackexchange_import_errors(max_pages=10, pagesize=100)
    print(f"   Found {len(se_reports)} import-error-related questions")
    all_reports.extend(se_reports)
    
    # 2. GitHub Issues - popular Python repos
    print("\n2. Fetching from GitHub Issues API...")
    popular_repos = [
        'python/cpython',
        'numpy/numpy',
        'pandas-dev/pandas',
        'psf/requests',
        'django/django',
        'pallets/flask',
        'scikit-learn/scikit-learn',
        'pytorch/pytorch',
        'tensorflow/tensorflow',
        'sqlalchemy/sqlalchemy',
    ]
    
    for repo in popular_repos:
        print(f"   Fetching from {repo}...")
        gh_reports = fetch_github_issues(repo, max_pages=2, pagesize=100)
        print(f"   Found {len(gh_reports)} import-error-related issues")
        all_reports.extend(gh_reports)
        time.sleep(2)  # Be nice to the API
    
    print(f"\nTotal reports collected: {len(all_reports)}")
    
    # Classify
    print("\n3. Classifying reports...")
    classified = classify_reports(all_reports)
    
    # Analyze
    print("\n4. Analyzing results...")
    results = analyze_results(classified)
    
    # Print results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total reports collected: {results['total_reports']}")
    print(f"Import error reports: {results['import_error_reports']}")
    print(f"  module_only: {results['module_only']}")
    print(f"  distribution_named: {results['distribution_named']}")
    print(f"  no_module: {results['no_module']}")
    print(f"\nmodule_only rate: {results['module_only_rate']:.4f} ({results['module_only']}/{results['import_error_reports']})")
    print(f"Wilson 95% CI: [{results['module_only_ci'][0]:.4f}, {results['module_only_ci'][1]:.4f}]")
    
    print("\nBy source:")
    for source, data in results['by_source'].items():
        print(f"  {source}: {data['import_errors']} import errors, {data['module_only']} module_only, rate={data['rate']:.4f}, CI=[{data['ci'][0]:.4f}, {data['ci'][1]:.4f}]")
    
    # Kill gate evaluation
    print("\n" + "=" * 80)
    print("KILL GATE EVALUATION")
    print("=" * 80)
    
    rate = results['module_only_rate']
    ci_lower = results['module_only_ci'][0]
    
    print(f"Measured module_only rate: {rate:.4f} (CI95 lower bound: {ci_lower:.4f})")
    print(f"Kill gate threshold: 0.01 (1%)")
    
    if rate < 0.01:
        decision = "KILL — Close package-name line"
    elif rate < 0.05:
        decision = "HOLD — Report CI, consider larger corpus"
    else:
        decision = "BUILD — Prototype resolver integration"
    
    print(f"Decision: {decision}")
    
    # Save detailed results
    output = {
        'results': results,
        'decision': decision,
        'reports': [asdict(r) for r in classified]
    }
    
    with open('EXPERIMENTS/086-import-error-demand/results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to EXPERIMENTS/086-import-error-demand/results.json")
    
    return decision


if __name__ == "__main__":
    main()