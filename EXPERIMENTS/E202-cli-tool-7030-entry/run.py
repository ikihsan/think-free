#!/usr/bin/env python3
"""E202 CLI tool: PSC code small-team entry analysis.

Queries USAspending API and outputs key metrics for small-team assessment
of federal marketplace accessibility by PSC code.

Usage:
    python3 EXPERIMENTS/E202-cli-tool-7030-entry/run.py --code 7030
    python3 EXPERIMENTS/E202-cli-tool-7030-entry/run.py --code DA01
    python3 EXPERIMENTS/E202-cli-tool-7030-entry/run.py --help
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import ssl
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E202)"
BASE = "https://api.usaspending.gov/api/v2/search/"

# Default time period: FY2020-FY2025 (consistent with E196-E201)
WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(**extra):
    f = {"time_period": WINDOW, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=3, pause=0.5):
    """POST to an endpoint, capture the body, return (status, parsed_or_text)."""
    os.makedirs(RAW, exist_ok=True)
    url = BASE + endpoint
    body = json.dumps(payload).encode()
    meta_path = os.path.join(RAW, capture_name + ".meta.json")
    for suffix in (".json", ".body"):
        body_path = os.path.join(RAW, capture_name + suffix)
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
                        break
            except Exception:
                break
    last = (None, "")
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
            if e.code == 422 and attempt == retries:
                break
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

    with open(os.path.join(RAW, capture_name + ".json"), "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status,
            "bytes": len(raw or b""),
            "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(os.path.join(RAW, capture_name + ".meta.json"), "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1,
                  sort_keys=True)
    try:
        parsed = json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        parsed = None
    return status, parsed, meta


def unused_filter_messages(parsed):
    """USAspending's silent way of ignoring a filter: a 'not used' message."""
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]


def recipient_page(psc_code, page, limit=100, capture_prefix="recip"):
    """Fetch one page of recipients for a PSC code."""
    payload = {
        "filters": base_filters(psc_codes=[psc_code]),
        "limit": limit,
        "page": page,
        "spending_level": "awards"
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_category/recipient/", payload, capture_name)


def recipient_all(psc_code, capture_prefix="recip"):
    """Fetch all pages of recipients for a PSC code."""
    all_results = []
    page = 1
    statuses = []
    unused_filters = []
    while True:
        st, parsed, meta = recipient_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        page += 1
        if page > 100:
            print("WARNING: Reached page limit of 100, stopping")
            break
    return all_results, statuses, unused_filters


def analyze_recipients(all_recipients):
    """Analyze recipient data and return metrics."""
    total_recipients = len(all_recipients)
    recipient_ids = [r.get('recipient_id', '') for r in all_recipients]
    unique_recipient_ids = set(recipient_ids)
    num_unique = len(unique_recipient_ids)

    # Amount analysis
    amounts = [r.get('amount', 0) or 0 for r in all_recipients]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0

    # Awards by size category
    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)
    over_100k = sum(1 for a in amounts if a > 100000)

    # Single-award recipient analysis
    id_counts = Counter(recipient_ids)
    single_award_recipients = sum(1 for count in id_counts.values() if count == 1)
    multi_award_recipients = sum(1 for count in id_counts.values() if count > 1)

    # Top-10 share
    top10 = sorted(all_recipients, key=lambda r: r.get('amount', 0) or 0, reverse=True)[:10]
    top10_total = sum(r.get('amount', 0) or 0 for r in top10)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0

    # Screen score
    screen_score = num_unique * (1 - top10_share)

    return {
        "total_recipients": total_recipients,
        "unique_recipients": num_unique,
        "total_obligation": total_obligation,
        "median_obligation": median_obligation,
        "under_40k": under_40k,
        "under_100k": under_100k,
        "over_100k": over_100k,
        "top10_share": top10_share,
        "single_award_recipients": single_award_recipients,
        "multi_award_recipients": multi_award_recipients,
        "screen_score": screen_score,
        "amounts": amounts
    }


