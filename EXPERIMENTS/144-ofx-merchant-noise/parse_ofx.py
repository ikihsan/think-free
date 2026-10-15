#!/usr/bin/env python3
"""
Parse OFX files (SGML format) and extract transactions.
Outputs normalized transactions compatible with E065's detect.py
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

RAW_DIR = Path(__file__).parent / "raw"
OUTPUT_FILE = Path(__file__).parent / "transactions.jsonl"

# OFX date format: YYYYMMDDHHMMSS[.sss][GMT/UTC offset]
OFX_DATE_PATTERN = re.compile(r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})')

def parse_ofx_date(date_str: str) -> Optional[datetime]:
    """Parse OFX date string to datetime."""
    # Extract just the date part: YYYYMMDD
    match = OFX_DATE_PATTERN.match(date_str)
    if not match:
        return None
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return datetime(year, month, day)
    except ValueError:
        return None

def extract_transactions_from_ofx(content: str, source_file: str) -> List[Dict[str, Any]]:
    """Extract transactions from OFX content."""
    transactions = []
    
    # Find all STMTTRN blocks
    # Pattern matches <STMTTRN> ... </STMTTRN> (or self-closing style)
    stmttrn_pattern = re.compile(r'<STMTTRN>(.*?)(?=<STMTTRN>|</BANKTRANLIST>|</CREDITCARDTRANLIST>)', re.DOTALL)
    
    for match in stmttrn_pattern.finditer(content):
        trn_block = match.group(1)
        
        # Extract fields
        trntype_match = re.search(r'<TRNTYPE>([^<]+)', trn_block)
        dtposted_match = re.search(r'<DTPOSTED>([^<]+)', trn_block)
        trnamt_match = re.search(r'<TRNAMT>([^<]+)', trn_block)
        fitid_match = re.search(r'<FITID>([^<]+)', trn_block)
        name_match = re.search(r'<NAME>([^<]*)', trn_block)
        memo_match = re.search(r'<MEMO>([^<]*)', trn_block)
        
        if not dtposted_match or not trnamt_match:
            continue
        
        dt = parse_ofx_date(dtposted_match.group(1))
        if not dt:
            continue
        
        try:
            amount = float(trnamt_match.group(1))
        except ValueError:
            continue
        
        # Only process debits (expenses)
        if amount >= 0:
            continue
        
        # Build merchant string
        merchant_parts = []
        if name_match and name_match.group(1).strip():
            merchant_parts.append(name_match.group(1).strip())
        if memo_match and memo_match.group(1).strip():
            merchant_parts.append(memo_match.group(1).strip())
        
        merchant = " | ".join(merchant_parts) if merchant_parts else "UNKNOWN"
        
        transactions.append({
            "date": dt.date().isoformat(),
            "amount": amount,
            "merchant": merchant,
            "raw_name": name_match.group(1).strip() if name_match else "",
            "raw_memo": memo_match.group(1).strip() if memo_match else "",
            "fitid": fitid_match.group(1) if fitid_match else "",
            "source_file": source_file,
            "trntype": trntype_match.group(1) if trntype_match else "DEBIT"
        })
    
    return transactions

def main():
    all_transactions = []
    
    for ofx_file in RAW_DIR.glob("*.ofx"):
        print(f"Parsing {ofx_file.name}...")
        content = ofx_file.read_text(encoding='utf-8', errors='ignore')
        txns = extract_transactions_from_ofx(content, ofx_file.name)
        print(f"  Found {len(txns)} debit transactions")
        all_transactions.extend(txns)
    
    # Also check for QFX files
    for qfx_file in RAW_DIR.glob("*.qfx"):
        print(f"Parsing {qfx_file.name}...")
        content = qfx_file.read_text(encoding='utf-8', errors='ignore')
        txns = extract_transactions_from_ofx(content, qfx_file.name)
        print(f"  Found {len(txns)} debit transactions")
        all_transactions.extend(txns)
    
    # Write transactions
    with open(OUTPUT_FILE, 'w') as f:
        for txn in all_transactions:
            f.write(json.dumps(txn) + '\n')
    
    print(f"\nTotal debit transactions: {len(all_transactions)}")
    print(f"Written to {OUTPUT_FILE}")
    
    # Print unique merchants for labeling
    merchants = {}
    for txn in all_transactions:
        m = txn['merchant']
        merchants[m] = merchants.get(m, 0) + 1
    
    print(f"\nUnique merchants ({len(merchants)}):")
    for m, count in sorted(merchants.items(), key=lambda x: -x[1]):
        print(f"  [{count}] {m}")

if __name__ == "__main__":
    main()