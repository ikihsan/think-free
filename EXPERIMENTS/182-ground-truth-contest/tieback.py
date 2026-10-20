#!/usr/bin/env python3
"""E182 stage 5: tieback check. Re-derive every headline number in RESULT.md
from the committed artifacts and fail if any disagrees.

D061's rule: a claim about text is evidence only if it can be tied to the bytes
it was read from. This does not recompute anything -- it re-reads states.json,
overlap.json, power.json and scores.json and checks the published sentences.

Read-only: it writes nothing.

Usage: python3 tieback.py     # exits 0 when every claim ties, 3 otherwise
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    states = json.load(open(os.path.join(HERE, "states.json")))
    ov = json.load(open(os.path.join(HERE, "overlap.json")))
    pw = json.load(open(os.path.join(HERE, "power.json")))
    scores = json.load(open(os.path.join(HERE, "scores.json")))
    result = open(os.path.join(HERE, "RESULT.md")).read()
    # Markdown hard-wraps, so a published sentence is split across lines. Match
    # against whitespace-collapsed text, and record that choice rather than
    # quietly loosening the needles.
    flat = re.sub(r"\s+", " ", result)

    rows = states["rows"]
    claims, fails = [], []

    def claim(label, ok, detail):
        claims.append((label, ok, detail))
        if not ok:
            fails.append("%s: %s" % (label, detail))

    # --- population ---
    qids = scores["qids"] if "qids" in scores else sorted(
        int(k) for k in scores["rows"])
    claim("population is 60 rows", len(qids) == 60, "%d" % len(qids))
    claim("G4 reproduced 59 of 60",
          states["gates"]["G4_population_stable"]["reproduced"] == 59,
          str(states["gates"]["G4_population_stable"]["reproduced"]))

    # --- state shares ---
    so = states["states_overall"]
    claim("contested 13/60 = 0.2167",
          so["contested"]["k"] == 13 and abs(so["contested"]["rate"] - 13 / 60.0) < 1e-9,
          "%d/%d" % (so["contested"]["k"], so["contested"]["n"]))
    claim("uncorroborated 16/60 = 0.2667", so["uncorroborated"]["k"] == 16,
          "%d/%d" % (so["uncorroborated"]["k"], so["uncorroborated"]["n"]))
    claim("48.3% contested-or-uncorroborated",
          abs((so["contested"]["k"] + so["uncorroborated"]["k"]) / 60.0 - 0.4833) < 5e-4,
          str((so["contested"]["k"] + so["uncorroborated"]["k"]) / 60.0))

    # --- G2 (first arm, withdrawn) ---
    g2 = states["gates"]["G2_differential"]
    claim("first-arm G2 p == 1.0", g2["fisher_p"] == 1.0, str(g2["fisher_p"]))
    claim("first-arm G2 diff -0.0278", abs(g2["diff"] + 0.0278) < 5e-4, str(g2["diff"]))
    claim("first-arm G2 did not fire", g2["fires"] is False, str(g2["fires"]))

    # --- instruments ---
    g2p = ov["gates"]["G5_repaired_instrument"]
    claim("residual instrument accepted", g2p["instrument_accepted"] is True, "")
    claim("balanced accuracy 0.8000",
          abs(g2p["balanced_accuracy_on_calibration"] - 0.80) < 1e-9,
          str(g2p["balanced_accuracy_on_calibration"]))
    claim("tau 0.05", g2p["tau"] == 0.05, str(g2p["tau"]))
    claim("G2' did not fire", g2p.get("fires") is False, str(g2p.get("fires")))
    claim("G2' fisher p == 1.0", g2p.get("fisher_p") == 1.0, str(g2p.get("fisher_p")))
    claim("G2' evid missed [4, 9]", g2p.get("evid_missed") == [4, 9],
          str(g2p.get("evid_missed")))
    claim("G2' evid hit [3, 6]", g2p.get("evid_hit") == [3, 6],
          str(g2p.get("evid_hit")))

    # --- calibration set size ---
    claim("9 calibration rows", len(ov["calibration"]) == 9,
          str(len(ov["calibration"])))
    hand = {"differ": 0, "same": 0}
    for c in ov["calibration"]:
        hand[c["truth"]] = hand.get(c["truth"], 0) + 1
    claim("calibration is 5 differ / 4 same (one row has no comparison)",
          hand.get("differ") == 5 and hand.get("same") == 4, str(hand))

    # --- power ---
    px = pw["EVID_missed_vs_EVID_hit"]
    claim("exact permutation p == 1.0", px["exact_permutation_p"] == 1.0,
          str(px["exact_permutation_p"]))
    claim("observed U is the centre", abs(px["U"] - px["n_x"] * px["n_y"] / 2.0) < 1e-9,
          "U=%s centre=%s" % (px["U"], px["n_x"] * px["n_y"] / 2.0))

    # --- coverage ---
    lab = [r for r in ov["rows"] if r.get("overlap") is not None]
    claim("37 of 60 rows labelled", len(lab) == 37, "%d" % len(lab))
    evid_lab = [r for r in lab if r["arm"] == "EVID"]
    claim("21 of 30 EVID rows labelled", len(evid_lab) == 21, "%d" % len(evid_lab))
    single = sum(1 for r in ov["rows"] if r.get("reason") == "single_answer")
    claim("16 single-answer rows", single == 16, str(single))
    claim("5 eligible rows with no runner-up prescription",
          sum(1 for r in ov["rows"] if r.get("reason")
              == "runner_up_no_prescriptive_tokens") == 5,
          str(sum(1 for r in ov["rows"] if r.get("reason")
                  == "runner_up_no_prescriptive_tokens")))

    # --- the published sentences actually say it ---
    for needle in ["13/60 = **0.2167**", "16/60 = 0.2667", "**48.3%**",
                   "**p = 1.0**", "**p = 1.0000**", "0.8000",
                   "**37 of 60 rows are labelled, and 21 of the 30 EVID rows.**",
                   "4 of 10"]:
        claim("RESULT.md states %r" % needle,
              re.sub(r"\s+", " ", needle) in flat, "absent")

    for label, ok, detail in claims:
        print("%-4s %-52s %s" % ("OK" if ok else "FAIL", label, detail))
    print()
    print("%d claims, %d failed" % (len(claims), len(fails)))
    if fails:
        for f in fails:
            print("  FAILED %s" % f)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())