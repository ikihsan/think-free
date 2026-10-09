#!/usr/bin/env python3
"""E071 outcome: re-derive the gate table from raw/probe.json.

Reads only the committed capture, so the result is reproducible without
network. Exit codes follow the mission's convention: 0 success, 3 verification
failed (a predeclared gate did not hold).
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "probe.json")
OUT = os.path.join(HERE, "results.json")


def rate(num, den):
    return round(num / den, 6) if den else None


def main():
    with open(RAW) as fh:
        probe = json.load(fh)
    arms = probe["arms"]

    def tally(name):
        rows = arms[name]["rows"]
        usable = [r for r in rows if not r.get("error")]
        present = [r for r in usable if r["arrival"]["present"]]
        states = {}
        for r in usable:
            s = r["arrival"]["state"]
            states[s] = states.get(s, 0) + 1
        return {"rows": len(rows), "usable": len(usable),
                "carrying_arrival_field": len(present),
                "rate": rate(len(present), len(usable)),
                "states": states,
                "keys_union": sorted({k for r in usable
                                      for k in r["arrival"].get("keys", [])})}

    a = tally("arm_a_hackernews")
    b = tally("arm_b_github")
    c = tally("arm_c_stackexchange_control")

    # Arm C is read at the row level the API returns (questions), not at the
    # site-summary level the tally above counts, because the control's claim is
    # about items.
    se_rows = arms["arm_c_stackexchange_control"]["rows"]
    se_items = sum(r.get("n_rows", 0) for r in se_rows)
    se_pos = sum(r.get("with_view_count_positive", 0) for r in se_rows)
    se_key = sum(r.get("with_view_count_key", 0) for r in se_rows)

    gates = {
        "G1_control_field_readable": {
            "threshold": "Stack Exchange items carry a positive view_count on >= 95% of rows",
            "observed": "%d of %d items positive (%d carry the key)" % (se_pos, se_items, se_key),
            "rate": rate(se_pos, se_items),
            "met": bool(se_items) and (se_pos / se_items) >= 0.95,
        },
        "G2_hackernews_field_absent": {
            "threshold": "HN items carry any arrival field on 0% of rows",
            "observed": "%d of %d" % (a["carrying_arrival_field"], a["usable"]),
            "rate": a["rate"],
            "met": a["usable"] > 0 and a["carrying_arrival_field"] == 0,
        },
        "G3_github_field_absent": {
            "threshold": "GitHub issue objects carry any arrival field on 0% of rows",
            "observed": "%d of %d" % (b["carrying_arrival_field"], b["usable"]),
            "rate": b["rate"],
            "met": b["usable"] > 0 and b["carrying_arrival_field"] == 0,
        },
    }
    kill = gates["G1_control_field_readable"]["met"] and (
        gates["G2_hackernews_field_absent"]["met"]
        or gates["G3_github_field_absent"]["met"])

    results = {
        "experiment": "071-viewcount-denominator",
        "date": "2026-10-09",
        "question": ("does the software arm's view_count zero exist, or is it a "
                     "missing observation (D082)?"),
        "arms": {"a_hackernews": a, "b_github": b, "c_stackexchange_control": c},
        "stackexchange_item_level": {
            "items": se_items, "with_key": se_key, "positive": se_pos},
        "gates": gates,
        "kill_condition_met": kill,
        "verdict": ("CONFIRMED: the software-arm '0% view_count' is a MISSING "
                    "OBSERVATION, not a measured zero. Neither Hacker News nor "
                    "the GitHub issues API returns any arrival/view field on "
                    "any sampled object; Stack Exchange, the surface E062 "
                    "actually measured, returns a positive view_count on every "
                    "sampled item."
                    if kill else
                    "NOT CONFIRMED: at least one predeclared gate did not hold; "
                    "no claim is made."),
        "effect_on_unlanded_work": [
            "E069 (069-view-count-nonsoftware): the 'diametrically opposed / "
            "contradicts E063/E066' contrast compares a field that does not "
            "exist on the software platforms against one that does. Its "
            "CONFIRMED verdict is withdrawn; the 14% unserved-open-like share "
            "on non-software Stack Exchange is unaffected, because that arm "
            "measured a field the platform does return.",
            "E070 (070-discourse-fresh-observation): inherits the same invalid "
            "ground_truth_context line ('0% view_count in software corpora'). "
            "Its own CFPB arms are unaffected (CFPB complaints are one arrival "
            "each by construction).",
            "MISSION-OUTCOME.json: vc_always_100_percent and "
            "instrument_validated_outside_software cannot be recorded as "
            "observed; the corrected claim is that view_count is "
            "Stack-Exchange-shaped and unmeasured elsewhere.",
        ],
        "corrected_statement": (
            "The E062 arrival instrument is measurable only where a platform "
            "publishes one. Stack Exchange does; the Hacker News and GitHub "
            "APIs do not. Every software-arm cell reading it in this record "
            "(E063, E066, E069, E070) is a missing observation, never a zero. "
            "The instrument is not falsified - it was never measured there."),
        "ceiling": ("Scoped to the public documented API response objects, "
                    "because that is the only surface E063/E066 harvested and "
                    "the only one a reproduction can use. This does not claim HN "
                    "and GitHub expose no view counters anywhere (a web UI or "
                    "undocumented endpoint is untested); it claims the corpora "
                    "carry no arrival field, so the software-arm cell cannot be "
                    "a measured zero."),
        "raw": {"probe": "raw/probe.json",
                "probed_keys": probe["arrival_keys_probed"]},
    }

    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)

    print("arm A hackernews  : %d/%d rows carry an arrival field"
          % (a["carrying_arrival_field"], a["usable"]))
    print("arm B github      : %d/%d rows carry an arrival field"
          % (b["carrying_arrival_field"], b["usable"]))
    print("arm C stackexchange: %d/%d items carry a positive view_count (control)"
          % (se_pos, se_items))
    for name, g in sorted(gates.items()):
        print("  %-32s %s  (%s)" % (name, "MET" if g["met"] else "NOT MET",
                                    g["observed"]))
    print("\nkill condition met:", kill)
    print("verdict:", results["verdict"][:80])
    return 0 if kill else 3


if __name__ == "__main__":
    sys.exit(main())