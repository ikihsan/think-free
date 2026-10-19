"""Repair planner for knitting graphs.

Split at the 300-line cap: the data model, the A0 baseline, the operation
primitives and the two search arms live in sibling modules; this file keeps
the experiment runner so the committed results.json is reproduced by
`python3 planner.py` exactly as before.
"""

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
from planner_baseline import get_affected_rows, full_row_rollback
from planner_ops import (get_repair_candidates, can_release, can_reknit,
                       apply_operation, is_repaired)
from planner_search import local_planner_search, exhaustive_search

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