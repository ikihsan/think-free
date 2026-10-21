#!/usr/bin/env python3
"""E207 Comparative Contract Vehicle Analysis across all 5 PSC codes."""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e207_vehicle import award_all, analyze_vehicles, classify_vehicle, extract_idv_from_generated_id


def run_analysis(psc_code, max_pages=50):
    """Run vehicle analysis for a single PSC code."""
    print(f"Analyzing {psc_code}...")
    all_awards, _ = award_all(psc_code, max_pages=max_pages)
    analysis = analyze_vehicles(all_awards)
    return analysis


def get_vehicle_summary(analysis):
    """Extract key summary metrics from analysis."""
    vehicle_stats = analysis["vehicle_stats"]
    total_awards = sum(s["award_count"] for s in vehicle_stats.values())
    total_obligation = sum(s["total_obligation"] for s in vehicle_stats.values())
    
    # Small vendor metrics
    recipient_total_awards = defaultdict(int)
    recipient_total_obligation = defaultdict(float)
    for recip, vehicles in analysis["recipient_vehicle"].items():
        recipient_total_awards[recip] = sum(vehicles.values())
        recipient_total_obligation[recip] = sum(analysis["recipient_obligation"][recip].values())
    
    small_vendors_awards = [r for r, c in recipient_total_awards.items() if c <= 3]
    small_vendors_money = [r for r, o in recipient_total_obligation.items() if o <= 100000]
    
    sv_vehicle_obligation = defaultdict(float)
    for recip in small_vendors_awards:
        for vehicle, obl in analysis["recipient_obligation"][recip].items():
            sv_vehicle_obligation[vehicle] += obl
    
    sv_total_obligation = sum(sv_vehicle_obligation.values())
    
    # Vehicle share for small vendors
    sv_vehicle_share = {}
    for vehicle, obl in sv_vehicle_obligation.items():
        sv_vehicle_share[vehicle] = (obl / sv_total_obligation * 100) if sv_total_obligation > 0 else 0
    
    # Overall vehicle share
    vehicle_share = {}
    for vehicle, stats in vehicle_stats.items():
        vehicle_share[vehicle] = (stats["total_obligation"] / total_obligation * 100) if total_obligation > 0 else 0
    
    return {
        "total_awards": total_awards,
        "total_obligation": total_obligation,
        "vehicle_share": vehicle_share,
        "small_vendor_count_awards": len(small_vendors_awards),
        "small_vendor_count_money": len(small_vendors_money),
        "sv_vehicle_share": sv_vehicle_share,
        "vehicle_stats": {v: {"awards": s["award_count"], "obligation": s["total_obligation"], "recipients": s["unique_recipients"]} for v, s in vehicle_stats.items()},
    }


def print_comparison(results):
    """Print comparative analysis across all PSC codes."""
    codes = list(results.keys())
    
    print("\n" + "="*120)
    print("COMPARATIVE CONTRACT VEHICLE ANALYSIS: ALL 5 IT/SOFTWARE PSC CODES")
    print("="*120)
    
    # Overall vehicle share comparison
    all_vehicles = set()
    for r in results.values():
        all_vehicles.update(r["vehicle_share"].keys())
    
    priority_vehicles = ["SEWP", "GSA MAS", "CIO-SP", "VA T4NG", "DoD ESI/DISA", 
                         "Navy SEAPORT", "Army ITES/CHESS", "Air Force", "DHA",
                         "Direct/Unknown", "Other/Unknown", "Other Federal"]
    sorted_vehicles = [v for v in priority_vehicles if v in all_vehicles]
    sorted_vehicles += [v for v in sorted(all_vehicles) if v not in priority_vehicles]
    
    print(f"\n{'Vehicle':<25}", end="")
    for code in codes:
        print(f"  {code:>6} %$", end="")
    print()
    print("-" * (25 + 10 * len(codes)))
    
    for vehicle in sorted_vehicles:
        print(f"{vehicle:<25}", end="")
        for code in codes:
            share = results[code]["vehicle_share"].get(vehicle, 0)
            print(f"  {share:>6.1f}%", end="")
        print()
    
    # Small vendor vehicle share
    print(f"\n{'='*120}")
    print("SMALL VENDOR VEHICLE SHARE (recipients with <=3 awards)")
    print(f"{'='*120}")
    print(f"\n{'Vehicle':<25}", end="")
    for code in codes:
        print(f"  {code:>6} %$", end="")
    print()
    print("-" * (25 + 10 * len(codes)))
    
    all_sv_vehicles = set()
    for r in results.values():
        all_sv_vehicles.update(r["sv_vehicle_share"].keys())
    
    sorted_sv_vehicles = [v for v in priority_vehicles if v in all_sv_vehicles]
    sorted_sv_vehicles += [v for v in sorted(all_sv_vehicles) if v not in priority_vehicles]
    
    for vehicle in sorted_sv_vehicles:
        print(f"{vehicle:<25}", end="")
        for code in codes:
            share = results[code]["sv_vehicle_share"].get(vehicle, 0)
            print(f"  {share:>6.1f}%", end="")
        print()
    
    # Key metrics table
    print(f"\n{'='*120}")
    print("KEY METRICS SUMMARY")
    print(f"{'='*120}")
    print(f"{'Code':<8} {'Total $':>15} {'Direct/Unk %':>12} {'GSA MAS %':>10} {'SEWP %':>8} {'Army ITES %':>11} {'Navy SEAPORT %':>13} {'Small Vendor %$ (GSA+SEWP)':>25}")
    print("-" * 120)
    
    for code in codes:
        r = results[code]
        total_b = r["total_obligation"]
        direct_pct = r["vehicle_share"].get("Direct/Unknown", 0) + r["vehicle_share"].get("Other/Unknown", 0)
        gsa_pct = r["vehicle_share"].get("GSA MAS", 0)
        sewp_pct = r["vehicle_share"].get("SEWP", 0)
        army_pct = r["vehicle_share"].get("Army ITES/CHESS", 0)
        navy_pct = r["vehicle_share"].get("Navy SEAPORT", 0)
        sv_gsa_sewp = r["sv_vehicle_share"].get("GSA MAS", 0) + r["sv_vehicle_share"].get("SEWP", 0)
        
        print(f"{code:<8} ${total_b:>14,.0f} {direct_pct:>11.1f}% {gsa_pct:>9.1f}% {sewp_pct:>7.1f}% {army_pct:>10.1f}% {navy_pct:>12.1f}% {sv_gsa_sewp:>24.1f}%")


from collections import defaultdict

if __name__ == "__main__":
    codes = ["7030", "DA10", "7A21", "DA01", "D304"]
    results = {}
    
    for code in codes:
        analysis = run_analysis(code)
        results[code] = get_vehicle_summary(analysis)
    
    print_comparison(results)
    
    # Save results
    output = {
        "experiment": "E207",
        "description": "Contract vehicle analysis for 5 IT/software PSC codes",
        "codes_analyzed": codes,
        "results": results,
    }
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e207_comparison.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\nResults saved to {output_path}")