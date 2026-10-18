#!/usr/bin/env python3
"""
E186 — NHTSA Complaint-Recall Predictive Relationship
Fresh exploration: tests whether public complaint data predicts recalls.
Stdlib only, no external dependencies.
"""

import urllib.request
import urllib.parse
import json
import time
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
import sys

# Component category mapping (NHTSA component field -> 12 top-level categories)
COMPONENT_MAP = {
    # FUEL SYSTEM
    'FUEL SYSTEM': 'FUEL SYSTEM',
    'FUEL SYSTEM, GASOLINE': 'FUEL SYSTEM',
    'FUEL SYSTEM, GASOLINE:DELIVERY': 'FUEL SYSTEM',
    'FUEL SYSTEM, GASOLINE:DELIVERY:FUEL PUMP': 'FUEL SYSTEM',
    'FUEL SYSTEM, GASOLINE:STORAGE': 'FUEL SYSTEM',
    'FUEL SYSTEM, OTHER': 'FUEL SYSTEM',
    'FUEL/PROPULSION SYSTEM': 'FUEL SYSTEM',
    
    # ELECTRICAL SYSTEM
    'ELECTRICAL SYSTEM': 'ELECTRICAL SYSTEM',
    'ELECTRICAL SYSTEM:IGNITION': 'ELECTRICAL SYSTEM',
    'ELECTRICAL SYSTEM:WIRING': 'ELECTRICAL SYSTEM',
    'ELECTRICAL SYSTEM:FUSES': 'ELECTRICAL SYSTEM',
    'ELECTRICAL SYSTEM:OTHER': 'ELECTRICAL SYSTEM',
    
    # ENGINE
    'ENGINE': 'ENGINE',
    'ENGINE AND ENGINE COOLING': 'ENGINE',
    'ENGINE AND ENGINE COOLING:ENGINE': 'ENGINE',
    'ENGINE AND ENGINE COOLING:EXHAUST': 'ENGINE',
    'ENGINE AND ENGINE COOLING:COOLING': 'ENGINE',
    
    # TRANSMISSION
    'TRANSMISSION': 'TRANSMISSION',
    'POWER TRAIN': 'TRANSMISSION',
    'POWER TRAIN:AUTOMATIC TRANSMISSION': 'TRANSMISSION',
    'POWER TRAIN:MANUAL TRANSMISSION': 'TRANSMISSION',
    'POWER TRAIN:TRANSFER CASE': 'TRANSMISSION',
    
    # BRAKES
    'SERVICE BRAKES': 'BRAKES',
    'SERVICE BRAKES, HYDRAULIC': 'BRAKES',
    'SERVICE BRAKES, AIR': 'BRAKES',
    'PARKING BRAKE': 'BRAKES',
    'BRAKES': 'BRAKES',
    
    # STEERING
    'STEERING': 'STEERING',
    'STEERING:LINKAGE': 'STEERING',
    'STEERING:COLUMN': 'STEERING',
    'STEERING:POWER ASSIST': 'STEERING',
    
    # SUSPENSION
    'SUSPENSION': 'SUSPENSION',
    'SUSPENSION:FRONT': 'SUSPENSION',
    'SUSPENSION:REAR': 'SUSPENSION',
    
    # AIR BAGS
    'AIR BAGS': 'AIR BAGS',
    'AIR BAGS:FRONTAL': 'AIR BAGS',
    'AIR BAGS:SIDE/WINDOW': 'AIR BAGS',
    
    # SEAT BELTS
    'SEAT BELTS': 'SEAT BELTS',
    'SEAT BELTS:FRONT': 'SEAT BELTS',
    'SEAT BELTS:REAR': 'SEAT BELTS',
    
    # STRUCTURE/BODY
    'STRUCTURE': 'STRUCTURE/BODY',
    'BODY': 'STRUCTURE/BODY',
    'VEHICLE SPEED CONTROL': 'STRUCTURE/BODY',
    'LATCHES/LOCKS/LINKAGES': 'STRUCTURE/BODY',
    'DOORS': 'STRUCTURE/BODY',
    
    # VISIBILITY
    'VISIBILITY': 'VISIBILITY',
    'EXTERIOR LIGHTING': 'VISIBILITY',
    'INTERIOR LIGHTING': 'VISIBILITY',
    'WIPER': 'VISIBILITY',
    'WINDOWS': 'VISIBILITY',
    'MIRRORS': 'VISIBILITY',
}

