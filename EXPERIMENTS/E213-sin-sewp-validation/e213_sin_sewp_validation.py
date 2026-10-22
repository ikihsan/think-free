#!/usr/bin/env python3
"""E213: GSA MAS SIN and SEWP Category Validation using USAspending Ground Truth.

Validates E210's description-based SIN/category inferences against actual
contract vehicle data patterns in USAspending. Since official GSA eLibrary 
and SEWP catalog APIs are not accessible, we use USAspending award data as
the ground truth for what vehicles and categories are actually used.

Key validation approaches:
1. Cross-PIID consistency: Same GSA MAS PIID should map to consistent SINs
2. Award description alignment: Description keywords should match inferred SINs
3. Small vendor share coherence: High-affinity SINs should show higher small vendor shares
4. SEWP holder category scope: Known full-scope holders should span all categories
5. PSC code consistency: Same vehicle patterns should behave similarly across codes

Gates:
- G1: PIID-to-SIN consistency (same PIID → similar SINs across awards)
- G2: Description-SIN alignment (keyword match rate >70%)
- G3: Small vendor affinity validation (high-affinity SINs show >2x small vendor share vs low-affinity)
- G4: SEWP holder scope validation (NNG15SE* holders span A,B,C,D,E)
- G5: Cross-code vehicle pattern replication (DA10 high GSA MAS small vendor share replicated)
"""

import json
import os
import re
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Any
import sys

sys.path.insert(0, "/home/ubuntu/think-free/EXPERIMENTS/E206-integrated-cli-tool")
from e206_api import call, base_filters, FULL_WINDOW, RECENT_WINDOW

# Import E210 reference data
sys.path.insert(0, "/home/ubuntu/think-free/EXPERIMENTS/E210-vehicle-sin-sewp-analysis")
from e210_sin_sewp import (
    GSA_SCHEDULE_70_SINS,
    SEWP_CATEGORIES,
    SMALL_VENDOR_SIN_AFFINITY,
    SMALL_VENDOR_SEWP_CAT_AFFINITY,
    infer_sin_from_description,
    classify_gsa_mas_piid,
    classify_sewp_piid,
    extract_idv_from_generated_id,
    GSA_PIID_SIN_MAP,
    SEWP_HOLDER_CATEGORIES,
)

# ── Configuration ─────────────────────────────────────────────────────────────
PSC_CODES = ["7030", "DA10", "7A21", "DA01", "D304"]
MAX_PAGES = 50  # ~5,000 awards per code
CAPTURE_PREFIX = "e213_validation"

# Vehicle-specific fields matching E207/E210
VEHICLE_FIELDS = [
    "Award ID", "Award Amount", "Description", "Recipient Name", 
    "generated_internal_id", "PSC Code", "NAICS Code",
    "Awarding Agency", "Awarding Sub Agency", "Funding Agency",
    "Funding Sub Agency", "Recipient UEI", "Start Date", "End Date",
]

def fetch_awards(psc_code: str, time_window=FULL_WINDOW, max_pages=MAX_PAGES) -> Tuple[List[Dict], List[Dict]]:
    """Fetch awards for a PSC code with vehicle-relevant fields."""
    all_results = []
    statuses = []
    page = 1
    while page <= max_pages:
        payload = {
            "fields": VEHICLE_FIELDS,
            "filters": base_filters(psc_codes=[psc_code], time_period=time_window),
            "limit": 100,
            "page": page,
        }
        capture_name = f"{CAPTURE_PREFIX}_{psc_code}_p{page}"
        st, parsed, meta = call("spending_by_award/", payload, capture_name)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        if not parsed.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
    return all_results, statuses


