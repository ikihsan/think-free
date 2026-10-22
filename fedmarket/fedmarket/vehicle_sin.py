#!/usr/bin/env python3
"""E210: GSA MAS SIN and SEWP Category Analysis for Small Vendor Entry.

Maps GSA MAS PIIDs to Schedule 70 SINs and SEWP PIIDs to SEWP categories
to identify which contract vehicle categories small software vendors actually win.

Reference tables live in `vehicle_sin_data`; report rendering in
`vehicle_sin_report`. Names are re-exported here for backward compatibility.
"""

import json
import os
import re
from collections import Counter, defaultdict

from .vehicle_sin_data import *  # noqa: F401,F403
from .vehicle_sin_report import print_sin_sewp_analysis  # noqa: F401

# ─── Description-based SIN/Category Inference ──────────────────────────────────

def infer_sin_from_description(description, vehicle_type):
    """Infer likely SIN/category from award description."""
    if not description:
        return []
    
    desc_lower = description.lower()
    
    if vehicle_type == "gsa_mas":
        # Software indicators
        if any(kw in desc_lower for kw in ["software", "license", "subscription", "saas", "cloud", "platform", "application", "erp", "crm", "database", "analytics", "cybersecurity", "security", "devops", "github", "gitlab", "jira", "atlassian", "slack", "teams", "zoom", "office 365", "o365", "google workspace", "machine learning", "ml", "ai", "artificial intelligence", "data science", "etl", "pipeline", "warehouse", "bi", "business intelligence"]):
            return ["511210", "511210S", "518210C"]
        # IT Services indicators
        elif any(kw in desc_lower for kw in ["service", "support", "maintenance", "help desk", "consulting", "advisory", "implementation", "integration", "migration", "deployment", "configuration", "customization", "training", "certification", "managed services", "outsourcing", "staffing", "augmentation", "contractor", "professional services", "technical services", "it services", "cloud services", "hosting", "colocation", "data center", "network services", "security services", "audit", "assessment", "penetration test", "vulnerability", "compliance", "governance", "risk", "project management", "pm", "scrum", "agile", "waterfall", "business analysis", "requirements", "testing", "qa", "quality"]):
            return ["54151S", "54151HACS", "54151SOC", "54151RM", "541611"]
        # Hardware indicators
        elif any(kw in desc_lower for kw in ["hardware", "server", "laptop", "desktop", "workstation", "router", "switch", "firewall appliance", "storage", "disk", "tape", "backup device", "ups", "power", "rack", "cabinet", "cable", "connector", "fiber", "copper", "patch panel", "monitor", "display", "projector", "printer", "scanner", "peripheral", "keyboard", "mouse", "docking station", "mobile", "tablet", "phone", "smartphone", "iphone", "android", "equipment", "device", "appliance", "blade", "chassis", "memory", "ram", "cpu", "processor", "gpu", "graphics card", "hard drive", "ssd", "nvme", "sata", "raid", "san", "nas"]):
            return ["33411", "811212", "132-52", "132-33", "132-34"]
        # Telecom indicators
        elif any(kw in desc_lower for kw in ["telecom", "telecommunications", "bandwidth", "internet", "circuit", "line", "trunk", "sip", "voip", "pbx", "pstn", "wireless", "cellular", "5g", "4g", "lte", "satellite", "transmission", "fiber optic", "dark fiber", "wavelength", "carrier", "isp", "provider", "connectivity", "network", "leased line", "mpls", "vpn", "sd-wan"]):
            return ["517311", "517312", "517911", "132-54"]
        # Health IT
        elif any(kw in desc_lower for kw in ["health", "medical", "clinical", "ehr", "emr", "hipaa", "patient", "hospital", "clinic", "pharmacy", "laboratory", "radiology", "cardiology"]):
            return ["132-56", "511210", "54151S"]
        else:
            return ["511210", "54151S", "33411", "517311"]  # Default broad
    
    elif vehicle_type == "sewp":
        # SEWP categories from description
        cats = []
        if any(kw in desc_lower for kw in ["software", "license", "subscription", "saas", "cloud", "platform", "application", "erp", "crm", "database", "analytics", "cybersecurity", "security", "devops", "machine learning", "ml", "ai", "artificial intelligence", "data science", "etl", "pipeline", "warehouse", "bi", "business intelligence", "operating system", "middleware"]):
            cats.append("B")
        if any(kw in desc_lower for kw in ["service", "support", "maintenance", "help desk", "consulting", "advisory", "implementation", "integration", "migration", "deployment", "configuration", "customization", "training", "certification", "managed services", "outsourcing", "staffing", "augmentation", "contractor", "professional services", "technical services", "it services", "cloud services", "hosting", "colocation", "data center", "network services", "security services", "audit", "assessment", "penetration test", "vulnerability", "compliance", "governance", "risk", "project management", "pm", "scrum", "agile", "waterfall", "business analysis", "requirements", "testing", "qa", "quality", "cybersecurity", "soc", "security operations"]):
            cats.append("C")
        if any(kw in desc_lower for kw in ["hardware", "server", "laptop", "desktop", "workstation", "router", "switch", "firewall appliance", "storage", "disk", "tape", "backup device", "ups", "power", "rack", "cabinet", "cable", "connector", "fiber", "copper", "patch panel", "monitor", "display", "projector", "printer", "scanner", "peripheral", "keyboard", "mouse", "docking station", "mobile", "tablet", "phone", "smartphone", "iphone", "android", "equipment", "device", "appliance", "blade", "chassis", "memory", "ram", "cpu", "processor", "gpu", "graphics card", "hard drive", "ssd", "nvme", "sata", "raid", "san", "nas"]):
            cats.append("A")
        if any(kw in desc_lower for kw in ["telecom", "telecommunications", "bandwidth", "internet", "circuit", "line", "trunk", "sip", "voip", "pbx", "pstn", "wireless", "cellular", "5g", "4g", "lte", "satellite", "transmission", "fiber optic", "dark fiber", "wavelength", "carrier", "isp", "provider", "connectivity", "network", "leased line", "mpls", "vpn", "sd-wan", "voice", "video", "conferencing", "unified communications"]):
            cats.append("D")
        if any(kw in desc_lower for kw in ["audio", "visual", "conferencing", "display", "projector", "collaboration", "video conferencing", "webex", "zoom", "teams", "av", "audiovisual"]):
            cats.append("E")
        
        return cats if cats else ["A", "B", "C", "D", "E"]
    
    return []


