#!/usr/bin/env python3
"""
Shared constants and utilities for E100 experiment.
"""

from dataclasses import dataclass
from math import sqrt

# Labels
LABEL_SERVED = 'served'
LABEL_UNSERVED_OPEN_LIKE = 'unserved-open-like'
LABEL_NOT_A_NEED = 'not_a_need'

# Seeded control items (pre-declared in PROTOCOL.md - adapted for industrial automation domain)
SEED_CONTROLS = {
    's1': {'label': LABEL_SERVED, 'text': 'Is there a tool to look up error code 0x8001 from Allen-Bradley CompactLogix?', 'rationale': 'names a well-known solution pattern (vendor error code lookup)'},
    's2': {'label': LABEL_SERVED, 'text': 'Need a database to interpret fault code 0x1234 from Siemens S7-1500', 'rationale': 'names a well-known solution pattern'},
    'u1': {'label': LABEL_UNSERVED_OPEN_LIKE, 'text': 'Need a tool to interpret error code 0x5678 from my Modbus device', 'rationale': 'concrete need, no code tool named'},
    'u2': {'label': LABEL_UNSERVED_OPEN_LIKE, 'text': 'Need a database to decode fault messages from my OPC UA server', 'rationale': 'concrete need, no tool named'},
}


@dataclass
class Classification:
    item_id: str
    label: str
    rationale: str
    title: str
    body: str
    view_count: int
    fault_codes: list
    instrument_types: list


def wilson_ci_lower(p, n, z=1.96):
    """Wilson score interval lower bound."""
    if n == 0:
        return 0.0
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjustment = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - adjustment) / denominator


def wilson_ci_upper(p, n, z=1.96):
    """Wilson score interval upper bound."""
    if n == 0:
        return 1.0
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjustment = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre + adjustment) / denominator