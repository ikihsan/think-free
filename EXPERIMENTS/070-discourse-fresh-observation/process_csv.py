#!/usr/bin/env python3
"""
Process CFPB complaints CSV to JSONL for E070 fresh observation.
"""
import csv
import json
import sys
import os
from collections import Counter

def classify_outcome(company_response):
    """Classify company_response as served or unserved."""
    served_responses = {
        'Closed with monetary relief',
        'Closed with non-monetary relief',
        'Closed with explanation',
    }
    return 'served' if company_response in served_responses else 'unserved'

def main():
    csv_path = '/home/ubuntu/think-free/EXPERIMENTS/070-discourse-fresh-observation/raw/complaints.csv'
    out_path = '/home/ubuntu/think-free/EXPERIMENTS/070-discourse-fresh-observation/raw/cfpb_complaints.jsonl'
    
    print(f"Processing {csv_path}...")
    
    processed = []
    row_count = 0
    max_rows = 10000  # Limit for manageability
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            processed.append({
                'complaint_id': row.get('Complaint ID', ''),
                'product': row.get('Product', ''),
                'sub_product': row.get('Sub-product', ''),
                'issue': row.get('Issue', ''),
                'sub_issue': row.get('Sub-issue', ''),
                'company': row.get('Company', ''),
                'company_response': row.get('Company response to consumer', ''),
                'company_public_response': row.get('Company public response', ''),
                'date_received': row.get('Date received', ''),
                'date_sent_to_company': row.get('Date sent to company', ''),
                'state': row.get('State', ''),
                'zip_code': row.get('ZIP code', ''),
                'tags': row.get('Tags', ''),
                'submitted_via': row.get('Submitted via', ''),
                'timely': row.get('Timely response?', ''),
                'outcome_class': classify_outcome(row.get('Company response to consumer', '')),
                'view_count': 1,  # Each complaint = 1 arrival
            })
            row_count += 1
            if row_count % 1000 == 0:
                print(f"  Processed {row_count} rows...")
            if row_count >= max_rows:
                break
    
    print(f"\nTotal processed: {len(processed)}")
    
    # Save JSONL
    with open(out_path, 'w') as f:
        for row in processed:
            f.write(json.dumps(row) + '\n')
    
    # Print summary
    total = len(processed)
    served = sum(1 for r in processed if r['outcome_class'] == 'served')
    unserved = total - served
    
    print(f"\nSummary:")
    print(f"  Total: {total}")
    print(f"  Served: {served} ({served/total*100:.1f}%)")
    print(f"  Unserved: {unserved} ({unserved/total*100:.1f}%)")
    
    by_product = Counter(r['product'] for r in processed)
    print(f"\nBy product:")
    for prod, count in by_product.most_common():
        print(f"  {prod}: {count}")
    
    by_response = Counter(r['company_response'] for r in processed)
    print(f"\nBy company_response:")
    for resp, count in by_response.most_common():
        print(f"  {resp}: {count}")
    
    return processed

if __name__ == '__main__':
    main()