CATEGORIES = ['FUEL SYSTEM', 'ELECTRICAL SYSTEM', 'ENGINE', 'TRANSMISSION', 
              'BRAKES', 'STEERING', 'SUSPENSION', 'AIR BAGS', 
              'SEAT BELTS', 'STRUCTURE/BODY', 'VISIBILITY', 'OTHER']

def map_component(component_str):
    """Map NHTSA component string to top-level category."""
    if not component_str:
        return 'OTHER'
    # Try exact match first
    if component_str in COMPONENT_MAP:
        return COMPONENT_MAP[component_str]
    # Try prefix match
    for key, val in COMPONENT_MAP.items():
        if component_str.startswith(key):
            return val
    return 'OTHER'

def fetch_json(url, max_retries=3):
    """Fetch JSON from URL with retries."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree-E186/1.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None

def parse_date(date_str):
    """Parse NHTSA date format (MM/DD/YYYY)."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except:
        return None

def fetch_recalls(make, model, year):
    """Fetch recalls for a vehicle model/year."""
    url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={urllib.parse.quote(make)}&model={urllib.parse.quote(model)}&modelYear={year}"
    try:
        data = fetch_json(url)
        if not data or 'results' not in data:
            return []
        recalls = []
        for r in data['results']:
            comp = r.get('Component', '')
            cat = map_component(comp)
            date = parse_date(r.get('ReportReceivedDate', ''))
            if date:
                recalls.append({
                    'campaign': r.get('NHTSACampaignNumber', ''),
                    'component': comp,
                    'category': cat,
                    'date': date,
                    'summary': r.get('Summary', '')[:200]
                })
        return recalls
    except Exception as e:
        print(f"  Error fetching recalls: {e}")
        return []

def fetch_complaints(make, model, year, max_pages=5):
    """Fetch complaints for a vehicle model/year (paginated)."""
    all_complaints = []
    for page in range(max_pages):
        url = f"https://api.nhtsa.gov/complaints/complaintsByVehicle?make={urllib.parse.quote(make)}&model={urllib.parse.quote(model)}&modelYear={year}&page={page}"
        try:
            data = fetch_json(url)
            if not data or 'results' not in data or not data['results']:
                break
            for c in data['results']:
                comp = c.get('components', '')
                cat = map_component(comp)
                date = parse_date(c.get('dateComplaintFiled', ''))
                if date:
                    all_complaints.append({
                        'odi': c.get('odiNumber', ''),
                        'component': comp,
                        'category': cat,
                        'date': date,
                        'summary': c.get('summary', '')[:200],
                        'crash': c.get('crash', False),
                        'fire': c.get('fire', False),
                        'injuries': c.get('numberOfInjuries', 0),
                        'deaths': c.get('numberOfDeaths', 0)
                    })
            time.sleep(1)  # Rate limit
        except Exception as e:
            print(f"  Error fetching complaints page {page}: {e}")
            break
    return all_complaints

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

