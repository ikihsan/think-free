"""
fedmarket — Federal Marketplace Assessment Toolkit.

Assess IT/software PSC codes in USAspending for small-team entry opportunities.
Data grounded in experiments E202-E211 (2026-10-20/21).

This is a REVERSIBLE EXPLORATORY PROTOTYPE: it packages pre-computed analysis
from the E206 integrated CLI tool into an importable CLI without claiming
new algorithms or real-world validation. Results are grounded in observed
USAspending data with clear provenance. Two-axis mode combines accessibility
metrics (screen score, award size distribution) with sustainability metrics
(survival, graduation) from E211 entry survival analysis.
"""

# Expose submodules for direct import
from . import api
from . import recipient
from . import award
from . import keywords
from . import agency
from . import output
from . import survival
from . import subaward
from . import vehicle_sin
from . import decide
from . import cli
from . import explore

__version__ = "0.1.0"
__author__ = "Think Free Research"
__license__ = "MIT"

__all__ = [
    "api",
    "recipient",
    "award",
    "keywords",
    "agency",
    "output",
    "survival",
    "subaward",
    "vehicle_sin",
    "decide",
    "cli",
    "explore",
]