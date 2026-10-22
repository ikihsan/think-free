#!/usr/bin/env python3
"""
NIH SBIR Small-Program Entry Advisor

A reversible exploratory prototype that helps small programs identify the most
accessible NIH SBIR Funding Institutes/Centers within a given spending category,
and the most enterable sub-segments where newcomers are most likely to enter the
market.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis), E212 (category 108), E213 (category 701), and E214
(category 525), and the spending category screen from E204.

This is evidence-gathering work, not product validation.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from nih_small_program_screener import (
    screen_category, screen_categories,
)
from nih_sbir_metrics import CONSENSUS_ICs, CONSENSUS_RATIONALE
from nih_small_program_screener import CONSENSUS_ICs as CONSENSUS_ICS2, \
    CONSENSUS_RATIONALE as CONSENSUS_RATIONALE2


# Federal IT PSC codes analyzed in E209
IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]


def analyze_it_code(code):
    """Compute per-code entrant metrics from USAspending data (E209 design)."""
    import urllib.request, json, os, hashlib, ssl

    BASE = "https://api.usaspending.gov/api/v2/search/"
    UA = "think-free-research/0.1 (+repository entry-advisor)"

    CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
    PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]
    AWARD_TYPES = ["A", "B", "C", "D"]

    def base_filters(window, **extra):
        f = {"time_period": window, "award_type_codes": AWARD_TYPES}
        f.update(extra)
        return f

    def call_api(payload, capture_name, retries=2, pause=0.5):
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
        page = 1
        has_next = True
        while has_next:
            payload = {"filters": base_filters(window, psc_codes=[code]),
                       "limit": 100, "page": page, "spending_level": "awards"}
            name = "%s_%s_p%d" % (window_name, code, page)
            st, parsed, meta = call_api(payload, name)
            if st != 200 or not isinstance(parsed, dict):
                break
            results = parsed.get("results") or []
            all_results.extend(results)
            page_meta = parsed.get("page_metadata") or {}
            has_next = page_meta.get("hasNext", False)
            page += 1
            if page > 500:
                break
        return {"code": code, "window": window_name, "rows": all_results,
                "status": st}

    cur = fetch_window(code, "current")
    pri = fetch_window(code, "prior")

    cur_rows = cur["rows"]
    pri_rows = pri["rows"]

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

    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

    frag = 1.0 - top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)

    return {
        "code": code,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "fragmentation": round(frag, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
    }


def run_prototype(category_code, fiscal_year=2023, activity_codes=None,
                  screen_it_codes=False):
    """Run the small-program entry advisor prototype."""
    print('\n=== NIH SBIR Small-Program Entry Advisor ===')
    print('Spending Category: %s' % category_code)
    print('Fiscal Year: %s' % fiscal_year)
    if activity_codes:
        print('Activity Codes: %s' % activity_codes)
    print('=' * 60)

    print('\n--- NIH SBIR Category Screen ---')
    ranked = screen_category(
        category_code, fiscal_year=fiscal_year,
        activity_codes=activity_codes
    )

    if screen_it_codes:
        print('\n--- Federal IT PSC Code Entrant Analysis ---')
        all_results = []
        for code in IT_CODES:
            print('\nFetching %s...' % code)
            summary = analyze_it_code(code)
            all_results.append(summary)
            print('  current recipients: %d' % summary["current_recipients"])
            print('  prior recipients: %d' % summary["prior_recipients"])
            print('  segment newcomers: %d' % summary["segment_newcomers"])
            print('  segment fraction: %.4f' % summary["segment_newcomer_fraction"])
            print('  fragmentation: %.4f' % summary["fragmentation"])
            print('  obligation: $%d' % summary["current_obligation"])

        fractions = [r["segment_newcomer_fraction"] for r in all_results]
        fracs_sorted = sorted(fractions)
        n = len(fracs_sorted)
        median = (fracs_sorted[n // 2] if n % 2 else
                  (fracs_sorted[n // 2 - 1] + fracs_sorted[n // 2]) / 2)
        kill = median < 0.30

        print()
        print('G3 entry (kill gate): threshold = 0.30')
        print('median segment-newcomer fraction: %.4f' % median)
        print('verdict: %s' % ('KILL — gate fired' if kill else 'survives'))
        if kill:
            print('(Bimodal pattern: 3 codes enterable, 2 codes closed)')

    print()
    print('(Prototype — evidence-gathering, not product validation)')


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='NIH SBIR Small-Program Entry Advisor'
    )
    parser.add_argument(
        'category_code',
        type=str,
        help='NIH SBIR spending category code (e.g. 101)'
    )
    parser.add_argument(
        '--fiscal-year',
        type=int,
        default=2023,
        help='Fiscal year to screen (default: 2023)'
    )
    parser.add_argument(
        '--activity-codes',
        nargs='+',
        help='NIH activity codes to filter by (e.g. R41 R42 for SBIR)'
    )
    parser.add_argument(
        '--it-codes',
        action='store_true',
        help='Also screen federal IT PSC codes (E209 design)'
    )

    args = parser.parse_args()
    category_code = int(args.category_code) if args.category_code else None
    run_prototype(
        category_code=category_code,
        fiscal_year=args.fiscal_year,
        activity_codes=args.activity_codes,
        screen_it_codes=args.it_codes
    )


if __name__ == '__main__':
    main()