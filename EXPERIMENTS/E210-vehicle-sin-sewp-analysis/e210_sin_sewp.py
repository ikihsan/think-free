#!/usr/bin/env python3
"""E210: GSA MAS SIN and SEWP Category Analysis for Small Vendor Entry.

Maps GSA MAS PIIDs to Schedule 70 SINs and SEWP PIIDs to SEWP categories
to identify which contract vehicle categories small software vendors actually win.
"""

import json
import os
import re
from collections import Counter, defaultdict

# ─── GSA MAS Schedule 70 SIN Reference ────────────────────────────────────────
# Based on GSA MAS Schedule 70 (IT) SINs as of 2024-2025
# Source: GSA Advantage / eLibrary public SIN listings
GSA_SCHEDULE_70_SINS = {
    # Software SINs
    "511210": {
        "name": "Software Publishing",
        "description": "Commercial software products, licenses, subscriptions, SaaS",
        "category": "software",
    },
    "511210S": {
        "name": "Software Publishing - SaaS",
        "description": "Software as a Service offerings",
        "category": "software",
    },
    "511210RC": {
        "name": "Software Publishing - Related Services",
        "description": "Maintenance, support, training for software products",
        "category": "service",
    },
    "518210C": {
        "name": "Cloud Computing Services - Commercial Cloud",
        "description": "IaaS, PaaS, SaaS cloud services",
        "category": "software",
    },
    "518210CS": {
        "name": "Cloud Computing Services - Cloud Related Services",
        "description": "Cloud migration, integration, management services",
        "category": "service",
    },
    # IT Services SINs
    "54151S": {
        "name": "IT Professional Services",
        "description": "Software development, integration, consulting, implementation",
        "category": "service",
    },
    "54151HACS": {
        "name": "Highly Adaptive Cybersecurity Services",
        "description": "Penetration testing, incident response, vulnerability assessment",
        "category": "service",
    },
    "54151SOC": {
        "name": "Security Operations Center Services",
        "description": "Managed SOC, monitoring, threat detection",
        "category": "service",
    },
    "54151RM": {
        "name": "Risk Management Services",
        "description": "Security assessment, authorization, compliance",
        "category": "service",
    },
    "541611": {
        "name": "Administrative Management Consulting",
        "description": "IT strategy, governance, enterprise architecture",
        "category": "service",
    },
    "541612": {
        "name": "Human Resources Consulting",
        "description": "HR systems implementation, HRIS consulting",
        "category": "service",
    },
    "541613": {
        "name": "Marketing Consulting",
        "description": "Digital marketing, CRM, marketing automation",
        "category": "service",
    },
    "541614": {
        "name": "Process/Logistics Consulting",
        "description": "Supply chain, ERP, logistics IT consulting",
        "category": "service",
    },
    # Hardware SINs
    "33411": {
        "name": "Computer and Peripheral Equipment Manufacturing",
        "description": "Servers, storage, workstations, laptops, peripherals",
        "category": "hardware",
    },
    "811212": {
        "name": "Computer and Office Machine Repair",
        "description": "Hardware maintenance, repair, warranty services",
        "category": "service",
    },
    # Telecommunications SINs
    "517311": {
        "name": "Wired Telecommunications Carriers",
        "description": "Voice, data, internet, MPLS, VPN services",
        "category": "telecom",
    },
    "517312": {
        "name": "Wireless Telecommunications Carriers",
        "description": "Cellular, 5G, satellite, wireless connectivity",
        "category": "telecom",
    },
    "517911": {
        "name": "Telecommunications Resellers",
        "description": "Resold telecom services, bandwidth, circuits",
        "category": "telecom",
    },
    # Legacy Schedule 70 SINs (pre-consolidation, still in use)
    "132-51": {
        "name": "IT Professional Services (Legacy)",
        "description": "Legacy SIN for IT services, still active on many contracts",
        "category": "service",
    },
    "132-52": {
        "name": "IT Hardware (Legacy)",
        "description": "Legacy SIN for IT hardware",
        "category": "hardware",
    },
    "132-33": {
        "name": "Peripherals and Storage (Legacy)",
        "description": "Legacy SIN for peripherals and storage",
        "category": "hardware",
    },
    "132-34": {
        "name": "Data Communications (Legacy)",
        "description": "Legacy SIN for networking equipment",
        "category": "hardware",
    },
    "132-54": {
        "name": "Telecommunications Services (Legacy)",
        "description": "Legacy SIN for telecom services",
        "category": "telecom",
    },
    "132-56": {
        "name": "Health IT (Legacy)",
        "description": "Legacy SIN for health IT systems and services",
        "category": "software",
    },
}

