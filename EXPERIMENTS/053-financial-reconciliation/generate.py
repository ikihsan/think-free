#!/usr/bin/env python3
"""Synthetic data generation for financial reconciliation experiment."""

from constants import (
    Transaction, MERCHANT_NAMES, BANK_FEES, INTEREST_DESC,
    generate_description, generate_reference, random_date
)
from datetime import date, timedelta
import random


def generate_clean_scenario(seed: int, n_pairs: int = 80, n_bank_only: int = 10, n_ledger_only: int = 10) -> tuple:
    """Generate clean scenario with exact matches."""
    random.seed(seed)
    base_date = date(2024, 1, 15)
    
    bank_txns = []
    ledger_txns = []
    matches = []  # list of (bank_id, ledger_id)
    
    # Generate matched pairs
    for i in range(n_pairs):
        merchant = random.choice(MERCHANT_NAMES)
        amount = round(random.uniform(5.0, 5000.0), 2) * random.choice([1, -1])
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        desc = generate_description(merchant, variant=0)
        ref = generate_reference()
        
        bank_id = f"B{i:04d}"
        ledger_id = f"L{i:04d}"
        
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
    
    # Bank-only transactions (fees, interest)
    for i in range(n_bank_only):
        fee_type = random.choice(BANK_FEES + INTEREST_DESC)
        amount = round(random.uniform(0.5, 50.0), 2) * (-1 if "FEE" in fee_type else 1)
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_id = f"B{n_pairs+i:04d}"
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, fee_type, generate_reference()))
    
    # Ledger-only transactions (outstanding checks)
    for i in range(n_ledger_only):
        amount = round(random.uniform(10.0, 2000.0), 2) * -1
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        ledger_id = f"L{n_pairs+i:04d}"
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, f"CHECK #{random.randint(1000,9999)}", generate_reference(), f"ACC{random.randint(1,5)}"))
    
    return bank_txns, ledger_txns, matches


def generate_realistic_scenario(seed: int, n_clean: int = 60, n_fuzzy: int = 20, n_partial: int = 10,
                                 n_bank_only: int = 5, n_ledger_only: int = 5, n_split: int = 5) -> tuple:
    """Generate realistic scenario with various matching challenges."""
    random.seed(seed)
    base_date = date(2024, 1, 15)
    
    bank_txns = []
    ledger_txns = []
    matches = []  # list of (bank_id, ledger_id) or (bank_id, [ledger_ids]) for splits
    
    idx = 0
    
    # Clean matches
    for i in range(n_clean):
        merchant = random.choice(MERCHANT_NAMES)
        amount = round(random.uniform(5.0, 5000.0), 2) * random.choice([1, -1])
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        desc = generate_description(merchant, variant=0)
        ref = generate_reference()
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Fuzzy matches (date shift, description variation)
    for i in range(n_fuzzy):
        merchant = random.choice(MERCHANT_NAMES)
        amount = round(random.uniform(5.0, 5000.0), 2) * random.choice([1, -1])
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date + timedelta(days=random.randint(-1, 1))
        ledger_date = base_txn_date + timedelta(days=random.randint(-1, 1))
        desc_variant = random.randint(1, 3)
        bank_desc = generate_description(merchant, variant=desc_variant)
        ledger_desc = generate_description(merchant, variant=random.randint(0, desc_variant))
        ref = generate_reference() if random.random() < 0.7 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), amount, bank_desc, ref))
        ledger_txns.append(Transaction(ledger_id, ledger_date.isoformat(), amount, ledger_desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Partial matches (bank fee deducted)
    for i in range(n_partial):
        merchant = random.choice(MERCHANT_NAMES)
        ledger_amount = round(random.uniform(50.0, 5000.0), 2) * -1
        fee = round(random.uniform(0.3, 5.0), 2)
        bank_amount = ledger_amount - fee  # more negative
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date + timedelta(days=random.randint(-1, 1))
        ledger_date = base_txn_date
        desc = generate_description(merchant, variant=0)
        ref = generate_reference() if random.random() < 0.8 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), bank_amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id, ledger_date.isoformat(), ledger_amount, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Bank-only
    for i in range(n_bank_only):
        fee_type = random.choice(BANK_FEES + INTEREST_DESC)
        amount = round(random.uniform(0.5, 50.0), 2) * (-1 if "FEE" in fee_type else 1)
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_id = f"B{idx:04d}"
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, fee_type, generate_reference()))
        idx += 1
    
    # Ledger-only
    for i in range(n_ledger_only):
        amount = round(random.uniform(10.0, 2000.0), 2) * -1
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        ledger_id = f"L{idx:04d}"
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, f"CHECK #{random.randint(1000,9999)}", generate_reference(), f"ACC{random.randint(1,5)}"))
        idx += 1
    
    # Split/merged: one bank txn matches two ledger txns
    for i in range(n_split):
        merchant = random.choice(MERCHANT_NAMES)
        amount1 = round(random.uniform(20.0, 500.0), 2) * -1
        amount2 = round(random.uniform(20.0, 500.0), 2) * -1
        bank_amount = amount1 + amount2
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date
        ledger_date = base_txn_date + timedelta(days=random.randint(-1, 1))
        desc = generate_description(merchant, variant=0)
        ref = generate_reference() if random.random() < 0.6 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id1 = f"L{idx:04d}"
        ledger_id2 = f"L{idx+1:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), bank_amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id1, ledger_date.isoformat(), amount1, desc, ref, f"ACC{random.randint(1,5)}"))
        ledger_txns.append(Transaction(ledger_id2, ledger_date.isoformat(), amount2, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, [ledger_id1, ledger_id2]))
        idx += 2
    
    return bank_txns, ledger_txns, matches