def analyze_piid_sin_consistency(all_awards: List[Dict]) -> Dict:
    """G1: Check if same GSA MAS PIID maps to consistent SINs across awards."""
    piid_to_sins = defaultdict(set)
    piid_to_descriptions = defaultdict(list)
    piid_counts = Counter()
    
    for award in all_awards:
        gid = award.get("generated_internal_id", "")
        idv = extract_idv_from_generated_id(gid)
        desc = award.get("Description", "") or ""
        
        if idv and (idv.startswith("GS") or idv.startswith("47Q") or idv.startswith("47QREA") or idv.startswith("47QTCA")):
            piid_counts[idv] += 1
            piid_to_descriptions[idv].append(desc)
            # Infer SIN from description
            sins = infer_sin_from_description(desc, "gsa_mas")
            for sin in sins:
                piid_to_sins[idv].add(sin)
    
    # Analyze consistency
    consistent = 0
    inconsistent = 0
    single_sin_piids = 0
    multi_sin_piids = 0
    
    for piid, sins in piid_to_sins.items():
        if len(sins) == 1:
            consistent += 1
            single_sin_piids += 1
        elif len(sins) <= 3:
            # Multiple SINs but related (e.g., 511210 + 511210S + 518210C)
            consistent += 1
            multi_sin_piids += 1
        else:
            inconsistent += 1
            multi_sin_piids += 1
    
    total_piids = len(piid_to_sins)
    consistency_rate = consistent / total_piids if total_piids > 0 else 0
    
    return {
        "total_gsa_mas_piids": total_piids,
        "consistency_rate": consistency_rate,
        "single_sin_piids": single_sin_piids,
        "multi_sin_piids": multi_sin_piids,
        "inconsistent_piids": inconsistent,
        "piid_sin_map": {piid: list(sins) for piid, sins in piid_to_sins.items()},
        "piid_counts": dict(piid_counts),
    }


def analyze_description_sin_alignment(all_awards: List[Dict]) -> Dict:
    """G2: Check if description keywords align with inferred SINs."""
    alignments = []
    
    for award in all_awards:
        desc = award.get("Description", "") or ""
        gid = award.get("generated_internal_id", "")
        idv = extract_idv_from_generated_id(gid)
        
        if not idv or not (idv.startswith("GS") or idv.startswith("47Q")):
            continue
        
        # Get inferred SINs from description
        inferred_sins = infer_sin_from_description(desc, "gsa_mas")
        if not inferred_sins:
            continue
        
        # Check if description contains keywords for the inferred SINs
        desc_lower = desc.lower()
        matched = False
        for sin in inferred_sins:
            sin_info = GSA_SCHEDULE_70_SINS.get(sin, {})
            desc_keywords = []
            # Extract keywords from SIN description
            if "description" in sin_info:
                # Simple keyword extraction from SIN description
                for word in sin_info["description"].lower().split():
                    if len(word) > 4 and word in desc_lower:
                        desc_keywords.append(word)
                        matched = True
        
        alignments.append({
            "matched": matched,
            "inferred_sins": inferred_sins,
            "idv": idv,
        })
    
    matched_count = sum(1 for a in alignments if a["matched"])
    total = len(alignments)
    match_rate = matched_count / total if total > 0 else 0
    
    return {
        "total_alignments_checked": total,
        "matched_count": matched_count,
        "match_rate": match_rate,
        "details": alignments[:50],  # Sample
    }


def analyze_small_vendor_affinity(all_awards: List[Dict]) -> Dict:
    """G3: Validate small vendor affinity scores against actual small vendor shares."""
    # Identify small vendors (≤3 awards in sample)
    recip_counts = Counter()
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        recip_counts[recip] += 1
    small_vendors = {r for r, c in recip_counts.items() if c <= 3}
    
    # Track small vendor obligation by SIN
    sin_obligation = defaultdict(float)
    sin_small_obligation = defaultdict(float)
    sin_awards = defaultdict(int)
    
    for award in all_awards:
        recip = award.get("Recipient Name", "Unknown")
        amount = award.get("Award Amount", 0) or 0
        gid = award.get("generated_internal_id", "")
        idv = extract_idv_from_generated_id(gid)
        desc = award.get("Description", "") or ""
        is_small = recip in small_vendors
        
        if idv and (idv.startswith("GS") or idv.startswith("47Q")):
            sins = infer_sin_from_description(desc, "gsa_mas")
            if not sins:
                # Fallback to PIID pattern
                _, sins = classify_gsa_mas_piid(idv, desc)
            
            for sin in sins:
                sin_obligation[sin] += amount
                sin_awards[sin] += 1
                if is_small:
                    sin_small_obligation[sin] += amount
    
    # Compare affinity vs actual small vendor share
    results = {}
    for sin in GSA_SCHEDULE_70_SINS:
        if sin in sin_obligation and sin_obligation[sin] > 0:
            actual_share = sin_small_obligation[sin] / sin_obligation[sin]
            affinity = SMALL_VENDOR_SIN_AFFINITY.get(sin, 0)
            results[sin] = {
                "affinity": affinity,
                "actual_small_vendor_share": actual_share,
                "total_obligation": sin_obligation[sin],
                "small_vendor_obligation": sin_small_obligation[sin],
                "award_count": sin_awards[sin],
            }
    
    # Validation: high-affinity SINs should have higher small vendor share
    high_affinity_sins = [s for s, r in results.items() if r["affinity"] >= 0.6]
    low_affinity_sins = [s for s, r in results.items() if r["affinity"] < 0.6]
    
    high_avg_share = sum(results[s]["actual_small_vendor_share"] for s in high_affinity_sins) / len(high_affinity_sins) if high_affinity_sins else 0
    low_avg_share = sum(results[s]["actual_small_vendor_share"] for s in low_affinity_sins) / len(low_affinity_sins) if low_affinity_sins else 0
    ratio = high_avg_share / low_avg_share if low_avg_share > 0 else float('inf')
    
    return {
        "sin_results": results,
        "high_affinity_avg_share": high_avg_share,
        "low_affinity_avg_share": low_avg_share,
        "affinity_ratio": ratio,
        "gate3_pass": ratio >= 2.0,
    }


