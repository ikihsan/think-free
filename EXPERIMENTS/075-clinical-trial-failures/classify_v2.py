#!/usr/bin/env python3
"""Improved classification for E075 with expanded keyword coverage."""
import json
import os
import re

RAW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "terminated_trials.json")

SCIENTIFIC_KEYWORDS = [
    # Safety
    r'\bsafety\b', r'\badverse\b', r'\btoxicit', r'\bhepatotox', r'\bnephrotox',
    r'\bcardiotox', r'\bneurotox', r'\bdose.limit', r'\bunacceptable.*risk',
    r'\brisk.benefit', r'\bfatal', r'\bdeath', r'\bserious.*adverse',
    r'\bimmune.*related', r'\bunfavorable.*risk', r'\bworse than placebo',
    
    # Efficacy/Futility
    r'\befficac', r'\bfutil', r'\bno.*benefit', r'\bno.*clinical.*benefit',
    r'\bdid not demonstrate', r'\bfailed.*endpoint', r'\bprimary endpoint',
    r'\bco.primary', r'\bfutility', r'\bconditional power',
    r'\bfutility analysis', r'\bstopped.*early.*efficacy',
    r'\binsufficient target engagement', r'\bno evidence.*efficacy',
    r'\blikelihood.*significant', r'\bresults expected', r'\bdid not yield.*results',
    r'\bparent study results', r'\bpreliminary.*result',
    
    # Mechanistic
    r'\bmechanis', r'\bbiomarker', r'\btarget.*engage', r'\bproof.*concept',
    r'\bpharmacodynamic', r'\bpd.*marker', r'\bnot.*achiev',
    r'\bnew.*data.*efficacy', r'\bphase 3.*no.*benefit', r'\bphase 3.*showed no',
    r'\babnormal distribution', r'\black.*tumor.*target',
]

ADMINISTRATIVE_KEYWORDS = [
    # Business/Funding
    r'\bbusiness.*decision', r'\bstrategic', r'\bportfolio', r'\bprioriti[sz]ation',
    r'\bfunding', r'\bfinancial', r'\bsponsor.*decision', r'\bcompany.*decision',
    r'\bdevelopment program.*terminat', r'\bmerger', r'\bacquisition',
    r'\bdissolution', r'\bdivest', r'\breprioriti[sz]e',
    r'\bloss of interest', r'\bno longer.*interest',
    
    # Recruitment
    r'\baccrual', r'\benroll', r'\brecruit', r'\bslow.*accrual',
    r'\blow.*recruit', r'\binsufficient.*enroll', r'\bdifficult.*recruit',
    r'\bcovid.*recruit', r'\bpandemic.*recruit', r'\bhalted.*recruit',
    r'\bunable.*complete.*enroll', r'\baccrual.*issue',
    r'\bpoor.*accrual', r'\btarget.*enrollment.*not met', r'\brecruitment target',
    
    # Regulatory
    r'\bregulatory', r'\bfda.*hold', r'\bprotocol.*amendment',
    r'\bhealth authorit', r'\bauthorit.*demand', r'\bnational health authorit',
    r'\bdemands by.*authorit',
    
    # Operational
    r'\badministrative', r'\boperational', r'\blogistical',
    r'\bprincipal investigator', r'\bpi.*no longer', r'\bdeparture.*leader',
    r'\btransfer.*ownership', r'\bstudy only continued',
    r'\binvestigator decision', r'\bproducts expired', r'\bexpired with irb',
    r'\bpi has terminated', r'\bno plans for scholarly',
    
    # COVID/Pandemic
    r'\bcovid', r'\bcovid-19', r'\bsars.cov.2', r'\bpandemic',
    
    # Standard of care / Competitive
    r'\bosimertinib approval', r'\bstandard of care', r'\bchange in standard',
    r'\bavastin refractory', r'\btreatment paradigm',
    r'\bbenefit.risk assessment',
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
    
    print(f"=== E075 Classification Results (Improved Automated) ===")
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
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classification_v2.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {output_path}")

if __name__ == "__main__":
    main()