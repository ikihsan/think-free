#!/usr/bin/env python3
"""E204 CLI tool: Time-window analysis for PSC codes.

Compares last 12 months vs. FY2020–FY2025 to detect market trends
and new entrant velocity in federal software marketplace.
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
UA = "think-free-research/0.1 (+repository think-free E204)"
BASE = "https://api.usaspending.gov/api/v2/search/"

AWARD_TYPES = ["A", "B", "C", "D"]

# Time windows
FULL_WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
RECENT_WINDOW = [{"start_date": "2024-10-01", "end_date": "2025-09-30"}]  # Last 12 months

# Fields for spending_by_award
AWARD_FIELDS = [
    "Award ID", "Award Amount", "Description", "Recipient Name",
    "PSC Code", "NAICS Code", "Agency Name", "Funding Agency Name",
    "Start Date", "End Date", "Award Type", "Type of Contract Pricing",
]

# Categorization keywords (same as E203)
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


def unused_filter_messages(parsed):
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]


def award_page(psc_code, page, limit=100, time_window=FULL_WINDOW, capture_prefix="award"):
    payload = {
        "fields": AWARD_FIELDS,
        "filters": base_filters(psc_codes=[psc_code], time_period=time_window),
        "limit": limit,
        "page": page,
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_award/", payload, capture_name)


def award_all(psc_code, time_window, max_pages=50, capture_prefix="award"):
    all_results = []
    page = 1
    statuses = []
    unused_filters = []
    while page <= max_pages:
        st, parsed, meta = award_page(psc_code, page, time_window=time_window, capture_prefix=capture_prefix)
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
    if not description:
        return "unknown"
    desc_lower = description.lower()
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
    max_cat = max(scores, key=scores.get)
    if scores[max_cat] == 0:
        return "other"
    return max_cat


def analyze_awards(all_awards):
    total_awards = len(all_awards)
    amounts = [a.get("Award Amount", 0) or 0 for a in all_awards]
    total_obligation = sum(amounts)
    median_obligation = sorted(amounts)[len(amounts) // 2] if amounts else 0

    categories = []
    for award in all_awards:
        desc = award.get("Description", "") or ""
        cat = categorize_description(desc)
        categories.append(cat)
        award["_category"] = cat

    cat_counts = Counter(categories)

    under_40k = sum(1 for a in amounts if a <= 40000)
    under_100k = sum(1 for a in amounts if a <= 100000)

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

    recipient_obligations = {}
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        amt = award.get("Award Amount", 0) or 0
        recipient_obligations[recip] = recipient_obligations.get(recip, 0) + amt
    top10_recipients = sorted(recipient_obligations.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_total = sum(amt for _, amt in top10_recipients)
    top10_share = top10_total / total_obligation if total_obligation > 0 else 0

    unique_recipients = len(recipient_obligations)

    # New entrant analysis: recipients not in top 50
    top50_recipients = set(r for r, _ in sorted(recipient_obligations.items(), key=lambda x: x[1], reverse=True)[:50])
    new_entrant_awards = [a for a in all_awards if a.get("Recipient Name", "Unknown") not in top50_recipients]
    new_entrant_count = len(new_entrant_awards)
    new_entrant_obligation = sum(a.get("Award Amount", 0) or 0 for a in new_entrant_awards)

    return {
        "total_awards": total_awards,
        "unique_recipients": unique_recipients,
        "total_obligation": total_obligation,
        "median_obligation": median_obligation,
        "under_40k": under_40k,
        "under_100k": under_100k,
        "categories": dict(cat_counts),
        "category_breakdown": cat_by_size,
        "top10_share": top10_share,
        "top10_recipients": top10_recipients,
        "new_entrant_awards": new_entrant_count,
        "new_entrant_obligation": new_entrant_obligation,
        "new_entrant_share": new_entrant_obligation / total_obligation if total_obligation > 0 else 0,
        "amounts": amounts,
    }


def compare_windows(full_analysis, recent_analysis):
    """Compare full period vs recent period."""
    print(f"\n=== TIME-WINDOW COMPARISON ===")
    print(f"Period A: FY2020-2025 (full)  |  Period B: Oct 2024-Sep 2025 (recent 12mo)")

    # Total metrics
    full_total = full_analysis["total_awards"]
    recent_total = recent_analysis["total_awards"]
    print(f"\nTotal awards: {full_total:,} (full) vs {recent_total:,} (recent)")

    full_oblig = full_analysis["total_obligation"]
    recent_oblig = recent_analysis["total_obligation"]
    print(f"Total obligation: ${full_oblig:,.0f} (full) vs ${recent_oblig:,.0f} (recent)")

    # Annualized rate
    if recent_total > 0:
        annualized_awards = recent_total * (5 / 1)  # 5-year full vs 1-year recent
        annualized_oblig = recent_oblig * 5
        print(f"Annualized recent rate: {annualized_awards:,.0f} awards/yr, ${annualized_oblig:,.0f}/yr")
        print(f"  vs full-period average: {full_total//5:,.0f} awards/yr, ${full_oblig//5:,.0f}/yr")

    # Software share
    full_soft = full_analysis["categories"].get("software", 0)
    recent_soft = recent_analysis["categories"].get("software", 0)
    print(f"\nSoftware awards: {full_soft:,} ({full_soft/full_total*100:.1f}%) full vs {recent_soft:,} ({recent_soft/recent_total*100:.1f}%) recent")

    full_soft_oblig = full_analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    recent_soft_oblig = recent_analysis["category_breakdown"].get("software", {}).get("total_obligation", 0)
    print(f"Software obligation: ${full_soft_oblig:,.0f} ({full_soft_oblig/full_oblig*100:.1f}%) full vs ${recent_soft_oblig:,.0f} ({recent_soft_oblig/recent_oblig*100:.1f}%) recent")

    # Small awards
    full_u40 = full_analysis["under_40k"]
    recent_u40 = recent_analysis["under_40k"]
    print(f"\nAwards ≤ $40k: {full_u40:,} ({full_u40/full_total*100:.1f}%) full vs {recent_u40:,} ({recent_u40/recent_total*100:.1f}%) recent")

    # Concentration
    print(f"\nTop-10 share: {full_analysis['top10_share']*100:.1f}% (full) vs {recent_analysis['top10_share']*100:.1f}% (recent)")

    # New entrants
    print(f"\nNew entrant share (outside top 50): {full_analysis['new_entrant_share']*100:.1f}% (full) vs {recent_analysis['new_entrant_share']*100:.1f}% (recent)")
    print(f"New entrant awards: {full_analysis['new_entrant_awards']:,} (full) vs {recent_analysis['new_entrant_awards']:,} (recent)")

    # Top recipients comparison
    print(f"\n=== Top 10 Recipients Comparison ===")
    full_top10 = {r: amt for r, amt in full_analysis["top10_recipients"]}
    recent_top10 = {r: amt for r, amt in recent_analysis["top10_recipients"]}
    all_top = set(full_top10.keys()) | set(recent_top10.keys())
    for recip in sorted(all_top, key=lambda r: -(full_top10.get(r, 0) + recent_top10.get(r, 0))):
        f_amt = full_top10.get(recip, 0)
        r_amt = recent_top10.get(recip, 0)
        f_pct = f_amt / full_oblig * 100 if full_oblig > 0 else 0
        r_pct = r_amt / recent_oblig * 100 if recent_oblig > 0 else 0
        marker = " ← NEW" if f_amt == 0 else (" ← GONE" if r_amt == 0 else "")
        print(f"  {recip[:50]:50s}  Full: ${f_amt:>12,.0f} ({f_pct:4.1f}%)  Recent: ${r_amt:>12,.0f} ({r_pct:4.1f}%){marker}")


def main():
    parser = argparse.ArgumentParser(
        description='E204 CLI tool: Time-window analysis for PSC codes'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Maximum pages per window (default: 50)')
    args = parser.parse_args()

    psc_code = args.code

    print(f"=== E204 Time-Window Analysis: {psc_code} ===")
    print(f"Fetching full period (FY2020-2025)...")
    full_awards, full_statuses, full_unused = award_all(psc_code, FULL_WINDOW, max_pages=args.max_pages, capture_prefix="award_full")
    print(f"Fetched {len(full_awards)} awards (full period)")
    full_analysis = analyze_awards(full_awards)

    print(f"Fetching recent period (Oct 2024-Sep 2025)...")
    recent_awards, recent_statuses, recent_unused = award_all(psc_code, RECENT_WINDOW, max_pages=args.max_pages, capture_prefix="award_recent")
    print(f"Fetched {len(recent_awards)} awards (recent period)")
    recent_analysis = analyze_awards(recent_awards)

    compare_windows(full_analysis, recent_analysis)

    if args.output:
        output_data = {
            "experiment": "E204",
            "psc_code": psc_code,
            "full_period": {k: v for k, v in full_analysis.items() if k != "amounts"},
            "recent_period": {k: v for k, v in recent_analysis.items() if k != "amounts"},
            "full_statuses": full_statuses,
            "recent_statuses": recent_statuses,
        }
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nJSON output saved to {args.output}")

    print(f"\n=== End of E204 tool ===")


if __name__ == "__main__":
    main()