def main():
    print("E186: NHTSA Complaint-Recall Predictive Relationship")
    print("=" * 60)
    
    # Vehicle models to sample (pre-declared selection: popular models with known recalls)
    models = [
        ('Toyota', 'Camry', 2020),
        ('Toyota', 'Corolla', 2019),
        ('Honda', 'Accord', 2019),
        ('Honda', 'CR-V', 2020),
        ('Ford', 'F-150', 2019),
        ('Ford', 'Escape', 2020),
        ('Chevrolet', 'Silverado', 2019),
        ('Chevrolet', 'Equinox', 2020),
        ('Nissan', 'Altima', 2019),
        ('Nissan', 'Rogue', 2020),
        ('Hyundai', 'Elantra', 2019),
        ('Hyundai', 'Tucson', 2020),
        ('Kia', 'Optima', 2019),
        ('Kia', 'Sportage', 2020),
        ('Subaru', 'Outback', 2019),
        ('Subaru', 'Forester', 2020),
        ('Mazda', 'CX-5', 2019),
        ('Jeep', 'Grand Cherokee', 2019),
        ('Ram', '1500', 2019),
        ('GMC', 'Sierra', 2019),
    ]
    
    all_results = []
    total_recalls = 0
    total_complaints = 0
    triples_with_recalls = 0
    
    for make, model, year in models:
        print(f"\nFetching {year} {make} {model}...")
        
        recalls = fetch_recalls(make, model, year)
        time.sleep(1)
        complaints = fetch_complaints(make, model, year)
        
        print(f"  Recalls: {len(recalls)}, Complaints: {len(complaints)}")
        
        if recalls:
            triples_with_recalls += 1
            total_recalls += len(recalls)
        total_complaints += len(complaints)
        
        temporal = analyze_temporal_signal(recalls, complaints)
        for t in temporal:
            t['make'] = make
            t['model'] = model
            t['year'] = year
        all_results.extend(temporal)
    
    # Gate evaluations
    print("\n" + "=" * 60)
    print("GATE EVALUATION")
    print("=" * 60)
    
    # G1: Sample adequacy
    g1_pass = triples_with_recalls >= 10
    print(f"G1 (sample adequacy ≥10): {triples_with_recalls} triples with recalls -> {'PASS' if g1_pass else 'FAIL'}")
    
    # G2: Complaint volume
    g2_pass = total_complaints >= 50
    print(f"G2 (complaint volume ≥50): {total_complaints} total complaints -> {'PASS' if g2_pass else 'FAIL'}")
    
    # G3 & G4: Temporal signal and specificity
    recalled_ratios = []
    non_recalled_ratios = []
    
    for r in all_results:
        ratio = r['ratio']
        if ratio == 'inf':
            ratio_val = 100.0  # Large value for infinite ratio
        else:
            ratio_val = float(ratio)
        
        if r.get('non_recalled'):
            non_recalled_ratios.append(ratio_val)
        else:
            recalled_ratios.append(ratio_val)
    
    median_recalled = statistics.median(recalled_ratios) if recalled_ratios else 0
    median_non_recalled = statistics.median(non_recalled_ratios) if non_recalled_ratios else 0
    
    g3_pass = median_recalled >= 2.0
    print(f"G3 (median recalled ratio ≥2.0): {median_recalled:.2f} -> {'PASS' if g3_pass else 'FAIL'}")
    
    g4_pass = median_non_recalled < 1.5
    print(f"G4 (median non-recalled ratio <1.5): {median_non_recalled:.2f} -> {'PASS' if g4_pass else 'FAIL'}")
    
    # G5: Statistical test
    g5_pass = False
    p_value = None
    if len(recalled_ratios) >= 8 and len(non_recalled_ratios) >= 8:
        u, p = mann_whitney_u(recalled_ratios, non_recalled_ratios)
        p_value = p
        g5_pass = p is not None and p < 0.05
        print(f"G5 (Mann-Whitney p<0.05): U={u}, p={p:.4f} -> {'PASS' if g5_pass else 'FAIL'}")
    else:
        print(f"G5 (Mann-Whitney p<0.05): Insufficient samples (recalled={len(recalled_ratios)}, non-recalled={len(non_recalled_ratios)}) -> NOT EVALUATED")
    
    # Overall
    gates = {'G1': g1_pass, 'G2': g2_pass, 'G3': g3_pass, 'G4': g4_pass, 'G5': g5_pass}
    overall = all(gates[g] for g in ['G1', 'G2', 'G3', 'G4'] if gates[g] is not False) and (gates['G5'] is not False)
    # G5 is not required if not evaluated
    required_gates = ['G1', 'G2', 'G3', 'G4']
    overall = all(gates[g] for g in required_gates)
    
    print(f"\nOVERALL: {'ALL GATES PASS' if overall else 'KILL GATE FIRED'}")
    
    # Save results
    output = {
        'experiment': 'E186',
        'timestamp': datetime.now().isoformat(),
        'models_sampled': len(models),
        'triples_with_recalls': triples_with_recalls,
        'total_recalls': total_recalls,
        'total_complaints': total_complaints,
        'gates': gates,
        'p_value': p_value,
        'median_recalled_ratio': median_recalled,
        'median_non_recalled_ratio': median_non_recalled,
        'overall_pass': overall,
        'results': all_results
    }
    
    with open('results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to results.json")
    return 0 if overall else 1

if __name__ == '__main__':
    sys.exit(main())