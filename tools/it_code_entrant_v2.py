#!/usr/bin/env python3
"""
E209: IT Code Entrant Measurement v2

Measures segment newcomer fractions for USAspending PSC codes,
mirroring the E208 experiment design for NIH SBIR. A reversible
exploratory prototype — evidence-gathering, not product validation.

Design:
  - Queries USAspending API for recipient data per PSC code
  - Computes segment newcomer fraction = |current IDs absent from prior| / |current IDs|
  - Also computes fragmentation = 1 - top-5 obligation share
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - Uses API meta.total for complete census (no arbitrary cap)

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
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
UA = "think-free-research/0.1 (+it-code-entrant-v2)"

CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]

DEFAULT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(window, **extra):
    f = {"time_period": window, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call_api(payload, capture_name, retries=3, pause=1.0):
    """Make a single API call; return (status, parsed, meta)."""
    url = BASE + "spending_by_category/recipient/"
    body = json.dumps(payload).encode()
    RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    meta_path = os.path.join(RAW_DIR, capture_name + ".meta.json")
    body_path = os.path.join(RAW_DIR, capture_name + ".json")

    # Check cache
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
    """Fetch all pages for a code + window. Returns dict with 'rows', 'statuses'."""
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

    return {
        "code": code,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "domain_newcomer_fraction": round(dom_frac, 4),
        "fragmentation": round(frag, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
    }


def main():
    codes = DEFAULT_CODES[:]
    if len(sys.argv) > 1:
        codes = sys.argv[1:]

    print("=" * 72)
    print("IT CODE ENTRANT MEASUREMENT — v2 (E209-inspired)")
    print("=" * 72)
    print()

    all_results = []

    for code in codes:
        print("Fetching %s ... " % code, flush=True)

        cur = fetch_window(code, "current")
        pri = fetch_window(code, "prior")

        cur_summary = analyze_code(code, {"current": cur, "prior": pri})
        all_results.append(cur_summary)

        print("  current recipients: %d" % cur_summary["current_recipients"])
        print("  prior recipients: %d" % cur_summary["prior_recipients"])
        print("  segment newcomers: %d" % cur_summary["segment_newcomers"])
        print("  segment fraction: %.4f" % cur_summary["segment_newcomer_fraction"])
        print("  domain newcomers: %d" % cur_summary["domain_newcomer_fraction"])
        print("  fragmentation: %.4f" % cur_summary["fragmentation"])
        print("  obligation: $%d" % cur_summary["current_obligation"])
        print()

    # Summary table using f-string formatting
    print("=" * 72)
    print("SUMMARY ACROSS CODES")
    print("=" * 72)
    print("%-8s %8s %7s %8s %8s %6s $%s" % ("code", "current", "prior",
                "segment", "domain", "frag", "obligation"))
    print("-" * 72)
    for r in sorted(all_results, key=lambda x: x["code"]):
        print("%-8s %8d %7d %8d %8.4f %6.4f $%d" % (
            r["code"],
            int(r["current_recipients"]),
            int(r["prior_recipients"]),
            int(r["segment_newcomers"]),
            float(r["segment_newcomer_fraction"]),
            float(r["domain_newcomer_fraction"]),
            int(r["current_obligation"])))

    # Kill gate verdict
    fractions = [r["segment_newcomer_fraction"] for r in all_results]
    fracs_sorted = sorted(fractions)
    n = len(fracs_sorted)
    median = (fracs_sorted[n // 2] if n % 2 else
              (fracs_sorted[n // 2 - 1] + fracs_sorted[n // 2]) / 2)
    kill = median < 0.30

    print()
    print("G3 entry (kill gate): threshold = 0.30")
    print("median segment-newcomer fraction: %.4f" % median)
    print("verdict: %s" % ("KILL — gate fired" if kill else "survives"))
    if kill:
        print("(The 0.30 bar comes from E208's single-category gate;")
        print(" bimodal distribution observed across codes.)")

    # Bimodality analysis
    print()
    print("BI MODALITY ANALYSIS")
    print("=" * 50)
    print("Segment newcomer fractions across codes:")
    for r in sorted(all_results, key=lambda x: x["segment_newcomer_fraction"]):
        marker = " *SURVIVE*" if r["segment_newcomer_fraction"] >= 0.30 else ""
        print("  %s: %.4f%s" % (r["code"], r["segment_newcomer_fraction"], marker))

    # Top-5 concentration comparison
    print()
    print("TOP-5 OBLIGATION SHARE COMPARISON")
    print("=" * 50)
    for r in sorted(all_results, key=lambda x: x["fragmentation"], reverse=True):
        pct = (1 - r["fragmentation"]) * 100
        print("  %s: fragmentation = %.4f (top-5 share = %.1f%%)" %
              (r["code"], r["fragmentation"], pct))

    # Newcomer origin analysis
    print()
    print("NEWCOMER ORIGIN ANALYSIS")
    print("=" * 50)
    for r in sorted(all_results, key=lambda x: x["segment_newcomer_fraction"], reverse=True):
        if r["segment_newcomer_fraction"] > 0:
            print("  %s: %d of %d current recipients (%.2f%%) are segment newcomers"
                  % (r["code"], r["segment_newcomers"], r["current_recipients"],
                     r["segment_newcomer_fraction"] * 100))
        else:
            print("  %s: 0 of %d current recipients are segment newcomers (all pre-existing)"
                  % (r["code"], r["current_recipients"]))


if __name__ == "__main__":
    import ssl
    main()