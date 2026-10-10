#!/usr/bin/env python3
"""
Apply fault_need_classifier_v3 to practitioner rows from ROS Discourse.
"""

import json
import re
from typing import Dict, List
from math import sqrt

# Load practitioner rows
rows = []
with open('raw/practitioner_rows_dedup.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

# Instrument logic (fault_need_classifier_v3)
ERROR_CODE_PATTERNS = [
    r'error\s+code\s+\d+',
    r'error\s+code\s+[A-Z_]+',
    r'error\s+[A-Z_]{3,}',
    r'fault\s+code\s+\d+',
    r'fault\s+code\s+[A-Z_]+',
    r'\b(INVALID_JOINTS|NO_PATH_FOUND|EXTRAPOLATION|CONTROLLER_FAILED|PLANNING_FAILED|CONTROL_FAILED)\b',
    r'\bError\s+Code\s+\d+\b',
    r'\bError\s+[A-Z_]{3,}\b',
    r'error\s+\d+',
    r'exit\s+code\s+-?\d+',
    r'segmentation\s+fault',
    r'segfault',
    r'cmake\s+error',
    r'build\s+error',
    r'launch\s+error',
    r'runtime\s+error',
    r'assertion\s+failed',
]

SOLUTION_KEYWORDS = [
    'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair', 
    'troubleshoot', 'step by step', 'method', 'procedure',
    'resolve', 'workaround', 'patch', 'update', 'upgrade',
    'solved', 'resolved', 'fixed', 'answer', 'workaround'
]

VENDOR_KEYWORDS = [
    'official', 'documentation', 'docs.ros.org', 'github.com/ros',
    'gazebosim.org', 'openrobotics.org', 'nav2', 'ros2_control',
    'moveit', 'tf2', 'rclcpp', 'rmw', 'ament', 'colcon'
]

def has_error_code(text: str) -> bool:
    text_lower = text.lower()
    for pattern in ERROR_CODE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def has_solution_keyword(text: str) -> bool:
    text_lower = text.lower()
    for kw in SOLUTION_KEYWORDS:
        if kw in text_lower:
            return True
    return False

def has_vendor_acknowledgment(text: str) -> bool:
    text_lower = text.lower()
    for kw in VENDOR_KEYWORDS:
        if kw in text_lower:
            return True
    return False

def classify_row(row: Dict) -> str:
    """
    Apply fault_need_classifier_v3 logic.
    """
    title = row.get('title', '')
    body = row.get('body', '') or row.get('excerpt', '')
    views = row.get('views', 0)
    reply_count = row.get('reply_count', 0)
    posts_count = row.get('posts_count', 0)
    
    # Combine title and body for analysis
    full_text = f"{title} {body}"
    
    error_code_present = has_error_code(full_text)
    vendor_acknowledged = has_vendor_acknowledgment(full_text)
    has_solution = has_solution_keyword(full_text)
    
    # fault_need_classifier_v3 logic:
    if error_code_present and vendor_acknowledged:
        return "served"
    elif views > 100 and reply_count > 0 and error_code_present:
        return "served"
    elif views > 500 and reply_count == 0 and error_code_present:
        return "unserved"
    elif views < 10 and reply_count == 0:
        return "unserved"
    else:
        return "unserved"

def wilson_ci(p: float, n: int, z: float = 1.96) -> tuple:
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denominator
    half = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))

def main():
    print("Measuring population on ROS error codes practitioner rows...")
    print("=" * 60)
    
    # First, filter for actual need statements (exclude announcements)
    need_rows = []
    for row in rows:
        title = row.get('title', '').lower()
        # Exclude announcements/feature posts
        if any(kw in title for kw in ['support for', 'release', 'announcing', 'new packages', 'new releases']):
            print(f"  Excluding announcement: {row['title'][:60]}")
            continue
        need_rows.append(row)
    
    print(f"\nNeed statements: {len(need_rows)} of {len(rows)} rows")
    
    # Classify each need row
    classifications = []
    for row in need_rows:
        classification = classify_row(row)
        classifications.append({
            'topic_id': row['topic_id'],
            'title': row['title'],
            'category': row['category_name'],
            'views': row['views'],
            'reply_count': row['reply_count'],
            'classification': classification,
            'error_code_present': has_error_code(f"{row['title']} {row.get('body', '')}"),
            'vendor_acknowledged': has_vendor_acknowledgment(f"{row['title']} {row.get('body', '')}"),
        })
    
    # Count classifications
    served = [c for c in classifications if c['classification'] == 'served']
    unserved = [c for c in classifications if c['classification'] == 'unserved']
    
    print(f"\nCLASSIFICATION RESULTS:")
    print(f"  Served: {len(served)}")
    print(f"  Unserved: {len(unserved)}")
    print(f"  Total: {len(classifications)}")
    
    # Print details
    print(f"\nDetailed classifications:")
    for c in classifications:
        print(f"  [{c['classification'].upper()}] Views={c['views']} Replies={c['reply_count']} ErrorCode={c['error_code_present']} VendorAck={c['vendor_acknowledged']} | {c['title'][:70]}")
    
    # Compute fractions
    total = len(classifications)
    if total > 0:
        served_frac = len(served) / total
        unserved_frac = len(unserved) / total
        
        served_ci = wilson_ci(served_frac, total)
        unserved_ci = wilson_ci(unserved_frac, total)
        
        print(f"\nFRACTIONS (Wilson 95% CI):")
        print(f"  Served: {served_frac:.1%} (CI95: {served_ci[0]:.1%}-{served_ci[1]:.1%})")
        print(f"  Unserved: {unserved_frac:.1%} (CI95: {unserved_ci[0]:.1%}-{unserved_ci[1]:.1%})")
    
    # View count validation (G4 equivalent)
    vc_positive = sum(1 for r in need_rows if r.get('views', 0) > 0)
    vc_rate = vc_positive / len(need_rows) if need_rows else 0
    print(f"\nVIEW COUNT VALIDATION:")
    print(f"  View count > 0: {vc_positive}/{len(need_rows)} = {vc_rate:.1%}")
    
    # Save results
    output = {
        'total_rows': len(rows),
        'need_rows': len(need_rows),
        'classifications': classifications,
        'summary': {
            'served_count': len(served),
            'unserved_count': len(unserved),
            'served_fraction': served_frac if total > 0 else 0,
            'unserved_fraction': unserved_frac if total > 0 else 0,
            'served_ci95': served_ci if total > 0 else [0, 0],
            'unserved_ci95': unserved_ci if total > 0 else [0, 0],
            'view_positive_rate': vc_rate,
        }
    }
    
    with open('raw/population_measurement_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to raw/population_measurement_results.json")

if __name__ == '__main__':
    main()