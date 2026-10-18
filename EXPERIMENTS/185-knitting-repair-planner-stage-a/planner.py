"""Repair planner for knitting graphs."""

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


class OperationType(Enum):
    RELEASE = "release"
    REKNIT = "reknit"
    SECURE = "secure"


@dataclass
class Operation:
    op_type: OperationType
    loop_id: str
    # For REKNIT: the new loop properties
    new_loop_type: Optional[LoopType] = None
    new_pull_direction: Optional[PullDirection] = None
    # For SECURE: just marks as boundary
    cost: int = 1

    def __lt__(self, other):
        return self.cost < other.cost


@dataclass
class RepairState:
    graph: KnitGraph
    operations: List[Operation] = field(default_factory=list)
    live_yarn_positions: List[int] = field(default_factory=list)  # yarn_order positions where yarn is live

    def copy(self) -> 'RepairState':
        return RepairState(
            graph=self.graph.copy(),
            operations=self.operations.copy(),
            live_yarn_positions=self.live_yarn_positions.copy(),
        )

    def total_cost(self) -> int:
        return sum(op.cost for op in self.operations)

    def loops_released(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.RELEASE)

    def loops_reknit(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.REKNIT)

    def holders_placed(self) -> int:
        return sum(1 for op in self.operations if op.op_type == OperationType.SECURE)


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


