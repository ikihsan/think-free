#!/usr/bin/env python3
"""Human-readable report rendering for GSA MAS SIN / SEWP analysis (E210/E213)."""

from .vehicle_sin_data import GSA_SCHEDULE_70_SINS, SEWP_CATEGORIES

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
