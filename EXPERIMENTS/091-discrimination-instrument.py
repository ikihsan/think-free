#!/usr/bin/env python3
"""
E091 Discrimination Test — instrument: the classifier and its gates.

Split out of `091-discrimination-harness.py` at the 300-line cap. This half owns
the judgement: what a thread is, whether its title names a fault code, whether
that makes it "served", and the G1/G2/G3 gate arithmetic over labelled probes.
It performs no I/O, so it is the half a falsification test can import.

Instrument from E090, validated by the discrimination test in
`../091-discrimination-harness.py`: G1 FPR=0.000, G2 TPR=0.704, G3 FNR=0.296.

Gate thresholds (E090/D088/D095), declared before the run:
  G1 FPR < 0.10   a known-unserved probe must not be called served
  G2 TPR > 0.70   a known-served probe must be called served
  G3 FNR < 0.30   and must not be lost to conservatism
"""

import re
import math
from dataclasses import dataclass
from typing import List, Optional, Tuple


# ============================================================================
# Instrument: fault_need_classifier (from E090, validated with discrimination test)
# ============================================================================

def has_specific_error_code(title: str) -> bool:
    """Check if title contains specific error/fault code patterns.

    Patterns: "error XXX", "fault XXX", "code XXX", "0xXXXX", "E06", "10901"
    """
    patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',       # E06, E10901, etc.
        r'\b\d{4,5}\b',        # 4-5 digit codes like 10901, 1134
        r'fault\s+code',
        r'error\s+code',
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)


def fault_need_classifier(title: str, views: int, replies: int) -> str:
    """Classify a forum thread as 'served' or 'unserved'.

    Classification logic:
    - If error code present AND vendor acknowledged: served (high confidence)
    - If views > 100 AND replies > 0 AND error code present: served (community served)
    - If views > 500 AND replies == 0 AND error code present: unserved (high interest, no answers)
    - If views < 10 AND replies == 0: unserved (no interest, no answers)
    - Default: unserved (conservative)
    """
    error_code_present = has_specific_error_code(title)
    vendor_acknowledged = False  # Not available from listing alone; set True only
    # with thread content analysis

    if error_code_present and vendor_acknowledged:
        return "served"
    elif views > 100 and replies > 0 and error_code_present:
        return "served"
    elif views > 500 and replies == 0 and error_code_present:
        return "unserved"
    elif views < 10 and replies == 0:
        return "unserved"
    else:
        return "unserved"


@dataclass
class ForumEntry:
    """Represents a single forum thread entry with classification data."""
    probe_id: str
    title: str
    forum: str
    replies: int
    views: int
    expected_label: Optional[str]  # 'served' or 'unserved' for known-label probes
    predicted_label: Optional[str]  # classifier output
    forum_url: Optional[str] = None


@dataclass
class GateResults:
    """Results of discrimination test gate evaluation."""
    g1_pass: bool      # FPR < 0.10 (known-unserved not classified as served)
    g2_pass: bool      # TPR > 0.70 (known-served classified as served)
    g3_pass: bool      # FNR < 0.30 (known-served not conservatively classified)
    fpr: float         # False Positive Rate
    tpr: float         # True Positive Rate
    fnr: float         # False Negative Rate
    s_hit: int         # known-served correctly classified
    u_hit: int         # known-unserved correctly classified (i.e. NOT called served)
    n_served: int      # number of known-served probes
    n_unserved: int    # number of known-unserved probes
    wilson_served: Tuple[float, float]  # Wilson CI for TPR
    wilson_unserved: Tuple[float, float]  # Wilson CI for FPR


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float, float]:
    """Wilson score interval for binomial proportion.

    Returns (p, lower, upper) where:
    - p = k/n (proportion)
    - lower = Wilson lower bound 95% CI
    - upper = Wilson upper bound 95% CI
    If n==0, returns (0.0, 0.0, 1.0).
    """
    if n == 0:
        return (0.0, 0.0, 1.0)
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    lower = max(0.0, min(1.0, centre - half))
    upper = max(0.0, min(1.0, centre + half))
    return (p, lower, upper)


def compute_gates(entries: List[ForumEntry]) -> GateResults:
    """Compute G1/G2/G3 gate results from a list of ForumEntry objects."""
    served_entries = [e for e in entries if e.expected_label == "served"]
    unserved_entries = [e for e in entries if e.expected_label == "unserved"]

    # Known-served: classifier should say "served"
    served_correct = 0
    for entry in served_entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)
        if entry.predicted_label == "served":
            served_correct += 1

    # Known-unserved: classifier should NOT say "served" (i.e. should say "unserved")
    # FPR = proportion of known-unserved that are classified as "served"
    unserved_false_served = 0
    for entry in unserved_entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)
        if entry.predicted_label == "served":
            unserved_false_served += 1

    s_hit = served_correct
    u_hit = len(unserved_entries) - unserved_false_served  # correctly classified unserved

    n_served = len(served_entries)
    n_unserved = len(unserved_entries)

    tpr = s_hit / n_served if n_served else 0.0  # G2: TPR
    fpr = unserved_false_served / n_unserved if n_unserved else 0.0  # G1: FPR
    fnr = 1 - tpr  # G3: FNR

    # Wilson 95% CIs
    _, wilson_s_low, wilson_s_high = wilson_ci(s_hit, n_served) if n_served else (0.0, 0.0, 0.0)
    # For FPR CI, we use the "successes" = unserved_false_served out of n_unserved
    if n_unserved > 0:
        # Wilson CI for the false-served proportion
        _, wilson_u_low, wilson_u_high = wilson_ci(unserved_false_served, n_unserved)
    else:
        wilson_u_low, wilson_u_high = 0.0, 0.0

    # Gate evaluation per E090/D088/D095 criteria
    g1_pass = fpr < 0.10  # FPR < 10%
    g2_pass = tpr > 0.70  # TPR > 70%
    g3_pass = fnr < 0.30  # FNR < 30%

    # Wilson CIs for reporting
    if n_served > 0:
        tpr_centre, tpr_half = wilson_ci(s_hit, n_served)[0], abs(wilson_ci(s_hit, n_served)[0] - wilson_ci(s_hit, n_served)[1])
        wilson_served = (tpr_centre, max(0, tpr_centre - tpr_half), min(1, tpr_centre + tpr_half))
    else:
        wilson_served = (0.0, 0.0, 0.0)

    if n_unserved > 0:
        fpr_centre, fpr_half = wilson_ci(unserved_false_served, n_unserved)[0], abs(wilson_ci(unserved_false_served, n_unserved)[0] - wilson_ci(unserved_false_served, n_unserved)[1])
        wilson_unserved = (fpr_centre, max(0, fpr_centre - fpr_half), min(1, fpr_centre + fpr_half))
    else:
        wilson_unserved = (0.0, 0.0, 0.0)

    return GateResults(
        g1_pass=g1_pass,
        g2_pass=g2_pass,
        g3_pass=g3_pass,
        fpr=fpr,
        tpr=tpr,
        fnr=fnr,
        s_hit=s_hit,
        u_hit=u_hit,
        n_served=n_served,
        n_unserved=n_unserved,
        wilson_served=wilson_served,
        wilson_unserved=wilson_unserved,
    )


if __name__ == "__main__":
    # The instrument's own discrimination test on the built-in probe sets.
    # The probe sets and the runner live in 091-discrimination-harness.py.
    import sys
    sys.exit("instrument: import from 091-discrimination-harness.py to run the gates")