def run_experiment() -> Dict[str, Any]:
    """Run the full experiment on all fixtures."""
    from knitting_graph import FIXTURES, detect_errors

    results = {
        'fixtures': [],
        'summary': {},
    }

    total_fixtures = len(FIXTURES)
    g1_pass = 0  # Planner completeness
    g2_pass = 0  # Improvement over baseline
    g3_pass = 0  # Optimality gap
    g4_pass = 0  # Refusal on unsupported (not tested in this simple version)

    for fix in FIXTURES:
        print(f"\n=== {fix['name']} ===")
        print(f"  {fix['description']}")

        # Create fixture with error
        error_graph = fix['factory']()
        correct_graph = fix['correct_factory']()
        valid, val_errors = error_graph.validate()
        print(f"  Graph valid: {valid}")
        if not valid:
            print(f"  Validation errors: {val_errors}")

        # Detect errors
        errors = detect_errors(error_graph)
        print(f"  Detected errors: {len(errors)}")
        for e in errors:
            print(f"    - {e['type']} at {e['location']}")

        if not errors:
            print(f"  WARNING: No errors detected!")
            continue

        fixture_result = {
            'name': fix['name'],
            'description': fix['description'],
            'errors_detected': len(errors),
            'arms': {},
        }

        # A0: Full-row rollback (using correct graph as reference)
        start = time.time()
        state_a0 = full_row_rollback(error_graph, correct_graph, errors)
        time_a0 = (time.time() - start) * 1000
        valid_a0, _ = state_a0.graph.validate()
        repaired_a0 = is_repaired(state_a0, errors, correct_graph)

        fixture_result['arms']['A0_full_row_rollback'] = {
            'loops_released': state_a0.loops_released(),
            'loops_reknit': state_a0.loops_reknit(),
            'holders_placed': state_a0.holders_placed(),
            'total_operations': state_a0.total_cost(),
            'valid': valid_a0,
            'repaired': repaired_a0,
            'time_ms': time_a0,
        }
        print(f"  A0 (full-row rollback): released={state_a0.loops_released()}, reknit={state_a0.loops_reknit()}, valid={valid_a0}, repaired={repaired_a0}, time={time_a0:.1f}ms")

        # A1: Local planner
        start = time.time()
        state_a1 = local_planner_search(error_graph, correct_graph, errors, max_steps=30)
        time_a1 = (time.time() - start) * 1000

        if state_a1:
            valid_a1, _ = state_a1.graph.validate()
            repaired_a1 = is_repaired(state_a1, errors, correct_graph)
            fixture_result['arms']['A1_local_planner'] = {
                'loops_released': state_a1.loops_released(),
                'loops_reknit': state_a1.loops_reknit(),
                'holders_placed': state_a1.holders_placed(),
                'total_operations': state_a1.total_cost(),
                'valid': valid_a1,
                'repaired': repaired_a1,
                'time_ms': time_a1,
            }
            print(f"  A1 (local planner): released={state_a1.loops_released()}, reknit={state_a1.loops_reknit()}, valid={valid_a1}, repaired={repaired_a1}, time={time_a1:.1f}ms")

            # G1: Planner completeness
            if repaired_a1:
                g1_pass += 1
                print(f"    G1: PASS (found repair)")

            # G2: Improvement over baseline
            if repaired_a1 and state_a1.loops_released() < state_a0.loops_released():
                g2_pass += 1
                print(f"    G2: PASS (released {state_a1.loops_released()} < {state_a0.loops_released()})")
            else:
                print(f"    G2: FAIL (released {state_a1.loops_released()} >= {state_a0.loops_released()})")
        else:
            fixture_result['arms']['A1_local_planner'] = {
                'loops_released': None,
                'loops_reknit': None,
                'holders_placed': None,
                'total_operations': None,
                'valid': False,
                'repaired': False,
                'time_ms': time_a1,
            }
            print(f"  A1 (local planner): NO REPAIR FOUND")
            print(f"    G1: FAIL (no repair found)")

        # A2: Exhaustive search (only for small fixtures F1-F3)
        if fix['name'] in ('F1_stockinette_dropped', 'F2_rib_twisted', 'F3_cable_wrong_cross'):
            start = time.time()
            state_a2 = exhaustive_search(error_graph, correct_graph, errors, max_depth=12)
            time_a2 = (time.time() - start) * 1000

            if state_a2:
                valid_a2, _ = state_a2.graph.validate()
                repaired_a2 = is_repaired(state_a2, errors, correct_graph)
                fixture_result['arms']['A2_exhaustive'] = {
                    'loops_released': state_a2.loops_released(),
                    'loops_reknit': state_a2.loops_reknit(),
                    'holders_placed': state_a2.holders_placed(),
                    'total_operations': state_a2.total_cost(),
                    'valid': valid_a2,
                    'repaired': repaired_a2,
                    'time_ms': time_a2,
                }
                print(f"  A2 (exhaustive): released={state_a2.loops_released()}, reknit={state_a2.loops_reknit()}, valid={valid_a2}, repaired={repaired_a2}, time={time_a2:.1f}ms")

                # G3: Optimality gap
                if state_a1 and repaired_a1 and repaired_a2:
                    opt_gap = state_a1.loops_released() - state_a2.loops_released()
                    if opt_gap <= 1:
                        g3_pass += 1
                        print(f"    G3: PASS (gap={opt_gap} <= 1)")
                    else:
                        print(f"    G3: FAIL (gap={opt_gap} > 1)")
            else:
                fixture_result['arms']['A2_exhaustive'] = {
                    'loops_released': None,
                    'repaired': False,
                }
                print(f"  A2 (exhaustive): NO REPAIR FOUND")
        else:
            print(f"  A2 (exhaustive): SKIPPED (fixture too large)")

        results['fixtures'].append(fixture_result)

    # Summary
    g1_rate = g1_pass / total_fixtures if total_fixtures > 0 else 0
    g2_rate = g2_pass / total_fixtures if total_fixtures > 0 else 0
    g3_count = sum(1 for f in FIXTURES if f['name'] in ('F1_stockinette_dropped', 'F2_rib_twisted', 'F3_cable_wrong_cross'))
    g3_rate = g3_pass / g3_count if g3_count > 0 else 0

    results['summary'] = {
        'total_fixtures': total_fixtures,
        'G1_planner_completeness': {'passed': g1_pass, 'total': total_fixtures, 'rate': g1_rate},
        'G2_improvement_over_baseline': {'passed': g2_pass, 'total': total_fixtures, 'rate': g2_rate},
        'G3_optimality_gap': {'passed': g3_pass, 'total': g3_count, 'rate': g3_rate},
        'G4_refusal_on_unsupported': {'passed': 0, 'total': 0, 'rate': 0, 'note': 'Not tested in this version'},
    }

    print(f"\n=== SUMMARY ===")
    print(f"G1 (completeness): {g1_pass}/{total_fixtures} = {g1_rate:.2f}")
    print(f"G2 (improvement): {g2_pass}/{total_fixtures} = {g2_rate:.2f}")
    print(f"G3 (optimality): {g3_pass}/{g3_count} = {g3_rate:.2f}")

    # Kill gate: G2 fails -> close
    kill_gate = g2_rate < 0.625  # <5/8
    results['kill_gate_fired'] = kill_gate
    print(f"Kill gate (G2 < 5/8): {'FIRED' if kill_gate else 'NOT FIRED'}")

    return results


if __name__ == "__main__":
    results = run_experiment()
    # Save results
    import json
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results.json")