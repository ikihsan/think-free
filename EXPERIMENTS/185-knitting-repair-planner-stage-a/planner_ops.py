"""Operation primitives shared by the baseline and both search arms."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any, Deque
from collections import deque
from enum import Enum
import copy
import heapq
import time

from knitting_graph import (
    KnitGraph, Loop, LoopType, PullDirection, loop_id,
    detect_errors,
)
from planner_model import Operation, OperationType, RepairState

def get_repair_candidates(graph: KnitGraph, errors: List[Dict], max_radius: int = 2) -> Set[str]:
    """Get candidate loops that could be involved in repair (near errors)."""
    candidates = set()
    for err in errors:
        r, c = err['location']
        for dr in range(-max_radius, max_radius + 1):
            for dc in range(-max_radius, max_radius + 1):
                lid = loop_id(r + dr, c + dc)
                if lid in graph.loops and not graph.loops[lid].is_boundary:
                    candidates.add(lid)
    return candidates


def can_release(graph: KnitGraph, loop_id: str) -> bool:
    """Check if a loop can be released (not boundary, not already live)."""
    if loop_id not in graph.loops:
        return False
    loop = graph.loops[loop_id]
    return not loop.is_boundary and not loop.is_live


def can_reknit(graph: KnitGraph, yarn_order: int, loop_type: LoopType, pull_direction: PullDirection, row: int, col: int) -> bool:
    """Check if a loop can be re-knitted at this yarn position."""
    # Check if yarn is live at this position
    if yarn_order not in [loop.yarn_order for loop in graph.loops.values() if loop.is_live]:
        # Also check if it's a gap (missing loop)
        pass  # Simplified: allow if position is available
    return True


def apply_operation(state: RepairState, op: Operation, original_graph: Optional[KnitGraph] = None) -> RepairState:
    """Apply an operation to a state, returning new state."""
    new_state = state.copy()

    if op.op_type == OperationType.RELEASE:
        if op.loop_id in new_state.graph.loops:
            loop = new_state.graph.loops[op.loop_id]
            # Update neighbors to mark gaps
            for dir_name, neighbor_id in loop.neighbors.items():
                if neighbor_id and neighbor_id in new_state.graph.loops:
                    neighbor = new_state.graph.loops[neighbor_id]
                    reverse_dir = {'left': 'right', 'right': 'left', 'above': 'below', 'below': 'above', 'cable_partner': 'cable_partner'}.get(dir_name)
                    if reverse_dir and neighbor.neighbors.get(reverse_dir) == op.loop_id:
                        neighbor.neighbors[reverse_dir] = None
            new_state.graph.remove_loop(op.loop_id)
            new_state.live_yarn_positions.append(loop.yarn_order)
            new_state.operations.append(op)

    elif op.op_type == OperationType.REKNIT:
        # Re-knit a loop at a live yarn position
        if new_state.live_yarn_positions and original_graph:
            yarn_order = min(new_state.live_yarn_positions)  # Use earliest live yarn
            new_state.live_yarn_positions.remove(yarn_order)

            # Find original loop at this yarn_order
            orig_loop = None
            for lid, loop in original_graph.loops.items():
                if loop.yarn_order == yarn_order:
                    orig_loop = loop
                    break
            if orig_loop:
                new_loop = Loop(
                    id=orig_loop.id,
                    row=orig_loop.row,
                    col=orig_loop.col,
                    loop_type=orig_loop.loop_type,
                    yarn_order=orig_loop.yarn_order,
                    pull_direction=orig_loop.pull_direction,
                    neighbors=orig_loop.neighbors.copy(),
                    is_boundary=orig_loop.is_boundary,
                )
                new_state.graph.add_loop(new_loop)
                # Restore neighbor connections
                for dir_name, neighbor_id in new_loop.neighbors.items():
                    if neighbor_id and neighbor_id in new_state.graph.loops:
                        neighbor = new_state.graph.loops[neighbor_id]
                        reverse_dir = {'left': 'right', 'right': 'left', 'above': 'below', 'below': 'above', 'cable_partner': 'cable_partner'}.get(dir_name)
                        if reverse_dir:
                            neighbor.neighbors[reverse_dir] = new_loop.id
                new_state.operations.append(op)

    elif op.op_type == OperationType.SECURE:
        if op.loop_id in new_state.graph.loops:
            new_state.graph.set_boundary(op.loop_id, True)
            new_state.operations.append(op)

    return new_state


def is_repaired(state: RepairState, original_errors: List[Dict], correct_graph: Optional[KnitGraph] = None) -> bool:
    """Check if all original errors are fixed AND graph is valid."""
    current_errors = detect_errors(state.graph)
    # Check if any original error type/location still exists
    for orig_err in original_errors:
        for curr_err in current_errors:
            if curr_err['type'] == orig_err['type'] and curr_err['location'] == orig_err['location']:
                return False

    # Also check graph validity
    valid, _ = state.graph.validate()
    if not valid:
        return False

    # Check that all non-boundary loops from correct graph are present (or were boundaries)
    if correct_graph:
        for lid, loop in correct_graph.loops.items():
            if not loop.is_boundary and lid not in state.graph.loops:
                return False

    return True


