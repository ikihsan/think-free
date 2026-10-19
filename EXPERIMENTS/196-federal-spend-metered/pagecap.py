#!/usr/bin/env python3
"""E196 instrument measurement -- how deep `spending_by_award` actually goes.

Not a gate and not a repair. `spending_by_award` answers 200 for page 1 and 422
for page 1,512 (R499's median stratum), and 422 for page 10,000. Panel 2 read
that as a per-code failure and reported `G1: false`; the honest reading needs
the *cutoff* measured rather than inferred, and the deepest reachable award
block captured as bytes so the ceiling is in the record rather than in a
terminal scroll.

Three numbers, each exact:
  * the highest page index that returns 200, found by bisection on R499
  * the resulting deepest reachable award rank (page x 100)
  * that deepest block's amount range, per affected code
"""
import json
import os
import sys

import client
from thresholds import SMALL_CUTOFF

PROBE_CODE = "R499"  # 302,317 awards: the code whose median is furthest out
# The codes panel 2 could not give a median stratum to, from panel2_rows.json.
AFFECTED = ["R499", "6505", "R706", "9130", "6515", "1560", "8915", "8905", "6640"]
MAX_PAGES = 500


def deepest_page():
    lo, hi = 1, 4096
    while lo < hi:
        mid = (lo + hi) // 2
        st, _, _ = client.by_award(
            {"filters": client.base_filters(psc_codes=[PROBE_CODE]),
             "order": "asc", "page": mid}, "pagecap_bisect_%s_%d" % (PROBE_CODE, mid))
        if st == 200:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


def deepest_block(code):
    st, parsed, _ = client.by_award(
        {"filters": client.base_filters(psc_codes=[code]), "order": "asc",
         "page": MAX_PAGES}, "pagecap_deep_%s" % code)
    amts = [r["Award Amount"] for r in ((parsed or {}).get("results") or [])
            if isinstance(r.get("Award Amount"), (int, float))]
    return {"code": code, "page": MAX_PAGES, "status": st, "rows": len(amts),
            "min": min(amts) if amts else None, "max": max(amts) if amts else None}


def main():
    page = deepest_page()
    blocks = [deepest_block(c) for c in AFFECTED]
    out = {"experiment": "E196", "measurement": "spending_by_award page ceiling",
           "probe_code": PROBE_CODE, "highest_page_returning_200": page,
           "first_page_returning_422": page + 1,
           "deepest_reachable_award_rank": page * 100,
           "rank_checkpoints_unreachable_by_construction": [100000, 1000000],
           "codes_panel2_could_not_median": AFFECTED,
           "deepest_block_amounts": blocks,
           "cutoff_note": "the %.0f-dollar cutoff is irrelevant here; these are "
                          "the smallest awards, not the sub-cutoff ones" % SMALL_CUTOFF}
    with open(os.path.join(client.RAW, "pagecap.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("highest page returning 200: %d  (page %d is the first 422)"
          % (page, page + 1))
    print("deepest reachable award rank: %d" % (page * 100))
    for b in blocks:
        print("  %-6s page %d status=%s rows=%-4s amount %s .. %s"
              % (b["code"], b["page"], b["status"], b["rows"],
                 format(b["min"], ",.2f") if b["min"] is not None else "None",
                 format(b["max"], ",.2f") if b["max"] is not None else "None"))
    return 0


if __name__ == "__main__":
    sys.exit(main())