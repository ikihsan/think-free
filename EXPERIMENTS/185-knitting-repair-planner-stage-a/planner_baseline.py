"""A0 baseline: full-row rollback."""

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

def get_affected_rows(graph: KnitGraph, errors: List[Dict]) -> Set[int]:
    """Get the set of rows affected by errors."""
    rows = set()
    for err in errors:
        rows.add(err['location'][0])
    return rows


def full_row_rollback(error_graph: KnitGraph, correct_graph: KnitGraph, errors: List[Dict]) -> RepairState:
    """A0: Full-row rollback baseline - release all loops in affected rows and re-knit from correct graph."""
    state = RepairState(graph=error_graph.copy())
    affected_rows = get_affected_rows(error_graph, errors)

    # Release all loops in affected rows from the CORRECT graph (except boundaries)
    # This ensures we release the right loops even if some are already missing
    for row in sorted(affected_rows):
        loops_in_row = [lid for lid, loop in correct_graph.loops.items() if loop.row == row]
        for lid in loops_in_row:
            # Check if this loop exists in our current state graph
            loop = state.graph.loops.get(lid)
            if loop and not loop.is_boundary:
                # Update neighbors to mark gaps
                for dir_name, neighbor_id in loop.neighbors.items():
                    if neighbor_id and neighbor_id in state.graph.loops:
                        neighbor = state.graph.loops[neighbor_id]
                        reverse_dir = {'left': 'right', 'right': 'left', 'above': 'below', 'below': 'above', 'cable_partner': 'cable_partner'}.get(dir_name)
                        if reverse_dir and neighbor.neighbors.get(reverse_dir) == lid:
                            neighbor.neighbors[reverse_dir] = None
                # Release this loop
                state.graph.remove_loop(lid)
                state.live_yarn_positions.append(loop.yarn_order)
                state.operations.append(Operation(
                    op_type=OperationType.RELEASE,
                    loop_id=lid,
                    cost=1
                ))
            elif lid not in state.graph.loops:
                # Loop is already missing (e.g., dropped stitch) - still need to account for its yarn
                correct_loop = correct_graph.loops[lid]
                if not correct_loop.is_boundary:
                    state.live_yarn_positions.append(correct_loop.yarn_order)

    # Re-knit all released loops from the CORRECT graph
    for yarn_order in sorted(state.live_yarn_positions):
        # Find the correct loop at this yarn_order
        for lid, loop in correct_graph.loops.items():
            if loop.yarn_order == yarn_order and lid not in state.graph.loops:
                # Re-create this loop with correct neighbors
                new_loop = Loop(
                    id=lid,
                    row=loop.row,
                    col=loop.col,
                    loop_type=loop.loop_type,
                    yarn_order=loop.yarn_order,
                    pull_direction=loop.pull_direction,
                    neighbors=loop.neighbors.copy(),
                    is_boundary=loop.is_boundary,
                )
                state.graph.add_loop(new_loop)
                # Restore neighbor connections
                for dir_name, neighbor_id in new_loop.neighbors.items():
                    if neighbor_id and neighbor_id in state.graph.loops:
                        neighbor = state.graph.loops[neighbor_id]
                        reverse_dir = {'left': 'right', 'right': 'left', 'above': 'below', 'below': 'above', 'cable_partner': 'cable_partner'}.get(dir_name)
                        if reverse_dir:
                            neighbor.neighbors[reverse_dir] = lid
                state.operations.append(Operation(
                    op_type=OperationType.REKNIT,
                    loop_id=lid,
                    new_loop_type=loop.loop_type,
                    new_pull_direction=loop.pull_direction,
                    cost=1
                ))
                break

    return state


