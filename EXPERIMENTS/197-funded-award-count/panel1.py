#!/usr/bin/env python3
"""E197 panel A -- the funded count, for every code in E196's head-100.

One row per code: the cell's total award count, the exact count of awards below
each of the six declared thresholds, and the derived funded count. No gate is
computed here; `analysis.py` does that from these bytes so that a defect in the
arithmetic can be reproduced rather than argued about.

The population is E196's committed `raw/head100.json`, read from disk rather than
re-selected, and control C6 in `controls.py` checks the codebook against E196's
own bytes.
"""
import json
import os
import sys
import time

import client
import funded
import thresholds as TH

HERE = os.path.dirname(os.path.abspath(__file__))
E196_RAW = os.path.join(HERE, "..", "196-federal-spend-metered", "raw")


def head100():
    """E196's 100 PSC base codes, in its order, from its committed bytes."""
    path = os.path.join(E196_RAW, "head100.json")
    with open(path) as fh:
        rows = json.load(fh)["results"]
    return [{"code": r["code"], "name": r["name"], "amount": r["amount"]}
            for r in rows]


def cell_total(code, capture):
    """N_code from `spending_by_award_count`, re-captured in this run.

    E196 read totals from `spending_by_category/psc/`; the two disagree by small
    amounts (`DA01` 27,425 there, 27,424 here). This experiment divides by the
    number it read itself, and the disagreement is reported as a data-vintage
    observation rather than repaired.
    """
    payload = {"filters": client.base_filters(psc_codes=[code]),
               "subawards": False, "page": 1, "limit": 1}
    st, parsed, meta = client.call("spending_by_award_count/", payload, capture)
    results = (parsed or {}).get("results") if isinstance(parsed, dict) else {}
    n = sum(v for v in results.values() if isinstance(v, int)) or None
    return n, st, meta, client.unused_filter_messages(parsed)


def one_code(code, verbose=True):
    """The whole per-code row: count, six order statistics, the derived fields."""
    n_total, st, meta, unused = cell_total(code, "a1_count_%s" % code)
    row = {"code": code, "n_total": n_total, "count_status": st,
           "count_unused_filters": unused,
           "count_meta": {"endpoint": meta.get("endpoint"),
                          "sha256": meta.get("sha256"), "reused": meta.get("reused")},
           "thresholds": {}, "unused_filters_seen": list(unused)}
    filters = client.base_filters(psc_codes=[code])
    for t in TH.THRESHOLDS:
        r = funded.n_below(filters, n_total, t, "a1_%s_asc" % code)
        row["thresholds"][str(t)] = r
        row["unused_filters_seen"].extend(r.get("unused_filters", []))
    nb = row["thresholds"]
    lo, hi = nb[str(TH.FUNDED_T)], nb[str(int(TH.SMALL_CUTOFF))]
    funded_ge_1 = (None if lo["n"] is None
                   else n_total - lo["n"])
    row["funded_ge_1"] = funded_ge_1
    row["funded_fraction"] = (None if funded_ge_1 is None or not n_total
                              else funded_ge_1 / float(n_total))
    row["purchases_1_100k"] = (None if lo["n"] is None or hi["n"] is None
                               else hi["n"] - lo["n"])
    row["deobligations_below_0"] = nb["0"]["n"]
    row["exhausted_reading"] = (row["funded_ge_1"] is None
                                and lo["turn_page"] is not None)
    if verbose:
        print("  %-6s N=%-9s funded=%-9s frac=%-8s purch[$1-$100k]=%-9s %s"
              % (code, n_total, funded_ge_1,
                 "%.4f" % row["funded_fraction"] if row["funded_fraction"] else "-",
                 row["purchases_1_100k"], "" if row["purchases_1_100k"] is not None
                 else "censored"))
    return row


def main():
    codes = head100()
    out_path = os.path.join(client.RAW, "panel1.json")
    rows, started = [], time.time()
    for i, c in enumerate(codes, 1):
        row = one_code(c["code"])
        row["name"] = c["name"]
        row["amount"] = c["amount"]
        rows.append(row)
        with open(out_path, "w") as fh:
            json.dump({"experiment": "E197", "panel": "A",
                       "population_source": "E196 raw/head100.json",
                       "rows": rows}, fh, indent=1, sort_keys=True)
        if i % 10 == 0:
            print("[%d/%d] %.0fs elapsed" % (i, len(codes), time.time() - started))
    print("wrote %s (%d codes, %.0fs)"
          % (out_path, len(rows), time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main())