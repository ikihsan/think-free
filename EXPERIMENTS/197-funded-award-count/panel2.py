#!/usr/bin/env python3
"""E197 controls C1, C2, C3, C6 and panel B -- the independent arm.

Panel B reads the same number panel A did from the **descending** end of the
award order, for E196's 25 addressability codes only. A bisection that is off by
one page produces a clean number with nothing to contradict it, so the arm that
contradicts it has to exist and has to run on the codes the decision rests on.

The controls here are the ones that can refuse the whole run:

* **C1 / C2** a PSC code that cannot exist must not produce a populated result.
  A numeric threshold over an unread population is the defect this record has
  hit three times.
* **C3** `order: "asc"` is ascending and `order: "desc"` is descending. E196's
  defect 1 was a sort parameter that read like a direction and returned the
  opposite, and nothing downstream looked wrong.
* **C6** the 25-code population is E196's, read from E196's committed bytes, not
  a list this session typed.

C4 (no ignored filter anywhere) and C5 (every count is a usable denominator) are
computed in `analysis.py` over panels A and B, because they are properties of
the whole run rather than of a request.
"""
import json
import os
import sys

import client
import funded
import thresholds as TH

HERE = os.path.dirname(os.path.abspath(__file__))
E196_RAW = os.path.join(HERE, "..", "196-federal-spend-metered", "raw")
OUT = os.path.join(client.RAW, "panel2.json")

# A cell with a wide amount spread and a readable depth, for the direction
# control. `DA01` has 27,424 awards over 275 pages.
DIRECTION_CODE = "DA01"
DIRECTION_PAGES = [1, 5, 50, 150]


def c1_nonexistent_code():
    """A well-formed PSC code that does not exist: empty, never populated."""
    out = []
    for page in (1, TH.MAX_PAGE):
        r = funded.read_block(client.base_filters(psc_codes=["ZZZZ"]), page,
                              "asc", "c1_ZZZZ_p%d" % page)
        out.append({"page": page, "status": r["status"], "rows": r["rows"],
                    "unused_filters": r["unused_filters"],
                    "ok": r["status"] == 200 and r["rows"] == 0
                    and not r["unused_filters"]})
    return out


def c2_malformed_code():
    """A syntactically invalid code: refused or empty, never populated."""
    r = funded.read_block(client.base_filters(psc_codes=["not-a-code"]), 1,
                          "asc", "c2_not_a_code")
    return [{"page": 1, "status": r["status"], "rows": r["rows"],
             "unused_filters": r["unused_filters"],
             "ok": r["rows"] == 0 and not r["unused_filters"]}]


def _direction_amounts(page, order, name):
    r = funded.read_block(client.base_filters(psc_codes=[DIRECTION_CODE]),
                          page, order, name)
    path = os.path.join(client.RAW, "%s_p%d_%s.json" % (name, page, order))
    try:
        with open(path, "rb") as fh:
            parsed = json.loads(fh.read().decode("utf-8", "replace"))
        amts = [x["Award Amount"] for x in (parsed.get("results") or [])
                if isinstance(x.get("Award Amount"), (int, float))]
    except Exception:
        amts = []
    return r, amts


def c3_sort_direction():
    """Consecutive readable pages must not reverse the declared direction."""
    checks, per_order = [], {}
    for order, cmp_name in (("asc", "ascending: max(p) <= min(p+1)"),
                            ("desc", "descending: max(p) >= min(p+1)")):
        prev = None
        for page in DIRECTION_PAGES:
            r, amts = _direction_amounts(page, order, "c3_%s" % DIRECTION_CODE)
            entry = {"page": page, "status": r["status"], "rows": len(amts),
                     "min": min(amts) if amts else None,
                     "max": max(amts) if amts else None, "pairs": []}
            if prev and len(amts) == 100 and len(prev[1]) == 100:
                if order == "asc":
                    ok = max(amts) >= min(prev[1])
                else:
                    ok = max(amts) <= min(prev[1])
                entry["pairs"].append({"vs_page": prev[0], "ok": bool(ok)})
            per_order.setdefault(order, []).append(entry)
            prev = (page, amts)
        checks.append({"order": order, "rule": cmp_name,
                       "pages": per_order[order],
                       "ok": all(p["ok"] for e in per_order[order]
                                 for p in e["pairs"])})
    return checks


def c6_population_matches_e196():
    """The 25 codes, from E196's committed bytes rather than from this file."""
    with open(os.path.join(E196_RAW, "panel2.json")) as fh:
        e196 = json.load(fh)
    theirs = sorted(r["code"] for r in
                    e196["G4"]["codes_clearing_rank_and_total"])
    ours = sorted(TH.G4_CODEBOOK)
    return {"e196": theirs, "here": ours, "match": theirs == ours,
            "e196_count": len(theirs)}


def panel_b(verbose=True):
    """The descending arm, for every code the decision rests on."""
    rows = []
    for code in TH.G4_CODEBOOK:
        filters = client.base_filters(psc_codes=[code])
        payload = {"filters": filters, "subawards": False, "page": 1, "limit": 1}
        st, parsed, _ = client.call("spending_by_award_count/", payload,
                                    "b_count_%s" % code)
        results = (parsed or {}).get("results") if isinstance(parsed, dict) else {}
        n = sum(v for v in results.values() if isinstance(v, int)) or None
        desc = funded.n_at_or_above(filters, n, TH.FUNDED_T, "b_%s_desc" % code)
        rows.append({"code": code, "n_total": n, "desc": desc,
                     "desc_funded_ge_1": desc["n"],
                     "unused_filters": desc.get("unused_filters", [])})
        if verbose:
            print("  %-6s N=%-9s descending funded>=1: %s"
                  % (code, n, desc["n"] if desc["n"] is not None
                     else "censored (lower bound %d)" % desc["lower_bound"]))
    return rows


def main():
    out = {"experiment": "E197", "panel": "B",
           "C1_nonexistent_code": c1_nonexistent_code(),
           "C2_malformed_code": c2_malformed_code(),
           "C3_sort_direction": c3_sort_direction(),
           "C6_population_matches_e196": c6_population_matches_e196(),
           "panel_b": panel_b()}
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("C1 %s | C2 %s | C3 %s | C6 %s"
          % ([r["ok"] for r in out["C1_nonexistent_code"]],
             [r["ok"] for r in out["C2_malformed_code"]],
             [r["ok"] for r in out["C3_sort_direction"]],
             out["C6_population_matches_e196"]["match"]))
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())