def print_summary(code, analysis, declared_screen_score=None, declared_top10_share=None):
    """Print a human-readable summary of the analysis."""
    print(f"=== {code} ===")
    print(f"PSC Code: {code}")

    # Get cell total from E196 data or compute from analysis
    cell_total = analysis["total_obligation"]

    print(f"\n=== Screen Metrics ===")
    print(f"Distinct recipients: {analysis['unique_recipients']:,}")
    print(f"Top-10 share: {analysis['top10_share']*100:.1f}%")

    if declared_top10_share is not None:
        diff = analysis["top10_share"] * 100 - declared_top10_share * 100
        print(f"(declared baseline: {declared_top10_share*100:.1f}%, diff: {diff:+.1f} pp)")

    screen_score = analysis["screen_score"]
    if declared_screen_score is not None:
        score_diff = screen_score - declared_screen_score
        print(f"Screen score: {screen_score:.1f} (declared baseline: {declared_screen_score}, diff: {score_diff:+.1f})")
    else:
        print(f"Screen score: {screen_score:.1f}")

    print(f"\n=== Small-Team Entry ===")
    under_40k_pct = analysis["under_40k"] / analysis["unique_recipients"] * 100 if analysis["unique_recipients"] > 0 else 0
    under_100k_pct = analysis["under_100k"] / analysis["unique_recipients"] * 100 if analysis["unique_recipients"] > 0 else 0

    print(f"Recipients with obligation ≤ $40k: {analysis['under_40k']} ({under_40k_pct:.1f}%)")
    print(f"Recipients with obligation ≤ $100k: {analysis['under_100k']} ({under_100k_pct:.1f}%)")
    print(f"Recipients with obligation > $100k: {analysis['over_100k']} ({(analysis['over_100k']/analysis['unique_recipients']*100):.1f}%)")

    single_pct = analysis["single_award_recipients"] / analysis["unique_recipients"] * 100 if analysis["unique_recipients"] > 0 else 0
    print(f"Recipients with exactly 1 award: {analysis['single_award_recipients']} ({single_pct:.1f}%)")

    print(f"\n=== Accessibility ===")
    accessible_pct = (1 - analysis["top10_share"]) * 100
    print(f"~{accessible_pct:.1f}% of total obligation potentially accessible to newcomers")
    print(f"(top {analysis['unique_recipients'] - 10} of {analysis['unique_recipients']} recipients hold {100 - accessible_pct:.1f}%)")

    print(f"\nScore = {analysis['unique_recipients']} × (1 − {analysis['top10_share']*100:.1f}%) = {screen_score:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description='E202 CLI tool: PSC code small-team entry analysis'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030, DA01)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path (default: prints to stdout)')
    parser.add_argument('--declared-score', type=float, default=None,
                        help='Declared screen score for comparison (optional)')
    parser.add_argument('--declared-share', type=float, default=None,
                        help='Declared top-10 share for comparison (optional)')
    args = parser.parse_args()

    psc_code = args.code

    print(f"=== E202 CLI Tool: {psc_code} ===")
    print(f"Querying USAspending API for PSC code {psc_code}...")

    # Fetch all recipients
    all_recipients, statuses, unused_filters = recipient_all(psc_code)

    print(f"Fetched {len(all_recipients)} recipient rows")
    print(f"Final status: {statuses[-1]['status'] if statuses else 'N/A'}")

    # Analyze the data
    analysis = analyze_recipients(all_recipients)

    # Print summary
    print_summary(
        psc_code,
        analysis,
        declared_screen_score=args.declared_score,
        declared_top10_share=args.declared_share
    )

    # Output JSON if requested
    if args.output:
        output_data = {
            "experiment": "E202",
            "psc_code": psc_code,
            "analysis": {k: v for k, v in analysis.items() if k != "amounts"},
            "statuses": statuses
        }
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nJSON output saved to {args.output}")

    # Print unused filter messages
    if unused_filters:
        print(f"\nUnused filter messages: {unused_filters[:5]}")

    print(f"\n=== End of E202 tool ===")


if __name__ == "__main__":
    main()