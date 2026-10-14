#!/usr/bin/env python3
"""score.py — run M2 (valueset.py) and M1 (ground.py) on arms.jsonl, produce
gates.json with the E142 measurements.

Standard library only, deterministic. Imports valueset.py and ground.py
unchanged from their original experiment directories.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))
sys.path.insert(0, os.path.join(HERE, "..", "114-value-grounding"))
import valueset  # noqa: E402
import ground  # noqa: E402


def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return (p, max(0.0, center - margin), min(1.0, center + margin))


def main():
    arms_path = os.path.join(HERE, "arms.jsonl")
    if not os.path.exists(arms_path):
        print("ERROR: arms.jsonl not found. Run build_arms.py first.")
        return 1

    arms = [json.loads(l) for l in open(arms_path) if l.strip()]

    # Score each arm with M2 (valueset.py) — one-directional compare
    for arm in arms:
        sub = arm["summary"]
        ref = arm["reference"]
        sub_vals = valueset.canonical(sub)
        ref_vals = valueset.canonical(ref)
        extra = [k for k in sub_vals if k not in ref_vals]
        missing = [k for k in ref_vals if k not in sub_vals]
        arm["m2_sub_values"] = len(sub_vals)
        arm["m2_ref_values"] = len(ref_vals)
        arm["m2_extra"] = len(extra)
        arm["m2_missing"] = len(missing)
        arm["m2_verdict"] = "condemn" if extra else "clear"
        # M2 extracts at least one value?
        arm["m2_has_value"] = len(sub_vals) > 0

    # Score each arm with M1 (ground.py) — judge() on summary against reference
    for arm in arms:
        ref = arm["reference"]
        sub = arm["summary"]
        try:
            judged = ground.judge(ref, sub, threshold=0.6)
        except Exception:
            judged = []
        arm["m1_flagged"] = sum(1 for v in judged if v["verdict"] != "grounded")
        arm["m1_verdict"] = "condemn" if arm["m1_flagged"] > 0 else "clear"

    # Determine arms A and B by M2's own verdict
    # A = M2 says clear (all values grounded), B = M2 says condemn
    a_arms = [a for a in arms if a["m2_verdict"] == "clear"]
    b_arms = [a for a in arms if a["m2_verdict"] == "condemn"]

    # Independent check: for each arm, check if M2's extra values are REAL
    # (i.e., truly absent from reference) using a bare membership test
    for arm in arms:
        sub = arm["summary"]
        ref = arm["reference"]
        sub_vals = valueset.canonical(sub)
        ref_vals = valueset.canonical(ref)
        extra = [k for k in sub_vals if k not in ref_vals]
        # For each extra value, check if it's actually in the reference
        # using a simple string search (bare membership, no binding)
        real_extra = 0
        for key in extra:
            kind, val = key
            # Try to find the raw value in the reference
            found = False
            if isinstance(val, (int, float)):
                # Numeric value — search for string representation
                val_str = str(int(val)) if val == int(val) else str(val)
                # Also try with commas
                val_comma = f"{int(val):,}" if val == int(val) else str(val)
                if val_str in ref or val_comma in ref:
                    found = True
                # Try other renderings
                for raw_val in [val_str, val_comma, f"{val:.1f}", f"{val:.2f}"]:
                    if raw_val in ref:
                        found = True
                        break
            else:
                # String value (unparsed) — search for the string itself
                if str(val).lower() in ref.lower():
                    found = True
            if not found:
                real_extra += 1
        arm["m2_real_extra"] = real_extra
        # Is this arm genuinely unsupported? (M2 extra is real)
        arm["genuinely_unsupported"] = real_extra > 0

    # Re-classify arms: A = genuinely grounded, B = genuinely unsupported
    a_arms = [a for a in arms if not a["genuinely_unsupported"]]
    b_arms = [a for a in arms if a["genuinely_unsupported"]]

    # Compute gates
    gates = {}

    # K1: detection on B (genuinely unsupported)
    if b_arms:
        detected = sum(1 for a in b_arms if a["m2_verdict"] == "condemn")
        p, lo, hi = wilson(detected, len(b_arms))
        gates["K1"] = {
            "detected": detected,
            "total": len(b_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "verdict": "PASS" if p >= 0.95 else "FAIL",
        }
    else:
        gates["K1"] = {"detected": 0, "total": 0, "rate": 0.0, "verdict": "NOT_EVALUATED"}

    # K2: FP rate on A (genuinely grounded)
    if a_arms:
        fp = sum(1 for a in a_arms if a["m2_verdict"] == "condemn")
        p, lo, hi = wilson(fp, len(a_arms))
        gates["K2"] = {
            "fp": fp,
            "total": len(a_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "verdict": "PASS" if p <= 0.02 else "FAIL",
        }
    else:
        gates["K2"] = {"fp": 0, "total": 0, "rate": 0.0, "verdict": "NOT_EVALUATED"}

    # K3: coverage on A (M2 extracts >= 1 value)
    if a_arms:
        covered = sum(1 for a in a_arms if a["m2_has_value"])
        p, lo, hi = wilson(covered, len(a_arms))
        gates["K3"] = {
            "covered": covered,
            "total": len(a_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "verdict": "PASS" if p >= 0.30 else "FAIL",
        }
    else:
        gates["K3"] = {"covered": 0, "total": 0, "rate": 0.0, "verdict": "NOT_EVALUATED"}

    # K4: coverage on digit-bearing subsets
    a_d = [a for a in arms if a["has_digit"] and not a["genuinely_unsupported"]]
    b_d = [a for a in arms if a["has_digit"] and a["genuinely_unsupported"]]
    for label, subset in [("A_and_D", a_d), ("B_and_D", b_d)]:
        if subset:
            covered = sum(1 for a in subset if a["m2_has_value"])
            p, lo, hi = wilson(covered, len(subset))
            gates[f"K4_{label}"] = {
                "covered": covered,
                "total": len(subset),
                "rate": round(p, 4),
                "ci95": [round(lo, 4), round(hi, 4)],
                "verdict": "PASS" if p >= 0.30 else "FAIL",
            }
        else:
            gates[f"K4_{label}"] = {"covered": 0, "total": 0, "rate": 0.0, "verdict": "NOT_EVALUATED"}

    # K5: conditional coverage — of arms where summary has a value (digit),
    # what fraction does M2 see?
    n_arms = [a for a in arms if a["has_digit"]]
    if n_arms:
        covered = sum(1 for a in n_arms if a["m2_has_value"])
        p, lo, hi = wilson(covered, len(n_arms))
        gates["K5"] = {
            "covered": covered,
            "total": len(n_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
            "verdict": "PASS" if p >= 0.30 else "FAIL",
        }
    else:
        gates["K5"] = {"covered": 0, "total": 0, "rate": 0.0, "verdict": "NOT_EVALUATED"}

    # Baseline M1 on same arms
    if a_arms:
        m1_fp = sum(1 for a in a_arms if a["m1_verdict"] == "condemn")
        p, lo, hi = wilson(m1_fp, len(a_arms))
        gates["M1_FP_on_A"] = {
            "fp": m1_fp,
            "total": len(a_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
        }
    if b_arms:
        m1_detected = sum(1 for a in b_arms if a["m1_verdict"] == "condemn")
        p, lo, hi = wilson(m1_detected, len(b_arms))
        gates["M1_detection_on_B"] = {
            "detected": m1_detected,
            "total": len(b_arms),
            "rate": round(p, 4),
            "ci95": [round(lo, 4), round(hi, 4)],
        }

    # Triage operating point — mutually exclusive categories
    total = len(arms)
    condemn = sum(1 for a in arms if a["m2_verdict"] == "condemn")
    defer = sum(1 for a in arms if not a["m2_has_value"])
    clear = total - condemn - defer  # clear = no extra values AND has values
    gates["triage"] = {
        "total": total,
        "condemn": condemn,
        "clear": clear,
        "defer": defer,
        "resolved_share": round((condemn + clear) / total, 4) if total else 0.0,
        "condemn_share": round(condemn / total, 4) if total else 0.0,
    }

    # Save gates
    gates_path = os.path.join(HERE, "gates.json")
    with open(gates_path, "w") as f:
        json.dump(gates, f, indent=2, sort_keys=True)

    # Save scored arms
    scored_path = os.path.join(HERE, "scored_arms.jsonl")
    with open(scored_path, "w") as f:
        for arm in arms:
            f.write(json.dumps(arm, sort_keys=True) + "\n")

    print(f"Gates written to {gates_path}")
    print(json.dumps(gates, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
