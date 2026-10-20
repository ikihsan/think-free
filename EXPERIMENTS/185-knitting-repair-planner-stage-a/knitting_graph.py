"""Knitting graph representation and operations for repair planning.

Split at the 300-line cap (docs/policy/doc-standards.md): the model, the
fabric constructors, error handling and the fixture list each live in a
sibling module. This file stays the import surface so `planner.py` and the
committed results.json keep working unchanged.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import json
import copy

from graph_model import (LoopType, PullDirection, Loop, KnitGraph, loop_id)
from graph_fabrics import (
    create_stockinette_graph, create_rib_graph, create_cable_graph,
    create_garter_graph, create_seed_stitch_graph,
)
from graph_errors import introduce_error, detect_errors
from fixtures import FIXTURES

if __name__ == "__main__":
    # Test fixture creation
    for fix in FIXTURES:
        g = fix['factory']()
        valid, errors = g.validate()
        detected = detect_errors(g)
        print(f"{fix['name']}: valid={valid}, errors={errors}, detected={len(detected)}")
        for d in detected:
            print(f"  - {d}")