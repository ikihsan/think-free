#!/usr/bin/env python3
"""Split transaction matching for financial reconciliation."""

from typing import List, Dict, Set, Tuple, DefaultDict
from collections import defaultdict
from scoring import date_diff_days, description_similarity_fast


def find_split_matches_fast(bank_txns: List['Transaction'], ledger_txns: List['Transaction'],
                           matched_bank: Set[str], matched_ledger: Set[str],
                           config: dict) -> List[Tuple[str, List[str]]]:
    """Find 1:many matches using amount indexing."""
    splits = []
    
    # Build unmatched lists
    unmatched_bank = [txn for txn in bank_txns if txn.id not in matched_bank]
    unmatched_ledger = [txn for txn in ledger_txns if txn.id not in matched_ledger]
    
    # Index unmatched ledger by amount (rounded)
    ledger_by_amount: DefaultDict[int, List['Transaction']] = defaultdict(list)
    for txn in unmatched_ledger:
        key = round(txn.amount * 100)  # cents as integer
        ledger_by_amount[key].append(txn)
    
    # Check bank -> ledger splits
    for bank in unmatched_bank:
        target_cents = round(bank.amount * 100)
        # Look for pairs of ledger txns that sum to bank amount
        for amt1_cents, txns1 in ledger_by_amount.items():
            amt2_cents = target_cents - amt1_cents
            if amt2_cents not in ledger_by_amount:
                continue
            txns2 = ledger_by_amount[amt2_cents]
            
            for txn1 in txns1:
                for txn2 in txns2:
                    if txn1.id == txn2.id:
                        continue
                    # Check date proximity
                    max_date_diff = max(date_diff_days(bank.date, txn1.date), date_diff_days(bank.date, txn2.date))
                    if max_date_diff > config['split_date_window']:
                        continue
                    # Check description similarity
                    desc_sim1 = description_similarity_fast(bank.description, txn1.description)
                    desc_sim2 = description_similarity_fast(bank.description, txn2.description)
                    if min(desc_sim1, desc_sim2) >= config['split_desc_threshold']:
                        splits.append((bank.id, [txn1.id, txn2.id]))
                        matched_bank.add(bank.id)
                        matched_ledger.add(txn1.id)
                        matched_ledger.add(txn2.id)
                        break
                if bank.id in matched_bank:
                    break
            if bank.id in matched_bank:
                break
    
    # Check ledger -> bank splits (reverse)
    bank_by_amount: DefaultDict[int, List['Transaction']] = defaultdict(list)
    for txn in unmatched_bank:
        if txn.id not in matched_bank:
            key = round(txn.amount * 100)
            bank_by_amount[key].append(txn)
    
    for ledger in [txn for txn in unmatched_ledger if txn.id not in matched_ledger]:
        target_cents = round(ledger.amount * 100)
        for amt1_cents, txns1 in bank_by_amount.items():
            amt2_cents = target_cents - amt1_cents
            if amt2_cents not in bank_by_amount:
                continue
            txns2 = bank_by_amount[amt2_cents]
            
            for txn1 in txns1:
                for txn2 in txns2:
                    if txn1.id == txn2.id:
                        continue
                    max_date_diff = max(date_diff_days(ledger.date, txn1.date), date_diff_days(ledger.date, txn2.date))
                    if max_date_diff > config['split_date_window']:
                        continue
                    desc_sim1 = description_similarity_fast(ledger.description, txn1.description)
                    desc_sim2 = description_similarity_fast(ledger.description, txn2.description)
                    if min(desc_sim1, desc_sim2) >= config['split_desc_threshold']:
                        splits.append((ledger.id, [txn1.id, txn2.id]))
                        matched_ledger.add(ledger.id)
                        matched_bank.add(txn1.id)
                        matched_bank.add(txn2.id)
                        break
                if ledger.id in matched_ledger:
                    break
            if ledger.id in matched_ledger:
                break
    
    return splits