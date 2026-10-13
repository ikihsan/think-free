#!/usr/bin/env python3
"""
E121b — Analyze Kubernetes Discourse data with E119 matched-harvest framework.

Adapts E094 data to E119 format and applies matched-harvest measurement.
"""

import json
import sys
from pathlib import Path

# Import E119 framework
import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent.parent
e119_path = repo_root / "EXPERIMENTS" / "119-viewcount-prototype"
sys.path.insert(0, str(e119_path))
old_cwd = Path.cwd()
import os
os.chdir(e119_path)
from measure_framework import measure_framework
os.chdir(old_cwd)


def convert_k8s_to_e119_format(input_path, output_path):
    """Convert E094 classification.log.json to E119 JSONL format."""
    with open(input_path, 'r') as f:
        topics = json.load(f)
    
    converted = []
    for topic in topics:
        # Skip excluded
        if topic.get('classification') == 'excluded':
            continue
        
        # Map Discourse fields - preserve Discourse-specific fields
        row = {
            "question_id": topic.get('id'),
            "title": topic.get('title', ''),
            "body": topic.get('excerpt', '')[:200] if topic.get('excerpt') else '',
            "view_count": topic.get('views', 0),
            "answer_count": topic.get('reply_count', 0),
            "reply_count": topic.get('reply_count', 0),
            "score": 0,  # Not available
            "accepted_answer_id": "1" if topic.get('has_accepted_answer') else None,
            "has_accepted_answer": topic.get('has_accepted_answer', False),
            "tags": topic.get('tags', []),
            "combined_text": f"{topic.get('title', '')} {topic.get('excerpt', '')}",
            "original_classification": topic.get('classification'),
        }
        converted.append(row)
    
    with open(output_path, 'w') as f:
        for row in converted:
            f.write(json.dumps(row) + "\n")
    
    print(f"Converted {len(converted)} topics to {output_path}")
    return converted


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    input_path = repo_root / "EXPERIMENTS" / "094-k8s-discourse-viewcount" / "classification.log.json"
    output_path = Path(__file__).parent / "data_k8s_discourse.jsonl"
    
    convert_k8s_to_e119_format(input_path, output_path)
    
    # Run E119 measurement framework
    print("\n=== Running E119 Measurement Framework ===")
    result = measure_framework(str(output_path), coverage_floor=0.60)
    
    print(f"\nG1: {'PASS' if result['g1_pass'] else 'FAIL'}")
    print(f"G2: {'PASS' if result['g2_pass'] else 'FAIL'}")
    print(f"G3: {'PASS' if result['g3_pass'] else 'FAIL'}")
    print(f"G4: {'PASS' if result['g4_pass'] else 'FAIL'}")
    print(f"Conclusion: {result['conclusion']}")
    print(f"\nDetails:")
    print(f"  Total rows: {result['total_rows']}")
    print(f"  Coverage: {result['coverage']*100:.1f}%")
    print(f"  Classified total: {result['classified_total']}")
    print(f"  Need-related: {result['need_related']}")
    print(f"  Random: {result['random']}")
    print(f"  Unclassified: {result['unclassified']}")
    print(f"  Unserved fraction: {result['unserved_fraction']*100:.2f}%")
    print(f"  CI95: [{result['ci95'][0]*100:.2f}%, {result['ci95'][1]*100:.2f}%]")


if __name__ == "__main__":
    main()