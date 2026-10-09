#!/usr/bin/env python3
"""
E079 — Gate evaluation and main entry point for Mechanics.SE data analysis.
"""

import json
import os
import sys
import random
from collections import Counter
from typing import Any, Dict, List

from classify import get_structured_cases


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
QUESTIONS_FILE = os.path.join(RAW_DIR, "questions_with_answers.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Gate evaluation
# ---------------------------------------------------------------------------

def evaluate_gates(structured_cases: List[Dict], all_questions: List[Dict]) -> Dict:
    """Evaluate all kill gates."""
    results = {}

    # G1: Population - ≥ 200 structured cases
    g1_count = len(structured_cases)
    results["G1_population"] = {
        "threshold": 200,
        "actual": g1_count,
        "pass": g1_count >= 200,
    }

    # G2: Code concentration - top 10 codes cover ≥ 30% of cases
    code_counter = Counter()
    for q in structured_cases:
        for code in q.get("obd2_codes", []):
            code_counter[code] += 1

    total_cases = len(structured_cases)
    top10_codes = code_counter.most_common(10)
    top10_count = sum(count for _, count in top10_codes)
    top10_coverage = top10_count / total_cases if total_cases > 0 else 0

    results["G2_code_concentration"] = {
        "threshold": 0.30,
        "actual": top10_coverage,
        "top10_codes": top10_codes,
        "pass": top10_coverage >= 0.30,
    }

    # G3: Vehicle coverage - ≥ 15 distinct make/model/year/engine in top 10 codes
    top10_code_set = {code for code, _ in top10_codes}
    vehicle_configs = set()
    for q in structured_cases:
        if any(code in top10_code_set for code in q.get("obd2_codes", [])):
            vc = q.get("vehicle_config", ("", "", "", ""))
            if vc[0] and vc[3]:  # make and engine at minimum
                vehicle_configs.add(vc)

    results["G3_vehicle_coverage"] = {
        "threshold": 15,
        "actual": len(vehicle_configs),
        "vehicle_configs": list(vehicle_configs)[:20],
        "pass": len(vehicle_configs) >= 15,
    }

    # G4: Root cause specificity - ≥ 60% name specific part (Level 4-5)
    random.seed(42)
    top10_cases = [q for q in structured_cases if any(c in top10_code_set for c in q.get("obd2_codes", []))]
    sample = random.sample(top10_cases, min(50, len(top10_cases)))

    specific_count = sum(1 for q in sample if q.get("specificity", 0) >= 4)
    specific_rate = specific_count / len(sample) if sample else 0

    results["G4_root_cause_specificity"] = {
        "threshold": 0.60,
        "actual": specific_rate,
        "sample_size": len(sample),
        "specific_count": specific_count,
        "pass": specific_rate >= 0.60,
    }

    # G5: Incumbent gap - survey free tools for top 10 codes
    results["G5_incumbent_gap"] = {
        "threshold": "no single free tool covers ≥50% of top 10 codes with vehicle-specific root causes",
        "actual": "MANUAL_REVIEW_REQUIRED",
        "pass": None,
        "note": "Survey OBD-Codes.com, Engine-Codes.com, AutoCodes.com for top 10 codes",
    }

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E079 Analyze Mechanics.SE Data ===")

    # Load questions with answers
    if not os.path.exists(QUESTIONS_FILE):
        print(f"Error: {QUESTIONS_FILE} not found. Run fetch.py first.")
        return 1

    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)

    print(f"Loaded {len(questions)} questions with answers")

    # Identify structured cases
    structured = get_structured_cases(questions)
    print(f"Structured cases: {len(structured)}")

    # Evaluate gates
    gate_results = evaluate_gates(structured, questions)

    # Print results
    print("\n=== GATE EVALUATION ===")
    for gate, result in gate_results.items():
        status = "PASS" if result.get("pass") else ("FAIL" if result.get("pass") is False else "PENDING")
        print(f"  {gate}: {status}")
        for k, v in result.items():
            if k != "pass":
                print(f"    {k}: {v}")

    # Save results
    output = {
        "structured_count": len(structured),
        "total_questions": len(questions),
        "gate_results": gate_results,
        "top_codes": dict(Counter(c for q in structured for c in q.get("obd2_codes", [])).most_common(20)),
    }

    out_path = os.path.join(OUTPUT_DIR, "gate_results.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved gate results to {out_path}")

    # Save structured cases for manual review
    structured_path = os.path.join(OUTPUT_DIR, "structured_cases.json")
    with open(structured_path, "w") as f:
        slim = []
        for q in structured:
            sq = {k: v for k, v in q.items() if k not in ["body", "answers", "best_answer"]}
            if "best_answer" in q:
                sq["best_answer_body_preview"] = q["best_answer"].get("body", "")[:500]
            slim.append(sq)
        json.dump(slim, f, indent=2)
    print(f"Saved structured cases to {structured_path}")

    # Overall verdict
    auto_gates = ["G1_population", "G2_code_concentration", "G3_vehicle_coverage", "G4_root_cause_specificity"]
    auto_pass = all(gate_results[g].get("pass", False) for g in auto_gates)
    g5_pending = gate_results["G5_incumbent_gap"]["pass"] is None

    print(f"\n=== OVERALL ===")
    print(f"Automatic gates (G1-G4): {'ALL PASS' if auto_pass else 'SOME FAIL'}")
    print(f"G5 (incumbent gap): {'PENDING - manual review needed' if g5_pending else ('PASS' if gate_results['G5_incumbent_gap']['pass'] else 'FAIL')}")

    if auto_pass and not g5_pending:
        print("VERDICT: CANDIDATE SURVIVES - proceed to G5 manual review")
    elif not auto_pass:
        print("VERDICT: KILL - automatic gates failed")
    else:
        print("VERDICT: PENDING - complete G5 manual review")

    return 0


if __name__ == "__main__":
    sys.exit(main())