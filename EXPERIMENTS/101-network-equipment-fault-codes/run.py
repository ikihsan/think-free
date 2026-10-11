#!/usr/bin/env python3
"""
E101 — Fresh observation in network equipment fault codes domain using Discourse forums.

Measures the view_count (arrival) instrument and unserved-open-like fraction
across network equipment Discourse forums. Uses the validated
Discourse harvest approach from E077/E082.
"""

import json
import os
import sys
from pathlib import Path

# Import harvest helpers
sys.path.insert(0, str(Path(__file__).parent))
from harvest import (
    TOPICS_PER_FORUM,
    harvest_forum_topics,
    save_raw_data,
)

# Import classification
from classify import classify_topics, summarize_classification, check_gates


# ---------------------------------------------------------------------------
# Pre-declared network equipment Discourse forums
# ---------------------------------------------------------------------------

# Note: Only accessible Discourse forums are included. Other target forums
# (community.cisco.com - 403, community.ui.com - parse error, 
# forums.juniper.net - 404) were not accessible via /latest.json API.
TARGET_FORUMS = [
    "forum.mikrotik.com",            # MikroTik RouterOS community
    "community.cambiumnetworks.com", # Cambium Networks community
    "community.f5.com",              # F5 Networks community
]


def main() -> int:
    """Main entry point for E101 Discourse measurement."""
    print("=== E101 Network Equipment Discourse view_count + unserved-open Measurement ===")
    print(f"Target forums: {len(TARGET_FORUMS)}")
    print(f"Topics per forum: {TOPICS_PER_FORUM}")
    print()
    
    output_dir = Path(__file__).parent / "raw"
    output_dir.mkdir(exist_ok=True)
    
    all_results = []
    all_topics = []
    all_classified = []
    
    for domain in TARGET_FORUMS:
        try:
            # Harvest
            print(f"\n--- Harvesting {domain} ---")
            topics = harvest_forum_topics(domain)
            # Map Discourse 'views' field to 'view_count' for compatibility
            for t in topics:
                t["view_count"] = t.get("views", 0)
            print(f"  Fetched {len(topics)} topics")
            
            # Classify
            classified = classify_topics(topics)
            
            # Save raw data
            save_raw_data(domain, topics, classified, str(output_dir))
            
            # Summarize
            summary = summarize_classification(classified)
            print(f"  Total: {summary['total']}, Need: {summary['need_count']}, Served: {summary['served_count']}, Unserved-open-like: {summary['unserved_open_like_count']}, View+ rate: {summary['view_positive_rate']:.2%}")
            
            # Check gates
            gates = check_gates(summary)
            print(f"  Gates: G1={gates['G1_need_prevalence']}, G2={gates['G2_control_validity']}, G3={gates['G3_unserved_fraction']}, G4={gates['G4_view_count']}")
            
            result = {
                "domain": domain,
                "summary": summary,
                "gates": gates,
            }
            all_results.append(result)
            
            all_topics.extend(topics)
            all_classified.extend(classified)
            
        except Exception as e:
            print(f"Error measuring {domain}: {e}")
            import traceback
            traceback.print_exc()
            all_results.append({
                "domain": domain,
                "total": 0,
                "error": str(e),
            })
    
    # Aggregate results
    if all_results:
        agg_summary = {
            "total": sum(r.get("summary", {}).get("total", 0) for r in all_results),
            "need_count": sum(r.get("summary", {}).get("need_count", 0) for r in all_results),
            "served_count": sum(r.get("summary", {}).get("served_count", 0) for r in all_results),
            "unserved_open_like_count": sum(r.get("summary", {}).get("unserved_open_like_count", 0) for r in all_results),
            "vc_positive": sum(r.get("summary", {}).get("vc_positive", 0) for r in all_results),
        }
        agg_summary["need_fraction"] = agg_summary["need_count"] / agg_summary["total"] if agg_summary["total"] else 0
        agg_summary["served_fraction"] = agg_summary["served_count"] / agg_summary["total"] if agg_summary["total"] else 0
        agg_summary["unserved_open_like_fraction"] = agg_summary["unserved_open_like_count"] / agg_summary["total"] if agg_summary["total"] else 0
        agg_summary["view_positive_rate"] = agg_summary["vc_positive"] / agg_summary["total"] if agg_summary["total"] else 0
        
        agg_gates = check_gates(agg_summary)
        all_gates_pass = all(agg_gates.values())
        
        print(f"\n=== AGGREGATE RESULTS ===")
        print(f"Total topics: {agg_summary['total']}")
        print(f"Need topics: {agg_summary['need_count']} ({agg_summary['need_fraction']:.2%})")
        print(f"Served: {agg_summary['served_count']} ({agg_summary['served_fraction']:.2%})")
        print(f"Unserved-open-like: {agg_summary['unserved_open_like_count']} ({agg_summary['unserved_open_like_fraction']:.2%})")
        print(f"View_count > 0: {agg_summary['vc_positive']} ({agg_summary['view_positive_rate']:.2%})")
        print(f"Gates: G1={agg_gates['G1_need_prevalence']}, G2={agg_gates['G2_control_validity']}, G3={agg_gates['G3_unserved_fraction']}, G4={agg_gates['G4_view_count']}")
        print(f"All gates pass: {all_gates_pass}")
        
        # Save aggregated results
        output_path = Path(__file__).parent / "results.json"
        with open(output_path, "w") as f:
            json.dump({
                "forums": all_results,
                "aggregate": {
                    "summary": agg_summary,
                    "gates": agg_gates,
                    "all_gates_pass": all_gates_pass,
                },
            }, f, sort_keys=True, indent=2)
        
        print(f"\n=== Results saved to {output_path} ===")
    
    return 0 if (all_results and all_gates_pass) else 1


if __name__ == "__main__":
    sys.exit(main())