#!/usr/bin/env python3
"""
E219: World Bank projects accessibility pattern entry test
Tests whether fragmented themes (by implementing agency concentration) admit more newcomers.
Domain: International development funding (World Bank projects)
Design mirrors E208 (NIH SBIR), E209 (Federal IT), E215 (Comtrade), E218 (OpenAlex)
"""
import json
import urllib.request
import time
from collections import defaultdict
import statistics

def fetch_page(os, rows=100):
    url = f"https://search.worldbank.org/api/v2/projects?format=json&rows={rows}&fl=id,mjthemecode,impagency,boardapprovaldate,totalcommamt,project_name&os={os}"
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free research'})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

def fetch_window(offsets, rows=100):
    """Fetch all projects for given offset range."""
    all_projects = {}
    for os in offsets:
        try:
            data = fetch_page(os, rows)
            projects = data.get('projects', {})
            all_projects.update(projects)
            time.sleep(0.1)  # Be nice to the API
        except Exception as e:
            print(f"Error at offset {os}: {e}")
    return all_projects

def parse_projects(projects):
    """Parse projects into structured data by theme."""
    by_theme = defaultdict(list)
    for pid, p in projects.items():
        theme = p.get('mjthemecode')
        agency = p.get('impagency', '').strip()
        date = p.get('boardapprovaldate', '')
        amount_str = p.get('totalcommamt', '0').replace(',', '')
        try:
            amount = float(amount_str) if amount_str else 0
        except:
            amount = 0
        year = int(date[:4]) if date and len(date) >= 4 else None
        
        if theme and agency and year:
            by_theme[theme].append({
                'id': pid,
                'agency': agency,
                'year': year,
                'amount': amount
            })
    return by_theme

# Define windows
# Current: 2020-2024 (offsets 0-1800)
current_offsets = list(range(0, 1900, 100))
# Prior: 2015-2019 (offsets 2000-3000)
prior_offsets = list(range(2000, 3100, 100))

print("Fetching current window (2020-2024)...")
current_projects = fetch_window(current_offsets)
print(f"  Fetched {len(current_projects)} projects")

print("Fetching prior window (2015-2019)...")
prior_projects = fetch_window(prior_offsets)
print(f"  Fetched {len(prior_projects)} projects")

# Parse
current_by_theme = parse_projects(current_projects)
prior_by_theme = parse_projects(prior_projects)

print("\nCurrent window theme counts:")
for theme, projs in sorted(current_by_theme.items()):
    agencies = set(p['agency'] for p in projs)
    print(f"  Theme {theme}: {len(projs)} projects, {len(agencies)} agencies")

print("\nPrior window theme counts:")
for theme, projs in sorted(prior_by_theme.items()):
    agencies = set(p['agency'] for p in projs)
    print(f"  Theme {theme}: {len(projs)} projects, {len(agencies)} agencies")

# Analyze each theme with sufficient data
results = []
for theme in sorted(set(current_by_theme.keys()) | set(prior_by_theme.keys())):
    curr_projs = current_by_theme.get(theme, [])
    prior_projs = prior_by_theme.get(theme, [])
    
    curr_agencies = set(p['agency'] for p in curr_projs)
    prior_agencies = set(p['agency'] for p in prior_projs)
    
    # Skip themes with too few agencies
    if len(curr_agencies) < 5:
        continue
    
    # Fragmentation: top-5 agency share of project count in current window
    agency_counts = defaultdict(int)
    for p in curr_projs:
        agency_counts[p['agency']] += 1
    total_curr = len(curr_projs)
    top5_share = sum(sorted(agency_counts.values(), reverse=True)[:5]) / total_curr if total_curr > 0 else 0
    
    # Newcomer fraction: agencies in current but not in prior
    newcomers = curr_agencies - prior_agencies
    newcomer_frac = len(newcomers) / len(curr_agencies) if curr_agencies else 0
    
    results.append({
        'theme': theme,
        'curr_projects': total_curr,
        'curr_agencies': len(curr_agencies),
        'prior_agencies': len(prior_agencies),
        'top5_share': top5_share,
        'newcomer_frac': newcomer_frac,
        'newcomers': len(newcomers)
    })
    
    print(f"\nTheme {theme}:")
    print(f"  Current: {total_curr} projects, {len(curr_agencies)} agencies")
    print(f"  Prior: {len(prior_projs)} projects, {len(prior_agencies)} agencies")
    print(f"  Top-5 share: {top5_share:.3f}")
    print(f"  Newcomer fraction: {newcomer_frac:.3f} ({len(newcomers)}/{len(curr_agencies)})")

# Correlation analysis
if len(results) >= 5:
    import scipy.stats as stats
    top5_shares = [r['top5_share'] for r in results]
    newcomer_fracs = [r['newcomer_frac'] for r in results]
    
    rho, pval = stats.spearmanr(top5_shares, newcomer_fracs)
    print(f"\nSpearman correlation: rho={rho:.4f}, p={pval:.4f}")
    
    # Also test with fragmentation = 1 - top5_share (higher = more fragmented)
    frag = [1 - r['top5_share'] for r in results]
    rho2, pval2 = stats.spearmanr(frag, newcomer_fracs)
    print(f"Spearman (fragmentation vs newcomer): rho={rho2:.4f}, p={pval2:.4f}")
else:
    print("\nInsufficient themes for correlation analysis")

# Save raw data
import os
os.makedirs('EXPERIMENTS/E219-wb-theme-entrant-share', exist_ok=True)
with open('EXPERIMENTS/E219-wb-theme-entrant-share/raw_current.json', 'w') as f:
    json.dump(current_projects, f, indent=2)
with open('EXPERIMENTS/E219-wb-theme-entrant-share/raw_prior.json', 'w') as f:
    json.dump(prior_projects, f, indent=2)
with open('EXPERIMENTS/E219-wb-theme-entrant-share/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nDone. Data saved to EXPERIMENTS/E219-wb-theme-entrant-share/")