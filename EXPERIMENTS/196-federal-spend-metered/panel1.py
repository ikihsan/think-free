#!/usr/bin/env python3
"""E196 panel 1 -- G2 (the zero control) and the instrument facts G1 relies on.

Run before panel 2 and independently of it. If panel 2's gates are all
unsatisfiable because a filter was ignored, this panel is where that is caught.

Checks, in order:
  C1  the non-existent PSC code `QQQQ` returns a well-formed 200 carrying zero
  C2  a nonsense keyword returns a well-formed 200 carrying no results
  C3  a nonsense keyword does NOT produce a "not used" filter message
  C4  `sort: "Award Amount"` with `order="asc"` really sorts ascending, so
      I3/I4 are order statistics and not arbitrary pages
  C5  `limit` above 100 is refused, which is why I3 stops at the 100th award
  C6  the three endpoints agree on one real code about how many awards exist
  C7  the same code's smallest awards are not all money (AMENDMENT-1's reason)
"""
import json
import os
import sys

import client

HERE = os.path.dirname(os.path.abspath(__file__))
NONSENSE_CODE = "QQQQ"
NONSENSE_KEYWORD = "zzqxkvv_nonexistent_term_8812"
DECLARED_PROBE_CODE = "R425"  # recon: #2 code by money; named before this run
SMALL_PURCHASE_CUTOFF = 100000.0  # AMENDMENT-1; unchanged from PROTOCOL.md
MAX_WALK_PAGES = 6  # declared ceiling on the low-tail walk, per code


def zero_control():
    out = {}
    st, parsed, meta = client.award_count(NONSENSE_CODE, "c1_nonsense_psc")
    res = ((parsed or {}).get("results") or {})
    out["C1_nonsense_psc_returns_200_zero"] = {
        "status": st, "contracts": res.get("contracts"),
        "unused_filter_messages": client.unused_filter_messages(parsed),
        "pass": st == 200 and res.get("contracts") == 0}
    return out


def keyword_control():
    out = {}
    payload = {"filters": {"time_period": client.WINDOW,
                           "award_type_codes": client.AWARD_TYPES,
                           "keywords": [NONSENSE_KEYWORD]},
               "fields": ["Award ID", "Award Amount"], "subawards": False,
               "page": 1, "limit": 100}
    st, parsed, meta = client.call("spending_by_award/", payload,
                                   "c2_nonsense_keyword")
    results = (parsed or {}).get("results")
    unused = client.unused_filter_messages(parsed)
    out["C2_nonsense_keyword_returns_200_empty"] = {
        "status": st, "results_returned": len(results) if isinstance(results, list) else None,
        "pass": st == 200 and results == []}
    out["C3_keyword_filter_is_used"] = {
        "unused_filter_messages": unused, "pass": st == 200 and not unused}
    return out


def sort_direction_and_limit_ceiling():
    """C4, C5 and C7 on one code."""
    out = {}
    st, parsed, _ = client.by_award(
        {"filters": client.base_filters(psc_codes=[DECLARED_PROBE_CODE]),
         "order": "asc"},
        "c4_sort_asc_page1")
    results = (parsed or {}).get("results") or []
    amts = [r["Award Amount"] for r in results if isinstance(r.get("Award Amount"), (int, float))]
    ascending = bool(amts) and amts == sorted(amts)
    out["C4_asc_order_is_ascending"] = {
        "status": st, "n": len(amts), "first": amts[0] if amts else None,
        "last": amts[-1] if amts else None, "pass": st == 200 and ascending}

    st5, parsed5, _ = client.by_award(
        {"filters": client.base_filters(psc_codes=[DECLARED_PROBE_CODE]),
         "order": "asc", "limit": 500}, "c5_limit_500")
    out["C5_limit_above_100_refused"] = {"status": st5, "pass": st5 == 422}

    # C7 -- the declared reason for AMENDMENT-1, asserted rather than described.
    below = [a for a in amts if a <= SMALL_PURCHASE_CUTOFF]
    money = [a for a in below if 0 < a <= SMALL_PURCHASE_CUTOFF]
    nonmoney = [a for a in below if a <= 0]
    out["C7_smallest_awards_are_not_all_money"] = {
        "cutoff": SMALL_PURCHASE_CUTOFF, "rows_at_or_below_cutoff": len(below),
        "of_which_positive": len(money), "of_which_zero_or_negative": len(nonmoney),
        "min": min(amts) if amts else None,
        "pass": st == 200 and len(nonmoney) > 0}
    return out


def endpoint_agreement():
    """C6 -- the same code counted two ways must agree about existence."""
    st, parsed, _ = client.award_count(DECLARED_PROBE_CODE, "c6a_award_count")
    counted = ((parsed or {}).get("results") or {}).get("contracts")
    stc, parsedc, _ = client.category_psc(
        {"filters": client.base_filters(psc_codes=[DECLARED_PROBE_CODE])},
        "c6b_category_total")
    rows = (parsedc or {}).get("results") or []
    amount = rows[0].get("amount") if rows else None
    return {"C6_endpoints_agree_on_existence": {
        "code": DECLARED_PROBE_CODE, "award_count_status": st, "awards": counted,
        "category_status": stc, "total_obligated_awards_level": amount,
        "pass": counted is not None and counted > 0 and amount is not None
                and amount > 0}}


def main():
    checks = {}
    checks.update(zero_control())
    checks.update(keyword_control())
    checks.update(sort_direction_and_limit_ceiling())
    checks.update(endpoint_agreement())

    g2 = [checks[k]["pass"] for k in checks if k.startswith(("C1", "C2", "C3"))]
    verdict = {"experiment": "E196", "panel": 1,
               "host_python": sys.version.split()[0],
               "checks": checks,
               "G1_instrument_facts": all(
                   checks[k]["pass"] for k in
                   ("C4_asc_order_is_ascending", "C5_limit_above_100_refused",
                    "C6_endpoints_agree_on_existence",
                    "C7_smallest_awards_are_not_all_money")),
               "G2_zero_control": all(g2),
               "G2_detail": {k: checks[k]["pass"] for k in
                             ("C1_nonsense_psc_returns_200_zero",
                              "C2_nonsense_keyword_returns_200_empty",
                              "C3_keyword_filter_is_used")}}
    path = os.path.join(client.RAW, "panel1.json")
    with open(path, "w") as fh:
        json.dump(verdict, fh, indent=2, sort_keys=True)

    for k in sorted(checks):
        print("%-45s %s  %s" % (k, "PASS" if checks[k]["pass"] else "FAIL",
                                json.dumps({x: y for x, y in checks[k].items()
                                            if x != "pass"})))
    print("G1_instrument_facts=%s  G2_zero_control=%s"
          % (verdict["G1_instrument_facts"], verdict["G2_zero_control"]))
    return 0 if (verdict["G1_instrument_facts"] and verdict["G2_zero_control"]) else 3


if __name__ == "__main__":
    sys.exit(main())