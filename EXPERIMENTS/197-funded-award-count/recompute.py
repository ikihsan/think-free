#!/usr/bin/env python3
"""E197 recomputation -- the tieback, from committed bytes only.

F049/D061: a judgement over fetched data that cannot be tied to the bytes it was
read from is not a measurement. This file opens the captures on disk, rebuilds
every derived number in `panel1.json`, and reports the disagreements. It
imports no fetch function and opens no socket, so it cannot repair itself by
asking the API again.

Two things are checked per code and threshold, not one:

* **the arithmetic** -- `100 x (turn - 1)` plus the rows of the turning block
  that match, recomputed from the capture;
* **the invariant the arithmetic rests on** -- every page before the turning one
  is entirely on one side of the threshold, checked by reading page
  `turn - 1` and confirming its maximum (or minimum, descending) is past the
  threshold. This is the part a bisection gets wrong quietly: a correct-looking
  sum over a page that should not have been counted.
"""
import json
import os
import sys

import thresholds as TH
from body import read_block_rows

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")


def rebuild(prefix, page, order, t, side):
    """The count, rebuilt from one capture plus the page-level invariant."""
    rows = read_block_rows(prefix, page, order)
    if not rows:
        return None, "turning block unreadable"
    keep = (lambda a: a < t) if side == "max" else (lambda a: a >= t)
    amts = [r["Award Amount"] for r in rows
            if isinstance(r.get("Award Amount"), (int, float))]
    rowwise = sum(1 for a in amts if keep(a))
    if page > 1:
        prev = read_block_rows(prefix, page - 1, order)
        p_amt = [r["Award Amount"] for r in prev
                 if isinstance(r.get("Award Amount"), (int, float))]
        if not p_amt:
            return None, "page before the turning block unreadable"
        edge = max(p_amt) if side == "max" else min(p_amt)
        ok = (edge < t) if side == "max" else (edge >= t)
        if not ok:
            return None, ("the page before the turning block already reaches "
                          "the threshold (edge %s)" % edge)
    else:
        ok = True
    return 100 * (page - 1) + rowwise, "ok" if ok else "invariant failed"


def main():
    with open(os.path.join(RAW, "panel1.json")) as fh:
        p1 = json.load(fh)
    disagreements, checked, unreadable = [], 0, []
    derived = []
    for row in p1["rows"]:
        code, n_total = row["code"], row["n_total"]
        rebuilt = {}
        for t in TH.THRESHOLDS:
            entry = row["thresholds"][str(t)]
            if entry.get("n") is None or not entry.get("turn_page"):
                rebuilt[str(t)] = {"n": None, "status": entry.get("reason", "")}
                continue
            n, status = rebuild("a1_%s_asc" % code, entry["turn_page"], "asc",
                                t, "max")
            rebuilt[str(t)] = {"n": n, "status": status}
            if n is None:
                unreadable.append({"code": code, "t": t, "status": status})
                continue
            checked += 1
            if n != entry["n"]:
                disagreements.append({"code": code, "t": t, "stored": entry["n"],
                                      "rebuilt": n, "status": status})
        lo = rebuilt[str(TH.FUNDED_T)]["n"]
        hi = rebuilt[str(int(TH.SMALL_CUTOFF))]["n"]
        derived.append({"code": code,
                        "funded_ge_1": None if lo is None else n_total - lo,
                        "purchases_1_100k": None if (lo is None or hi is None)
                        else hi - lo})
        row["funded_ge_1"] = derived[-1]["funded_ge_1"]
        row["purchases_1_100k"] = derived[-1]["purchases_1_100k"]
        row["funded_fraction"] = (None if derived[-1]["funded_ge_1"] is None
                                  or not n_total
                                  else derived[-1]["funded_ge_1"] / float(n_total))
    out = {"experiment": "E197", "measurement": "tieback from committed captures",
           "rows_checked": checked, "disagreements": disagreements,
           "unreadable": unreadable,
           "C7_tieback": {"ok": not disagreements and not unreadable,
                          "rows_checked": checked,
                          "disagreements": len(disagreements),
                          "unreadable": len(unreadable)}}
    with open(os.path.join(RAW, "recompute.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("C7 %s -- %d counts rebuilt from captures, %d disagreements, %d unreadable"
          % ("PASS" if out["C7_tieback"]["ok"] else "FAIL", checked,
             len(disagreements), len(unreadable)))
    for d in disagreements[:10]:
        print("   %s t=%s stored=%s rebuilt=%s" % (d["code"], d["t"], d["stored"],
                                                  d["rebuilt"]))
    return 0 if out["C7_tieback"]["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())