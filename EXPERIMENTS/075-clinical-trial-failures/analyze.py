#!/usr/bin/env python3
"""Analyze E075 results and evaluate gates."""
import json
import os

CLASSIFICATION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classification_v2.json")
MANUAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "sample_with_manual.json")

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    margin = z * ((p*(1-p)/n + z*z/(4*n*n)) ** 0.5) / denom
    return (center - margin, center + margin)

def main():
    with open(CLASSIFICATION_PATH) as f:
        results = json.load(f)
    
    with open(MANUAL_PATH) as f:
        manual_sample = json.load(f)
    
    total = len(results)
    scientific = [r for r in results if r["classification"] == "scientific_failure"]
    administrative = [r for r in results if r["classification"] == "administrative_failure"]
    ambiguous = [r for r in results if r["classification"] == "ambiguous"]
    
    print("=" * 60)
    print("E075 — Terminated Clinical Trials: Gate Evaluation")
    print("=" * 60)
    
    # G1 Retrieval
    print("\n--- G1 Retrieval ---")
    conditions = set(r["condition"] for r in results)
    cond_counts = {}
    for cond in conditions:
        cond_counts[cond] = sum(1 for r in results if r["condition"] == cond)
    
    g1_met = total >= 200 and len(conditions) >= 3
    print(f"Total terminated trials: {total} (target ≥ 200) {'✓' if total >= 200 else '✗'}")
    print(f"Conditions: {len(conditions)} (target ≥ 3) {'✓' if len(conditions) >= 3 else '✗'}")
    for cond, count in sorted(cond_counts.items()):
        print(f"  {cond}: {count}")
    print(f"G1: {'MET' if g1_met else 'NOT MET'}")
    
    # G2 Classification Validity (using manual review sample)
    print("\n--- G2 Classification Validity ---")
    manual_results = []
    for m in manual_sample:
        auto = m.get("classification", "")
        manual = m.get("manual_classification", "")
        manual_results.append({"auto": auto, "manual": manual})
    
    # Cohen's kappa
    from collections import Counter
    categories = ['scientific_failure', 'administrative_failure', 'ambiguous']
    n = len(manual_results)
    agreements = sum(1 for m in manual_results if m['auto'] == m['manual'])
    po = agreements / n
    auto_counts = Counter(m['auto'] for m in manual_results)
    manual_counts = Counter(m['manual'] for m in manual_results)
    pe = sum((auto_counts.get(c, 0)/n) * (manual_counts.get(c, 0)/n) for c in categories)
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 0 else 0
    
    print(f"Manual review sample: {n} trials")
    print(f"Observed agreement: {po:.3f} ({agreements}/{n})")
    print(f"Cohen's kappa: {kappa:.3f} (target ≥ 0.80)")
    
    # Confusion matrix
    print("Confusion Matrix:")
    header = "{:<25} {:>6} {:>6} {:>6}".format("Auto \\ Manual", "Sci", "Adm", "Amb")
    print(header)
    for a_cat in categories:
        row = []
        for m_cat in categories:
            count = sum(1 for m in manual_results if m['auto'] == a_cat and m['manual'] == m_cat)
            row.append("{:>6}".format(count))
        print("{:<25} {}".format(a_cat, " ".join(row)))
    
    g2_met = kappa >= 0.80
    print(f"G2: {'MET' if g2_met else 'NOT MET'} (kappa={kappa:.3f})")
    
    # Note: automated vs manual kappa; two human readers not available
    if not g2_met:
        print("  NOTE: Kappa measured between automated classifier and single human reader.")
        print("  Two independent human readers not available in this session.")
    
    # G3 The Measurement
    print("\n--- G3 The Measurement ---")
    print(f"Scientific failure fraction: {len(scientific)}/{total} = {len(scientific)/total:.1%}")
    ci = wilson_ci(len(scientific), total)
    if ci:
        print(f"Wilson CI95: [{ci[0]:.4f}, {ci[1]:.4f}]")
    
    print("\nBy Condition:")
    for cond in sorted(conditions):
        cond_results = [r for r in results if r["condition"] == cond]
        cond_sci = sum(1 for r in cond_results if r["classification"] == "scientific_failure")
        cond_adm = sum(1 for r in cond_results if r["classification"] == "administrative_failure")
        cond_amb = sum(1 for r in cond_results if r["classification"] == "ambiguous")
        ci_cond = wilson_ci(cond_sci, len(cond_results))
        ci_str = f" [{ci_cond[0]:.3f}, {ci_cond[1]:.3f}]" if ci_cond else ""
        print(f"  {cond}: {cond_sci}/{len(cond_results)} = {cond_sci/len(cond_results):.1%} scientific{ci_str}")
        print(f"    Administrative: {cond_adm} ({cond_adm/len(cond_results):.1%}), Ambiguous: {cond_amb} ({cond_amb/len(cond_results):.1%})")
    
    print("G3: MET (measurement completed)")
    
    # G4 Enrollment Validation
    print("\n--- G4 Enrollment Validation ---")
    enrolled = sum(1 for r in results if r["enrollment"] > 0)
    enrolled_rate = enrolled / total
    print(f"Trials with enrollment > 0: {enrolled}/{total} = {enrolled_rate:.1%} (target ≥ 80%)")
    g4_met = enrolled_rate >= 0.80
    print(f"G4: {'MET' if g4_met else 'NOT MET'}")
    
    # Overall
    print("\n" + "=" * 60)
    print("OVERALL RESULT")
    print("=" * 60)
    
    all_gates = {
        "G1 Retrieval": g1_met,
        "G2 Classification Validity": g2_met,
        "G3 Measurement": True,
        "G4 Enrollment": g4_met,
    }
    
    for gate, met in all_gates.items():
        print(f"  {gate}: {'MET' if met else 'NOT MET'}")
    
    # Conclusion
    sci_frac = len(scientific) / total
    adm_frac = len(administrative) / total
    
    print(f"\nScientific failure fraction: {sci_frac:.1%} (CI95 {ci[0]:.1%}-{ci[1]:.1%})")
    print(f"Administrative failure fraction: {adm_frac:.1%}")
    
    if sci_frac < 0.20 and adm_frac > 0.40:
        conclusion = "HYPOTHESIS NOT SUPPORTED"
        detail = "Terminated trials are predominantly administrative failures (recruitment, funding, business decisions), not scientific failures. No candidate emerges from failed mechanistic hypotheses."
    elif sci_frac >= 0.30:
        conclusion = "HYPOTHESIS SUPPORTED"
        detail = "Substantial fraction of scientific failures with potential mechanistic patterns. Candidate opportunity in research intelligence."
    else:
        conclusion = "INCONCLUSIVE"
        detail = "Scientific failure fraction is low but not negligible. Further investigation needed with better classification."
    
    print(f"\nConclusion: {conclusion}")
    print(f"Detail: {detail}")
    
    # Save analysis result
    analysis_result = {
        "experiment": "E075",
        "total_terminated": total,
        "scientific_fraction": sci_frac,
        "scientific_ci95": ci,
        "administrative_fraction": adm_frac,
        "ambiguous_fraction": len(ambiguous)/total,
        "gates": all_gates,
        "kappa": kappa,
        "conclusion": conclusion,
        "detail": detail,
    }
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ANALYSIS.json")
    with open(output_path, "w") as f:
        json.dump(analysis_result, f, indent=2)
    print(f"\nAnalysis saved to {output_path}")

if __name__ == "__main__":
    main()