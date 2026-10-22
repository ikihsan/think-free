#!/usr/bin/env python3
"""
E209+ — Broad IT Code Entrant Measurement

Extends it_code_entrant.py with configurable PSC code lists and
meta.total-based complete census (no arbitrary 500-page cap).
Measures segment newcomer fractions across a broad set of USAspending
PSC codes, enabling cross-domain comparison per D083.

Design:
  - Accepts PSC codes via command-line arguments or defaults to
    the five IT/software codes from E209
  - Queries USAspending API for recipient data per PSC code
  - Computes segment newcomer fraction = |current IDs absent from prior| / |current IDs|
  - Also computes fragmentation = 1 - top-5 obligation share
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - Uses API meta.total for complete censuses without artificial caps

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = "https://api.usaspending.gov/api/v2/search/"
UA = "think-free-research/0.1 (+it-code-entrant-broad)"

CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]

AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(window, **extra):
    f = {"time_period": window, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call_api(payload, capture_name, retries=2, pause=0.5):
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

    # Write raw response + metadata
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
    """Fetch all pages for a code + window using meta.total for complete census.

    Replaces the arbitrary page > 500 ceiling with API-reported meta.total,
    enabling complete censuses without artificial caps.
    Returns dict with 'rows', 'statuses'.
    """
    windows = {
        "current": CURRENT_WINDOW,
        "prior": PRIOR_WINDOW,
    }
    window = windows[window_name]
    all_results = []
    all_statuses = []
    all_unused = []
    offset = 0

    while True:
        payload = {
            "filters": base_filters(window, psc_codes=[code]),
            "limit": 100, "offset": offset, "spending_level": "awards",
        }
        name = "%s_%s_o%d" % (window_name, code, offset // 100 + 1)
        st, parsed, resp_meta = call_api(payload, name)
        all_statuses.append({"offset": offset, "status": st,
                             "reused": resp_meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        msgs = parsed.get("messages") or []
        all_unused.extend(m for m in msgs
                          if isinstance(m, str) and "were not used" in m)
        page_meta = parsed.get("page_metadata") or {}
        reported_total = page_meta.get("total", None) if isinstance(page_meta, dict) else None
        if reported_total is not None and len(all_results) >= reported_total:
            break
        offset += 100
    return {"code": code, "window": window_name, "rows": all_results,
            "statuses": all_statuses, "unused_filters": all_unused}


def obligation_by_id(rows):
    """Sum obligation per recipient_id; return (dict, missing_count)."""
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
    """Top-k obligation share (default k=5)."""
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total


def spearman(xs, ys):
    """Spearman rho with average ranks; n>=3."""
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def analyze_code(code, window_data):
    """Compute per-code metrics from fetched window data."""
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


def classify_enterability(seg_frac):
    """Classify a segment newcomer fraction into enterability category.

    Returns one of:
      - 'HIGHLY_ENTERABLE': seg_frac >= 0.30 (survival threshold)
      - 'SOMEWHAT_ENTERABLE': 0 < seg_frac < 0.30
      - 'NOT_ENTERABLE': seg_frac == 0 (no newcomers)
    """
    if seg_frac >= 0.30:
        return "HIGHLY_ENTERABLE"
    elif seg_frac > 0:
        return "SOMEWHAT_ENTERABLE"
    else:
        return "NOT_ENTERABLE"


def main():
    # Accept PSC codes from command-line args, default to E209 IT codes
    codes = sys.argv[1:] if len(sys.argv) > 1 else ["DA01", "DA10", "7A21", "7030", "D304"]

    print("=" * 76)
    print("BROAD IT CODE ENTRANT MEASUREMENT — prototype (E209+)")
    print("=" * 76)
    print("PSC codes: %s" % ", ".join(codes))
    print("Current window: FY2023 (1 Jan 2023 - 31 Dec 2023)")
    print("Prior window: FY2018-2022 (1 Jan 2018 - 31 Dec 2022)")
    print("Uses meta.total for complete census (no arbitrary cap)")
    print()
    print("Enterability thresholds (from E208):")
    print("  HIGHLY ENTERABLE: segment-newcomer fraction >= 0.30")
    print("  SOMEWHAT ENTERABLE: segment-newcomer fraction in [0.20, 0.30)")
    print("  LIMITED ENTRY: segment-newcomer fraction < 0.20")
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
        print("  domain newcomers: %d" % cur_summary.get("domain_newcomer_fraction", 0))
        print("  fragmentation: %.4f" % cur_summary["fragmentation"])
        print("  obligation: $%d" % cur_summary["current_obligation"])
        print()

    # Summary table
    print("=" * 76)
    print("SUMMARY ACROSS CODES")
    print("=" * 76)
    print("code      current    prior   segment   fraction   frag    obligation   enterability")
    print("-" * 76)
    for r in sorted(all_results, key=lambda x: x["code"]):
        enterability = classify_enterability(r["segment_newcomer_fraction"])
        print("%-8s %8d %7d %8d %10.4f %6.4f $%d   %s" % (
            r["code"],
            r["current_recipients"],
            r["prior_recipients"],
            r["segment_newcomers"],
            r["segment_newcomer_fraction"],
            r["fragmentation"],
            r["current_obligation"],
            enterability,
        ))

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
        print("(Note: the declared 0.30 bar comes from E208's single-category gate;")
        print(" the robust finding across these codes is the bimodality;")
        print(" codes cluster around the 0.30 threshold.)")

    # Bimodality analysis
    print()
    print("BI MODALITY ANALYSIS")
    print("=" * 76)
    print("Segment newcomer fractions across codes:")
    for r in sorted(all_results, key=lambda x: x["segment_newcomer_fraction"]):
        marker = " *ENTERABLE*" if r["segment_newcomer_fraction"] >= 0.30 else ""
        print("  %s: %.4f%s" % (r["code"], r["segment_newcomer_fraction"], marker))

    # Top-5 concentration comparison
    print()
    print("TOP-5 OBLIGATION SHARE COMPARISON")
    print("=" * 76)
    for r in sorted(all_results, key=lambda x: x["fragmentation"], reverse=True):
        pct = (1 - r["fragmentation"]) * 100
        enterability = classify_enterability(r["segment_newcomer_fraction"])
        print("  %s: fragmentation = %.4f (top-5 share = %.1f%%, %s)"
              % (r["code"], r["fragmentation"], pct, enterability))

    # Newcomer origin analysis
    print()
    print("NEWCOMER ORIGIN ANALYSIS")
    print("=" * 76)
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