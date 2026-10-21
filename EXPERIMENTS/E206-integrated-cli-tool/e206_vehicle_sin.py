#!/usr/bin/env python3
"""E206 Vehicle SIN/SEWP Analysis Module (E210).

GSA MAS Schedule 70 SIN and SEWP Category analysis for small vendor entry.
"""

from collections import Counter, defaultdict
import re
import sys

# Import from E210
sys.path.insert(0, "/home/ubuntu/think-free/EXPERIMENTS/E210-vehicle-sin-sewp-analysis")
from e210_sin_sewp import (
    analyze_awards_for_vehicle_categories,
    print_sin_sewp_analysis,
    GSA_SCHEDULE_70_SINS,
    SEWP_CATEGORIES,
    SMALL_VENDOR_SIN_AFFINITY,
    SMALL_VENDOR_SEWP_CAT_AFFINITY,
)

# Import from E206 API
sys.path.insert(0, "/home/ubuntu/think-free/EXPERIMENTS/E206-integrated-cli-tool")
from e206_api import call, base_filters, FULL_WINDOW, RECENT_WINDOW


def vehicle_sin_all(psc_code, max_pages=50, capture_prefix="vehicle_sin", time_window=FULL_WINDOW):
    """Fetch awards and analyze for GSA MAS SIN and SEWP category exposure.
    
    Uses same fields as E207 for consistency: includes generated_internal_id and Description.
    """
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
    import sys
    psc_code = sys.argv[1] if len(sys.argv) > 1 else "7030"
    
    print(f"Fetching awards for PSC {psc_code} (vehicle SIN analysis)...")
    all_awards, statuses = vehicle_sin_all(psc_code, max_pages=50)
    print(f"Fetched {len(all_awards)} awards")
    
    analysis = analyze_vehicle_sin(all_awards)
    print_vehicle_sin_summary(psc_code, analysis)