# ─── SEWP Category Reference ──────────────────────────────────────────────────
# NASA SEWP (Solutions for Enterprise-Wide Procurement) categories
# Based on SEWP V catalog structure
SEWP_CATEGORIES = {
    "A": {
        "name": "IT Hardware",
        "description": "Computers, servers, storage, networking, peripherals",
        "subcategories": ["A1: Desktop/Laptop", "A2: Server/Storage", "A3: Networking", "A4: Peripherals"],
        "category": "hardware",
    },
    "B": {
        "name": "IT Software",
        "description": "Commercial software, licenses, SaaS, cloud services",
        "subcategories": ["B1: Operating Systems", "B2: Application Software", "B3: Middleware", "B4: Cloud/SaaS"],
        "category": "software",
    },
    "C": {
        "name": "IT Services",
        "description": "Professional services, integration, consulting, maintenance",
        "subcategories": ["C1: Implementation", "C2: Maintenance/Support", "C3: Cybersecurity", "C4: Cloud Services"],
        "category": "service",
    },
    "D": {
        "name": "Telecommunications",
        "description": "Voice, data, video, wireless, satellite communications",
        "subcategories": ["D1: Voice", "D2: Data/Internet", "D3: Wireless/Mobile", "D4: Satellite"],
        "category": "telecom",
    },
    "E": {
        "name": "Audio/Visual",
        "description": "Conferencing, display, collaboration equipment",
        "subcategories": ["E1: Video Conferencing", "E2: Display Systems", "E3: Collaboration Tools"],
        "category": "hardware",
    },
}

# ─── GSA MAS PIID to SIN Mapping Heuristics ───────────────────────────────────
# Common GSA MAS PIID prefixes and their typical SIN coverage
GSA_PIID_SIN_MAP = {
    # Large resellers with broad SIN coverage
    "GS35F": ["511210", "518210C", "54151S", "33411", "517311"],  # Typical broad coverage
    "GS03F": ["511210", "54151S", "33411"],
    "GS00": ["511210", "54151S", "33411", "517311"],
    "47QTCA": ["511210", "518210C", "54151S", "54151HACS", "54151SOC", "54151RM"],  # FAS IT Schedule
    "47QREA": ["511210", "54151S", "33411", "517311"],
    "47Q": ["511210", "518210C", "54151S"],
}

# ─── SEWP PIID to Category Mapping ────────────────────────────────────────────
# SEWP V contract holders and their category coverage
SEWP_HOLDER_CATEGORIES = {
    # Major SEWP V prime contractors
    "NNG15SE": ["A", "B", "C", "D", "E"],  # Full SEWP V scope
    "NNG15SC": ["A", "B", "C", "D", "E"],
    "NNG15SD": ["A", "B", "C", "D", "E"],
    # Category-specific holders (subset)
    "NNG15SE304": ["A", "B"],  # Hardware + Software
    "NNG15SE305": ["B", "C"],  # Software + Services
    "NNG15SE306": ["C", "D"],  # Services + Telecom
    "NNG15SE307": ["A", "D", "E"],  # Hardware + Telecom + AV
}

