#!/usr/bin/env python3
"""E207 Contract Vehicle Analysis: Map awards to SEWP, GSA MAS, CIO-SP4, VA T4NG, etc."""

import re
from collections import Counter, defaultdict
from e206_api import call, base_filters, FULL_WINDOW, RECENT_WINDOW


# Contract vehicle mapping based on IDV PIID patterns
VEHICLE_PATTERNS = {
    # SEWP (Solutions for Enterprise-Wide Procurement) - NASA
    "SEWP": [
        r"^NNG15SE",      # SEWP V
        r"^NNG15SC",      # SEWP / NASA GWACs
        r"^NNG15SD",      # NASA GWACs
    ],
    # GSA MAS (Multiple Award Schedule) - GSA
    "GSA MAS": [
        r"^GS35F",        # GSA Schedule 70 (IT)
        r"^GS00",         # GSA Schedule (generic)
        r"^GS03F",        # GSA Schedule 70 (older)
        r"^47QTCA",       # GSA Schedule (new format, FAS)
        r"^47QREA",       # GSA Schedule (new format)
        r"^47Q",          # GSA FAS (generic)
    ],
    # CIO-SP (Chief Information Officer - Solutions and Partners) - HHS/NIH
    "CIO-SP": [
        r"^HHSN316",      # CIO-SP3 / CIO-SP4
        r"^HHSN263",      # CIO-CS / CIO-SP variants
    ],
    # VA T4NG (Transformational Technology Next Generation) - VA
    "VA T4NG": [
        r"^VA",           # VA contracts (broad)
        r"^36C",          # VA specific
        r"^523",          # VA T4NG patterns
    ],
    # DoD Enterprise Software Initiative (ESI) / DISA
    "DoD ESI/DISA": [
        r"^HC1028",       # DISA
        r"^HC1047",       # DISA
        r"^HC1084",       # DISA
    ],
    # Navy SEAPORT
    "Navy SEAPORT": [
        r"^N00178",       # SEAPORT-e
        r"^N00189",       # Navy
        r"^N00039",       # Navy (MHS Genesis etc.)
        r"^N66001",       # SPAWAR
        r"^N65236",       # Navy
        r"^N68335",       # Navy
        r"^N68836",       # Navy
    ],
    # Army ITES / CHESS
    "Army ITES/CHESS": [
        r"^W52P1J",       # Army CHESS/ITES
        r"^W91",          # Army (broad)
        r"^W56JSR",       # Army
        r"^W912",         # Army Corps of Engineers
        r"^W91Q",         # Army
        r"^W91Y",         # Army
        r"^W91R",         # Army
        r"^W91QF",        # Army
        r"^W91QV",        # Army
        r"^W91CRB",       # Army
        r"^W9133L",       # Army
        r"^W912PP",       # Army
        r"^W912NW",       # Army
        r"^W912L7",       # Army
        r"^W912K",        # Army
        r"^W912JF",       # Army
        r"^W912HZ",       # Army
        r"^W912KZ",       # Army
        r"^W912K6",       # Army
        r"^W912K3",       # Army
        r"^W81",          # Army Medical
        r"^W56",          # Army
    ],
    # Air Force
    "Air Force": [
        r"^FA",           # Air Force
        r"^HT",           # Air Force (Hanscom)
        r"^HTC711",       # Hanscom
        r"^HT0038",       # DHA/Health
    ],
    # DHA (Defense Health Agency)
    "DHA": [
        r"^HT0038",       # DHA MHS Genesis
    ],
    # Other Federal
    "Other Federal": [
        r"^GS",           # GSA generic
        r"^47",           # GSA generic
        r"^HHSN",         # HHS generic
        r"^033103",       # Unknown federal
    ],
}

# Priority order for matching (first match wins)
VEHICLE_PRIORITY = [
    "SEWP",
    "GSA MAS",
    "CIO-SP",
    "VA T4NG",
    "DoD ESI/DISA",
    "Navy SEAPORT",
    "Army ITES/CHESS",
    "Air Force",
    "DHA",
    "Other Federal",
]


