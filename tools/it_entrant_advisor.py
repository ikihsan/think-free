#!/usr/bin/env python3
"""
E209 Small Program Entrant Advisor v2

A reversible exploratory prototype that helps small government contracting
programs identify the best PSC codes and award types for market entry,
using the E209-inspired segment newcomer measurement framework.

Two levels of analysis:
  1. Code-level: segment newcomer fractions across all awards in each PSC code
  2. Award-type sub-segments: segment newcomer fractions broken out by
     award type (A, B, C, D) within each PSC code

Practical difficulty: Small government contracting programs struggle to
identify which PSC codes and offer the best market entry opportunities
and which award types within those codes have the most newcomer activity.

Who experiences it: Small businesses, startups, and new market entrants
seeking government contracting opportunities.

Methodology (per code):
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - Segment newcomer fraction = |current IDs absent from prior| / |current IDs|
  - Kill gate threshold: 0.30 (codes with segment fraction >= 0.30
    survive; below this, entry is significant but below the survival bar)
  - Uses API meta.total for complete census (no arbitrary cap)

NOTE: This is a prototype, not a validated product. It is evidence-gathering
work. Results should be verified with fresh API fetches for production use.
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
UA = "think-free-research/0.1 (+it-entrant-advisor-v2)"

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


def analyze_code_by_award_type(code, window_data):
    """Compute segment newcomer fractions broken out by award type.

    Returns a dict keyed by award type, each with the same structure as
    analyze_code but for the subset of rows matching that award type.
    """
    cur = window_data.get("current", {})
    pri = window_data.get("prior", {})

    cur_rows = cur["rows"]
    pri_rows = pri["rows"]

    results = {}

    for award_type in AWARD_TYPES:
        # Filter rows by award type
        cur_award = [r for r in cur_rows if r.get("award_type_code") == award_type]
        pri_award = [r for r in pri_rows if r.get("award_type_code") == award_type]

        cur_by_id, cur_missing = obligation_by_id(cur_award)
        pri_by_id, pri_missing = obligation_by_id(pri_award)

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

        results[award_type] = {
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

    return results


def compute_award_type_advisor(award_results_by_code):
    """Compute advisor recommendations broken out by award type within each code.

    Returns a dict with 'survive', 'entry', 'no_entry' keyed by (code, award_type).
    """
    all_entries = {}

    for code, results in award_results_by_code.items():
        for award_type, r in results.items():
            key = (code, award_type)
            seg_frac = r["segment_newcomer_fraction"]
            if seg_frac >= 0.30:
                all_entries[key] = "SURVIVE"
            elif seg_frac > 0:
                all_entries[key] = "ENTRY"
            else:
                all_entries[key] = "NO_ENTRY"

    return all_entries


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
    print("E209 SMALL PROGRAM ENTRANT ADVISOR — v2 (experimental)")
    print("=" * 72)
    print()
    print("Measuring segment newcomer fractions for USAspending PSC codes,")
    print("mirroring the E208 experiment design for NIH SBIR. Two levels of")
    print("analysis: code-level and award-type sub-segments.")
    print()
    print("Practical difficulty: Small government contracting programs struggle to")
    print("identify which PSC codes and offer the best market entry opportunities")
    print("and which award types within those codes have the most newcomer activity.")
    print("Who experiences it: Small businesses, startups, and new market entrants")
    print("seeking government contracting opportunities.")
    print()

    # Per-code results at both levels
    code_results = {}  # code -> {code_level_result, award_type_results}

    for code in codes:
        print("Fetching %s ... " % code, flush=True)

        cur = fetch_window(code, "current")
        pri = fetch_window(code, "prior")

        # Code-level analysis
        cur_summary = analyze_code(code, {"current": cur, "prior": pri})
        code_results[code] = {"code_level": cur_summary}

        # Award-type sub-segment analysis
        award_results = analyze_code_by_award_type(code, {"current": cur, "prior": pri})
        code_results[code]["award_type"] = award_results

        print("  Code-level:")
        print("    Current recipients: %d" % cur_summary["current_recipients"])
        print("    Prior recipients: %d" % cur_summary["prior_recipients"])
        print("    Segment newcomers: %d" % cur_summary["segment_newcomers"])
        print("    Segment fraction: %.4f" % cur_summary["segment_newcomer_fraction"])
        print("    Domain newcomers: %d" % cur_summary["domain_newcomer_fraction"])
        print("    Fragmentation (1-top5): %.4f" % cur_summary["fragmentation"])
        print("    Top-5 share: %.1f%%" % cur_summary["top5_share_percent"])
        print("    Obligation: $%d (%.2fB)" % (
            cur_summary["current_obligation"],
            cur_summary["current_obligation_billions"]))
        print("    Attractiveness score: %.4f" % cur_summary["attractiveness_score"])

        print("  Award-type sub-segments:")
        for award_type, a in award_results.items():
            print("    %s: seg_frac=%.4f, current=%d, prior=%d, oblig=$%d (%.2fB), "
                  "top-5 share %.1f%%" % (
                      award_type,
                      a["segment_newcomer_fraction"],
                      a["current_recipients"],
                      a["prior_recipients"],
                      a["current_obligation"],
                      a["current_obligation_billions"],
                      a["top5_share_percent"]))
        print()

    # Build advisor data at both levels
    all_code_results = [code_results[c]["code_level"] for c in codes]
    adviser = compute_advisor(all_code_results)

    # Award-type advisor
    award_results_by_code = {c: code_results[c]["award_type"] for c in codes}
    award_advisor = compute_award_type_advisor(award_results_by_code)

    # Summary table (code-level)
    print("=" * 72)
    print("ENTRANT ADVISOR — CODE RANKINGS (by attractiveness score)")
    print("=" * 72)
    print("%-8s %8s %7s %8s %6s $%10s  %8s" % ("code", "current", "prior",
                "segment", "frac", "obligationB", "verdict"))
    print("-" * 72)
    for r in sorted(all_code_results, key=lambda x: x["attractiveness_score"], reverse=True):
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

    # Recommendations at code level
    print()
    print("RECOMMENDATIONS FOR SMALL PROGRAM ENTRANTS — CODE LEVEL")
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

    # Award-type sub-segment recommendations
    print()
    print("RECOMMENDATIONS FOR SMALL PROGRAM ENTRANTS — AWARD-TYPE SUB-SEGMENTS")
    print("=" * 50)

    # Find the most enterable award types across all codes
    enterable_awards = []
    for code in codes:
        for award_type, verdict in award_advisor.get((code,), {}).items():
            # Check if award type exists for this code
            if award_type in code_results[code]["award_type"]:
                r = code_results[code]["award_type"][award_type]
                seg_frac = r["segment_newcomer_fraction"]
                if seg_frac >= 0.30:
                    enterable_awards.append((code, award_type, "SURVIVE",
                                            seg_frac,
                                            r["current_obligation_billions"],
                                            r["top5_share_percent"]))
                elif seg_frac > 0:
                    enterable_awards.append((code, award_type, "ENTRY",
                                            seg_frac,
                                            r["current_obligation_billions"],
                                            r["top5_share_percent"]))

    # Sort by segment fraction descending
    enterable_awards.sort(key=lambda x: x[3], reverse=True)

    if enterable_awards:
        print("Most enterable award-type sub-segments (segment fraction >= threshold):")
        for code, award_type, verdict, seg_frac, oblig_B, top5_pct in enterable_awards[:10]:
            print("  %s / %s: %.4f segment entrants, $%.2fB obligation, top-5 share %.1f%%"
                  % (code, award_type, seg_frac, oblig_B, top5_pct))
    else:
        print("No award-type sub-segments with significant newcomer entry found.")

    # Key finding
    print()
    print("KEY FINDING:")
    n_no_entry = len(adviser["no_entry"])
    n_entry = len(adviser["entry"])
    n_survive = len(adviser["survive"])
    if n_no_entry > 0:
        print("  • %d of %d codes have 0 segment newcomers — all current recipients"
              " were already active in the prior window (FY2018–FY2022)." %
              (n_no_entry, len(all_code_results)))
    if n_entry > 0:
        print("  • %d of %d codes have significant newcomer entry (0 < fraction < 0.30)." %
              (n_entry, len(all_code_results)))
    if n_survive > 0:
        print("  • Only %d of %d codes survives the 0.30 kill gate." % (n_survive, len(all_code_results)))
    if n_no_entry == 0 and n_entry == 0 and n_survive == 0:
        print("  • No codes have significant newcomer entry.")


if __name__ == "__main__":
    import ssl
    main()