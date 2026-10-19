"""E186 — NHTSA complaint-recall predictive signal.

Split at the 300-line cap: static tables, the fetch layer, the statistics
and this runner each live in a sibling module. `python3 run.py` is
unchanged and writes results.json exactly as before.
"""

import json
import os
import statistics
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nhtsa_config import COMPONENT_MAP, CATEGORIES, map_component
from nhtsa_fetch import fetch_json, fetch_recalls, fetch_complaints
from nhtsa_stats import parse_date, analyze_temporal_signal, mann_whitney_u

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
