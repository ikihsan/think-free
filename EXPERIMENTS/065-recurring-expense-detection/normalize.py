#!/usr/bin/env python3
"""
Normalization utilities for bank transaction CSV parsing.
Handles multiple bank formats, date parsing, amount parsing, and merchant normalization.
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# Known bank format detectors
FORMAT_DETECTORS = {
    "chase": lambda row: "Transaction Date" in row and "Post Date" in row and "Description" in row,
    "boa": lambda row: "Posted Date" in row and "Reference Number" in row and "Payee" in row,
    "wells_fargo": lambda row: "Date" in row and "Amount" in row and "Description" in row,
    "generic": lambda row: "Date" in row and "Merchant" in row and "Amount" in row,
}


# Date format patterns to try
DATE_FORMATS = [
    "%m/%d/%Y",
    "%m/%d/%y",
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%Y/%m/%d",
    "%b %d, %Y",
    "%b %d %Y",
    "%d %b %Y",
]


# Merchant normalization: patterns to strip (conservative - only clear noise)
MERCHANT_STRIP_PATTERNS = [
    r'\s*\d{4,}\s*$',           # trailing numbers (store IDs, terminal IDs) - 4+ digits
    r'\s*#\d+\s*$',             # trailing #123
    r'^\s*|\s*$',               # leading/trailing whitespace
    r'\s+',                     # multiple spaces -> single space
]

# Business suffixes to strip ONLY when they appear as separate words at the end
MERCHANT_SUFFIX_PATTERNS = [
    r'\s+\b(LL[C]?|INC|CORP|CO|LTD|LLC)\b\.?$',
    r'\s+\b(COM|NET|ORG|IO|AI)\b\.?$',
    r'\s+[A-Z]{2}$',         # trailing state codes (space + 2 caps)
]

MERCHANT_REPLACEMENTS = {
    "AMAZON.COM": "AMAZON",
    "AMAZON MARKETPLACE": "AMAZON",
    "PAYPAL *": "PAYPAL",
    "SQ *": "SQUARE",
    "TST*": "",
    "SP *": "",
}


def detect_format(header: List[str]) -> str:
    """Detect CSV format from header row."""
    for fmt, detector in FORMAT_DETECTORS.items():
        if detector(header):
            return fmt
    return "unknown"


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string trying multiple formats."""
    date_str = date_str.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def parse_amount(amount_str: str) -> Optional[float]:
    """Parse amount string handling various formats."""
    amount_str = amount_str.strip()
    
    # Handle parentheses for negative (accounting format)
    if amount_str.startswith('(') and amount_str.endswith(')'):
        amount_str = '-' + amount_str[1:-1]
    
    # Remove currency symbols and commas
    amount_str = re.sub(r'[\$,]', '', amount_str)
    
    # Handle explicit signs
    if amount_str.startswith('+'):
        amount_str = amount_str[1:]
    
    try:
        return float(amount_str)
    except ValueError:
        return None


def normalize_merchant(merchant: str) -> str:
    """Normalize merchant name for grouping."""
    if not merchant:
        return ""
    
    # Uppercase for consistency
    merchant = merchant.upper().strip()
    
    # Apply replacements first
    for pattern, replacement in MERCHANT_REPLACEMENTS.items():
        if merchant.startswith(pattern):
            merchant = replacement + merchant[len(pattern):]
            break
    
    # Apply strip patterns (noise removal)
    for pattern in MERCHANT_STRIP_PATTERNS:
        merchant = re.sub(pattern, ' ', merchant, flags=re.IGNORECASE)
    
    # Apply suffix patterns (business suffixes as separate words)
    for pattern in MERCHANT_SUFFIX_PATTERNS:
        merchant = re.sub(pattern, '', merchant, flags=re.IGNORECASE)
    
    # Collapse whitespace
    merchant = re.sub(r'\s+', ' ', merchant).strip()
    
    return merchant


