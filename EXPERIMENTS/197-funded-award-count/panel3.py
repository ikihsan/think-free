#!/usr/bin/env python3
"""E197 panel D -- exploratory: is the small-purchase metering spread out or
concentrated in a few buyers?

Declared exploratory in `PROTOCOL.md` §5 and gated by nothing: the agency list
is not fixed in advance, so a number here can be right and still change no
decision. It is in the run because the question is the one the next experiment
would ask, and answering it now costs about five hundred requests instead of a
whole session -- if it turns out the metering lives inside two offices, the
recipient read is not the next step and something else is.

**Filter shape, found by nine capability probes and recorded because it is the
kind of thing that reads as "not supported".** `spending_by_award` filters by
awarding agency through `filters.agencies`, but `name` must be **scalar text**,
not a list: `{"type": "awarding", "tier": "toptier", "name": ["Department of
Defense"]}` returns 422 `is not a valid type (text)` and
`"tier": "department"` returns 422 `outside valid values 'toptier' or 'subtier'`.
Two plausible-looking alternatives, `agency_codes` and `awarding_agency_ids`,
are **accepted and silently ignored** by `spending_by_award_count/` and
explicitly reported as unused by `spending_by_award/` -- the same split
`probe.py` found for `amount_requirement`. Agency totals come from
`spending_by_category/awarding_agency/`, which does honour `psc_codes`.
"""
import json
import os
import sys

import client
import funded
import thresholds as TH

RAW = client.RAW
AGENCIES_PER_CODE = 5


def top_agencies(code):
    """Top agencies by obligation inside one cell, from the category endpoint."""
    payload = {"filters": client.base_filters(psc_codes=[code]),
               "limit": AGENCIES_PER_CODE, "page": 1,
               "spending_level": "awards"}
    st, parsed, meta = client.call("spending_by_category/awarding_agency/",
                                   payload, "d3_agencies_%s" % code)
    rows = parsed.get("results") if isinstance(parsed, dict) else []
    return [{"code": r.get("code"), "name": r.get("name"), "amount": r.get("amount"),
             "status": st,
             "unused_filters": client.unused_filter_messages(parsed)} for r in rows]


def sub_cell(code, agency):
    """The same two counts, inside one cell and one awarding agency."""
    filters = client.base_filters(psc_codes=[code])
    filters["agencies"] = [{"type": "awarding", "tier": "toptier",
                            "name": agency["name"]}]
    tag = "%s_%s" % (code, (agency["code"] or "NA"))
    st, parsed, _ = client.call("spending_by_award_count/",
                                {"filters": filters, "subawards": False,
                                 "page": 1, "limit": 1}, "d3_count_%s" % tag)
    results = (parsed or {}).get("results") if isinstance(parsed, dict) else {}
    n = sum(v for v in results.values() if isinstance(v, int)) or None
    lo = funded.n_below(filters, n, TH.FUNDED_T, "d3_%s_asc" % tag)
    hi = funded.n_below(filters, n, int(TH.SMALL_CUTOFF), "d3_%s_asc" % tag)
    funded_ge_1 = None if lo["n"] is None else n - lo["n"]
    return {"code": code, "agency_code": agency["code"],
            "agency": agency["name"], "agency_share_of_cell": agency["amount"],
            "n_total": n, "funded_ge_1": funded_ge_1,
            "funded_fraction": (None if funded_ge_1 is None or not n
                                else funded_ge_1 / float(n)),
            "purchases_1_100k": (None if lo["n"] is None or hi["n"] is None
                                 else hi["n"] - lo["n"]),
            "censored_funded": lo.get("censored"),
            "unused_filters": (lo.get("unused_filters") or [])
            + (hi.get("unused_filters") or [])}


def main():
    rows = []
    for code in TH.IT_CODES:
        agencies = top_agencies(code)
        print("%s -- %d agencies" % (code, len(agencies)))
        for a in agencies:
            row = sub_cell(code, a)
            rows.append(row)
            print("   %-34s cell=%-14s N=%-7s funded=%-7s purch=%-7s frac=%s"
                  % ((row["agency"] or "")[:34], format(a["amount"] or 0, ",.0f"),
                     row["n_total"], row["funded_ge_1"],
                     row["purchases_1_100k"],
                     "%.4f" % row["funded_fraction"] if row["funded_fraction"]
                     else "-"))
        with open(os.path.join(RAW, "panel3.json"), "w") as fh:
            json.dump({"experiment": "E197", "panel": "D", "gated": False,
                       "rows": rows}, fh, indent=1, sort_keys=True)
    print("wrote %s" % os.path.join(RAW, "panel3.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())