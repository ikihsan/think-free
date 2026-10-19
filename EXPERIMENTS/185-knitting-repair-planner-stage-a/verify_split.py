#!/usr/bin/env python3
"""Verify the module split reproduces E185's committed numbers.

The split at the 300-line cap moved code between files. This runs two
fixtures through the split modules and compares every field except the
machine-dependent `time_ms` against the committed `results.json`, so the
split is checked against the record rather than against my expectation of it.

Usage: python3 verify_split.py   (run from the experiment directory)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from knitting_graph import FIXTURES, detect_errors  # noqa: E402
from planner import full_row_rollback, local_planner_search, exhaustive_search  # noqa: E402

FIELDS = ("loops_released", "loops_reknit", "holders_placed",
          "total_operations", "valid", "repaired")
CHECK = ("A0_full_row_rollback", "A1_local_planner", "A2_exhaustive")


def stats(state):
    ops = state.operations if state else []
    released = sum(1 for o in ops if o.op_type.name == "RELEASE")
    reknit = sum(1 for o in ops if o.op_type.name == "REKNIT")
    return {
        "loops_released": released,
        "loops_reknit": reknit,
        "holders_placed": sum(1 for o in ops if o.op_type.name == "SECURE"),
        # The committed runner counted RELEASE+REKNIT only; holders are
        # reported separately, so reproducing it needs the same convention.
        "total_operations": released + reknit,
        "valid": state.graph.validate()[0] if state else False,
        "repaired": True if state else False,
    }


def main():
    committed = {f["name"]: f["arms"] for f in
                 json.load(open("results.json"))["fixtures"]}
    here = os.path.dirname(os.path.abspath(__file__))
    ok = True
    for fix in FIXTURES[:2]:
        err_graph = fix["factory"]()
        correct = fix["correct_factory"]()
        errors = detect_errors(err_graph)
        arms = {
            "A0_full_row_rollback": full_row_rollback(err_graph, correct, errors),
            "A1_local_planner": local_planner_search(err_graph, correct, errors, max_steps=30),
            "A2_exhaustive": exhaustive_search(err_graph, correct, errors, max_depth=10),
        }
        for name in CHECK:
            got = stats(arms[name])
            want = {k: committed[fix["name"]][name][k] for k in FIELDS}
            same = got == want
            ok = ok and same
            print("%-26s %-22s %s" % (fix["name"], name, "MATCH" if same else "DIFFERS"))
            if not same:
                print("   committed: %s" % want)
                print("   now:       %s" % got)
    print("\nsplit reproduces committed results: %s" % ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())