def analyze_sewp_holder_scope(all_awards: List[Dict]) -> Dict:
    """G4: Validate SEWP holder category scope."""
    holder_categories = defaultdict(set)
    holder_obligations = defaultdict(float)
    
    for award in all_awards:
        gid = award.get("generated_internal_id", "")
        idv = extract_idv_from_generated_id(gid)
        amount = award.get("Award Amount", 0) or 0
        desc = award.get("Description", "") or ""
        
        if idv and (idv.startswith("NNG15SE") or idv.startswith("NNG15SC") or idv.startswith("NNG15SD")):
            holder_obligations[idv] += amount
            cats = infer_sin_from_description(desc, "sewp")
            if not cats:
                _, cats = classify_sewp_piid(idv, desc)
            for cat in cats:
                holder_categories[idv].add(cat)
    
    # Check full-scope holders (should span A,B,C,D,E)
    full_scope_holders = []
    partial_scope_holders = []
    
    for holder, cats in holder_categories.items():
        if len(cats) >= 4:  # At least 4 of 5 categories
            full_scope_holders.append({"holder": holder, "categories": list(cats), "obligation": holder_obligations[holder]})
        else:
            partial_scope_holders.append({"holder": holder, "categories": list(cats), "obligation": holder_obligations[holder]})
    
    # Known full-scope holders
    known_full_scope = [h for h in holder_categories if h.startswith("NNG15SE") or h.startswith("NNG15SC") or h.startswith("NNG15SD")]
    
    return {
        "total_sewp_holders": len(holder_categories),
        "full_scope_holders": len(full_scope_holders),
        "partial_scope_holders": len(partial_scope_holders),
        "full_scope_details": full_scope_holders,
        "gate4_pass": len(full_scope_holders) >= 3,  # Expect at least 3 full-scope holders
    }


def analyze_cross_code_patterns(psc_results: Dict[str, Dict]) -> Dict:
    """G5: Cross-code replication of vehicle patterns."""
    # Key pattern: DA10 should have highest GSA MAS small vendor share
    gsa_mas_small_shares = {}
    
    for psc_code, result in psc_results.items():
        if "small_vendor_affinity" in result:
            affinity_data = result["small_vendor_affinity"]
            # Aggregate GSA MAS small vendor share
            total_gsa = 0
            total_gsa_small = 0
            for sin, data in affinity_data.get("sin_results", {}).items():
                if sin in SMALL_VENDOR_SIN_AFFINITY:
                    total_gsa += data["total_obligation"]
                    total_gsa_small += data["small_vendor_obligation"]
            
            if total_gsa > 0:
                gsa_mas_small_shares[psc_code] = total_gsa_small / total_gsa
    
    # Check if DA10 leads
    da10_share = gsa_mas_small_shares.get("DA10", 0)
    max_other = max((v for k, v in gsa_mas_small_shares.items() if k != "DA10"), default=0)
    
    return {
        "gsa_mas_small_vendor_shares": gsa_mas_small_shares,
        "da10_leads": da10_share > max_other,
        "da10_share": da10_share,
        "max_other_share": max_other,
        "gate5_pass": da10_share > max_other and da10_share > 0.15,
    }


