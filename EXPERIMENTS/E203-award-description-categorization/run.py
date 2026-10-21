#!/usr/bin/env python3
"""E203 CLI tool: Award description categorization for PSC code 7030.

Queries USAspending API spending_by_award endpoint and classifies individual
awards as software/service/other via description text analysis to confirm
software-market fit for small teams.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import ssl
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E203)"
BASE = "https://api.usaspending.gov/api/v2/search/"

# Default time period: FY2020-FY2025 (consistent with E196-E202)
WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
AWARD_TYPES = ["A", "B", "C", "D"]

# Fields to request from spending_by_award endpoint
AWARD_FIELDS = [
    "Award ID",
    "Award Amount",
    "Description",
    "Recipient Name",
    "PSC Code",
    "NAICS Code",
    "Agency Name",
    "Funding Agency Name",
    "Start Date",
    "End Date",
    "Award Type",
    "Type of Contract Pricing",
]

# Categorization keyword sets (case-insensitive)
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

SERVICE_KEYWORDS = [
    "service", "support", "maintenance", "help desk", "helpdesk",
    "consulting", "advisory", "implementation", "integration",
    "migration", "deployment", "configuration", "customization",
    "training", "education", "certification", "managed services",
    "outsourcing", "staffing", "augmentation", "contractor",
    "professional services", "technical services", "it services",
    "cloud services", "hosting", "colocation", "data center",
    "network services", "telecom", "telecommunications", "voice",
    "video", "conferencing", "unified communications",
    "security services", "audit", "assessment", "penetration test",
    "vulnerability", "compliance", "governance", "risk",
    "project management", "pm", "scrum", "agile", "waterfall",
    "business analysis", "requirements", "testing", "qa", "quality",
]

HARDWARE_KEYWORDS = [
    "hardware", "server", "laptop", "desktop", "workstation",
    "router", "switch", "firewall appliance", "storage", "disk",
    "tape", "backup device", "ups", "power", "rack", "cabinet",
    "cable", "connector", "fiber", "copper", "patch panel",
    "monitor", "display", "projector", "printer", "scanner",
    "peripheral", "keyboard", "mouse", "docking station",
    "mobile", "tablet", "phone", "smartphone", "iphone", "android",
    "equipment", "device", "appliance", "blade", "chassis",
    "memory", "ram", "cpu", "processor", "gpu", "graphics card",
    "hard drive", "ssd", "nvme", "sata", "raid", "san", "nas",
]

TELECOM_KEYWORDS = [
    "telecom", "telecommunications", "bandwidth", "internet",
    "circuit", "line", "trunk", "sip", "voip", "pbx", "pstn",
    "wireless", "cellular", "5g", "4g", "lte", "satellite",
    "transmission", "fiber optic", "dark fiber", "wavelength",
    "carrier", "isp", "provider", "connectivity", "network",
    "leased line", "mpls", "vpn", "sd-wan",
]

def base_filters(**extra):
    f = {"time_period": WINDOW, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=3, pause=0.5):
    """POST to an endpoint, capture the body, return (status, parsed_or_text, meta)."""
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
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]


def award_page(psc_code, page, limit=100, capture_prefix="award"):
    """Fetch one page of awards for a PSC code."""
    payload = {
        "fields": AWARD_FIELDS,
        "filters": base_filters(psc_codes=[psc_code]),
        "limit": limit,
        "page": page,
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_award/", payload, capture_name)


def award_all(psc_code, max_pages=50, capture_prefix="award"):
    """Fetch all pages of awards for a PSC code up to max_pages."""
    all_results = []
    page = 1
    statuses = []
    unused_filters = []
    while page <= max_pages:
        st, parsed, meta = award_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses, unused_filters


def categorize_description(description):
    """Categorize an award description as software, service, hardware, telecom, or other."""
    if not description:
        return "unknown"
    desc_lower = description.lower()

    # Count keyword matches for each category
    software_score = sum(1 for kw in SOFTWARE_KEYWORDS if kw in desc_lower)
    service_score = sum(1 for kw in SERVICE_KEYWORDS if kw in desc_lower)
    hardware_score = sum(1 for kw in HARDWARE_KEYWORDS if kw in desc_lower)
    telecom_score = sum(1 for kw in TELECOM_KEYWORDS if kw in desc_lower)

    scores = {
        "software": software_score,
        "service": service_score,
        "hardware": hardware_score,
        "telecom": telecom_score,
    }

    # Return category with highest score, or "other" if all zero
    max_cat = max(scores, key=scores.get)
    if scores[max_cat] == 0:
        return "other"
    return max_cat


def analyze_awards(all_awards):
    """Analyze award data and return metrics including categorization."""
    total_awards = len(all_awards)
    amounts = [a.get("Award Amount", 0) or 0 for a in all_awards]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0

    # Categorize each award
    categories = []
    for award in all_awards:
        desc = award.get("Description", "") or ""
        cat = categorize_description(desc)
        categories.append(cat)
        award["_category"] = cat

    cat_counts = Counter(categories)

    # Awards by size category
    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)
    over_100k = sum(1 for a in amounts if a > 100000)

    # Category breakdown by size
    cat_by_size = {}
    for cat in ["software", "service", "hardware", "telecom", "other", "unknown"]:
        cat_awards = [a for a in all_awards if a.get("_category") == cat]
        cat_amounts = [a.get("Award Amount", 0) or 0 for a in cat_awards]
        cat_by_size[cat] = {
            "count": len(cat_awards),
            "total_obligation": sum(cat_amounts),
            "median_obligation": sorted(cat_amounts)[len(cat_amounts) // 2] if cat_amounts else 0,
            "under_40k": sum(1 for a in cat_amounts if a <= 40000),
            "under_100k": sum(1 for a in cat_amounts if a <= 100000),
        }

    # Top recipients by obligation
    recipient_obligations = {}
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        amt = award.get("Award Amount", 0) or 0
        recipient_obligations[recip] = recipient_obligations.get(recip, 0) + amt
    top10_recipients = sorted(recipient_obligations.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_total = sum(amt for _, amt in top10_recipients)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0

    # Unique recipients
    unique_recipients = len(recipient_obligations)

    return {
        "total_awards": total_awards,
        "unique_recipients": unique_recipients,
        "total_obligation": total_obligation,
        "median_obligation": median_obligation,
        "under_40k": under_40k,
        "under_100k": under_100k,
        "over_100k": over_100k,
        "categories": dict(cat_counts),
        "category_breakdown": cat_by_size,
        "top10_share": top10_share,
        "top10_recipients": top10_recipients,
        "amounts": amounts,
    }


def print_summary(code, analysis):
    """Print a human-readable summary of the analysis."""
    print(f"=== E203 Award Description Categorization: {code} ===")
    print(f"PSC Code: {code}")

    print(f"\n=== Overall Metrics ===")
    print(f"Total awards analyzed: {analysis['total_awards']:,}")
    print(f"Unique recipients: {analysis['unique_recipients']:,}")
    print(f"Total obligation: ${analysis['total_obligation']:,.2f}")
    print(f"Median award: ${analysis['median_obligation']:,.2f}")

    print(f"\n=== Category Distribution ===")
    total = analysis["total_awards"]
    for cat in ["software", "service", "hardware", "telecom", "other", "unknown"]:
        count = analysis["categories"].get(cat, 0)
        pct = count / total * 100 if total > 0 else 0
        cat_data = analysis["category_breakdown"].get(cat, {})
        cat_obligation = cat_data.get("total_obligation", 0)
        cat_pct_oblig = cat_obligation / analysis["total_obligation"] * 100 if analysis["total_obligation"] > 0 else 0
        print(f"  {cat:12s}: {count:5d} ({pct:5.1f}%)  |  ${cat_obligation:>15,.2f} ({cat_pct_oblig:5.1f}%)")

    print(f"\n=== Small-Team Entry by Category ===")
    for cat in ["software", "service", "hardware", "telecom"]:
        cat_data = analysis["category_breakdown"].get(cat, {})
        cat_count = cat_data.get("count", 0)
        if cat_count == 0:
            continue
        under_40k = cat_data.get("under_40k", 0)
        under_100k = cat_data.get("under_100k", 0)
        pct_40k = under_40k / cat_count * 100 if cat_count > 0 else 0
        pct_100k = under_100k / cat_count * 100 if cat_count > 0 else 0
        print(f"  {cat:12s}: {under_40k:4d}/{cat_count} ({pct_40k:5.1f}%) ≤ $40k | {under_100k:4d}/{cat_count} ({pct_100k:5.1f}%) ≤ $100k")

    print(f"\n=== Top-10 Concentration ===")
    print(f"Top 10 recipients hold {analysis['top10_share']*100:.1f}% of total obligation")
    for i, (recip, amt) in enumerate(analysis["top10_recipients"], 1):
        pct = amt / analysis["total_obligation"] * 100 if analysis["total_obligation"] > 0 else 0
        print(f"  {i:2d}. {recip[:60]:60s}  ${amt:>15,.2f} ({pct:5.1f}%)")

    print(f"\n=== Software Market Fit Assessment ===")
    soft_count = analysis["categories"].get("software", 0)
    soft_pct = soft_count / total * 100 if total > 0 else 0
    soft_oblig = analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    soft_oblig_pct = soft_oblig / analysis["total_obligation"] * 100 if analysis["total_obligation"] > 0 else 0
    soft_under_40k = analysis["category_breakdown"].get("software", {}).get("under_40k", 0)
    soft_under_100k = analysis["category_breakdown"].get("software", {}).get("under_100k", 0)

    print(f"  Software awards: {soft_count} ({soft_pct:.1f}% of count, {soft_oblig_pct:.1f}% of obligation)")
    print(f"  Software ≤ $40k: {soft_under_40k}/{soft_count} ({soft_under_40k/soft_count*100:.1f}%)" if soft_count > 0 else "  Software ≤ $40k: N/A")
    print(f"  Software ≤ $100k: {soft_under_100k}/{soft_count} ({soft_under_100k/soft_count*100:.1f}%)" if soft_count > 0 else "  Software ≤ $100k: N/A")

    if soft_pct >= 30 and soft_under_100k > 50:
        print("  ✅ STRONG software market fit for small teams")
    elif soft_pct >= 15 and soft_under_100k > 20:
        print("  ⚠️  MODERATE software market fit for small teams")
    else:
        print("  ❌ WEAK software market fit for small teams")


def main():
    parser = argparse.ArgumentParser(
        description='E203 CLI tool: Award description categorization for PSC code'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path (default: prints to stdout)')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Maximum pages to fetch (default: 50)')
    parser.add_argument('--limit', type=int, default=100,
                        help='Results per page (default: 100)')
    args = parser.parse_args()

    psc_code = args.code

    print(f"=== E203 CLI Tool: {psc_code} ===")
    print(f"Querying USAspending API spending_by_award/ for PSC code {psc_code}...")
    print(f"Max pages: {args.max_pages}, Limit per page: {args.limit}")

    # Fetch all awards
    all_awards, statuses, unused_filters = award_all(psc_code, max_pages=args.max_pages)

    print(f"Fetched {len(all_awards)} award rows")
    print(f"Final status: {statuses[-1]['status'] if statuses else 'N/A'}")

    # Analyze the data
    analysis = analyze_awards(all_awards)

    # Print summary
    print_summary(psc_code, analysis)

    # Output JSON if requested
    if args.output:
        output_data = {
            "experiment": "E203",
            "psc_code": psc_code,
            "analysis": {k: v for k, v in analysis.items() if k not in ("amounts",)},
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

    print(f"\n=== End of E203 tool ===")


if __name__ == "__main__":
    main()