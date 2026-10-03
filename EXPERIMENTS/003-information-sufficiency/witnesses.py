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
    """Two input sets for the knitting planner: original and repaired.

    The permitted input in the *original* specification is the chart (stitch
    symbol) plus connectivity, live stitches, and facing side, mirroring
    RESEARCH/C.md's stated inputs.  Physical mount (whether a loop is twisted)
    is deliberately absent, to test whether the stated input set is sufficient.

    Reality A: dropped loops are mounted normally -> re-form in place.
    Reality B: the same loops are mounted twisted -> re-form and untwist.

    The witness reports two cases:

      - original: both realities share identical permitted inputs and need
        different repairs, and no input field can represent the difference, so
        the specification is information-insufficient (F007).
      - repaired: orientation (mount) is added to the input, so the two
        realities no longer share identical inputs.  The silent pair is gone and
        the input is sufficient for the decision.
    """

    chart = {
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

    # Original specification: no orientation field anywhere in the input.
    original_input = {"chart": chart}
    original_encodes_mount = "mount" in _jsonish_keys(chart)

    # Repaired specification: each loop carries its mount, and the level is
    # derived from it.  The input now distinguishes A from B.
    repaired_a = {
        "chart": chart,
        "mount": reality_a["mount"],
    }
    repaired_b = {
        "chart": chart,
        "mount": reality_b["mount"],
    }
    repaired_encodes_mount = repaired_a != repaired_b

    return {
        "candidate": "knitting repair planner",
        "system": "passive",
        "original": {
            "permitted_input": original_input,
            "reality_A": reality_a,
            "reality_B": reality_b,
            "inputs_identical": not original_encodes_mount,
            "required_output_A": repair_a,
            "required_output_B": repair_b,
            "outputs_differ": repair_a != repair_b,
            "permitted_encoding_can_represent_the_difference": original_encodes_mount,
            "silent_pair_found": not original_encodes_mount,
        },
        "repaired_input_set": {
            "permitted_input_A": repaired_a,
            "permitted_input_B": repaired_b,
            "inputs_identical": repaired_a == repaired_b,
            "permitted_encoding_can_represent_the_difference": repaired_encodes_mount,
            "silent_pair_found": repaired_a == repaired_b,
        },
        # Flat mirrors of the repaired result so a caller can assert on them
        # without descending into the nested dict.
        "permitted_input": repaired_a,
        "reality_A": reality_a,
        "reality_B": reality_b,
        "inputs_identical": repaired_a == repaired_b,
        "required_output_A": repair_a,
        "required_output_B": repair_b,
        "outputs_differ": repair_a != repair_b,
        "permitted_encoding_can_represent_the_difference": repaired_encodes_mount,
        "silent_pair_found": repaired_a == repaired_b,
        "repaired": True,
        "verdict": (
            "repaired: the original specification (chart symbols, connectivity, live "
            "stitches, side) was information-insufficient because loop orientation was "
            "absent, so two realities required different repairs from identical inputs "
            "(F007). Adding each loop's mount to the input distinguishes the two "
            "realities; no silent pair remains. Residual limit: this shows the input "
            "*can* represent orientation, not that a knitter can always perceive it, nor "
            "that topology-only analysis is physically sufficient."
        ),
    }


def _jsonish_keys(obj):
    """Collect every dict key appearing anywhere in a JSON-like structure."""
    found = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.add(k)
            found |= _jsonish_keys(v)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            found |= _jsonish_keys(item)
    return found
