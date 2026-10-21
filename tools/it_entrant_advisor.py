#!/usr/bin/env python3
"""
E209 Small Program Entrant Advisor v1

A reversible exploratory prototype that helps small government contracting
programs identify the best PSC codes for market entry, using the
E209-inspired segment newcomer measurement framework.
"""

import sys
import os
import json
import math
import urllib.request
import urllib.error
import hashlib
import time
import ssl

sys.path.insert(0, os.path.dirname(__file__))

BASE = "https://api.usaspending.gov/api/v2/search/"
UA = "think-free-research/0.1 (+it-entrant-advisor)"

CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]

DEFAULT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(window, **extra):
    f = {"time_period": window, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call_api(payload, capture_name, retries=3, pause=1.0):
    url = BASE + "spending_by_category/recipient/"
    body = json.dumps(payload).encode()
    RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    meta_path = os.path.join(RAW_DIR, capture_name + ".meta.json")
    body_path = os.path.join(RAW_DIR, capture_name + ".json")

    if os.path.exists(body_path) and os.path.exists(meta_path):
        try:
            prior = json.load(open(meta_path))
            if (prior.get("request") == payload
                    and prior.get("response", {}).get("endpoint") == url):
                with open(body_path, "rb") as fh:
                    cached = fh.read()
                meta = dict(prior["response"], reused=True)
                try:
                    return (meta.get("status"),
                            json.loads(cached.decode("utf-8", "replace")), meta)
                except Exception:
                    pass
        except Exception:
            pass

    last = (None, b"")
    status, raw = None, b""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json",
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(
                    req, timeout=180,
                    context=ssl.create_default_context()) as r:
                status, raw = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
            last = (status, raw)
            if e.code not in (429, 500, 502, 503, 504) and attempt == retries:
                break
        except Exception as e:
            last = (None, ("%s: %s" % (type(e).__name__, e)).encode())
            raw = b""
            if attempt == retries:
                break
        time.sleep(pause * (attempt + 1))
    else:
        status, raw = last

    os.makedirs(RAW_DIR, exist_ok=True)
    with open(body_path, "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status, "bytes": len(raw or b""),
             "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(meta_path, "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1, sort_keys=True)

    try:
        parsed = json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        parsed = None
    return status, parsed, meta


def fetch_window(code, window_name):
    windows = {"current": CURRENT_WINDOW, "prior": PRIOR_WINDOW}
    window = windows[window_name]
    all_results = []
    all_statuses = []
    all_unused = []
    page = 1
    has_next = True
    while has_next:
        payload = {
            "filters": base_filters(window, psc_codes=[code]),
            "limit": 100, "page": page, "spending_level": "awards",
        }
        name = "%s_%s_p%d" % (window_name, code, page)
        st, parsed, meta = call_api(payload, name)
        all_statuses.append({"page": page, "status": st,
                             "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        msgs = parsed.get("messages") or []
        all_unused.extend(m for m in msgs
                          if isinstance(m, str) and "were not used" in m)
        page_meta = parsed.get("page_metadata") or {}
        has_next = page_meta.get("hasNext", False)
        page += 1
        if page > 500:
            all_statuses.append({"page": page, "status": "CEILING",
                                 "reused": False})
            break
    return {"code": code, "window": window_name, "rows": all_results,
            "statuses": all_statuses, "unused_filters": all_unused}


def obligation_by_id(rows):
    by_id = {}
    missing = 0
    for r in rows:
        rid = r.get("recipient_id")
        if not rid:
            missing += 1
            continue
        amt = r.get("amount") or 0.0
        by_id[rid] = by_id.get(rid, 0.0) + amt
    return by_id, missing


def top_k_share(by_id, k=5):
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total


def analyze_code(code, window_data):
    cur = window_data.get("current", {})
    pri = window_data.get("prior", {})

    cur_rows = cur["rows"]
    pri_rows = pri["rows"]

    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

    dom_new = cur_ids - pri_ids
    dom_frac = len(dom_new) / len(cur_ids) if cur_ids else 0.0

    frag = 1.0 - top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)
    obligation_billions = round(obligation / 1e9, 2)
    attractiveness = round(seg_frac * (obligation / 1e9), 4)

    return {
        "code": code,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "domain_newcomer_fraction": round(dom_frac, 4),
        "fragmentation": round(frag, 4),
        "top5_share_percent": round((1 - frag) * 100, 1),
        "current_obligation": obligation,
        "current_obligation_billions": obligation_billions,
        "attractiveness_score": attractiveness,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
    }


def compute_advisor(results):
    sorted_results = sorted(results, key=lambda x: x["attractiveness_score"], reverse=True)

    survive = [r for r in results if r["segment_newcomer_fraction"] >= 0.30]
    entry = [r for r in results if 0 < r["segment_newcomer_fraction"] < 0.30]
    no_entry = [r for r in results if r["segment_newcomer_fraction"] == 0]

    survive_sorted = sorted(survive, key=lambda x: x["attractiveness_score"], reverse=True)
    entry_sorted = sorted(entry, key=lambda x: x["segment_newcomer_fraction"], reverse=True)
    no_entry_sorted = sorted(no_entry, key=lambda x: x["current_obligation_billions"], reverse=True)

    median_frac = round(
        sorted([r["segment_newcomer_fraction"] for r in results])[
            len(results) // 2] if len(results) % 2 else
        (sorted([r["segment_newcomer_fraction"] for r in results])[
         len(results) // 2 - 1] +
         sorted([r["segment_newcomer_fraction"] for r in results])[
         len(results) // 2]) / 2, 4)

    return {
        "survive": survive_sorted,
        "entry": entry_sorted,
        "no_entry": no_entry_sorted,
        "all_ranked": sorted_results,
        "median_frac": median_frac,
    }


def main():
    codes = DEFAULT_CODES[:]
    if len(sys.argv) > 1:
        codes = sys.argv[1:]

    print("=" * 72)
    print("E209 SMALL PROGRAM ENTRANT ADVISOR — v1 (experimental)")
    print("=" * 72)
    print()
    print("Measuring segment newcomer fractions for USAspending PSC codes,")
    print("mirroring the E208 experiment design for NIH SBIR.")
    print()
    print("Practical difficulty: Small government contracting programs struggle to")
    print("identify which PSC codes offer the best market entry opportunities.")
    print("Who experiences it: Small businesses, startups, and new market entrants.")
    print()

    all_results = []

    for code in codes:
        print("Fetching %s ... " % code, flush=True)

        cur = fetch_window(code, "current")
        pri = fetch_window(code, "prior")

        cur_summary = analyze_code(code, {"current": cur, "prior": pri})
        all_results.append(cur_summary)

        print("  Current recipients: %d" % cur_summary["current_recipients"])
        print("  Prior recipients: %d" % cur_summary["prior_recipients"])
        print("  Segment newcomers: %d" % cur_summary["segment_newcomers"])
        print("  Segment fraction: %.4f" % cur_summary["segment_newcomer_fraction"])
        print("  Domain newcomers: %d" % cur_summary["domain_newcomer_fraction"])
        print("  Fragmentation (1-top5): %.4f" % cur_summary["fragmentation"])
        print("  Top-5 share: %.1f%%" % cur_summary["top5_share_percent"])
        print("  Obligation: $%d (%.2fB)" % (
            cur_summary["current_obligation"],
            cur_summary["current_obligation_billions"]))
        print("  Attractiveness score: %.4f" % cur_summary["attractiveness_score"])
        print()

    adviser = compute_advisor(all_results)

    # Summary table
    print("=" * 72)
    print("ENTRANT ADVISOR — CODE RANKINGS (by attractiveness score)")
    print("=" * 72)
    print("%-8s %8s %7s %8s %6s $%10s  %8s" % ("code", "current", "prior",
                "segment", "frac", "obligationB", "verdict"))
    print("-" * 72)
    for r in sorted(all_results, key=lambda x: x["attractiveness_score"], reverse=True):
        frac = r["segment_newcomer_fraction"]
        if frac >= 0.30:
            verdict = "SURVIVE"
        elif frac > 0:
            verdict = "ENTRY"
        else:
            verdict = "NO_ENTRY"
        print("%-8s %8d %7d %8d %6.4f $%10.2fB  %8s" %
              (r["code"],
               r["current_recipients"],
               r["prior_recipients"],
               r["segment_newcomers"],
               frac,
               r["current_obligation_billions"],
               verdict))

    # Kill gate verdict
    print()
    print("G3 entry (kill gate): threshold = 0.30")
    print("median segment-newcomer fraction: %.4f" % adviser["median_frac"])
    kill = adviser["median_frac"] < 0.30
    print("verdict: %s" % ("KILL — gate fired" if kill else "survives"))

    # Recommendations
    print()
    print("RECOMMENDATIONS FOR SMALL PROGRAM ENTRANTS")
    print("=" * 50)

    if adviser["survive"]:
        print()
        print("Codes SURVIVING the kill gate (segment fraction >= 0.30):")
        for r in adviser["survive"]:
            print("  %s: %.4f segment entrants, $%.2fB obligation, top-5 share %.1f%%"
                  % (r["code"], r["segment_newcomer_fraction"],
                     r["current_obligation_billions"], r["top5_share_percent"]))

    if adviser["entry"]:
        print()
        print("Codes with significant entry (0 < segment fraction < 0.30):")
        for r in adviser["entry"]:
            print("  %s: %.4f segment entrants, $%.2fB obligation, top-5 share %.1f%%"
                  % (r["code"], r["segment_newcomer_fraction"],
                     r["current_obligation_billions"], r["top5_share_percent"]))

    if adviser["no_entry"]:
        print()
        print("Codes with 0 segment newcomers (all recipients pre-existing):")
        for r in adviser["no_entry"]:
            print("  %s: 0 newcomers, $%.2fB obligation, top-5 share %.1f%%"
                  % (r["code"], r["current_obligation_billions"], r["top5_share_percent"]))

    # Key finding
    print()
    print("KEY FINDING:")
    n_no_entry = len(adviser["no_entry"])
    n_entry = len(adviser["entry"])
    n_survive = len(adviser["survive"])
    if n_no_entry > 0:
        print("  • %d of %d codes have 0 segment newcomers — all current recipients"
              " were already active in the prior window (FY2018–FY2022)." %
              (n_no_entry, len(all_results)))
    if n_entry > 0:
        print("  • %d of %d codes have significant newcomer entry (0 < fraction < 0.30)." %
              (n_entry, len(all_results)))
    if n_survive > 0:
        print("  • Only %d of %d codes survives the 0.30 kill gate." % (n_survive, len(all_results)))
    if n_no_entry == 0 and n_entry == 0 and n_survive == 0:
        print("  • No codes have significant newcomer entry.")


if __name__ == "__main__":
    import ssl
    main()