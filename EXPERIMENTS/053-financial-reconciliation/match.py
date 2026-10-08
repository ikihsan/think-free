#!/usr/bin/env python3
"""Main matching orchestration for financial reconciliation."""

from typing import List, Dict, Tuple, Set, DefaultDict
from collections import defaultdict
from constants import Transaction
from scoring import score_pair_fast, date_diff_days
from splits import find_split_matches_fast


DEFAULT_CONFIG = {
    'amount_exact': 100,
    'amount_close_threshold': 1.00,
    'amount_close': 50,
    'amount_loose_threshold': 10.00,
    'amount_loose': 10,
    'date_exact': 50,
    'date_close_threshold': 1,
    'date_close': 30,
    'date_loose_threshold': 3,
    'date_loose': 15,
    'date_very_loose_threshold': 5,
    'date_very_loose': 5,
    'desc_weight': 30,
    'ref_match': 200,
    'min_match_score': 100,
    'split_amount_tolerance': 0.02,
    'split_date_window': 3,
    'split_desc_threshold': 0.6,
}


def match_transactions_fast(bank_txns: List[Dict], ledger_txns: List[Dict],
                           config: dict) -> Tuple[List[Tuple[str, str, float]], List[Tuple[str, List[str]]]]:
    """
    Optimized matching using amount indexing and fast filters.
    """
    bank = [Transaction.from_dict(txn) if isinstance(txn, dict) else txn for txn in bank_txns]
    ledger = [Transaction.from_dict(txn) if isinstance(txn, dict) else txn for txn in ledger_txns]
    
    matched_bank: Set[str] = set()
    matched_ledger: Set[str] = set()
    matches: List[Tuple[str, str, float]] = []
    
    # Index ledger by amount (rounded to cents) for fast candidate retrieval
    ledger_by_amount: DefaultDict[int, List[Transaction]] = defaultdict(list)
    for txn in ledger:
        key = round(txn.amount * 100)
        ledger_by_amount[key].append(txn)
    
    max_date_window = config['date_very_loose_threshold']
    
    # Build candidate pairs using amount index
    pairs = []
    for b in bank:
        if b.id in matched_bank:
            continue
        
        # Exact amount candidates
        exact_key = round(b.amount * 100)
        candidates = ledger_by_amount.get(exact_key, [])
        
        # Close amount candidates (±$1)
        close_key1 = round((b.amount + 1.0) * 100)
        close_key2 = round((b.amount - 1.0) * 100)
        candidates.extend(ledger_by_amount.get(close_key1, []))
        candidates.extend(ledger_by_amount.get(close_key2, []))
        
        # Loose amount candidates (±$10)
        loose_key1 = round((b.amount + 10.0) * 100)
        loose_key2 = round((b.amount - 10.0) * 100)
        candidates.extend(ledger_by_amount.get(loose_key1, []))
        candidates.extend(ledger_by_amount.get(loose_key2, []))
        
        # Deduplicate candidates
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c.id not in seen and c.id not in matched_ledger:
                seen.add(c.id)
                unique_candidates.append(c)
        
        # Score candidates
        for l in unique_candidates:
            # Quick date filter before scoring
            if date_diff_days(b.date, l.date) > max_date_window:
                continue
            s = score_pair_fast(b, l, config)
            if s >= config['min_match_score']:
                pairs.append((s, b.id, l.id))
    
    # Sort by score descending
    pairs.sort(reverse=True, key=lambda x: x[0])
    
    # Greedy matching
    for score, b_id, l_id in pairs:
        if b_id not in matched_bank and l_id not in matched_ledger:
            matches.append((b_id, l_id, score))
            matched_bank.add(b_id)
            matched_ledger.add(l_id)
    
    # Find split matches
    splits = find_split_matches_fast(bank, ledger, matched_bank, matched_ledger, config)
    
    return matches, splits


def match_with_config(bank_txns: List[dict], ledger_txns: List[dict], config: dict = None) -> dict:
    """Main entry point with configurable parameters."""
    if config is None:
        config = DEFAULT_CONFIG.copy()
    
    matches, splits = match_transactions_fast(bank_txns, ledger_txns, config)
    
    return {
        'matches': [{'bank_id': b, 'ledger_id': l, 'score': s} for b, l, s in matches],
        'splits': [{'primary_id': p, 'secondary_ids': s} for p, s in splits],
        'config_used': config
    }


if __name__ == "__main__":
    # Quick test
    from generate import generate_clean_scenario
    bank, ledger, true_matches = generate_clean_scenario(42)
    result = match_with_config([txn.to_dict() for txn in bank], [txn.to_dict() for txn in ledger])
    print(f"Matches found: {len(result['matches'])}")
    print(f"Splits found: {len(result['splits'])}")
    print(f"True matches: {len(true_matches)}")
    for m in result['matches'][:5]:
        print(f"  {m}")