def classify_gsa_mas_piid(idv_piid, description=""):
    """Classify a GSA MAS PIID and estimate likely SINs."""
    if not idv_piid or idv_piid in ("NONE", "-NONE-"):
        return None, []
    
    # Use description-based inference if available
    if description:
        sins = infer_sin_from_description(description, "gsa_mas")
        if sins:
            return "Description-based", sins
    
    # Check known patterns
    for prefix, sins in GSA_PIID_SIN_MAP.items():
        if idv_piid.startswith(prefix):
            return prefix, sins
    
    # Generic GSA MAS patterns
    if idv_piid.startswith("GS") or idv_piid.startswith("47"):
        return "GSA MAS (generic)", ["511210", "54151S", "33411", "517311"]
    
    return None, []


def classify_sewp_piid(idv_piid, description=""):
    """Classify a SEWP PIID and estimate likely categories."""
    if not idv_piid or idv_piid in ("NONE", "-NONE-"):
        return None, []
    
    # Use description-based inference if available
    if description:
        cats = infer_sin_from_description(description, "sewp")
        if cats:
            return "Description-based", cats
    
    # Check specific holders
    for prefix, cat_list in SEWP_HOLDER_CATEGORIES.items():
        if idv_piid.startswith(prefix):
            return prefix, cat_list
    
    # Generic SEWP
    if idv_piid.startswith("NNG15SE") or idv_piid.startswith("NNG15SC") or idv_piid.startswith("NNG15SD"):
        return "SEWP V (generic)", ["A", "B", "C", "D", "E"]
    
    return None, []


def extract_idv_from_generated_id(generated_id):
    """Extract IDV PIID from generated_internal_id field."""
    if not generated_id:
        return None
    match = re.search(r'CONT_AWD_[^_]+_9700_([^_]+)_', generated_id)
    if match:
        return match.group(1)
    return None


