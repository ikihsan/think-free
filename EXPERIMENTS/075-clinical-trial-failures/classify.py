#!/usr/bin/env python3
"""Classify terminated trials for E075."""
import json
import os
import re
import random

RAW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "terminated_trials.json")

SCIENTIFIC_KEYWORDS = [
    # Safety
    r'\bsafety\b', r'\badverse\b', r'\btoxicit', r'\bhepatotox', r'\bnephrotox',
    r'\bcardiotox', r'\bneurotox', r'\bdose.limit', r'\bunacceptable.*risk',
    r'\brisk.benefit', r'\bfatal', r'\bdeath', r'\bserious.*adverse',
    
    # Efficacy/Futility
    r'\befficac', r'\bfutil', r'\bno.*benefit', r'\bno.*clinical.*benefit',
    r'\bdid not demonstrate', r'\bfailed.*endpoint', r'\bprimary endpoint',
    r'\bco.primary', r'\bfutility', r'\bconditional power',
    r'\bfutility analysis', r'\bstopped.*early.*efficacy',
    
    # Mechanistic
    r'\bmechanis', r'\bbiomarker', r'\btarget.*engage', r'\bproof.*concept',
    r'\bpharmacodynamic', r'\bpd.*marker', r'\bnot.*achiev',
    r'\bnew.*data.*efficacy', r'\bphase 3.*no.*benefit', r'\bphase 3.*showed no',
]

ADMINISTRATIVE_KEYWORDS = [
    # Business/Funding
    r'\bbusiness.*decision', r'\bstrategic', r'\bportfolio', r'\bprioriti[sz]ation',
    r'\bfunding', r'\bfinancial', r'\bsponsor.*decision', r'\bcompany.*decision',
    r'\bdevelopment program.*terminat', r'\bmerger', r'\bacquisition',
    r'\bdissolution', r'\bdivest', r'\breprioriti[sz]e',
    
    # Recruitment
    r'\baccrual', r'\benroll', r'\brecruit', r'\bslow.*accrual',
    r'\blow.*recruit', r'\binsufficient.*enroll', r'\bdifficult.*recruit',
    r'\bcovid.*recruit', r'\bpandemic.*recruit', r'\bhalted.*recruit',
    r'\bunable.*complete.*enroll', r'\baccrual.*issue',
    
    # Regulatory
    r'\bregulatory', r'\bfda.*hold', r'\bprotocol.*amendment',
    r'\bhealth authorit', r'\bauthorit.*demand',
    
    # Operational
    r'\badministrative', r'\boperational', r'\blogistical',
    r'\bprincipal investigator', r'\bpi.*no longer', r'\bdeparture.*leader',
    r'\btransfer.*ownership', r'\bstudy only continued',
]

AMBIGUOUS_KEYWORDS = [
    r'\bterminated\b', r'\bstopped\b', r'\bclosed\b', r'\bhalted\b',
    r'\bdiscontinued\b', r'\bended\b', r'\bconcluded\b',
]

def classify_reason(reason_text):
    """Classify a why_stopped reason into scientific, administrative, or ambiguous."""
    if not reason_text or not reason_text.strip():
        return "ambiguous", "empty_reason"
    
    text = reason_text.lower()
    
    # Check scientific keywords
    for pattern in SCIENTIFIC_KEYWORDS:
        if re.search(pattern, text):
            return "scientific_failure", pattern
    
    # Check administrative keywords
    for pattern in ADMINISTRATIVE_KEYWORDS:
        if re.search(pattern, text):
            return "administrative_failure", pattern
    
    # Check ambiguous keywords (generic termination words without specific cause)
    for pattern in AMBIGUOUS_KEYWORDS:
        if re.search(pattern, text):
            return "ambiguous", pattern
    
    # Default to ambiguous if no keywords match
    return "ambiguous", "no_keyword_match"

def main():
    with open(RAW_PATH) as f:
        trials = json.load(f)
    
    results = []
    for t in trials:
        classification, matched_pattern = classify_reason(t.get("why_stopped", ""))
        results.append({
            "nct_id": t["nct_id"],
            "condition": t["_condition_name"],
            "phase": t["phase"],
            "enrollment": t["enrollment"],
            "why_stopped": t.get("why_stopped", ""),
            "classification": classification,
            "matched_pattern": matched_pattern,
            "lead_sponsor": t.get("lead_sponsor", ""),
        })
    
    # Stats
    total = len(results)
    scientific = [r for r in results if r["classification"] == "scientific_failure"]
    administrative = [r for r in results if r["classification"] == "administrative_failure"]
    ambiguous = [r for r in results if r["classification"] == "ambiguous"]
    
    print(f"=== E075 Classification Results (Automated) ===")
    print(f"Total terminated trials: {total}")
    print(f"Scientific failures: {len(scientific)} ({len(scientific)/total:.1%})")
    print(f"Administrative failures: {len(administrative)} ({len(administrative)/total:.1%})")
    print(f"Ambiguous: {len(ambiguous)} ({len(ambiguous)/total:.1%})")
    
    # By condition
    print(f"\n=== By Condition ===")
    conditions = set(r["condition"] for r in results)
    for cond in sorted(conditions):
        cond_results = [r for r in results if r["condition"] == cond]
        sci = sum(1 for r in cond_results if r["classification"] == "scientific_failure")
        adm = sum(1 for r in cond_results if r["classification"] == "administrative_failure")
        amb = sum(1 for r in cond_results if r["classification"] == "ambiguous")
        print(f"  {cond}: {len(cond_results)} total, {sci} sci ({sci/len(cond_results):.1%}), {adm} adm ({adm/len(cond_results):.1%}), {amb} amb ({amb/len(cond_results):.1%})")
    
    # Wilson CI95 for scientific failure fraction
    n = total
    k = len(scientific)
    if n > 0:
        p = k / n
        z = 1.96
        denom = 1 + z*z/n
        center = (p + z*z/(2*n)) / denom
        margin = z * ((p*(1-p)/n + z*z/(4*n*n)) ** 0.5) / denom
        print(f"\nWilson CI95 for scientific failure fraction: [{center-margin:.4f}, {center+margin:.4f}]")
    
    # Save results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classification.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {output_path}")
    
    # Sample for manual review (stratified 20%, min 30 per protocol)
    print(f"\n=== Sample for Manual Review (20% stratified) ===")
    random.seed(42)
    sample = []
    for cond in sorted(conditions):
        cond_results = [r for r in results if r["condition"] == cond]
        sample_size = max(10, int(0.2 * len(cond_results)))
        sampled = random.sample(cond_results, min(sample_size, len(cond_results)))
        sample.extend(sampled)
        print(f"  {cond}: {len(sampled)} sampled")
    
    # Ensure minimum 30 total
    if len(sample) < 30:
        remaining = [r for r in results if r not in sample]
        extra = random.sample(remaining, 30 - len(sample))
        sample.extend(extra)
    
    sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "sample_for_manual_review.json")
    with open(sample_path, "w") as f:
        json.dump(sample, f, indent=2)
    print(f"Manual review sample ({len(sample)} trials) saved to {sample_path}")
    
    # Print sample for manual review
    print("\n=== Manual Review Sample (first 10) ===")
    for s in sample[:10]:
        print(f"  [{s['nct_id']}] {s['condition']} | {s['classification']} ({s['matched_pattern']})")
        print(f"    why_stopped: {s['why_stopped'][:100]}")
        print()

if __name__ == "__main__":
    main()