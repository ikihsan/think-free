"""
fedmarket — Federal Marketplace Assessment Toolkit.

Assess IT/software PSC codes in USAspending for small-team entry opportunities.
Data grounded in experiments E202-E211 (2026-10-20/21); see EXPERIMENTS/ for raw results.

This is a REVERSIBLE EXPLORATORY PROTOTYPE: it packages pre-computed analysis
from the E206 integrated CLI tool into an importable/form API without claiming
new algorithms or real-world validation. Results are grounded in observed
USAspending data with clear provenance. Two-axis mode combines accessibility
metrics (screen score, award size distribution) with sustainability metrics
(survival, graduation) from E211 entry survival analysis.

Dynamic mode queries USAspending API for current metrics and caches results locally.
Falls back to static lookup when API is unavailable, with clear provenance tracking.

Decision mode helps small software teams apply the two-axis framework
(entry accessibility vs. business sustainability) to choose a PSC code and
entry strategy matched to their characteristics.

Evidence labels (per docs/policy/evidence-labels.md):
- Observed: Directly measured from USAspending API responses
- Inferred: Derived from observed data with stated assumptions
- Speculative: Not directly measured; based on reasoning or incomplete evidence
"""

from .core import (
    assess_code,
    compare_codes,
    budget_accessible_pct,
    CODES,
    KNOWN_GRADUATION,
)

from .decision import decide_code, TWO_AXIS_CONTEXT

__version__ = "0.1.0"
__all__ = [
    "assess_code",
    "compare_codes",
    "budget_accessible_pct",
    "decide_code",
    "CODES",
    "KNOWN_GRADUATION",
    "TWO_AXIS_CONTEXT",
]