def analyze_awards_for_vehicle_categories(all_awards):
    """Analyze awards for GSA MAS SIN and SEWP category exposure."""
    results = {
        "gsa_mas": {
            "by_piid": defaultdict(lambda: {"count": 0, "obligation": 0, "recipients": set(), "sins": []}),
            "by_sin": defaultdict(lambda: {"count": 0, "obligation": 0, "recipients": set(), "small_vendor_est": 0}),
        },
        "sewp": {
            "by_piid": defaultdict(lambda: {"count": 0, "obligation": 0, "recipients": set(), "categories": []}),
            "by_category": defaultdict(lambda: {"count": 0, "obligation": 0, "recipients": set(), "small_vendor_est": 0}),
        },
        "small_vendors": [],
        "small_vendor_set": set(),
    }
    
    # Identify small vendors (<=3 awards in sample)
    recip_counts = Counter()
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        recip_counts[recip] += 1
    
    small_vendors = {r for r, c in recip_counts.items() if c <= 3}
    results["small_vendors"] = list(small_vendors)
    results["small_vendor_set"] = small_vendors
    
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        amount = award.get("Award Amount", 0) or 0
        gid = award.get("generated_internal_id", "")
        desc = award.get("Description", "") or ""
        idv = extract_idv_from_generated_id(gid)
        is_small = recip in small_vendors
        
        if idv:
            # GSA MAS analysis
            if idv.startswith("GS") or idv.startswith("47Q") or idv.startswith("47QREA") or idv.startswith("47QTCA"):
                prefix, sins = classify_gsa_mas_piid(idv, desc)
                piid_stats = results["gsa_mas"]["by_piid"][idv]
                piid_stats["count"] += 1
                piid_stats["obligation"] += amount
                piid_stats["recipients"].add(recip)
                if prefix:
                    piid_stats["sins"] = sins
                
                # Aggregate by SIN
                for sin in sins:
                    sin_stats = results["gsa_mas"]["by_sin"][sin]
                    sin_stats["count"] += 1
                    sin_stats["obligation"] += amount
                    sin_stats["recipients"].add(recip)
                    if is_small:
                        sin_stats["small_vendor_est"] += amount
            
            # SEWP analysis
            elif idv.startswith("NNG15SE") or idv.startswith("NNG15SC") or idv.startswith("NNG15SD"):
                prefix, cats = classify_sewp_piid(idv, desc)
                piid_stats = results["sewp"]["by_piid"][idv]
                piid_stats["count"] += 1
                piid_stats["obligation"] += amount
                piid_stats["recipients"].add(recip)
                if prefix:
                    piid_stats["categories"] = cats
                
                # Aggregate by category
                for cat in cats:
                    cat_stats = results["sewp"]["by_category"][cat]
                    cat_stats["count"] += 1
                    cat_stats["obligation"] += amount
                    cat_stats["recipients"].add(recip)
                    if is_small:
                        cat_stats["small_vendor_est"] += amount
    
    # Convert sets to counts (keep recipients set for PIID stats for small vendor counting)
    for cat in ["gsa_mas", "sewp"]:
        for subcat in ["by_sin" if cat == "gsa_mas" else "by_category"]:
            for key, stats in results[cat][subcat].items():
                stats["unique_recipients"] = len(stats["recipients"])
                del stats["recipients"]
        # Also convert for by_piid
        for key, stats in results[cat]["by_piid"].items():
            stats["unique_recipients"] = len(stats["recipients"])
    
    return results


def vehicle_sin_all(psc_code, max_pages=50, capture_prefix="vehicle_sin", time_window=None):
    """Fetch awards and analyze for GSA MAS SIN and SEWP category exposure.
    
    Uses same fields as E207 for consistency: includes generated_internal_id and Description.
    """
    from .api import call, base_filters, FULL_WINDOW, RECENT_WINDOW
    
    if time_window is None:
        time_window = FULL_WINDOW
    
    # Vehicle-specific fields matching E207
    VEHICLE_FIELDS = [
        "Award ID", "Award Amount", "Description", "Recipient Name", 
        "generated_internal_id", "PSC Code", "NAICS Code",
        "Awarding Agency", "Awarding Sub Agency", "Funding Agency",
        "Funding Sub Agency", "Recipient UEI", "Start Date", "End Date",
    ]
    
    def award_page(psc_code, page, limit=100, time_window=time_window, capture_prefix=capture_prefix):
        payload = {
            "fields": VEHICLE_FIELDS,
            "filters": base_filters(psc_codes=[psc_code], time_period=time_window),
            "limit": limit,
            "page": page,
        }
        capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
        return call("spending_by_award/", payload, capture_name)
    
    all_results = []
    page = 1
    statuses = []
    while page <= max_pages:
        st, parsed, meta = award_page(psc_code, page, time_window=time_window, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses


def analyze_vehicle_sin(all_awards):
    """Analyze awards for GSA MAS SIN and SEWP category exposure."""
    return analyze_awards_for_vehicle_categories(all_awards)


def print_vehicle_sin_summary(psc_code, analysis):
    """Print GSA MAS SIN and SEWP category analysis summary."""
    print_sin_sewp_analysis(psc_code, analysis)


if __name__ == "__main__":
    # Test with existing E207 data
    import sys
    sys.path.insert(0, "/home/ubuntu/think-free/EXPERIMENTS/E207-contract-vehicle-analysis")
    from e207_vehicle import award_all, extract_idv_from_generated_id
    
    psc_code = sys.argv[1] if len(sys.argv) > 1 else "7030"
    print(f"Fetching awards for PSC {psc_code}...")
    all_awards, _ = award_all(psc_code, max_pages=50)
    print(f"Fetched {len(all_awards)} awards")
    
    analysis = analyze_awards_for_vehicle_categories(all_awards)
    print_sin_sewp_analysis(psc_code, analysis)
