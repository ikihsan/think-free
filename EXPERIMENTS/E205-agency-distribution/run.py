#!/usr/bin/env python3
"""E205 CLI tool: Agency distribution analysis for PSC codes.

Analyzes which agencies buy in each PSC code via funding_agency/awarding_agency
endpoints, and analyzes recipient patterns from award-level data.
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
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E205)"
BASE = "https://api.usaspending.gov/api/v2/search/"

AWARD_TYPES = ["A", "B", "C", "D"]
FULL_WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]

AWARD_FIELDS = [
    "Award ID", "Award Amount", "Description", "Recipient Name",
    "PSC Code", "NAICS Code", "Agency Name", "Funding Agency Name",
    "Start Date", "End Date", "Award Type", "Type of Contract Pricing",
]

SOFTWARE_KEYWORDS = [
    "software", "saas", "license", "licence", "subscription", "cloud",
    "platform", "application", "app", "system", "solution", "service now",
    "servicenow", "salesforce", "microsoft", "oracle", "sap", "adobe",
    "red hat", "linux", "windows", "vmware", "docker", "kubernetes",
    "aws", "azure", "gcp", "google cloud", "amazon web",
    "development", "programming", "coding", "api", "sdk", "framework",
    "database", "analytics", "reporting", "dashboard", "portal",
    "cybersecurity", "security", "encryption", "firewall", "antivirus",
    "backup", "recovery", "monitoring", "logging", "devops", "ci/cd",
    "github", "gitlab", "jira", "confluence", "atlassian", "slack",
    "teams", "zoom", "webex", "office 365", "o365", "google workspace",
    "erp", "crm", "hris", "hrms", "payroll", "finance", "accounting",
    "machine learning", "ml", "ai", "artificial intelligence", "data science",
    "etl", "pipeline", "warehouse", "bi", "business intelligence",
]

def base_filters(**extra):
    f = {"award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=3, pause=0.5):
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


def category_all(category, psc_code, max_pages=100, capture_prefix="cat"):
    """Fetch all pages of a spending_by_category endpoint."""
    all_results = []
    page = 1
    statuses = []
    while page <= max_pages:
        payload = {
            "filters": base_filters(psc_codes=[psc_code]),
            "limit": 100,
            "page": page,
            "spending_level": "awards"
        }
        capture_name = "%s_%s_%s_p%d" % (capture_prefix, category, psc_code, page)
        st, parsed, meta = call(f"spending_by_category/{category}/", payload, capture_name)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses


def award_page(psc_code, page, limit=100, capture_prefix="award"):
    payload = {
        "fields": AWARD_FIELDS,
        "filters": base_filters(psc_codes=[psc_code], time_period=FULL_WINDOW),
        "limit": limit,
        "page": page,
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_award/", payload, capture_name)


def award_all(psc_code, max_pages=50, capture_prefix="award"):
    all_results = []
    page = 1
    statuses = []
    while page <= max_pages:
        st, parsed, meta = award_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses


def categorize_description(description):
    if not description:
        return "unknown"
    desc_lower = description.lower()
    software_score = sum(1 for kw in SOFTWARE_KEYWORDS if kw in desc_lower)
    if software_score > 0:
        return "software"
    return "non-software"


def analyze_awards(all_awards):
    """Analyze awards for recipient patterns."""
    recipient_stats = defaultdict(lambda: {
        "awards": 0, "obligation": 0,
        "software_awards": 0, "software_obligation": 0,
        "small_awards": 0, "small_obligation": 0,
    })

    for award in all_awards:
        recip = award.get("Recipient Name") or "Unknown"
        amount = award.get("Award Amount", 0) or 0
        desc = award.get("Description", "") or ""
        is_software = categorize_description(desc) == "software"
        is_small = amount <= 100000

        r = recipient_stats[recip]
        r["awards"] += 1
        r["obligation"] += amount
        if is_software:
            r["software_awards"] += 1
            r["software_obligation"] += amount
        if is_small:
            r["small_awards"] += 1
            r["small_obligation"] += amount

    return dict(recipient_stats)


def print_agency_category_results(category_name, results):
    """Print agency category results."""
    total_amount = sum(r.get("amount", 0) for r in results)
    print(f"\n=== {category_name} Distribution ({len(results)} agencies) ===")
    print(f"Total obligation: ${total_amount:,.0f}")
    for i, agency in enumerate(results[:20], 1):
        name = agency.get("name", "Unknown")
        code = agency.get("code", "")
        amount = agency.get("amount", 0)
        pct = amount / total_amount * 100 if total_amount > 0 else 0
        print(f"  {i:2d}. {name[:50]:50s} ({code:4s})  ${amount:>15,.0f} ({pct:5.1f}%)")

    # Concentration
    top5 = sum(r.get("amount", 0) for r in results[:5])
    top10 = sum(r.get("amount", 0) for r in results[:10])
    print(f"  Top 5 concentration: {top5/total_amount*100:.1f}%")
    print(f"  Top 10 concentration: {top10/total_amount*100:.1f}%")


def print_recipient_analysis(psc_code, recipient_stats, all_awards):
    total_obligation = sum(s["obligation"] for s in recipient_stats.values())
    total_awards = sum(s["awards"] for s in recipient_stats.values())

    print(f"\n=== Recipient Analysis ({len(recipient_stats)} unique recipients) ===")
    print(f"Total: {total_awards:,} awards, ${total_obligation:,.0f}")

    # Top recipients by obligation
    sorted_recips = sorted(recipient_stats.items(), key=lambda x: x[1]["obligation"], reverse=True)
    print(f"\nTop 20 Recipients by Obligation:")
    for i, (recip, stats) in enumerate(sorted_recips[:20], 1):
        pct = stats["obligation"] / total_obligation * 100
        soft_pct = stats["software_obligation"] / stats["obligation"] * 100 if stats["obligation"] > 0 else 0
        small_pct = stats["small_awards"] / stats["awards"] * 100 if stats["awards"] > 0 else 0
        print(f"  {i:2d}. {recip[:50]:50s}  ${stats['obligation']:>15,.0f} ({pct:5.1f}%)  "
              f"SW: {soft_pct:4.1f}%  Small: {small_pct:4.1f}%  Awards: {stats['awards']}")

    # Recipient concentration
    top10_oblig = sum(s["obligation"] for _, s in sorted_recips[:10])
    print(f"\nRecipient concentration: Top 10 = {top10_oblig/total_obligation*100:.1f}%")

    # Small business analysis: recipients with mostly small awards
    small_biz_recips = {r: s for r, s in recipient_stats.items() 
                        if s["small_awards"] / max(s["awards"], 1) > 0.5 and s["awards"] >= 3}
    print(f"\n=== Small-Business-Like Recipients (≥3 awards, >50% ≤ $100k) ===")
    print(f"Count: {len(small_biz_recips)} / {len(recipient_stats)} ({len(small_biz_recips)/len(recipient_stats)*100:.1f}%)")
    if small_biz_recips:
        sorted_small = sorted(small_biz_recips.items(), key=lambda x: x[1]["obligation"], reverse=True)
        for i, (recip, stats) in enumerate(sorted_small[:20], 1):
            pct = stats["obligation"] / total_obligation * 100
            print(f"  {i:2d}. {recip[:50]:50s}  ${stats['obligation']:>12,.0f} ({pct:5.2f}%)  "
                  f"Awards: {stats['awards']}  Small: {stats['small_awards']}/{stats['awards']}  "
                  f"SW: {stats['software_obligation']/stats['obligation']*100:.1f}%")

    # Award size distribution
    amounts = [a.get("Award Amount", 0) or 0 for a in all_awards]
    print(f"\n=== Award Size Distribution ===")
    for threshold in [10000, 25000, 40000, 100000, 250000, 500000, 1000000]:
        count = sum(1 for a in amounts if a <= threshold)
        pct = count / len(amounts) * 100
        print(f"  ≤ ${threshold:>8,}: {count:5d} ({pct:5.1f}%)")

    # Software vs non-software award sizes
    soft_amounts = [a.get("Award Amount", 0) or 0 for a in all_awards 
                    if categorize_description(a.get("Description", "") or "") == "software"]
    nonsft_amounts = [a.get("Award Amount", 0) or 0 for a in all_awards 
                      if categorize_description(a.get("Description", "") or "") != "software"]
    if soft_amounts:
        print(f"\n  Software awards (n={len(soft_amounts)}): median=${sorted(soft_amounts)[len(soft_amounts)//2]:,.0f}")
    if nonsft_amounts:
        print(f"  Non-software awards (n={len(nonsft_amounts)}): median=${sorted(nonsft_amounts)[len(nonsft_amounts)//2]:,.0f}")


def main():
    parser = argparse.ArgumentParser(
        description='E205 CLI tool: Agency distribution analysis for PSC codes'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Maximum pages for award fetch (default: 50)')
    args = parser.parse_args()

    psc_code = args.code

    print(f"=== E205 Agency Distribution Analysis: {psc_code} ===")

    # 1. Funding agency distribution
    print(f"\nFetching funding_agency category...")
    funding_agencies, funding_statuses = category_all("funding_agency", psc_code)
    print_agency_category_results("Funding Agency", funding_agencies)

    # 2. Awarding agency distribution
    print(f"\nFetching awarding_agency category...")
    awarding_agencies, awarding_statuses = category_all("awarding_agency", psc_code)
    print_agency_category_results("Awarding Agency", awarding_agencies)

    # 3. Federal account distribution
    print(f"\nFetching federal_account category...")
    federal_accounts, fa_statuses = category_all("federal_account", psc_code)
    print_agency_category_results("Federal Account", federal_accounts)

    # 4. Award-level recipient analysis
    print(f"\nFetching award-level data (max {args.max_pages} pages)...")
    all_awards, award_statuses = award_all(psc_code, max_pages=args.max_pages)
    print(f"Fetched {len(all_awards)} awards")

    recipient_stats = analyze_awards(all_awards)
    print_recipient_analysis(psc_code, recipient_stats, all_awards)

    if args.output:
        output_data = {
            "experiment": "E205",
            "psc_code": psc_code,
            "funding_agencies": funding_agencies,
            "awarding_agencies": awarding_agencies,
            "federal_accounts": federal_accounts,
            "recipient_stats": {k: v for k, v in recipient_stats.items()},
            "funding_statuses": funding_statuses,
            "awarding_statuses": awarding_statuses,
            "fa_statuses": fa_statuses,
            "award_statuses": award_statuses,
        }
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nJSON output saved to {args.output}")

    print(f"\n=== End of E205 tool ===")


if __name__ == "__main__":
    main()