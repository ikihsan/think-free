#!/usr/bin/env python3
"""
E107 — GitHub code repositories view_count + unserved-open measurement

Run: python3 run.py
"""

import urllib.request
import json as json_mod
import sys
import time
import os
from classify import is_need, wilson_upper_bound, check_gates

def fetch_with_retry(url, headers, max_retries=3, delay=2):
    """Fetch URL with retry logic for rate limits."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            r = urllib.request.urlopen(req, timeout=30)
            data = r.read()
            return json_mod.loads(data)
        except urllib.error.HTTPError as e:
            if e.code == 403 and 'rate limit' in str(e).lower():
                wait = delay * (attempt + 1)
                print(f'Rate limited, waiting {wait}s...')
                time.sleep(wait)
                continue
            elif e.code == 404:
                return None
            raise
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
    return None

def main():
    headers = {'User-Agent': 'think-free-e107/1.0'}
    gh_token = os.environ.get('GITHUB_TOKEN')
    if gh_token:
        headers['Authorization'] = f'token {gh_token}'
        print('Using authenticated GitHub API')
    else:
        print('Using unauthenticated GitHub API (60 req/hr)')
    
    # Step 1: Search for repositories
    print('Searching for repositories...')
    search_url = 'https://api.github.com/search/repositories?q=stars:>100+is:public+fork:false&sort=stars&order=desc&per_page=50'
    search_data = fetch_with_retry(search_url, headers)
    
    if not search_data or 'items' not in search_data:
        print('Error: Could not fetch repositories')
        sys.exit(1)
    
    repos = search_data['items'][:50]
    print(f'Found {len(repos)} repositories')
    
    # Step 2: Fetch issues for each repository
    all_issues = []
    repo_stats = {}
    
    for i, repo in enumerate(repos):
        repo_name = repo['full_name']
        stars = repo['stargazers_count']
        print(f'[{i+1}/50] Fetching issues for {repo_name} ({stars} stars)...')
        
        # Fetch issues (open + closed, recent)
        issues_url = f'https://api.github.com/repos/{repo_name}/issues?state=all&per_page=30&sort=updated&direction=desc'
        issues_data = fetch_with_retry(issues_url, headers)
        
        if not issues_data:
            print(f'  Failed to fetch issues for {repo_name}')
            repo_stats[repo_name] = {'stars': stars, 'issues': 0, 'need': 0, 'unserved': 0, 'served': 0}
            time.sleep(1)
            continue
        
        # Filter out PRs (they have 'pull_request' key)
        issues = [iss for iss in issues_data if 'pull_request' not in iss]
        
        repo_need = 0
        repo_unserved = 0
        repo_served = 0
        repo_arrival_positive = 0
        
        for issue in issues:
            title = issue.get('title', '')
            state = issue.get('state', 'open')
            comments = issue.get('comments', 0)
            reactions = issue.get('reactions', {}).get('total_count', 0)
            
            # Arrival signal: reactions > 0 OR comments > 0
            if reactions > 0 or comments > 0:
                repo_arrival_positive += 1
            
            if is_need(title):
                repo_need += 1
                
                # Check if unserved: open AND no resolution indicator
                is_open = state == 'open'
                
                if is_open:
                    repo_unserved += 1
                else:
                    repo_served += 1
                
                all_issues.append({
                    'repo': repo_name,
                    'title': title,
                    'state': state,
                    'comments': comments,
                    'reactions': reactions,
                    'is_need': True,
                    'is_served': not is_open,
                    'arrival_positive': reactions > 0 or comments > 0
                })
            else:
                all_issues.append({
                    'repo': repo_name,
                    'title': title,
                    'state': state,
                    'comments': comments,
                    'reactions': reactions,
                    'is_need': False,
                    'arrival_positive': reactions > 0 or comments > 0
                })
        
        repo_stats[repo_name] = {
            'stars': stars,
            'issues': len(issues),
            'need': repo_need,
            'unserved': repo_unserved,
            'served': repo_served,
            'arrival_positive': repo_arrival_positive
        }
        
        time.sleep(1)
    
    # Aggregate results
    total_issues = len(all_issues)
    total_need = sum(1 for i in all_issues if i['is_need'])
    total_served = sum(1 for i in all_issues if i.get('is_served', False))
    total_unserved = sum(1 for i in all_issues if i['is_need'] and not i.get('is_served', True))
    total_arrival_positive = sum(1 for i in all_issues if i['arrival_positive'])
    
    # Per-repo unserved fractions
    repo_fractions = {}
    for repo_name, stats in repo_stats.items():
        need = stats['need']
        unserved = stats['unserved']
        served = stats['served']
        total_repo_need = need
        if total_repo_need > 0:
            repo_fractions[repo_name] = unserved / total_repo_need
        else:
            repo_fractions[repo_name] = 0
    
    # Classified dict for gate checking
    classified = {
        'arrival_positive': total_arrival_positive,
        'need': total_need,
        'served_count': total_served,
        'unserved_count': total_unserved,
    }
    
    # Print results
    print(f'\nTotal issues: {total_issues}')
    print(f'Need topics: {total_need}/{total_issues} = {total_need/total_issues*100:.1f}%' if total_issues > 0 else 'Need topics: N/A')
    print(f'Served: {total_served}/{total_need} = {total_served/total_need*100:.1f}%' if total_need > 0 else 'Served: N/A')
    print(f'Unserved: {total_unserved}/{total_need} = {total_unserved/total_need*100:.1f}%' if total_need > 0 else 'Unserved: N/A')
    print(f'Arrival positive: {total_arrival_positive}/{total_issues} = {total_arrival_positive/total_issues*100:.1f}%')
    print()
    
    # Per-repo summary
    print('=== PER-REPO SUMMARY ===')
    for repo_name, stats in repo_stats.items():
        need = stats['need']
        unserved = stats['unserved']
        served = stats['served']
        if need > 0:
            print(f'{repo_name}: {need} need, {served} served, {unserved} unserved ({unserved/need*100:.1f}%)')
    
    print()
    
    # Gate assessment
    print('=== GATE ASSESSMENT ===')
    gate_results = check_gates(classified, total_issues, repo_fractions)
    
    all_pass = all(r['pass'] for r in gate_results.values())
    print(f'All gates pass: {all_pass}')
    print()
    
    for gate_name, gate_info in gate_results.items():
        status = 'PASS' if gate_info['pass'] else 'FAIL'
        print(f'G{gate_name}: {status} — {gate_info["value"]}')
        print(f'  Detail: {gate_info["detail"]}')
    
    # Write results.json
    results = {
        'observed_at_utc': __import__('datetime').datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'user_date': __import__('datetime').datetime.now().strftime('%Y-%m-%d'),
        'platform': 'GitHub code repositories',
        'sample_size': total_issues,
        'repos_sampled': len(repos),
        'classified': {
            'need_topics': total_need,
            'served_topics': total_served,
            'unserved_topics': total_unserved
        },
        'arrival_metric': {
            'positive': total_arrival_positive,
            'total': total_issues
        },
        'repo_fractions': {k: f'{v:.4f}' for k, v in repo_fractions.items()},
        'repo_stats': repo_stats,
        'g1_pass': gate_results['g1']['pass'],
        'g1_details': gate_results['g1']['detail'],
        'g2_pass': gate_results['g2']['pass'],
        'g2_details': gate_results['g2']['detail'],
        'g3_pass': gate_results['g3']['pass'],
        'g3_details': gate_results['g3']['detail'],
        'g4_pass': gate_results['g4']['pass'],
        'g4_details': gate_results['g4']['detail'],
        'conclusion': 'GATE_CLOSED' if not all_pass else 'GATE_OPEN'
    }
    
    with open('results.json', 'w') as f:
        json_mod.dump(results, f, indent=2)
    
    print()
    print('Results written to results.json')
    
    # Exit code: 0 if all gates pass, 3 if any gate fails
    if not all_pass:
        sys.exit(3)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()