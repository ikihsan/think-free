#!/usr/bin/env python3
"""
Synthetic fixture generator for NEC 220 load calculation experiment.
Generates 100 test cases across 10 load profiles.
"""

import json
from pathlib import Path
from profiles import generate_all_cases

def main():
    output_dir = Path(__file__).parent / 'fixtures'
    output_dir.mkdir(exist_ok=True)
    
    train, val, test = generate_all_cases()
    
    # Write splits
    for split_name, split_cases in [('train', train), ('val', val), ('test', test)]:
        with open(output_dir / f'{split_name}.jsonl', 'w') as f:
            for case in split_cases:
                f.write(json.dumps(case) + '\n')
    
    print(f'Generated {len(train)+len(val)+len(test)} cases: train={len(train)}, val={len(val)}, test={len(test)}')
    
    # Print profile distribution in test set
    test_profiles = [c['profile'] for c in test]
    for profile in set(test_profiles):
        count = test_profiles.count(profile)
        print(f'  Test {profile}: {count} cases')

if __name__ == '__main__':
    main()