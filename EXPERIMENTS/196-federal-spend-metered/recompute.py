#!/usr/bin/env python3
"""E196 recompute -- rebuild every gate from the captured response bytes.

The RESULT's numbers are not trusted and are not re-typed. This script reads
only `raw/*.json` (what the API returned, written to disk before anything was
parsed), re-derives the per-code quantities, and re-runs G3, G4 and G5.

Its purpose is narrower than "verify": it is the F049/D061 requirement that a
judgement over fetched data be tied to the bytes it was read from. If the
committed capture and the committed verdict ever disagree, this says so and
exits 3.
"""
import glob
import json
import os
import re
import sys

import client
from analysis import analyse
from stats import median
from thresholds import SMALL_CUTOFF

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = client.RAW
MAX_PAGES = 6  # client.low_tail_awards default; the declared cap (AMENDMENT-2 s1)
NAME_RE = re.compile(r"^(\d{3})_([A-Za-z0-9]+)_(count|median|tail_p\d+|rank(\d+)_p(\d+))\.json$")


def load(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        return json.loads(raw.decode("utf-8", "replace")), len(raw)
    except Exception:
        return None, len(raw)


def main():
    head_body = os.path.join(RAW, "head100.json")
    head, _ = load(head_body)
    codes = [{"code": r["code"], "name": r["name"],
              "total_awards_level": r["amount"]} for r in head["results"]]

    by_code = {}
    for path in sorted(glob.glob(os.path.join(RAW, "*.json"))):
        m = NAME_RE.match(os.path.basename(path))
        if not m:
            continue
        idx, code, kind = m.group(1), m.group(2), m.group(3)
        rec = by_code.setdefault(code, {"code": code, "tail_pages": 0,
                                        "tail_censored": False,
                                        "rank_profile": {}})
        parsed, _ = load(path)
        if kind == "count":
            rec["award_count"] = ((parsed or {}).get("results") or {}).get("contracts")
        elif kind.startswith("rank"):
            rank = int(m.group(4))
            amts = [r["Award Amount"] for r in ((parsed or {}).get("results") or [])
                    if isinstance(r.get("Award Amount"), (int, float))]
            rec["rank_profile"][rank] = {
                "page": int(m.group(5)), "status": 200 if parsed else None,
                "rows": len(amts), "min": min(amts) if amts else None,
                "max": max(amts) if amts else None}
        elif kind == "median":
            amts = [r["Award Amount"] for r in ((parsed or {}).get("results") or [])
                    if isinstance(r.get("Award Amount"), (int, float))]
            descs = [r.get("Description") or "" for r in (parsed or {}).get("results") or []]
            rec["median_award"] = median(amts)
            rec["median_rows"] = len(amts)
            rec["median_descriptions"] = descs
            rec["median_status"] = 200 if parsed else None
        elif kind.startswith("tail_p"):
            rec["tail_pages"] = max(rec["tail_pages"], int(kind.split("p")[-1]))
            rows = (parsed or {}).get("results") or []
            rec.setdefault("tail_page_status", {})[int(kind.split("p")[-1])] = {
                "status": 200 if parsed else None, "rows": len(rows)}
            if not rows:
                # an empty page ends the walk cleanly -- not censoring
                rec["tail_stop_reason"] = "empty_page"
            for r in rows:
                amt = r.get("Award Amount")
                if not isinstance(amt, (int, float)):
                    continue
                if amt > SMALL_CUTOFF:
                    # crossing the cutoff is the walk *succeeding*, not censoring.
                    # The first version of this file read it the other way and
                    # disagreed with the committed run on exactly these fields.
                    rec["tail_stop_reason"] = "crossed_cutoff"
                    continue
                if amt > 0:
                    rec["tail_positive"] = rec.get("tail_positive", 0) + 1
                    rec["small_purchase_sum"] = rec.get("small_purchase_sum", 0.0) + amt
                    rec.setdefault("tail_descriptions", []).append(
                        (amt, r.get("Description") or ""))
                elif amt == 0:
                    rec["tail_zero"] = rec.get("tail_zero", 0) + 1
                else:
                    rec["tail_negative"] = rec.get("tail_negative", 0) + 1

    for rec in by_code.values():
        pages = sorted((rec.get("tail_page_status") or {}))
        reached_cap = bool(pages) and pages[-1] >= MAX_PAGES
        rec["tail_censored"] = bool(reached_cap
                                    and rec.get("tail_stop_reason") is None)
        rec.setdefault("tail_stop_reason", "ran_out_of_pages")

    recs = []
    for h in codes:
        rec = by_code.get(h["code"], {"code": h["code"], "award_count": None,
                                      "tail_positive": 0, "small_purchase_sum": 0.0})
        rec["name"] = h["name"]
        rec["total_awards_level"] = h["total_awards_level"]
        rec.setdefault("small_purchase_sum", 0.0)
        rec.setdefault("tail_positive", 0)
        recs.append(rec)

    result = analyse(codes, recs, True, True)
    committed = json.load(open(os.path.join(RAW, "panel2.json")))
    same = {}
    for key in ("G3", "G4", "G5"):
        a, b = result[key], committed[key]
        if key == "G3":
            same[key] = (abs((a["p"] or -1) - (b["p"] or -2)) < 1e-12
                         and a["fire"] == b["fire"])
        elif key == "G4":
            same[key] = (a["fire"] == b["fire"]
                         and a["top10_small_purchase_sum"] == b["top10_small_purchase_sum"])
        else:
            same[key] = (a["fire"] == b["fire"]
                         and a["families"] == b["families"])
    same["families_rollup"] = result["families"] == committed["families"]

    out = {"script": "recompute.py", "codes_rebuilt": len(recs),
           "gates_agree_with_committed_run": same,
           "recomputed_verdict": {
               "G3_p": result["G3"]["p"], "G3": result["G3"]["fire"],
               "G4": result["G4"]["fire"], "G5": result["G5"]["fire"]},
           "committed_verdict": committed["verdict"]}
    with open(os.path.join(RAW, "recompute.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for k, v in same.items():
        print("%-40s %s" % (k, "AGREES" if v else "DISAGREES"))
    print("codes rebuilt:", len(recs))
    return 0 if all(same.values()) else 3


if __name__ == "__main__":
    sys.exit(main())