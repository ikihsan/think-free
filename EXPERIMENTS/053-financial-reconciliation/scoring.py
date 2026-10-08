#!/usr/bin/env python3
"""Scoring utilities for financial reconciliation matching."""

from datetime import date


def date_diff_days(d1: str, d2: str) -> int:
    """Absolute difference in days between two ISO dates."""
    y1, m1, d1_ = map(int, d1.split('-'))
    y2, m2, d2_ = map(int, d2.split('-'))
    date1 = date(y1, m1, d1_)
    date2 = date(y2, m2, d2_)
    return abs((date1 - date2).days)


def description_similarity_fast(desc1: str, desc2: str) -> float:
    """
    Fast token-based similarity (Jaccard on words).
    Much faster than Levenshtein for long strings.
    """
    if not desc1 and not desc2:
        return 1.0
    if not desc1 or not desc2:
        return 0.0
    
    # Tokenize: split on non-alphanumeric, uppercase
    tokens1 = set(t for t in desc1.upper().split() if t)
    tokens2 = set(t for t in desc2.upper().split() if t)
    
    if not tokens1 and not tokens2:
        return 1.0
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = len(tokens1 & tokens2)
    union = len(tokens1 | tokens2)
    return intersection / union


def score_pair_fast(bank: 'Transaction', ledger: 'Transaction', config: dict) -> float:
    """Fast scoring using token similarity."""
    score = 0.0
    
    # Amount scoring (cheap)
    amt_diff = abs(bank.amount - ledger.amount)
    if amt_diff < 0.01:
        score += config['amount_exact']
    elif amt_diff < config['amount_close_threshold']:
        score += config['amount_close']
    elif amt_diff < config['amount_loose_threshold']:
        score += config['amount_loose']
    else:
        return 0.0  # Early exit: amount too different
    
    # Date scoring (cheap)
    day_diff = date_diff_days(bank.date, ledger.date)
    if day_diff == 0:
        score += config['date_exact']
    elif day_diff <= config['date_close_threshold']:
        score += config['date_close']
    elif day_diff <= config['date_loose_threshold']:
        score += config['date_loose']
    elif day_diff <= config['date_very_loose_threshold']:
        score += config['date_very_loose']
    else:
        return 0.0  # Early exit: date too far
    
    # Description scoring (fast token-based)
    desc_sim = description_similarity_fast(bank.description, ledger.description)
    score += desc_sim * config['desc_weight']
    
    # Reference scoring (strong signal if both present and match)
    if bank.reference and ledger.reference and bank.reference == ledger.reference:
        score += config['ref_match']
    
    return score