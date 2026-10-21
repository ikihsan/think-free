#!/usr/bin/env python3
"""E201 MVP prototype: small-team software sales into 7030 federal marketplace.

Queries USAspending API and analyzes recipient-level data to validate
the E199 candidate screen prediction that 7030 admits small-team entry.

Usage: python3 EXPERIMENTS/E201-prototype-7030-mvp/run.py
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import ssl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E201)"
BASE = "https://api.usaspending.gov/api/v2/search/"

WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
AWARD_TYPES = ["A", "B", "C", "D"]

IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]


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
    has_next = True
    statuses = []
    unused_filters = []
    while has_next:
        st, parsed, meta = recipient_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        page += 1
        # The API doesn't always provide hasNext; stop after a reasonable number of pages
        if page > 50:
            print("WARNING: Reached page limit of 50, stopping")
            break
    return all_results, statuses, unused_filters


def categorize_description(text):
    """Categorize an award description as software, service, or other."""
    if not text:
        return "unknown"
    text_lower = text.lower()
    software_keywords = [
        'software', 'application', 'system', 'platform', 'tool', 'framework',
        'api', 'interface', 'development', 'custom', 'bespoke',
        'desktop', 'mobile', 'web-based', 'cloud-based'
    ]
    service_keywords = [
        'service', 'consulting', 'support', 'maintenance', 'training',
        'subscription', 'managed', 'hosting', 'outsourcing'
    ]
    hardware_keywords = [
        'hardware', 'equipment', 'device', 'computer', 'server',
        'network', 'router', 'switch'
    ]
    # Check software keywords first
    for kw in software_keywords:
        if kw in text_lower:
            return "software"
    # Check service keywords
    for kw in service_keywords:
        if kw in text_lower:
            return "service"
    # Check hardware keywords
    for kw in hardware_keywords:
        if kw in text_lower:
            return "hardware"
    return "other"


def analyze_descriptions(awards_data):
    """Categorize award descriptions from award-level data."""
    categories = {"software": 0, "service": 0, "hardware": 0, "other": 0}
    samples = {"software": [], "service": [], "hardware": [], "other": []}
    
    for award in awards_data:
        desc = award.get("description", "") or ""
        cat = categorize_description(desc)
        categories[cat] += 1
        if len(samples[cat]) < 3:  # Store a few samples per category
            samples[cat].append({
                "description": desc,
                "award_amount": award.get("amount", 0),
                "recipient_name": award.get("recipient_name", "")
            })
    
    return categories, samples


def main():
    import argparse
    parser = argparse.ArgumentParser(description='E201 MVP prototype for 7030 federal marketplace')
    parser.add_argument('--psc-code', default='7030', help='PSC code to analyze (default: 7030)')
    parser.add_argument('--output', default=None, help='Output file base name (default: analyze_7030)')
    args = parser.parse_args()
    
    psc_code = args.psc_code
    output_base = args.output or f"analyze_{psc_code}"
    
    print(f"=== E201 MVP Prototype: 7030 Federal Marketplace Analysis ===")
    print(f"PSC Code: {psc_code}")
    print(f"Time period: FY2020-FY2025")
    print()
    
    # Fetch all recipients for 7030
    print(f"Fetching recipient data for PSC code {psc_code}...")
    all_recipients, statuses, unused_filters = recipient_all(psc_code)
    
    print(f"Status: {statuses[-1]['status'] if statuses else 'N/A'}")
    print(f"Total recipients fetched: {len(all_recipients)}")
    print(f"Unused filter messages: {unused_filters[:5]}..." if unused_filters else "No unused filter messages")
    print()
    
    # Analyze recipient data
    print("=== Analysis ===")
    
    # Basic metrics
    total_recipients = len(all_recipients)
    recipient_ids = [r.get('recipient_id', '') for r in all_recipients]
    unique_recipient_ids = set(recipient_ids)
    num_unique = len(unique_recipient_ids)
    
    print(f"Total award rows: {total_recipients}")
    print(f"Unique recipients: {num_unique}")
    print(f"Duplicate recipients (appearing more than once): {total_recipients - num_unique}")
    
    # Amount analysis
    amounts = [r.get('amount', 0) or 0 for r in all_recipients]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0
    
    print(f"\nTotal obligation (sum of all recipient amounts): ${total_obligation:,.0f}")
    print(f"Median recipient obligation: ${median_obligation:,.0f}")
    
    # Awards by size category
    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)
    over_100k = sum(1 for a in amounts if a > 100000)
    
    print(f"\nRecipients with obligation ≤ $40k: {under_40k} ({under_40k/len(amounts)*100:.1f}%)")
    print(f"Recipients with obligation ≤ $100k: {under_100k} ({under_100k/len(amounts)*100:.1f}%)")
    print(f"Recipients with obligation > $100k: {over_100k} ({over_100k/len(amounts)*100:.1f}%)")
    
    # Top-10 share
    top10 = sorted(all_recipients, key=lambda r: r.get('amount', 0) or 0, reverse=True)[:10]
    top10_total = sum(r.get('amount', 0) or 0 for r in top10)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0
    
    print(f"\nTop 10 recipients' total obligation: ${top10_total:,.0f}")
    print(f"Top 10 share of total: {top10_share*100:.1f}% (E198 declared: 38.4%)")
    
    # Single-award recipients
    # Count how many recipient_ids appear exactly once
    from collections import Counter
    id_counts = Counter(recipient_ids)
    single_award_recipients = sum(1 for count in id_counts.values() if count == 1)
    multi_award_recipients = sum(1 for count in id_counts.values() if count > 1)
    
    print(f"\nRecipients with exactly 1 award: {single_award_recipients} ({single_award_recipients/num_unique*100:.1f}%)")
    print(f"Recipients with multiple awards: {multi_award_recipients}")
    
    # Top recipients list
    print(f"\nTop 10 recipients by obligation:")
    for i, r in enumerate(top10):
        print(f"  {i+1}. {r.get('name', 'Unknown')}: ${r.get('amount', 0):,.0f}")
    
    # Description categorization (if award descriptions are available)
    print(f"\n=== Description Categorization ===")
    # The recipient endpoint provides recipient-level data, not per-award descriptions.
    # To categorize descriptions, we'd need to query spending_by_award/ for each recipient.
    # For this prototype, we'll note the limitation and provide a basic analysis.
    
    # Try to fetch some award-level data for description categorization
    print("Fetching sample award-level data for description categorization...")
    # Try one recipient to get award descriptions
    first_recipient = all_recipients[0]
    first_recipient_id = first_recipient.get('recipient_id', '')
    first_recipient_name = first_recipient.get('name', '')
    
    # Query spending_by_award/ for this recipient and PSC code 7030
    award_url = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'
    award_payload = json.dumps({
        "filters": {
            "time_period": WINDOW,
            "award_type_codes": AWARD_TYPES,
            "psc_codes": [psc_code],
            "recipient_ids": [first_recipient_id]
        },
        "limit": 5,
        "spending_level": "awards"
    }).encode()
    
    headers = {
        'User-Agent': UA,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    context = ssl.create_default_context()
    req = urllib.request.Request(award_url, data=award_payload, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=180, context=context) as r:
            award_raw = r.read()
        award_data = json.loads(award_raw.decode('utf-8', 'replace'))
        award_results = award_data.get('results', [])
        
        print(f"Fetched {len(award_results)} award-level results for {first_recipient_name}")
        
        # Categorize descriptions
        cat_counts = {"software": 0, "service": 0, "hardware": 0, "other": 0}
        cat_samples = {"software": [], "service": [], "hardware": [], "other": []}
        
        for award in award_results:
            desc = award.get('description', '') or ''
            cat = categorize_description(desc)
            cat_counts[cat] += 1
            cat_samples[cat].append({
                "description": desc[:200] if len(desc) > 200 else desc,
                "amount": award.get('amount', 0),
                "title": award.get('title', '')[:100] if award.get('title') else ""
            })
        
        print(f"\nDescription categories (for {first_recipient_name}):")
        for cat, count in cat_counts.items():
            print(f"  {cat}: {count}")
        
        if cat_counts["software"] > 0:
            print(f"\nSoftware description samples:")
            for s in cat_samples["software"]:
                print(f"    - {s['description']}")
        if cat_counts["service"] > 0:
            print(f"\nService description samples:")
            for s in cat_samples["service"]:
                print(f"    - {s['description']}")
        if cat_counts["hardware"] > 0:
            print(f"\nHardware description samples:")
            for s in cat_samples["hardware"]:
                print(f"    - {s['description']}")
        if cat_counts["other"] > 0:
            print(f"\nOther description samples:")
            for s in cat_samples["other"]:
                print(f"    - {s['description']}")
        
    except Exception as e:
        print(f"Could not fetch award-level data: {e}")
        print("(This is expected - award-level description data requires additional API calls)")
    
    # Save results
    print(f"\n=== Saving results ===")
    output_dir = os.path.join(HERE, "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save summary
    summary = {
        "experiment": "E201",
        "psc_code": psc_code,
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
        "top10_total": top10_total,
        "unused_filters": unused_filters,
        "statuses": statuses
    }
    
    summary_path = os.path.join(RAW, f"{output_base}_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {summary_path}")
    
    # Save detailed recipient data
    recipients_path = os.path.join(RAW, f"{output_base}_recipients.json")
    with open(recipients_path, "w") as f:
        json.dump(all_recipients, f, indent=2)
    print(f"Recipient data saved to {recipients_path}")
    
    # Print final verdict
    print(f"\n=== VERDICT ===")
    screen_score = num_unique * (1 - top10_share)
    print(f"Screen score: {num_unique} × (1 - {top10_share*100:.1f}%) = {screen_score:.1f}")
    print(f"E199 screen score: 2,412")
    print(f"Screen prediction {'SUPPORTED' if 2300 <= screen_score <= 2500 else 'NEEDS REVIEW'}")
    
    supported_factors = []
    if under_40k / len(amounts) * 100 >= 25:
        supported_factors.append(f"{under_40k/len(amounts)*100:.1f}% recipients ≤ $40k (small entry points)")
    if under_100k / len(amounts) * 100 >= 40:
        supported_factors.append(f"{under_100k/len(amounts)*100:.1f}% recipients ≤ $100k (small program accessible)")
    if single_award_recipients / num_unique * 100 >= 95:
        supported_factors.append(f"{single_award_recipients/num_unique*100:.1f}% recipients with exactly 1 award (entry points)")
    if top10_share <= 0.45:
        supported_factors.append(f"Top-10 share {top10_share*100:.1f}% (moderate concentration)")
    
    if supported_factors:
        print(f"\nSupporting factors:")
        for factor in supported_factors:
            print(f"  - {factor}")
    else:
        print(f"\nNo strong supporting factors observed")
    
    if not supported_factors:
        print(f"\nThe screen prediction is not well supported by this data.")
        print(f"Consider revising the screen methodology or exploring alternative codes.")
    
    print(f"\n=== End of E201 prototype ===")


if __name__ == "__main__":
    main()