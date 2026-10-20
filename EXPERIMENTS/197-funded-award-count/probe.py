#!/usr/bin/env python3
"""E197 instrument capability probe -- which filters does USAspending honour here?

Not a gate and not a result. E196 left a named next action ("bisect the ascending
order for the rank at which award amounts turn positive") written for the only
instrument that record had used, `spending_by_award` sorted ascending, whose
readable depth is capped at 50,000 awards (E196 F143). If the API can answer
"how many awards in this cell carry money" directly, the count does not need
bisection and the 50,000 ceiling stops being the limiting instrument.

This probe asks three questions and records the raw bodies of the answers:

  P1  does `spending_by_award_count/` accept an `award_amounts` range filter,
      and does the count it returns actually differ from the unfiltered count?
  P2  does `spending_by_award/` return rows that *satisfy* the same filter, or
      rows that merely carry a "not used" message while answering about the
      whole cell?
  P3  what is the smallest amount that separates records, i.e. how many distinct
      low values sit in the ascending head of a cell?

Everything here is `not evaluated` with respect to any gate; the gates are
declared in PROTOCOL.md and run by panel1.py.
"""
import json
import os
import sys

import client

# Two codes with known shapes from E196: DA01 is one of the five IT/software
# cells with $203.32B between them and a 10,000th-smallest award of $27,519;
# R499 is the cell whose 50,000th award is about $52, so it is where the
# zero-record question is sharpest.
CODES = ["DA01", "R499"]


def count_with(code, amount_from, amount_to, name):
    """`spending_by_award_count` with an amount range, if the API honours one."""
    filters = client.base_filters(psc_codes=[code])
    if amount_from is not None:
        filters["award_amounts"] = {"from": amount_from}
    if amount_to is not None:
        filters["award_amounts"] = filters.get("award_amounts", {})
        filters["award_amounts"]["to"] = amount_to
    payload = {"filters": filters, "subawards": False, "page": 1, "limit": 1}
    st, parsed, meta = client.call("spending_by_award_count/", payload, name)
    return {"code": code, "from": amount_from, "to": amount_to, "status": st,
            "response": parsed, "meta": meta,
            "ignored_filter_messages": client.unused_filter_messages(parsed)}


def rows_with(code, amount_from, amount_to, name):
    """`spending_by_award` with the same filter, ascending, so the amounts on
    the first page can be checked against the filter rather than assumed."""
    filters = client.base_filters(psc_codes=[code])
    if amount_from is not None:
        filters["award_amounts"] = {"from": amount_from}
    if amount_to is not None:
        filters["award_amounts"] = filters.get("award_amounts", {})
        filters["award_amounts"]["to"] = amount_to
    payload = {"filters": filters, "subawards": False,
               "fields": ["Award ID", "Award Amount", "Description",
                          "generated_unique_award_id", "Awarding Agency"],
               "sort": "Award Amount", "order": "asc", "page": 1, "limit": 100}
    st, parsed, meta = client.call("spending_by_award/", payload, name)
    results = parsed.get("results") if isinstance(parsed, dict) else None
    amts = [r.get("Award Amount") for r in (results or [])]
    return {"code": code, "from": amount_from, "to": amount_to, "status": st,
            "rows": len(amts or []),
            "min_amount": min(amts) if amts else None,
            "max_amount": max(amts) if amts else None,
            "total_available": (parsed or {}).get("page_metadata", {}).get("total")
                if isinstance(parsed, dict) else None,
            "ignored_filter_messages": client.unused_filter_messages(parsed)}


def main():
    out = {"experiment": "E197", "stage": "instrument capability probe",
           "codes": CODES, "P1_count_filter": [], "P2_rows_honour_filter": [],
           "P3_low_tail": []}
    for code in CODES:
        # P1: unfiltered count, then three thresholds. `from=0.01` is the
        # cheapest statement of "carries money" that the API can express, since
        # the API takes decimals rather than an inequality.
        out["P1_count_filter"].append(
            count_with(code, None, None, "probe_count_%s_total" % code))
        for frm in (0.01, 1.0, 100.0):
            out["P1_count_filter"].append(
                count_with(code, frm, None, "probe_count_%s_from%s" % (code, frm)))
        # P2: does the row-level read agree with the count-level read?
        out["P2_rows_honour_filter"].append(
            rows_with(code, 1.0, None, "probe_rows_%s_from1" % code))
        out["P2_rows_honour_filter"].append(
            rows_with(code, None, 100000.0, "probe_rows_%s_to100000" % code))
        # P3: the ascending head, unfiltered, to see what the low end holds.
        out["P3_low_tail"].append(
            rows_with(code, None, None, "probe_rows_%s_head" % code))

    path = os.path.join(client.RAW, "probe.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("P1 -- does an amount filter change the count?")
    for r in out["P1_count_filter"]:
        body = r["response"] if isinstance(r["response"], dict) else {}
        print("  %-6s from=%-5s status=%s count=%-12s ignored=%s"
              % (r["code"], r["from"], r["status"], body.get("total"),
                 r["ignored_filter_messages"] or "-"))
    print("P2 -- do returned rows satisfy the filter?")
    for r in out["P2_rows_honour_filter"]:
        print("  %-6s from=%-5s to=%-8s status=%s rows=%-4s min=%-12s max=%-12s total=%s"
              % (r["code"], r["from"], r["to"], r["status"], r["rows"],
                 r["min_amount"], r["max_amount"], r["total_available"]))
    print("P3 -- ascending head, unfiltered")
    for r in out["P3_low_tail"]:
        print("  %-6s status=%s rows=%-4s min=%-12s max=%-12s"
              % (r["code"], r["status"], r["rows"], r["min_amount"], r["max_amount"]))
    print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())