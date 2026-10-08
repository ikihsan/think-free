#!/usr/bin/env python3
"""Constants and utilities for financial reconciliation experiment."""

import random
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import date, timedelta


# Deterministic descriptions for realistic variation
MERCHANT_NAMES = [
    "STARBUCKS", "AMAZON", "UBER", "LYFT", "TARGET", "WALMART", "COSTCO",
    "SHELL", "EXXON", "CHEVRON", "BP", "MCDONALDS", "CHIPOTLE", "SUBWAY",
    "APPLE", "GOOGLE", "MICROSOFT", "ADOBE", "SLACK", "ZOOM", "DROPBOX",
    "AWS", "DIGITALOCEAN", "LINODE", "GITHUB", "GITLAB", "ATLASSIAN",
    "VERIZON", "AT&T", "T-MOBILE", "COMCAST", "SPECTRUM", "PG&E", "CONED",
    "RENT", "PAYROLL", "TAX", "INSURANCE", "INTEREST", "FEE", "REFUND",
    "TRANSFER", "WIRE", "ACH", "CHECK", "DEPOSIT", "WITHDRAWAL"
]

DESCRIPTION_TEMPLATES = [
    "{merchant} {store_num}",
    "{merchant} #{store_num}",
    "{merchant} STORE {store_num}",
    "{merchant}",
    "{merchant} ONLINE",
    "{merchant} COM",
    "PAYMENT TO {merchant}",
    "PURCHASE {merchant}",
]

BANK_FEES = ["MONTHLY FEE", "OVERDRAFT FEE", "ATM FEE", "WIRE FEE", "FOREIGN TXN FEE"]
INTEREST_DESC = ["INTEREST PAYMENT", "INTEREST EARNED", "DIVIDEND"]


@dataclass
class Transaction:
    id: str
    date: str  # ISO format YYYY-MM-DD
    amount: float  # positive for credit/deposit, negative for debit/withdrawal
    description: str
    reference: Optional[str] = None
    account: Optional[str] = None  # only for ledger

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Transaction':
        return Transaction(
            id=d['id'],
            date=d['date'],
            amount=d['amount'],
            description=d['description'],
            reference=d.get('reference'),
            account=d.get('account')
        )


def levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein distance."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def random_date(base: date, max_offset: int) -> date:
    return base + timedelta(days=random.randint(-max_offset, max_offset))


def generate_description(merchant: str, variant: int = 0) -> str:
    """Generate a description with controlled variation."""
    template = random.choice(DESCRIPTION_TEMPLATES)
    store_num = random.randint(1, 9999)
    desc = template.format(merchant=merchant, store_num=store_num)
    
    # Apply variants for fuzzy matching
    if variant == 1:  # Minor typo
        if len(desc) > 3:
            idx = random.randint(0, len(desc) - 1)
            desc = desc[:idx] + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + desc[idx+1:]
    elif variant == 2:  # Abbreviation
        desc = desc.replace("STORE", "ST").replace("STREET", "ST").replace("AVENUE", "AVE")
    elif variant == 3:  # Case variation
        desc = desc.lower() if random.random() < 0.5 else desc.upper()
    elif variant == 4:  # Extra words
        desc = f"{desc} {random.choice(['INC', 'LLC', 'CORP', 'LTD', 'CO'])}"
    return desc


def generate_reference() -> str:
    """Generate a transaction reference."""
    return f"REF{random.randint(100000, 999999)}"