def classify_vehicle(idv_piid):
    """Classify an IDV PIID into a contract vehicle category."""
    if not idv_piid or idv_piid in ("NONE", "-NONE-"):
        return "Direct/Unknown"
    
    for vehicle in VEHICLE_PRIORITY:
        patterns = VEHICLE_PATTERNS.get(vehicle, [])
        for pattern in patterns:
            if re.match(pattern, idv_piid):
                return vehicle
    return "Other/Unknown"


def extract_idv_from_generated_id(generated_id):
    """Extract IDV PIID from generated_internal_id field."""
    if not generated_id:
        return None
    # Pattern: CONT_AWD_{AwardID}_9700_{IDV_PIID}_{suffix}
    match = re.search(r'CONT_AWD_[^_]+_9700_([^_]+)_', generated_id)
    if match:
        return match.group(1)
    return None


def award_page(psc_code, page, limit=100, time_window=FULL_WINDOW, capture_prefix="award"):
    """Fetch a page of awards with generated_internal_id field."""
    payload = {
        "fields": ["Award ID", "Award Amount", "Description", "Recipient Name", 
                   "generated_internal_id", "PSC Code", "NAICS Code",
                   "Awarding Agency", "Awarding Sub Agency", "Funding Agency",
                   "Funding Sub Agency", "Recipient UEI", "Start Date", "End Date"],
        "filters": base_filters(psc_codes=[psc_code], time_period=time_window),
        "limit": limit,
        "page": page,
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_award/", payload, capture_name)


def award_all(psc_code, time_window=FULL_WINDOW, max_pages=100, capture_prefix="award"):
    """Fetch all pages of awards for a PSC code."""
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


def analyze_vehicles(all_awards):
    """Analyze contract vehicle usage across awards."""
    vehicle_stats = defaultdict(lambda: {
        "award_count": 0,
        "total_obligation": 0,
        "recipients": set(),
        "awards": [],
    })
    
    recipient_vehicle = defaultdict(lambda: defaultdict(int))  # recip -> vehicle -> count
    recipient_obligation = defaultdict(lambda: defaultdict(float))  # recip -> vehicle -> obligation
    
    for award in all_awards:
        gid = award.get("generated_internal_id", "")
        idv = extract_idv_from_generated_id(gid)
        vehicle = classify_vehicle(idv)
        
        recip = award.get("Recipient Name", "Unknown")
        amount = award.get("Award Amount", 0) or 0
        
        vehicle_stats[vehicle]["award_count"] += 1
        vehicle_stats[vehicle]["total_obligation"] += amount
        vehicle_stats[vehicle]["recipients"].add(recip)
        vehicle_stats[vehicle]["awards"].append({
            "award_id": award.get("Award ID"),
            "recipient": recip,
            "amount": amount,
            "idv_piid": idv,
            "description": award.get("Description", "")[:100],
        })
        
        recipient_vehicle[recip][vehicle] += 1
        recipient_obligation[recip][vehicle] += amount
    
    # Convert sets to counts
    for vehicle, stats in vehicle_stats.items():
        stats["unique_recipients"] = len(stats["recipients"])
        del stats["recipients"]
    
    return {
        "vehicle_stats": dict(vehicle_stats),
        "recipient_vehicle": {r: dict(v) for r, v in recipient_vehicle.items()},
        "recipient_obligation": {r: dict(v) for r, v in recipient_obligation.items()},
    }


def print_vehicle_summary(psc_code, analysis):
    """Print a summary of contract vehicle analysis."""
    vehicle_stats = analysis["vehicle_stats"]
    
    print(f"\n{'='*70}")
    print(f"CONTRACT VEHICLE ANALYSIS: {psc_code}")
    print(f"{'='*70}")
    
    # Sort vehicles by total obligation
    sorted_vehicles = sorted(
        vehicle_stats.items(),
        key=lambda x: x[1]["total_obligation"],
        reverse=True
    )
    
    total_awards = sum(s["award_count"] for s in vehicle_stats.values())
    total_obligation = sum(s["total_obligation"] for s in vehicle_stats.values())
    total_recipients = set()
    for s in vehicle_stats.values():
        # We can't easily get unique recipients across vehicles without the sets
        pass
    
    print(f"{'Vehicle':<25} {'Awards':>8} {'Obligation':>18} {'% of $':>8} {'Recipients':>12}")
    print(f"{'-'*70}")
    
    for vehicle, stats in sorted_vehicles:
        pct = (stats["total_obligation"] / total_obligation * 100) if total_obligation > 0 else 0
        print(f"{vehicle:<25} {stats['award_count']:>8} ${stats['total_obligation']:>15,.0f} {pct:>7.1f}% {stats['unique_recipients']:>12}")
    
    print(f"{'-'*70}")
    print(f"{'TOTAL':<25} {total_awards:>8} ${total_obligation:>15,.0f} {'100.0%':>8}")
    
    # Small vendor analysis (recipients with <= 3 awards or <= $100k total)
    print(f"\n{'='*70}")
    print(f"SMALL VENDOR VEHICLE USAGE (recipients with <=3 awards total)")
    print(f"{'='*70}")
    
    # Find small vendors
    recipient_total_awards = defaultdict(int)
    recipient_total_obligation = defaultdict(float)
    
    for recip, vehicles in analysis["recipient_vehicle"].items():
        recipient_total_awards[recip] = sum(vehicles.values())
        recipient_total_obligation[recip] = sum(analysis["recipient_obligation"][recip].values())
    
    small_vendors = [r for r, c in recipient_total_awards.items() if c <= 3]
    small_vendor_obligation = [r for r, o in recipient_total_obligation.items() if o <= 100000]
    
    print(f"Small vendors (<=3 awards): {len(small_vendors)}")
    print(f"Small vendors (<= $100k): {len(small_vendor_obligation)}")
    
    # Vehicle usage by small vendors
    sv_vehicle_counts = Counter()
    sv_vehicle_obligation = defaultdict(float)
    
    for recip in small_vendors:
        for vehicle, count in analysis["recipient_vehicle"][recip].items():
            sv_vehicle_counts[vehicle] += count
            sv_vehicle_obligation[vehicle] += analysis["recipient_obligation"][recip][vehicle]
    
    print(f"\n{'Vehicle':<25} {'Awards':>8} {'Obligation':>18} {'% of Small Vendor $':>18}")
    print(f"{'-'*70}")
    
    sv_total_obligation = sum(sv_vehicle_obligation.values())
    for vehicle, count in sv_vehicle_counts.most_common():
        obl = sv_vehicle_obligation[vehicle]
        pct = (obl / sv_total_obligation * 100) if sv_total_obligation > 0 else 0
        print(f"{vehicle:<25} {count:>8} ${obl:>15,.0f} {pct:>17.1f}%")
    
    # Top recipients per vehicle
    print(f"\n{'='*70}")
    print(f"TOP RECIPIENTS PER VEHICLE (by obligation)")
    print(f"{'='*70}")
    
    for vehicle in sorted(vehicle_stats.keys()):
        stats = vehicle_stats[vehicle]
        if stats["award_count"] == 0:
            continue
        # Get top 5 recipients for this vehicle
        recip_obligations = defaultdict(float)
        for award in stats["awards"]:
            recip_obligations[award["recipient"]] += award["amount"]
        
        top5 = sorted(recip_obligations.items(), key=lambda x: -x[1])[:5]
        if top5:
            print(f"\n{vehicle}:")
            for recip, obl in top5:
                print(f"  {recip:<50} ${obl:>15,.0f}")


if __name__ == "__main__":
    import sys
    psc_code = sys.argv[1] if len(sys.argv) > 1 else "7030"
    
    print(f"Fetching awards for PSC {psc_code}...")
    all_awards, statuses = award_all(psc_code, max_pages=50)
    print(f"Fetched {len(all_awards)} awards")
    
    analysis = analyze_vehicles(all_awards)
    print_vehicle_summary(psc_code, analysis)