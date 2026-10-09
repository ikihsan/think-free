#!/usr/bin/env python3
"""
Harvest CFPB consumer complaints for E070 fresh observation.
CFPB domain: financial consumer complaints (non-technical, non-Stack-Exchange).
"""
import json
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

BASE_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

# Product categories to sample from (top-level products)
PRODUCTS = [
    "Credit reporting or other personal consumer reports",
    "Debt collection",
    "Mortgage",
    "Credit card or prepaid card",
    "Bank account or service",
    "Consumer loan",
    "Student loan",
    "Payday loan",
    "Money transfer or virtual currency",
    "Credit repair services",
]

def fetch_complaints(size=500, offset=0):
    """Fetch complaints (no product filter)."""
    params = f"?size={size}&from={offset}"
    url = BASE_URL + params
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree-E070/1.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching: {e}")
        return None

def fetch_all_complaints(target=5000):
    """Fetch complaints up to target count."""
    all_hits = []
    offset = 0
    page_size = 500
    
    while len(all_hits) < target:
        data = fetch_complaints(page_size, offset)
        if not data or not data.get('hits', {}).get('hits'):
            break
        hits = data['hits']['hits']
        all_hits.extend(hits)
        if len(hits) < page_size:
            break
        offset += page_size
        time.sleep(0.2)  # Be polite
        if len(all_hits) % 1000 == 0:
            print(f"  Fetched {len(all_hits)} so far...")
    
    return all_hits[:target]

def classify_outcome(company_response):
    """Classify company_response as served or unserved."""
    served_responses = {
        'Closed with monetary relief',
        'Closed with non-monetary relief',
        'Closed with explanation',
    }
    return 'served' if company_response in served_responses else 'unserved'

def main():
    print("Harvesting CFPB consumer complaints...")
    all_complaints = fetch_all_complaints(target=5000)
    
    print(f"\nTotal complaints harvested: {len(all_complaints)}")
    
    # Process and save
    processed = []
    for hit in all_complaints:
        src = hit['_source']
        processed.append({
            'complaint_id': src.get('complaint_id'),
            'product': src.get('product'),
            'sub_product': src.get('sub_product'),
            'issue': src.get('issue'),
            'sub_issue': src.get('sub_issue'),
            'company': src.get('company'),
            'company_response': src.get('company_response'),
            'company_public_response': src.get('company_public_response'),
            'date_received': src.get('date_received'),
            'state': src.get('state'),
            'zip_code': src.get('zip_code'),
            'submitted_via': src.get('submitted_via'),
            'timely': src.get('timely'),
            'outcome_class': classify_outcome(src.get('company_response', '')),
            'view_count': 1,  # Each complaint = 1 arrival
        })
    
    # Save raw data
    import os
    out_dir = os.path.join(os.path.dirname(__file__), 'raw')
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, 'cfpb_complaints.jsonl'), 'w') as f:
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
    
    # By product
    from collections import Counter
    by_product = Counter(r['product'] for r in processed)
    print(f"\nBy product:")
    for prod, count in by_product.most_common():
        print(f"  {prod}: {count}")
    
    # By outcome
    by_response = Counter(r['company_response'] for r in processed)
    print(f"\nBy company_response:")
    for resp, count in by_response.most_common():
        print(f"  {resp}: {count}")
    
    return processed

if __name__ == '__main__':
    main()