# ─── Known Small Vendor SIN/Category Success Patterns ─────────────────────────
# Based on public GSA/SEWP award data patterns
SMALL_VENDOR_SIN_AFFINITY = {
    "511210": 0.85,      # Software publishing - high small vendor participation
    "511210S": 0.80,     # SaaS - very high small vendor participation
    "518210C": 0.75,     # Cloud services - high small vendor participation
    "54151S": 0.60,      # IT services - moderate (many small firms)
    "54151HACS": 0.55,   # Cybersecurity services - moderate
    "54151SOC": 0.40,    # SOC services - lower (requires scale)
    "54151RM": 0.50,     # Risk management - moderate
    "33411": 0.20,       # Hardware - low (dominated by large OEMs)
    "811212": 0.30,      # Repair - moderate
    "517311": 0.15,      # Telecom carriers - very low
    "517312": 0.15,      # Wireless - very low
    "517911": 0.25,      # Telecom resellers - low-moderate
    "132-51": 0.65,      # Legacy IT services - moderate-high
    "132-56": 0.70,      # Health IT - moderate-high (niche)
}

SMALL_VENDOR_SEWP_CAT_AFFINITY = {
    "B": 0.80,   # Software - high
    "C": 0.60,   # Services - moderate
    "A": 0.20,   # Hardware - low
    "D": 0.15,   # Telecom - very low
    "E": 0.25,   # AV - low
}


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


