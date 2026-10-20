#!/usr/bin/env python3
"""E198 controls."""
import json
import os
import sys

import client


def run_controls():
    results = {}

    # C1: PSC ZZZZ returns empty 200
    print("Running C1 (ZZZZ)...")
    st, parsed, meta = client.control_zzzz()
    c1_pass = (st == 200 and isinstance(parsed, dict)
               and (parsed.get("results") or []) == [])
    results["C1"] = {"pass": c1_pass, "status": st, "results_count": len(parsed.get("results") or []) if isinstance(parsed, dict) else None}
    print("  C1: %s (status=%s)" % ("PASS" if c1_pass else "FAIL", st))

    # C2: PSC not-a-code returns 422 or empty
    print("Running C2 (not-a-code)...")
    st, parsed, meta = client.control_not_a_code()
    c2_pass = (st == 422) or (st == 200 and isinstance(parsed, dict)
                                and (parsed.get("results") or []) == [])
    results["C2"] = {"pass": c2_pass, "status": st, "results_count": len(parsed.get("results") or []) if isinstance(parsed, dict) else None}
    print("  C2: %s (status=%s)" % ("PASS" if c2_pass else "FAIL", st))

    return results


if __name__ == "__main__":
    run_controls()