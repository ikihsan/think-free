#!/usr/bin/env python3
"""
Scoring utilities for recurring expense detection.
"""

from statistics import mean, stdev
from typing import List, Tuple, Optional


# Target intervals in days (with tolerance)
TARGET_INTERVALS = {
    "weekly": (7, 2),
    "biweekly": (14, 2),
    "monthly": (30, 3),
    "quarterly": (91, 5),
    "semiannual": (182, 7),
    "annual": (365, 10),
}


def coefficient_of_variation(values: List[float]) -> float:
    """Compute coefficient of variation (std/mean). Returns inf if mean is 0."""
    if len(values) < 2:
        return float('inf')
    m = mean(values)
    if m == 0:
        return float('inf')
    return stdev(values) / abs(m)


def median_absolute_deviation(values: List[float]) -> float:
    """Compute median absolute deviation from median."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    mid = len(sorted_vals) // 2
    median = sorted_vals[mid] if len(sorted_vals) % 2 == 1 else (sorted_vals[mid-1] + sorted_vals[mid]) / 2
    deviations = [abs(v - median) for v in values]
    deviations.sort()
    mid = len(deviations) // 2
    return deviations[mid] if len(deviations) % 2 == 1 else (deviations[mid-1] + deviations[mid]) / 2


def detect_interval_pattern(gaps: List[int]) -> Tuple[Optional[str], float, float]:
    """
    Detect the most likely interval pattern from a list of day gaps.
    Returns: (interval_name, regularity_score, expected_interval_days)
    """
    if len(gaps) < 2:
        return None, 0.0, 0.0

    best_interval = None
    best_score = 0.0
    best_expected = 0.0

    for name, (target, tolerance) in TARGET_INTERVALS.items():
        # Count gaps that fall within tolerance
        matches = sum(1 for g in gaps if abs(g - target) <= tolerance)
        if matches == 0:
            continue

        # Regularity = fraction of gaps matching this interval
        regularity = matches / len(gaps)

        # Penalize high variance in matching gaps
        matching_gaps = [g for g in gaps if abs(g - target) <= tolerance]
        if len(matching_gaps) >= 2:
            cv = coefficient_of_variation(matching_gaps)
            # More tolerant variance penalty: weekly with ±2 jitter has CV ~0.2
            variance_penalty = 1.0 / (1.0 + cv * 5)
        else:
            variance_penalty = 0.5  # uncertain with only 1 match

        score = regularity * variance_penalty

        if score > best_score:
            best_score = score
            best_interval = name
            best_expected = target

    return best_interval, best_score, best_expected


def amount_consistency(amounts: List[float]) -> Tuple[float, float, float]:
    """
    Compute amount consistency metrics.
    Returns: (cv, mad, median_amount)
    """
    if not amounts:
        return float('inf'), float('inf'), 0.0

    abs_amounts = [abs(a) for a in amounts]
    cv = coefficient_of_variation(abs_amounts)
    mad = median_absolute_deviation(abs_amounts)
    median_amt = sorted(abs_amounts)[len(abs_amounts) // 2]

    return cv, mad, median_amt


def compute_recurring_score(
    transaction_count: int,
    interval_regularity: float,
    amount_cv: float,
    interval_name: str,
    is_variable: bool = False
) -> float:
    """
    Compute overall recurring score (0-1).
    Higher = more likely to be a recurring expense.
    """
    if transaction_count < 3:
        return 0.0

    # Base score from interval regularity (0-1)
    score = interval_regularity

    # Amount consistency factor (0-1): lower CV = higher factor
    if amount_cv == float('inf'):
        amount_factor = 0.0
    elif amount_cv < 0.02:
        amount_factor = 1.0
    elif amount_cv < 0.05:
        amount_factor = 0.9
    elif amount_cv < 0.10:
        amount_factor = 0.7
    elif amount_cv < 0.20:
        amount_factor = 0.4
    else:
        amount_factor = 0.1

    # For variable merchants, be more tolerant
    if is_variable:
        if amount_cv < 0.15:
            amount_factor = max(amount_factor, 0.9)
        elif amount_cv < 0.30:
            amount_factor = max(amount_factor, 0.7)
        elif amount_cv < 0.50:
            amount_factor = max(amount_factor, 0.5)
        else:
            amount_factor = max(amount_factor, 0.2)

    score *= amount_factor

    # Transaction count bonus (capped)
    count_factor = min(1.0, transaction_count / 10.0)
    score = score * 0.7 + count_factor * 0.3

    # Interval type adjustment: monthly/quarterly/annual are more typical for subscriptions
    interval_bonus = {
        "weekly": 0.9,
        "biweekly": 0.95,
        "monthly": 1.0,
        "quarterly": 1.05,
        "semiannual": 1.0,
        "annual": 1.0,
    }.get(interval_name, 1.0)

    score *= interval_bonus

    return min(1.0, score)