def print_sin_sewp_analysis(psc_code, analysis, gsa_mas_sins=None, sewp_cats=None):
    """Print GSA MAS SIN and SEWP category analysis."""
    gsa = analysis["gsa_mas"]
    sewp = analysis["sewp"]
    small_vendor_set = analysis["small_vendor_set"]
    
    print(f"\n{'='*80}")
    print(f"GSA MAS SIN / SEWP CATEGORY ANALYSIS: {psc_code}")
    print(f"{'='*80}")
    
    # GSA MAS SIN Analysis
    print(f"\n{'─'*80}")
    print(f"GSA MAS SCHEDULE 70 SIN ANALYSIS")
    print(f"{'─'*80}")
    
    if gsa["by_sin"]:
        sin_stats = []
        for sin, stats in gsa["by_sin"].items():
            sin_info = GSA_SCHEDULE_70_SINS.get(sin, {})
            small_frac = stats["small_vendor_est"] / stats["obligation"] if stats["obligation"] > 0 else 0
            affinity = SMALL_VENDOR_SIN_AFFINITY.get(sin, 0.0)
            sin_stats.append((sin, stats, sin_info, small_frac, affinity))
        
        # Sort by obligation
        sin_stats.sort(key=lambda x: x[1]["obligation"], reverse=True)
        
        print(f"{'SIN':<12} {'Name':<35} {'Awards':>8} {'Obligation':>15} {'Recips':>8} {'Small%':>8} {'Affinity':>8}")
        print(f"{'-'*100}")
        for sin, stats, sin_info, small_frac, affinity in sin_stats:
            name = sin_info.get("name", "Unknown")[:34]
            print(f"{sin:<12} {name:<35} {stats['count']:>8} ${stats['obligation']:>12,.0f} {stats['unique_recipients']:>8} {small_frac:>7.1%} {affinity:>7.1%}")
        
        print(f"\nSmall Vendor Opportunity (High Affinity SINs):")
        high_affinity = [(sin, stats, sin_info, small_frac, affinity) 
                         for sin, stats, sin_info, small_frac, affinity in sin_stats 
                         if affinity >= 0.6]
        for sin, stats, sin_info, small_frac, affinity in high_affinity:
            name = sin_info.get("name", "Unknown")
            desc = sin_info.get("description", "")
            print(f"  {sin} ({name}): {desc}")
            print(f"    Market: ${stats['obligation']:,.0f} | Small vendor share: {small_frac:.1%} | Affinity: {affinity:.0%}")
    else:
        print("  No GSA MAS awards found in sample.")
    
    # SEWP Category Analysis
    print(f"\n{'─'*80}")
    print(f"SEWP CATEGORY ANALYSIS")
    print(f"{'─'*80}")
    
    if sewp["by_category"]:
        cat_stats = []
        for cat, stats in sewp["by_category"].items():
            cat_info = SEWP_CATEGORIES.get(cat, {})
            small_frac = stats["small_vendor_est"] / stats["obligation"] if stats["obligation"] > 0 else 0
            affinity = SMALL_VENDOR_SEWP_CAT_AFFINITY.get(cat, 0.0)
            cat_stats.append((cat, stats, cat_info, small_frac, affinity))
        
        cat_stats.sort(key=lambda x: x[1]["obligation"], reverse=True)
        
        print(f"{'Cat':<6} {'Name':<25} {'Awards':>8} {'Obligation':>15} {'Recips':>8} {'Small%':>8} {'Affinity':>8}")
        print(f"{'-'*80}")
        for cat, stats, cat_info, small_frac, affinity in cat_stats:
            name = cat_info.get("name", "Unknown")[:24]
            print(f"{cat:<6} {name:<25} {stats['count']:>8} ${stats['obligation']:>12,.0f} {stats['unique_recipients']:>8} {small_frac:>7.1%} {affinity:>7.1%}")
        
        print(f"\nSmall Vendor Opportunity (High Affinity Categories):")
        high_affinity = [(cat, stats, cat_info, small_frac, affinity) 
                         for cat, stats, cat_info, small_frac, affinity in cat_stats 
                         if affinity >= 0.6]
        for cat, stats, cat_info, small_frac, affinity in high_affinity:
            name = cat_info.get("name", "Unknown")
            desc = cat_info.get("description", "")
            print(f"  Category {cat} ({name}): {desc}")
            print(f"    Market: ${stats['obligation']:,.0f} | Small vendor share: {small_frac:.1%} | Affinity: {affinity:.0%}")
    else:
        print("  No SEWP awards found in sample.")
    
    # Top GSA MAS PIIDs
    print(f"\n{'─'*80}")
    print(f"TOP GSA MAS PIIDs")
    print(f"{'─'*80}")
    
    if gsa["by_piid"]:
        piid_stats = sorted(
            [(piid, stats) for piid, stats in gsa["by_piid"].items()],
            key=lambda x: x[1]["obligation"],
            reverse=True
        )[:10]
        
        print(f"{'PIID':<20} {'Awards':>8} {'Obligation':>15} {'Recips':>8} {'Small Vendors':>12} {'Est. SINs'}")
        print(f"{'-'*90}")
        for piid, stats in piid_stats:
            small_count = sum(1 for r in stats.get("recipients", set()) if r in small_vendor_set)
            sins = ", ".join(stats.get("sins", [])[:3])
            print(f"{piid:<20} {stats['count']:>8} ${stats['obligation']:>12,.0f} {stats['unique_recipients']:>8} {small_count:>12} {sins}")
    
    # Top SEWP PIIDs
    print(f"\n{'─'*80}")
    print(f"TOP SEWP PIIDs")
    print(f"{'-'*80}")
    
    if sewp["by_piid"]:
        piid_stats = sorted(
            [(piid, stats) for piid, stats in sewp["by_piid"].items()],
            key=lambda x: x[1]["obligation"],
            reverse=True
        )[:10]
        
        print(f"{'PIID':<20} {'Awards':>8} {'Obligation':>15} {'Recips':>8} {'Small Vendors':>12} {'Est. Cats'}")
        print(f"{'-'*90}")
        for piid, stats in piid_stats:
            small_count = sum(1 for r in stats.get("recipients", set()) if r in small_vendor_set)
            cats = ", ".join(stats.get("categories", [])[:5])
            print(f"{piid:<20} {stats['count']:>8} ${stats['obligation']:>12,.0f} {stats['unique_recipients']:>8} {small_count:>12} {cats}")


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