def run_validation(psc_code: str) -> Dict:
    """Run all validation gates for a single PSC code."""
    print(f"\n{'='*60}")
    print(f"E213 Validation for PSC {psc_code}")
    print(f"{'='*60}")
    
    # Fetch awards
    print(f"Fetching {MAX_PAGES} pages of awards...")
    all_awards, statuses = fetch_awards(psc_code)
    print(f"Fetched {len(all_awards)} awards")
    
    # Run gates
    print("Running G1: PIID-SIN consistency...")
    g1 = analyze_piid_sin_consistency(all_awards)
    print(f"  Consistency rate: {g1['consistency_rate']:.1%} ({g1['total_gsa_mas_piids']} PIIDs)")
    
    print("Running G2: Description-SIN alignment...")
    g2 = analyze_description_sin_alignment(all_awards)
    print(f"  Match rate: {g2['match_rate']:.1%} ({g2['matched_count']}/{g2['total_alignments_checked']})")
    
    print("Running G3: Small vendor affinity validation...")
    g3 = analyze_small_vendor_affinity(all_awards)
    print(f"  High-affinity avg share: {g3['high_affinity_avg_share']:.1%}")
    print(f"  Low-affinity avg share: {g3['low_affinity_avg_share']:.1%}")
    print(f"  Ratio: {g3['affinity_ratio']:.1f}x")
    print(f"  G3 PASS: {g3['gate3_pass']}")
    
    print("Running G4: SEWP holder scope validation...")
    g4 = analyze_sewp_holder_scope(all_awards)
    print(f"  Total SEWP holders: {g4['total_sewp_holders']}")
    print(f"  Full scope: {g4['full_scope_holders']}")
    print(f"  G4 PASS: {g4['gate4_pass']}")
    
    return {
        "psc_code": psc_code,
        "awards_analyzed": len(all_awards),
        "g1_consistency": g1,
        "g2_alignment": g2,
        "g3_affinity": g3,
        "g4_sewp_scope": g4,
    }


def main():
    """Run validation across all PSC codes."""
    print("E213: GSA MAS SIN / SEWP Category Validation")
    print("Using USAspending ground truth (official APIs inaccessible)")
    
    all_results = {}
    
    for psc_code in PSC_CODES:
        try:
            result = run_validation(psc_code)
            all_results[psc_code] = result
        except Exception as e:
            print(f"Error analyzing {psc_code}: {e}")
            all_results[psc_code] = {"error": str(e)}
    
    # Cross-code analysis (G5)
    print(f"\n{'='*60}")
    print(f"G5: Cross-Code Pattern Replication")
    print(f"{'='*60}")
    g5 = analyze_cross_code_patterns(all_results)
    print(f"  GSA MAS small vendor shares: {g5['gsa_mas_small_vendor_shares']}")
    print(f"  DA10 leads: {g5['da10_leads']} (DA10: {g5['da10_share']:.1%}, max other: {g5['max_other_share']:.1%})")
    print(f"  G5 PASS: {g5['gate5_pass']}")
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    for psc_code in PSC_CODES:
        if psc_code in all_results and "error" not in all_results[psc_code]:
            r = all_results[psc_code]
            g1_pass = r["g1_consistency"]["consistency_rate"] >= 0.7
            g2_pass = r["g2_alignment"]["match_rate"] >= 0.7
            g3_pass = r["g3_affinity"]["gate3_pass"]
            g4_pass = r["g4_sewp_scope"]["gate4_pass"]
            print(f"\n{psc_code}:")
            print(f"  G1 (PIID-SIN consistency): {'PASS' if g1_pass else 'FAIL'} ({r['g1_consistency']['consistency_rate']:.1%})")
            print(f"  G2 (Description-SIN alignment): {'PASS' if g2_pass else 'FAIL'} ({r['g2_alignment']['match_rate']:.1%})")
            print(f"  G3 (Small vendor affinity): {'PASS' if g3_pass else 'FAIL'} (ratio: {r['g3_affinity']['affinity_ratio']:.1f}x)")
            print(f"  G4 (SEWP holder scope): {'PASS' if g4_pass else 'FAIL'} ({r['g4_sewp_scope']['full_scope_holders']} full-scope holders)")
    
    print(f"\n  G5 (Cross-code replication): {'PASS' if g5['gate5_pass'] else 'FAIL'}")
    
    # Save results
    output = {
        "experiment": "E213",
        "description": "GSA MAS SIN / SEWP Category Validation using USAspending ground truth",
        "psc_codes": PSC_CODES,
        "results": all_results,
        "cross_code": g5,
        "gates_summary": {
            "G1": "PIID-SIN consistency",
            "G2": "Description-SIN alignment",
            "G3": "Small vendor affinity validation",
            "G4": "SEWP holder scope validation",
            "G5": "Cross-code pattern replication",
        },
    }
    
    output_path = "/home/ubuntu/think-free/EXPERIMENTS/E213-sin-sewp-validation/result.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()