def generate_adversarial_scenario(seed: int, n_clean: int = 40, n_fuzzy: int = 20, n_partial: int = 15,
                                   n_bank_only: int = 10, n_ledger_only: int = 10, n_split: int = 5) -> tuple:
    """Generate adversarial scenario with harder matching challenges."""
    random.seed(seed)
    base_date = date(2024, 1, 15)
    
    bank_txns = []
    ledger_txns = []
    matches = []
    
    idx = 0
    
    # Clean matches
    for i in range(n_clean):
        merchant = random.choice(MERCHANT_NAMES)
        amount = round(random.uniform(5.0, 5000.0), 2) * random.choice([1, -1])
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        desc = generate_description(merchant, variant=0)
        ref = generate_reference()
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Fuzzy matches (larger date shifts, more description variation)
    for i in range(n_fuzzy):
        merchant = random.choice(MERCHANT_NAMES)
        amount = round(random.uniform(5.0, 5000.0), 2) * random.choice([1, -1])
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date + timedelta(days=random.randint(-3, 3))
        ledger_date = base_txn_date + timedelta(days=random.randint(-3, 3))
        desc_variant = random.randint(2, 4)
        bank_desc = generate_description(merchant, variant=desc_variant)
        ledger_desc = generate_description(merchant, variant=random.randint(0, desc_variant))
        ref = generate_reference() if random.random() < 0.5 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), amount, bank_desc, ref))
        ledger_txns.append(Transaction(ledger_id, ledger_date.isoformat(), amount, ledger_desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Partial matches (FX rounding, larger fees)
    for i in range(n_partial):
        merchant = random.choice(MERCHANT_NAMES)
        ledger_amount = round(random.uniform(100.0, 10000.0), 2) * -1
        fee = round(random.uniform(1.0, 50.0), 2)
        bank_amount = ledger_amount - fee
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date + timedelta(days=random.randint(-2, 2))
        ledger_date = base_txn_date
        desc = generate_description(merchant, variant=random.randint(0, 2))
        ref = generate_reference() if random.random() < 0.6 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id = f"L{idx:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), bank_amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id, ledger_date.isoformat(), ledger_amount, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, ledger_id))
        idx += 1
    
    # Bank-only
    for i in range(n_bank_only):
        fee_type = random.choice(BANK_FEES + INTEREST_DESC)
        amount = round(random.uniform(0.5, 100.0), 2) * (-1 if "FEE" in fee_type else 1)
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_id = f"B{idx:04d}"
        bank_txns.append(Transaction(bank_id, txn_date.isoformat(), amount, fee_type, generate_reference()))
        idx += 1
    
    # Ledger-only
    for i in range(n_ledger_only):
        amount = round(random.uniform(10.0, 5000.0), 2) * -1
        txn_date = base_date + timedelta(days=random.randint(0, 30))
        ledger_id = f"L{idx:04d}"
        ledger_txns.append(Transaction(ledger_id, txn_date.isoformat(), amount, f"CHECK #{random.randint(1000,9999)}", generate_reference(), f"ACC{random.randint(1,5)}"))
        idx += 1
    
    # Split/merged
    for i in range(n_split):
        merchant = random.choice(MERCHANT_NAMES)
        amount1 = round(random.uniform(50.0, 1000.0), 2) * -1
        amount2 = round(random.uniform(50.0, 1000.0), 2) * -1
        bank_amount = amount1 + amount2
        base_txn_date = base_date + timedelta(days=random.randint(0, 30))
        bank_date = base_txn_date + timedelta(days=random.randint(-1, 1))
        ledger_date = base_txn_date + timedelta(days=random.randint(-2, 2))
        desc = generate_description(merchant, variant=random.randint(0, 1))
        ref = generate_reference() if random.random() < 0.4 else None
        
        bank_id = f"B{idx:04d}"
        ledger_id1 = f"L{idx:04d}"
        ledger_id2 = f"L{idx+1:04d}"
        
        bank_txns.append(Transaction(bank_id, bank_date.isoformat(), bank_amount, desc, ref))
        ledger_txns.append(Transaction(ledger_id1, ledger_date.isoformat(), amount1, desc, ref, f"ACC{random.randint(1,5)}"))
        ledger_txns.append(Transaction(ledger_id2, ledger_date.isoformat(), amount2, desc, ref, f"ACC{random.randint(1,5)}"))
        matches.append((bank_id, [ledger_id1, ledger_id2]))
        idx += 2
    
    return bank_txns, ledger_txns, matches


def generate_scenario(scenario: str, seed: int) -> tuple:
    """Generate scenario by name."""
    if scenario == "clean":
        return generate_clean_scenario(seed)
    elif scenario == "realistic":
        return generate_realistic_scenario(seed)
    elif scenario == "adversarial":
        return generate_adversarial_scenario(seed)
    else:
        raise ValueError(f"Unknown scenario: {scenario}")


if __name__ == "__main__":
    import sys
    scenario = sys.argv[1] if len(sys.argv) > 1 else "clean"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    
    bank, ledger, matches = generate_scenario(scenario, seed)
    print(f"Generated {scenario} scenario: {len(bank)} bank txns, {len(ledger)} ledger txns, {len(matches)} true matches")
    print(f"Bank sample: {bank[0].to_dict()}")
    print(f"Ledger sample: {ledger[0].to_dict()}")
    print(f"Match sample: {matches[0]}")