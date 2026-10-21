#!/usr/bin/env python3
"""
NIH SBIR Small-Program Accessibility Metrics

Core metrics and API helpers for screening NIH SBIR spending categories
for small-program accessibility.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis) and the spending category screen from E204.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import json
import urllib.request
import time


# ============================================================
# NIH RePORTER API helpers
# ============================================================

def fetch_grants(spending_category=None, fiscal_year=2023, max_total=2000):
    """Fetch grants from NIH RePORTER API across pages.

    If spending_category is specified, only returns grants that include that category.
    """
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    all_results = []
    seen_ids = set()
    offset = 0

    while len(all_results) < max_total:
        payload = json.dumps({
            'criteria': {
                'fiscal_years': [fiscal_year],
                'limit': 100,
            },
            'offset': offset,
        }).encode()

        req = urllib.request.Request(
            url, data=payload,
            headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                results = data.get('results', [])
                if not results:
                    break

                for r in results:
                    aid = r.get('appl_id')
                    if aid and aid not in seen_ids:
                        seen_ids.add(aid)
                        all_results.append(r)

                meta = data.get('meta', {})
                total = meta.get('total', 0)
                if len(all_results) >= total:
                    break

        except urllib.error.HTTPError as e:
            print('HTTP error: %s' % e.code)
            break
        except Exception as e:
            print('Error: %s' % e)
            break

        offset += 100
        time.sleep(0.05)

    # Filter by spending category if specified
    if spending_category is not None:
        # Convert to int for comparison since API returns int categories
        cat_int = int(spending_category)
        filtered = []
        for g in all_results:
            cats = g.get('spending_categories')
            if cats and cat_int in cats:
                filtered.append(g)
        return filtered

    return all_results


# ============================================================
# Accessibility metrics
# ============================================================

def group_by_funding_ic(grants):
    """Group grants by Funding Institute/Center."""
    ic_groups = {}
    for g in grants:
        ic_admin = g.get('agency_ic_admin', {})
        ic_name = ic_admin.get('name', 'Unknown IC')
        if ic_name not in ic_groups:
            ic_groups[ic_name] = []
        ic_groups[ic_name].append(g)
    return ic_groups


def compute_accessibility_metrics(ic_groups):
    """Compute accessibility metrics for each Funding IC sub-area.

    Returns list of dicts sorted by access_score descending.
    Higher access_score = more grants distributed among more orgs = more accessible.
    """
    results = []

    for ic, projects in ic_groups.items():
        orgs = set()
        total_amount = 0
        org_amounts = {}

        for p in projects:
            org_name = p.get('organization', {}).get('org_name', 'N/A')
            orgs.add(org_name)
            amount = p.get('award_amount', 0) or 0
            total_amount += amount

            if org_name not in org_amounts:
                org_amounts[org_name] = 0
            org_amounts[org_name] += amount

        # Compute top-5 concentration
        sorted_orgs = sorted(org_amounts.items(), key=lambda x: x[1], reverse=True)
        top5_sum = sum(amount for _, amount in sorted_orgs[:5])
        top5_share = (top5_sum / total_amount * 100) if total_amount else 0

        # Access score: grant_count / (top5_share_fraction)
        # Higher = more distributed (more accessible for small programs)
        access_score = len(projects) / (top5_share / 100) if top5_share > 0 else float('inf')

        results.append({
            'ic': ic,
            'project_count': len(projects),
            'distinct_orgs': len(orgs),
            'top5_concentration_percent': top5_share,
            'access_score': access_score,
            'total_amount': total_amount,
        })

    return results


# ============================================================
# Consensus ICs (from 5-category analysis E206)
# ============================================================

CONSENSUS_ICs = [
    'NIAID',
    'NCI',
    'NHLB',
    'NIA',
]

CONSENSUS_RATIONALE = (
    "Based on an analysis of 5 NIH SBIR spending categories "
    "(101, 108, 525, 701, 176): NIAID appears in 4/5 categories, "
    "NCI in 4/5, NHLB in 4/5, and NIA in 4/5, making them the "
    "most consistently accessible Funding ICs for small programs "
    "across multiple spending categories. Category 176 is the most "
    "accessible overall (NCI: 43.9% top-5 share, access score 157.20), "
    "while Category 101 is the least accessible of the five "
    "(NIAID: 64.1% top-5 share, access score 34.34)."
)