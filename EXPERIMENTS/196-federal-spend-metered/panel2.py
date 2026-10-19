#!/usr/bin/env python3
"""E196 panel 2 -- is federal contract spend metered?

The measurement PROTOCOL.md declares and AMENDMENT-1/2 repair. Reads nothing it
wrote: every number comes from api.usaspending.gov and every response body is on
disk under raw/ before it is parsed. Panel 1 holds G2; it is re-asserted here as
a precondition rather than treated as a result.
"""
import json
import os
import sys
import math
import time

import client
from analysis import analyse
from thresholds import SMALL_CUTOFF, RANK_CHECKPOINTS
from stats import median

RAW = client.RAW


def fetch_head():
    st, parsed, meta = client.category_psc(
        {"filters": client.base_filters()}, "head100")
    rows = (parsed or {}).get("results") or []
    unused = client.unused_filter_messages(parsed)
    head = [{"code": r.get("code"), "name": r.get("name"),
             "total_awards_level": r.get("amount")} for r in rows
            if r.get("code")]
    return st, head, unused, meta


def fetch_code(code, idx, total_awards_level):
    """I2, I3 (AMENDMENT-3 rank profile), I3' (AMENDMENT-1 low tail) and I4."""
    rec = {"code": code, "total_awards_level": total_awards_level}
    st, parsed, _ = client.award_count(code, "%03d_%s_count" % (idx, code))
    res = ((parsed or {}).get("results") or {})
    rec["award_count"] = res.get("contracts")
    rec["count_status"] = st
    rec["count_unused_filters"] = client.unused_filter_messages(parsed)

    rows, walked, stopped, statuses = client.low_tail_awards(
        code, SMALL_CUTOFF, "%03d_%s_tail" % (idx, code))
    rec["tail_statuses"] = statuses
    rec["tail_pages"] = walked
    rec["tail_censored"] = not stopped

    pos, zero, neg = [], 0, 0
    for r in rows:
        amt = r.get("Award Amount")
        if not isinstance(amt, (int, float)):
            continue
        if amt > 0:
            pos.append((amt, r.get("Description") or ""))
        elif amt == 0:
            zero += 1
        else:
            neg += 1
    rec["tail_rows_below_cutoff"] = len(rows)
    rec["tail_positive"] = len(pos)
    rec["tail_zero"] = zero
    rec["tail_negative"] = neg
    rec["small_purchase_sum"] = sum(a for a, _ in pos)
    rec["small_purchase_is_lower_bound"] = rec["tail_censored"]
    rec["tail_descriptions"] = pos

    n = rec["award_count"]
    if isinstance(n, int) and n > 0:
        page = max(1, int(math.ceil(n / 200.0)))
        st4, parsed4, _ = client.by_award(
            {"filters": client.base_filters(psc_codes=[code]), "order": "desc",
             "page": page}, "%03d_%s_median" % (idx, code))
        res4 = (parsed4 or {}).get("results") or []
        amts4 = [r["Award Amount"] for r in res4
                 if isinstance(r.get("Award Amount"), (int, float))]
        desc4 = [(r.get("Description") or "") for r in res4]
        rec["median_status"] = st4
        rec["median_page"] = page
        rec["median_rows"] = len(amts4)
        rec["median_award"] = median(amts4)
        rec["median_descriptions"] = desc4
        rec["rank_profile"] = client.rank_profile(
            code, RANK_CHECKPOINTS, "%03d_%s" % (idx, code))
    else:
        rec["median_status"] = None
        rec["median_page"] = None
        rec["median_rows"] = 0
        rec["median_award"] = None
        rec["median_descriptions"] = []
        rec["rank_profile"] = {}
    return rec




def main():
    started = time.time()
    st, head, unused, meta = fetch_head()
    print("I1 head100: status=%s codes=%d unused_filters=%d"
          % (st, len(head), len(unused)), flush=True)
    if st != 200 or len(head) < 10:
        json.dump({"error": "head fetch failed", "status": st,
                   "unused_filters": unused},
                  open(os.path.join(RAW, "panel2.json"), "w"), indent=2)
        return 3

    g2_ok = all(c["pass"] for c in [
        json.load(open(os.path.join(RAW, "panel1.json")))["checks"][k] for k in
        ("C1_nonsense_psc_returns_200_zero",
         "C2_nonsense_keyword_returns_200_empty", "C3_keyword_filter_is_used")])

    recs = []
    for i, h in enumerate(head, 1):
        rec = fetch_code(h["code"], i, h["total_awards_level"])
        rec["name"] = h["name"]
        recs.append(rec)
        prof = rec.get("rank_profile") or {}
        at10k = prof.get(10000) or {}
        print("  %3d/%d %-6s total=$%-15s awards=%-8s med=$%-13s "
              "rank10k<=$%-12s%s"
              % (i, len(head), rec["code"],
                 format(int(rec.get("total_awards_level") or 0), ","),
                 rec.get("award_count"),
                 format(int(rec.get("median_award") or 0), ","),
                 format(int(at10k.get("max") or 0), ","),
                 " CENSORED" if rec.get("tail_censored") else ""), flush=True)

    # G1 is a source-shape gate, so it is evaluated on what actually came back.
    g1_ok = all(isinstance(r.get("total_awards_level"), (int, float))
                and isinstance(r.get("award_count"), int)
                and r.get("award_count") >= 0
                and r.get("median_status") == 200
                for r in recs)
    unused_seen = sum(len(r.get("count_unused_filters") or []) for r in recs)

    result = analyse(head, recs, g1_ok, g2_ok)
    result["panel2_unused_filter_messages_in_count_requests"] = unused_seen
    result["codes_with_unused_filter_message"] = [
        r["code"] for r in recs if r.get("count_unused_filters")]
    result["head_unused_filter_messages"] = unused
    result["wall_seconds"] = round(time.time() - started, 1)
    result["verdict"] = {
        "G1_source_shape": g1_ok, "G2_zero_control": g2_ok,
        "G3_discrimination": result["G3"]["fire"],
        "G4_addressability": result["G4"]["fire"],
        "G5_description_control": result["G5"]["fire"],
        "axis_closed": not (g2_ok and g1_ok and result["G4"]["fire"])}
    with open(os.path.join(RAW, "panel2.json"), "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
    for r in recs:
        r.pop("tail_descriptions", None)
        r.pop("median_descriptions", None)
    with open(os.path.join(RAW, "panel2_rows.json"), "w") as fh:
        json.dump(recs, fh, indent=1, sort_keys=True)

    print("\nG1=%s G2=%s G3(p=%.4g)=%s G4=%s G5=%s  axis_closed=%s"
          % (g1_ok, g2_ok, result["G3"]["p"], result["G3"]["fire"],
             result["G4"]["fire"], result["G5"]["fire"],
             result["verdict"]["axis_closed"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
