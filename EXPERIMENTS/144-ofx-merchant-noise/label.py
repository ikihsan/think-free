#!/usr/bin/env python3
"""
Create ground truth labels for OFX merchants.
This must be run BEFORE the detector, and labels must be committed.
"""

import json
from pathlib import Path

TRANSACTIONS_FILE = Path(__file__).parent / "transactions.jsonl"
LABELS_FILE = Path(__file__).parent / "labels.jsonl"

# Predeclared labels based on manual inspection of merchant strings
# Positive = recurring payment (subscription, utility, insurance, loan, membership, standing order)
# Negative = one-off purchase, variable retail, food, transport
# Ambiguous = cannot determine, excluded from evaluation

MERCHANT_LABELS = {
    # Actual Budget test fixtures - real merchant strings
    "STARBUCKS STORE 07604 01/21 PURC": "negative",
    "PATIENT FIRST TOKEN 01/22 PURCHA": "negative",  # medical visit, not subscription
    "URBAN FARMHOUSE NO 2 01/19 PURCH": "negative",  # restaurant
    "VERIZON DES:PAYMENTREC ID:XXXXX3": "positive",  # phone bill - recurring
    "TMOBILE*AUTO PAY 01/19 PURCHASE": "positive",   # phone bill auto-pay - recurring
    "COUNTY WASTE 01/18 PURCHASE 804-": "positive",  # trash service - recurring
    "REGENCY MART CITGO 01/18 PURCHAS": "negative",  # gas station
    "CHICK-FIL-A #01342 01/17 PURCHAS": "negative",  # restaurant
    "LOUISIANA STATE MUSEUM751 PLACE JOHN PAUL NEW ORLEANS 70116-3205LA USA": "negative",  # one-off
    
    # Test fixtures from data-payee-memo.ofx
    "Payee Name | Memo Text": "ambiguous",
    "Payee Name Only": "ambiguous",
    "Memo Only Text": "ambiguous",
    "UNKNOWN": "ambiguous",
}

def main():
    # Load transactions to get all unique merchants
    merchants = set()
    with open(TRANSACTIONS_FILE) as f:
        for line in f:
            txn = json.loads(line)
            merchants.add(txn['merchant'])
    
    print(f"Found {len(merchants)} unique merchants in transactions")
    print(f"Predeclared labels for {len(MERCHANT_LABELS)} merchants")
    
    # Check for unlabeled merchants
    unlabeled = merchants - set(MERCHANT_LABELS.keys())
    if unlabeled:
        print(f"WARNING: {len(unlabeled)} merchants have no predeclared label:")
        for m in sorted(unlabeled):
            print(f"  {m}")
    
    # Write labels
    with open(LABELS_FILE, 'w') as f:
        for merchant, label in sorted(MERCHANT_LABELS.items()):
            f.write(json.dumps({"merchant": merchant, "label": label}) + '\n')
    
    print(f"\nLabels written to {LABELS_FILE}")
    
    # Summary
    pos = sum(1 for v in MERCHANT_LABELS.values() if v == "positive")
    neg = sum(1 for v in MERCHANT_LABELS.values() if v == "negative")
    amb = sum(1 for v in MERCHANT_LABELS.values() if v == "ambiguous")
    print(f"Positive: {pos}, Negative: {neg}, Ambiguous: {amb}")

if __name__ == "__main__":
    main()