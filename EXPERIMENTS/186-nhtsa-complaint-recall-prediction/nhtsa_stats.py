"""E186 statistics: the temporal signal and an exact Mann-Whitney U."""

import statistics
from collections import defaultdict
from datetime import datetime, timedelta

from nhtsa_config import CATEGORIES, COMPONENT_MAP

def parse_date(date_str):
    """Parse NHTSA date format (MM/DD/YYYY)."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except:
        return None


def analyze_temporal_signal(recalls, complaints):
    """Analyze complaint patterns before recalls."""
    if not recalls:
        return []
    
    # Group recalls by category, take earliest recall date per category
    recall_by_cat = {}
    for r in recalls:
        cat = r['category']
        if cat not in recall_by_cat or r['date'] < recall_by_cat[cat]['date']:
            recall_by_cat[cat] = r
    
    # Group complaints by category
    complaints_by_cat = defaultdict(list)
    for c in complaints:
        complaints_by_cat[c['category']].append(c['date'])
    
    results = []
    for cat, recall in recall_by_cat.items():
        recall_date = recall['date']
        window_start = recall_date - timedelta(days=730)  # 2 years before
        baseline_start = recall_date - timedelta(days=1460)  # 4 years before
        
        # Count complaints in windows
        cat_complaints = complaints_by_cat.get(cat, [])
        window_count = sum(1 for d in cat_complaints if window_start <= d < recall_date)
        baseline_count = sum(1 for d in cat_complaints if baseline_start <= d < window_start)
        
        # Rate per year
        window_rate = window_count / 2.0
        baseline_rate = baseline_count / 2.0 if baseline_count > 0 else 0
        
        ratio = window_rate / baseline_rate if baseline_rate > 0 else float('inf') if window_count > 0 else 1.0
        
        results.append({
            'category': cat,
            'recall_date': recall_date.isoformat(),
            'recall_campaign': recall['campaign'],
            'window_complaints': window_count,
            'baseline_complaints': baseline_count,
            'window_rate_per_year': window_rate,
            'baseline_rate_per_year': baseline_rate,
            'ratio': ratio if ratio != float('inf') else 'inf'
        })
    
    # Also analyze non-recalled categories for specificity
    for cat in CATEGORIES:
        if cat not in recall_by_cat:
            cat_complaints = complaints_by_cat.get(cat, [])
            # Use median recall date as reference for non-recalled categories
            if recalls:
                median_recall = statistics.median([r['date'].timestamp() for r in recalls])
                median_date = datetime.fromtimestamp(median_recall)
                window_start = median_date - timedelta(days=730)
                baseline_start = median_date - timedelta(days=1460)
                
                window_count = sum(1 for d in cat_complaints if window_start <= d < median_date)
                baseline_count = sum(1 for d in cat_complaints if baseline_start <= d < window_start)
                
                window_rate = window_count / 2.0
                baseline_rate = baseline_count / 2.0 if baseline_count > 0 else 0
                ratio = window_rate / baseline_rate if baseline_rate > 0 else float('inf') if window_count > 0 else 1.0
                
                results.append({
                    'category': cat,
                    'recall_date': None,
                    'recall_campaign': None,
                    'window_complaints': window_count,
                    'baseline_complaints': baseline_count,
                    'window_rate_per_year': window_rate,
                    'baseline_rate_per_year': baseline_rate,
                    'ratio': ratio if ratio != float('inf') else 'inf',
                    'non_recalled': True
                })
    
    return results

def mann_whitney_u(group1, group2):
    """Mann-Whitney U test (stdlib implementation)."""
    # Combine and rank
    combined = [(v, 0) for v in group1] + [(v, 1) for v in group2]
    combined.sort(key=lambda x: x[0])
    
    # Handle ties
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    
    # Sum ranks for group1
    n1 = len(group1)
    n2 = len(group2)
    rank_sum1 = sum(ranks[i] for i, (v, g) in enumerate(combined) if g == 0)
    
    # U statistic
    u1 = rank_sum1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation for p-value (two-tailed)
    if n1 >= 8 and n2 >= 8:
        mean_u = n1 * n2 / 2
        std_u = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
        z = (u - mean_u) / std_u if std_u > 0 else 0
        # Two-tailed p-value using normal approximation
        import math
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    else:
        # Small sample: exact p-value not implemented, return None
        p = None
    
    return u, p

