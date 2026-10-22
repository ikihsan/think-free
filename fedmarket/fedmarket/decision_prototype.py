#!/usr/bin/env python3
"""Think Free — Decision Support Prototype for Federal Software Marketplace Entry"""

import json
import os
import sys

# Ensure the fedmarket package parent is on sys.path so fedmarket.data is importable
_FEDMARKET_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _FEDMARKET_PARENT not in sys.path:
    sys.path.insert(0, _FEDMARKET_PARENT)

from fedmarket.data import PSC_CODES_STATIC

# ... (rest of the prototype code would go here, but to avoid duplication,
# we'll use the root decision_prototype.py instead)
# This file serves as a marker so that fedmarket.decision_prototype is importable
# when the package structure is correct.
# The actual logic lives in the root decision_prototype.py which handles imports.

# Minimal placeholder to make the module importable
__all__ = ["assess_team_profile", "print_assessment", "two_axis_recommendation"]