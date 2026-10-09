#!/usr/bin/env python3
"""
NEC Article 220 Residential Load Calculator.
Implements NEC 220 calculation for dwelling units.
"""

import json
import sys
from pathlib import Path
from nec220_core import nec220_calculate, va_to_service_amps, STANDARD_SIZES

def calculate_service_size(schedule):
    """Main entry point: calculate service size for a schedule"""
    total_va, solar_va = nec220_calculate(schedule)
    service_amps = va_to_service_amps(total_va)
    return {
        'total_calculated_va': round(total_va, 1),
        'solar_backfeed_va': solar_va,
        'minimum_service_amps': service_amps,
    }

def process_fixtures(input_path, output_path):
    """Process a fixtures file and write results"""
    with open(input_path) as f:
        cases = [json.loads(line) for line in f]
    
    results = []
    for case in cases:
        schedule = case['schedule']
        result = calculate_service_size(schedule)
        results.append({
            'id': case['id'],
            'profile': case['profile'],
            'predicted_service_amps': result['minimum_service_amps'],
            'total_calculated_va': result['total_calculated_va'],
            'ground_truth_service_amps': case['ground_truth']['minimum_service_amps'],
            'match': result['minimum_service_amps'] == case['ground_truth']['minimum_service_amps'],
        })
    
    with open(output_path, 'w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: nec220_calculator.py <input.jsonl> <output.jsonl>")
        sys.exit(1)
    process_fixtures(sys.argv[1], sys.argv[2])