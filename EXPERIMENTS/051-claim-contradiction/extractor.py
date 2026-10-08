#!/usr/bin/env python3
"""Detect directional-claim contradictions across abstracts.
Extraction lives in claim_extraction.py; stdlib only."""
import argparse
import json
from collections import defaultdict
from typing import Dict, List

from claim_extraction import extract_claims

def detect_contradictions(claims_by_abstract: Dict[str, List[Dict]]) -> List[Dict]:
    """Detect contradictions across abstracts for the same variable pair."""
    pair_claims = defaultdict(list)
    for abstract_id, claims in claims_by_abstract.items():
        for claim in claims:
            key = (claim["subject"], claim["object"])
            pair_claims[key].append({**claim, "abstract_id": abstract_id})
    
    contradictions = []
    for (subject, obj), claims in pair_claims.items():
        if len(claims) < 2:
            continue
        
        relationships = set(c["relationship"] for c in claims)
        
        has_increase = any(r.startswith("INCREASE") or r.startswith("MAY_INCREASE") for r in relationships)
        has_decrease = any(r.startswith("DECREASE") or r.startswith("MAY_DECREASE") for r in relationships)
        has_no_effect = any(r == "NO_EFFECT" or r.startswith("MAY_NO_EFFECT") for r in relationships)
        
        contradiction_type = None
        if has_increase and has_decrease:
            contradiction_type = "INCREASE_vs_DECREASE"
        elif has_increase and has_no_effect:
            contradiction_type = "INCREASE_vs_NO_EFFECT"
        elif has_decrease and has_no_effect:
            contradiction_type = "DECREASE_vs_NO_EFFECT"
        
        if contradiction_type:
            conflicting = [c for c in claims if c["relationship"] in relationships]
            contradictions.append({
                "subject": subject,
                "object": obj,
                "contradiction_type": contradiction_type,
                "relationships": list(relationships),
                "claims": conflicting,
                "abstract_ids": [c["abstract_id"] for c in conflicting]
            })
    
    return contradictions


def load_abstracts(input_file: str) -> Dict[str, str]:
    """Load abstracts from JSONL file."""
    abstracts = {}
    with open(input_file, "r") as f:
        for line in f:
            data = json.loads(line)
            abstracts[data["id"]] = data["abstract"]
    return abstracts


def main():
    parser = argparse.ArgumentParser(description="Extract directional claims and detect contradictions")
    parser.add_argument("--input", required=True, help="Input JSONL file with abstracts")
    parser.add_argument("--output", required=True, help="Output JSONL file with contradictions")
    args = parser.parse_args()
    
    abstracts = load_abstracts(args.input)
    
    claims_by_abstract = {}
    for abs_id, abstract in abstracts.items():
        claims_by_abstract[abs_id] = extract_claims(abstract)
    
    contradictions = detect_contradictions(claims_by_abstract)
    
    with open(args.output, "w") as f:
        for contra in contradictions:
            f.write(json.dumps(contra) + "\n")
    
    print(f"Processed {len(abstracts)} abstracts")
    print(f"Extracted claims from {len(claims_by_abstract)} abstracts")
    print(f"Found {len(contradictions)} contradictions")


if __name__ == "__main__":
    main()
