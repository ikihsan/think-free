#!/usr/bin/env python3
"""
Select top 20 diagnosis-shaped questions by view_count for attempt sample.
Since Arm A has 0 diagnosis-shaped, use Arm B (noted as deviation).
"""

import json
from pathlib import Path

def select_sample():
    with open(Path(__file__).parent / 'screening.json') as f:
        screening = json.load(f)
    
    # Arm A diagnosis-shaped
    arm_a_diag = [r for r in screening if r['arm'] == 'A' and r['shape'] == 'diagnosis']
    # Arm B diagnosis-shaped
    arm_b_diag = [r for r in screening if r['arm'] == 'B' and r['shape'] == 'diagnosis']
    
    print(f"Arm A diagnosis-shaped: {len(arm_a_diag)}")
    print(f"Arm B diagnosis-shaped: {len(arm_b_diag)}")
    
    # Sort by view_count
    arm_a_diag.sort(key=lambda x: x['view_count'], reverse=True)
    arm_b_diag.sort(key=lambda x: x['view_count'], reverse=True)
    
    # Protocol says top 20 from Arm A, but Arm A has 0
    # Deviation: use top 20 from Arm B
    sample = arm_b_diag[:20]
    
    print(f"\nSelected {len(sample)} questions for attempt sample (from Arm B - deviation noted)")
    for i, q in enumerate(sample):
        print(f"  {i+1}. Q{q['question_id']} (views={q['view_count']}) {q['shape']}/{q['sub_shape']}: {q['title'][:70]}")
    
    # Save sample
    with open(Path(__file__).parent / 'attempt_sample.json', 'w') as f:
        json.dump(sample, f, indent=2)
    
    return sample

if __name__ == '__main__':
    select_sample()