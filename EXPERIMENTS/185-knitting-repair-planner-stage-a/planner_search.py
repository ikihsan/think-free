"""A1 prioritized search and A2 exhaustive search."""

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
from planner_ops import (get_repair_candidates, can_release, can_reknit,
                       apply_operation, is_repaired)

def local_planner_search(error_graph: KnitGraph, correct_graph: KnitGraph, errors: List[Dict], max_steps: int = 20) -> Optional[RepairState]:
    """A1: Local planner using BFS over valid operations."""
    # Priority queue: (cost, steps, state)
    # Use cost as primary, steps as tiebreaker
    initial_state = RepairState(graph=error_graph.copy())
    # Mark boundary loops as secure
    for lid, loop in initial_state.graph.loops.items():
        if loop.is_boundary:
            initial_state.operations.append(Operation(OperationType.SECURE, lid, cost=0))

    # For dropped stitches, the yarn is already live at that position
    # Add their yarn_orders from the correct graph to live_yarn_positions
    for err in errors:
        if err['type'] == 'dropped_stitch':
            lid = err['loop_id']
            if lid in correct_graph.loops:
                initial_state.live_yarn_positions.append(correct_graph.loops[lid].yarn_order)

    # Get candidate loops near errors
    candidates = get_repair_candidates(error_graph, errors, max_radius=2)

    # Identify error loops (loops that have errors) for prioritization
    error_loop_ids = set()
    for err in errors:
        error_loop_ids.add(err['loop_id'])

    # Priority queue: (total_cost, steps, state_id, state)
    # state_id ensures tiebreaking
    state_id = 0
    pq: List[Tuple[int, int, int, RepairState]] = [(0, 0, state_id, initial_state)]
    visited: Set[str] = set()

    def state_signature(state: RepairState) -> str:
        # Signature based on which loops exist, their types, and pull directions
        sig_parts = []
        for lid in sorted(state.graph.loops.keys()):
            loop = state.graph.loops[lid]
            sig_parts.append(f"{lid}:{loop.loop_type.value}:{loop.pull_direction.value}:{loop.yarn_order}")
        return "|".join(sig_parts)

    while pq:
        cost, steps, _, state = heapq.heappop(pq)

        sig = state_signature(state)
        if sig in visited:
            continue
        visited.add(sig)

        if steps > max_steps:
            continue

        # Check if repaired
        if is_repaired(state, errors, correct_graph):
            return state

        # Generate possible operations
        # PRIORITY 1: Re-knit operations (for each live yarn position) - do these first!
        for yarn_order in state.live_yarn_positions:
            # Find original loop at this yarn_order from correct graph
            orig_loop = None
            for lid, loop in correct_graph.loops.items():
                if loop.yarn_order == yarn_order:
                    orig_loop = loop
                    break
            if orig_loop and orig_loop.id not in state.graph.loops:
                new_state = apply_operation(state, Operation(
                    OperationType.REKNIT,
                    orig_loop.id,
                    new_loop_type=orig_loop.loop_type,
                    new_pull_direction=orig_loop.pull_direction
                ), correct_graph)
                new_cost = new_state.total_cost()
                heapq.heappush(pq, (new_cost, steps + 1, state_id, new_state))
                state_id += 1

        # PRIORITY 2: Release operations on error loops first
        for lid in candidates:
            if lid in error_loop_ids and can_release(state.graph, lid):
                new_state = apply_operation(state, Operation(OperationType.RELEASE, lid), correct_graph)
                new_cost = new_state.total_cost()
                heapq.heappush(pq, (new_cost, steps + 1, state_id, new_state))
                state_id += 1

        # PRIORITY 3: Release operations on other candidate loops
        for lid in candidates:
            if lid not in error_loop_ids and can_release(state.graph, lid):
                new_state = apply_operation(state, Operation(OperationType.RELEASE, lid), correct_graph)
                new_cost = new_state.total_cost()
                heapq.heappush(pq, (new_cost, steps + 1, state_id, new_state))
                state_id += 1

    return None  # No repair found within max_steps


def exhaustive_search(error_graph: KnitGraph, correct_graph: KnitGraph, errors: List[Dict], max_depth: int = 10) -> Optional[RepairState]:
    """A2: Exhaustive search for true minimum (only feasible for small graphs)."""
    initial_state = RepairState(graph=error_graph.copy())
    for lid, loop in initial_state.graph.loops.items():
        if loop.is_boundary:
            initial_state.operations.append(Operation(OperationType.SECURE, lid, cost=0))

    # For dropped stitches, the yarn is already live
    for err in errors:
        if err['type'] == 'dropped_stitch':
            lid = err['loop_id']
            if lid in correct_graph.loops:
                initial_state.live_yarn_positions.append(correct_graph.loops[lid].yarn_order)

    candidates = get_repair_candidates(error_graph, errors, max_radius=2)

    best_state = None
    best_cost = float('inf')

    # DFS with pruning
    def dfs(state: RepairState, depth: int):
        nonlocal best_state, best_cost

        if depth > max_depth:
            return
        if state.total_cost() >= best_cost:
            return

        if is_repaired(state, errors, correct_graph):
            if state.total_cost() < best_cost:
                best_cost = state.total_cost()
                best_state = state.copy()
            return

        # Try release operations
        for lid in candidates:
            if can_release(state.graph, lid):
                new_state = apply_operation(state, Operation(OperationType.RELEASE, lid), correct_graph)
                dfs(new_state, depth + 1)

        # Try re-knit operations
        for yarn_order in state.live_yarn_positions:
            for lid, loop in correct_graph.loops.items():
                if loop.yarn_order == yarn_order and lid not in state.graph.loops:
                    new_state = apply_operation(state, Operation(
                        OperationType.REKNIT, lid,
                        new_loop_type=loop.loop_type,
                        new_pull_direction=loop.pull_direction
                    ), correct_graph)
                    dfs(new_state, depth + 1)

    dfs(initial_state, 0)
    return best_state


