"""Information-sufficiency witnesses, part 1: the two symbolic candidates.

Each function returns a plain dict: the two underlying realities, the permitted
input they share, the divergent required outputs, and a verdict.  The witness
runner (`witness.py`) collects them and writes `results.json`.  The numerical
ventilation witness lives in `witness_vent.py`.

All inputs are SYNTHETIC.  See README.md for the claim, oracle, and limits of
each construction.
"""

from __future__ import annotations


# --------------------------------------------------------------------------
# Candidate 1 — decision-directed sidewalk survey (active sensing)
# --------------------------------------------------------------------------


def sidewalk_witness() -> dict:
    """Two networks with identical observable measurements, different repairs.

    Network: one origin, candidate destinations D1 (weight 10) and D2
    (weight 6), reached through crossings c1 and c2.  A crossing is traversable
    only if repaired.  The survey's permitted inputs are the masked crossing
    conditions ({unknown, safe, unsafe}) and the set of origin/destination
    pairs whose access is being planned (RESEARCH/A.md step 2 provides the OD
    pairs as an input).

    The falsifying question: can two realities share *identical permitted
    inputs* yet require different repair packages under every askable
    observation?  Reality A and Reality B do share those inputs and do need
    different repairs; an askable crossing inspection separates them, so the
    policy has an advantage.  No silent pair was found inside the permitted
    input set.
    """

    weights = {"D1": 10, "D2": 6}
    dest_path = {"D1": ("c1",), "D2": ("c2",)}

    def reachable(fixed, condition, demand):
        total = 0
        for d, path in dest_path.items():
            # condition[c] True means the crossing is traversable (safe).
            if demand.get(d, False) and all(condition[c] for c in path) and set(path) <= fixed:
                total += weights[d]
        return total

    def best_decision(condition, demand, budget=1):
        """Best reachable weight fixing at most `budget` crossings."""
        best = (-1, None)
        crossings = ("c1", "c2")
        for mask in range(4):
            fixed = frozenset(crossings[i] for i in range(2) if mask & (1 << i))
            if len(fixed) > budget:
                continue
            val = reachable(fixed, condition, demand)
            if val > best[0]:
                best = (val, tuple(sorted(fixed)))
        return best

    # Identical permitted current observation for every reality: both crossings
    # masked/unknown.  The OD pairs are a separate permitted input.
    permitted = {
        "crossings": {"c1": "unknown", "c2": "unknown"},
        "origin_destination_pairs": ["D1", "D2"],
    }

    reality_a = {"condition": {"c1": True, "c2": False}, "demand": {"D1": True, "D2": True}}
    reality_b = {"condition": {"c1": False, "c2": True}, "demand": {"D1": True, "D2": True}}

    da = best_decision(reality_a["condition"], reality_a["demand"])
    db = best_decision(reality_b["condition"], reality_b["demand"])

    # An inspection of c1 (or c2) reveals that crossing's true condition, which
    # is exactly where A and B differ, so it separates them.
    sep_ab, via_ab = False, None
    for c in ("c1", "c2"):
        if reality_a["condition"][c] != reality_b["condition"][c]:
            sep_ab, via_ab = True, c
            break

    return {
        "candidate": "decision-directed sidewalk survey",
        "system": "active",
        "permitted_input": permitted,
        "pair_within_measurement_vocabulary": {
            "reality_A": reality_a,
            "reality_B": reality_b,
            "permitted_inputs_identical": True,
            "required_output_A": da,
            "required_output_B": db,
            "outputs_differ": da != db,
            "permitted_observation_separates": sep_ab,
            "separating_action": via_ab,
        },
        "silent_pair_found": not sep_ab,
        "verdict": (
            "survives: two realities share identical permitted inputs (masked "
            "crossings and the same OD pairs) yet need different repair packages, "
            "and an askable crossing inspection separates them, so decision-directed "
            "selection adds decision-relevant information the current data lacks. "
            "No silently-different pair was found inside the permitted input set; "
            "the decision only fails if the OD pairs themselves are dropped from the "
            "inputs, which RESEARCH/A.md step 2 does not do. Scope condition: the "
            "claim is 'given known origin/destination pairs'."
        ),
    }


# --------------------------------------------------------------------------
# Candidate 2 — knitting repair planner (passive, symbolic)
# --------------------------------------------------------------------------


def knitting_witness() -> dict:
    """Two stitch states with identical chart-level inputs, different repairs.

    The permitted input is the chart (stitch symbol) plus connectivity, mirroring
    RESEARCH/C.md's stated inputs ("the intended chart, the actual local error,
    the current live stitches, and the side facing the user").  Physical mount
    (whether a loop is twisted) is deliberately absent, to test whether the
    stated input set is sufficient.

    Reality A: dropped loops are mounted normally -> re-form in place.
    Reality B: the same loops are mounted twisted -> re-form and untwist.
    The chart-level input is identical; the valid repairs differ.
    """

    permitted_chart = {
        "loops": {
            "c1r1": {"stitch": "knit", "next": ["c0r1", "c2r1", "c1r0", "c1r2"]},
            "c2r1": {"stitch": "knit", "next": ["c1r1", "c3r1", "c2r0", "c2r2"]},
            "c1r2": {"stitch": "purl", "next": ["c2r2", "c1r1"]},
            "c2r2": {"stitch": "purl", "next": ["c1r2", "c2r1"]},
        },
        "live_stitches": ["c1r2", "c2r2"],
        "side": "public",
    }

    reality_a = {"mount": {"c1r1": "normal", "c2r1": "normal"}}
    reality_b = {"mount": {"c1r1": "twisted", "c2r1": "twisted"}}

    repair_a = ("re-form (1,1) and (2,1) in place",)
    repair_b = ("re-form (1,1) and (2,1) in place and untwist each",)

    # Is mount among the permitted inputs?  If not, the two states are
    # indistinguishable from the permitted input.
    permitted_encodes_mount = any(
        "mount" in node for node in permitted_chart["loops"].values()
    )

    return {
        "candidate": "knitting repair planner",
        "system": "passive",
        "permitted_input": permitted_chart,
        "reality_A": reality_a,
        "reality_B": reality_b,
        "inputs_identical": not permitted_encodes_mount,
        "required_output_A": repair_a,
        "required_output_B": repair_b,
        "outputs_differ": repair_a != repair_b,
        "permitted_encoding_can_represent_the_difference": permitted_encodes_mount,
        "verdict": (
            "information-insufficient as specified: two stitch states with identical "
            "chart-level inputs need different repairs because mount (twist) is not a "
            "permitted input. The claim must be narrowed to include orientation, or the "
            "planner must refuse. This does not kill the mechanism; it bounds its input."
        ),
    }