def parse_chase_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Parse a Chase CSV row."""
    date_str = row.get("Transaction Date", "") or row.get("Post Date", "")
    dt = parse_date(date_str)
    if not dt:
        return None
    
    amount = parse_amount(row.get("Amount", ""))
    if amount is None:
        return None
    
    merchant = normalize_merchant(row.get("Description", ""))
    if not merchant:
        return None
    
    return {
        "date": dt.date(),
        "amount": amount,
        "merchant": merchant,
        "raw_merchant": row.get("Description", ""),
        "category": row.get("Category", ""),
        "type": row.get("Type", ""),
    }


def parse_boa_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Parse a Bank of America CSV row."""
    date_str = row.get("Posted Date", "")
    dt = parse_date(date_str)
    if not dt:
        return None
    
    amount = parse_amount(row.get("Amount", ""))
    if amount is None:
        return None
    
    merchant = normalize_merchant(row.get("Payee", ""))
    if not merchant:
        return None
    
    return {
        "date": dt.date(),
        "amount": amount,
        "merchant": merchant,
        "raw_merchant": row.get("Payee", ""),
        "reference": row.get("Reference Number", ""),
    }


def parse_wells_fargo_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Parse a Wells Fargo CSV row."""
    date_str = row.get("Date", "")
    dt = parse_date(date_str)
    if not dt:
        return None
    
    amount = parse_amount(row.get("Amount", ""))
    if amount is None:
        return None
    
    merchant = normalize_merchant(row.get("Description", ""))
    if not merchant:
        return None
    
    return {
        "date": dt.date(),
        "amount": amount,
        "merchant": merchant,
        "raw_merchant": row.get("Description", ""),
    }


def parse_generic_row(row: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Parse a generic CSV row."""
    date_str = row.get("Date", "")
    dt = parse_date(date_str)
    if not dt:
        return None
    
    amount = parse_amount(row.get("Amount", ""))
    if amount is None:
        return None
    
    merchant = normalize_merchant(row.get("Merchant", ""))
    if not merchant:
        return None
    
    return {
        "date": dt.date(),
        "amount": amount,
        "merchant": merchant,
        "raw_merchant": row.get("Merchant", ""),
    }


PARSERS = {
    "chase": parse_chase_row,
    "boa": parse_boa_row,
    "wells_fargo": parse_wells_fargo_row,
    "generic": parse_generic_row,
}


def parse_csv_file(filepath: Path, fmt: str = None) -> Tuple[List[Dict[str, Any]], str]:
    """Parse a CSV file, auto-detecting format if not provided."""
    with open(filepath, 'r', newline='', encoding='utf-8', errors='ignore') as f:
        # Read header
        first_line = f.readline().strip()
        f.seek(0)
        
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        
        if fmt is None:
            fmt = detect_format(header)
        
        parser = PARSERS.get(fmt)
        if parser is None:
            raise ValueError(f"Unknown format: {fmt}")
        
        transactions = []
        for row in reader:
            parsed = parser(row)
            if parsed:
                parsed["source_file"] = filepath.name
                transactions.append(parsed)
        
        return transactions, fmt


def load_corpus(manifest_path: Path) -> Dict[str, Any]:
    """Load corpus from manifest.json."""
    import json
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    corpus = {}
    for entry in manifest:
        filepath = manifest_path.parent / entry["file"]
        if filepath.exists():
            transactions, detected_fmt = parse_csv_file(filepath, entry.get("format"))
            corpus[entry["file"]] = {
                "transactions": transactions,
                "format": detected_fmt,
                "metadata": entry,
            }
    
    return corpus


if __name__ == "__main__":
    # Test with synthetic corpus
    manifest_path = Path("/home/ubuntu/think-free/EXPERIMENTS/065-recurring-expense-detection/corpus/synthetic/manifest.json")
    corpus = load_corpus(manifest_path)
    
    print(f"Loaded {len(corpus)} files")
    for fname, data in list(corpus.items())[:3]:
        print(f"\n{fname} ({data['format']}): {len(data['transactions'])} transactions")
        for txn in data['transactions'][:5]:
            print(f"  {txn['date']} | {txn['amount']:>8.2f} | {txn['merchant']}")