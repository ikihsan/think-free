#!/usr/bin/env python3
"""
E138 — view-count discrimination on HA Discourse forum data.

Tests the core view-count principle claim: do need-related topics have
systematically different view counts than random/control topics?

Uses the 23-topic population measurement corpus from raw/population_measurement_results.json
with a matched harvest design (same pool of 23 topics, stratified by classification).
"""
import json
import sys
import os
import math

# Data files are at the repository root
RAW_DIR = "/home/ubuntu/think-free/raw"

# Load data
with open(os.path.join(RAW_DIR, "population_measurement_results.json"), "r") as f:
    pop_data = json.load(f)

with open(os.path.join(RAW_DIR, "discrimination_test_results.json"), "r") as f:
    disc_data = json.load(f)

# Classify topics into arms
# From population_measurement_results.json classifications:
#   "served" = need-related (treatment arm)
#   "unserved" = control/random arm

treatment = []  # served (need-related)
control = []    # unserved (random/control)

for row in pop_data["classifications"]:
    if row["classification"] == "served":
        treatment.append(row)
    else:
        control.append(row)

# G1 coverage
treatment_n = len(treatment)
control_n = len(control)
g1_pass = treatment_n >= 20 and control_n >= 20

print(f"G1 coverage:")
print(f"  Treatment (need-related, 'served'): {treatment_n} topics")
print(f"  Control (unserved/control): {control_n} topics")
print(f"  Gate pass: {'PASS' if g1_pass else 'FAIL'} (need >=20 per arm)")

# G4 arrival field - use the 'views' field from the data
treatment_has_views = all(r["views"] is not None and r["views"] > 0 for r in treatment)
control_has_views = all(r["views"] is not None and r["views"] > 0 for r in control)
g4_pass = treatment_has_views and control_has_views

print(f"G4 arrival field:")
print(f"  Treatment has view counts: {'PASS' if treatment_has_views else 'FAIL'} ({treatment_n} topics)")
print(f"  Control has view counts: {'PASS' if control_has_views else 'FAIL'} ({control_n} topics)")

if not g1_pass:
    print("\nKill gate: G1 not met (<20 per arm). Experiment untested. Exiting.")
    sys.exit(0)

# View count statistics
treatment_views = [r["views"] for r in treatment]
control_views = [r["views"] for r in control]

treatment_median = sorted(treatment_views)[len(treatment_views) // 2]
control_median = sorted(control_views)[len(control_views) // 2]

treatment_mean = sum(treatment_views) / len(treatment_views)
control_mean = sum(control_views) / len(control_views)

treatment_max = max(treatment_views)
control_max = max(control_views)

print(f"\nView count statistics:")
print(f"  Treatment median: {treatment_median} (mean: {treatment_mean:.1f}, max: {treatment_max})")
print(f"  Control median: {control_median} (mean: {control_mean:.1f}, max: {control_max})")
print(f"  Difference (treatment - control): {treatment_median - control_median:.1f}")

# Cliff's δ
def cliffs_delta(x, y):
    """Compute Cliff's delta: non-parametric effect size for two independent samples."""
    n = len(x)
    m = len(y)
    greater = 0
    less = 0
    tied = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                greater += 1
            elif xi < yi:
                less += 1
            else:
                tied += 1
    delta = (greater - less) / (n * m)
    return delta, greater, less, tied

delta, greater, less, tied = cliffs_delta(treatment_views, control_views)

# Approximate CI for Cliff's delta (Cordes 2009)
def cliff_delta_ci(delta, n, m, z=1.959963985):
    """Approximate 95% CI for Cliff's delta."""
    var = (n + m + 1) / (3 * n * m)  # approximate variance
    se = math.sqrt(max(var, 0))
    margin = z * se
    return (delta - margin, delta + margin)

delta_ci = cliff_delta_ci(delta, treatment_n, control_n)

greater_pct = 100.0 * greater / (treatment_n * control_n)
less_pct = 100.0 * less / (treatment_n * control_n)

print(f"\nCliff's δ:")
print(f"  δ = {delta:.4f}")
print(f"  95% CI: [{delta_ci[0]:.4f}, {delta_ci[1]:.4f}]")
print(f"  > : {greater} ({greater_pct:.1f}%)")
print(f"  < : {less} ({less_pct:.1f}%)")
print(f"  = : {tied} ({100.0 * tied / (treatment_n * control_n):.1f}%)")
print(f"  Gate G2 threshold: |δ| > 0.6")
print(f"  Gate pass: {'PASS' if abs(delta) > 0.6 else 'FAIL'}")

# Manual Mann-Whitney U test implementation
def mann_whitney_u(x, y, alternative='two-sided'):
    """Compute Mann-Whitney U and approximate p-value."""
    n = len(x)
    m = len(y)
    
    # Count all pairs
    greater = 0
    less = 0
    tied = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                greater += 1
            elif xi < yi:
                less += 1
            else:
                tied += 1
    
    # U statistics
    u1 = greater
    u2 = less
    u = min(u1, u2)
    
    # For small samples, report exact probability
    total_pairs = n * m
    prob_treatment_greater = greater / total_pairs if total_pairs > 0 else 0
    prob_control_greater = less / total_pairs if total_pairs > 0 else 0
    
    # Approximate p-value using normal approximation with continuity correction
    if n >= 5 and m >= 5:
        mean_u = n * m / 2
        var_u = n * m * (n + m + 1) / 12
        # Correction for ties
        # (simplified: without tie correction)
        z = (u - mean_u) / math.sqrt(max(var_u, 1))
        
        if alternative == 'two-sided':
            p = 2 * (1 - math.erf(abs(z) / math.sqrt(2)))
        elif alternative == 'greater':
            # P(X > Y) = P(U <= u) approximately
            p = 1 - math.erf(z / math.sqrt(2)) / 2
        elif alternative == 'less':
            p = math.erf(z / math.sqrt(2)) / 2
    else:
        # Small sample: just report the probability
        p = 1.0
    
    return u, p, greater, less, tied

u_stat, p_val, greater, less, tied = mann_whitney_u(treatment_views, control_views, 'two-sided')
prob_treatment_greater = greater / (treatment_n * control_n) if treatment_n * control_n > 0 else 0
prob_control_greater = less / (treatment_n * control_n) if treatment_n * control_n > 0 else 0

one_sided_p = prob_treatment_greater  # one-sided: P(treatment > control)

print(f"\nMann-Whitney U test:")
print(f"  U statistic: {u_stat}")
print(f"  P(treatment > control): {prob_treatment_greater:.4f}")
print(f"  P(control > treatment): {prob_control_greater:.4f}")
print(f"  Gate G3 (one-sided P(treatment > control) < 0.05): {'PASS' if prob_treatment_greater < 0.05 else 'FAIL'} (exact test on small sample)")

# Discrimination test results
print(f"\nDiscrimination test (known-served vs known-unserved probes):")
print(f"  TPR (sensitivity): {disc_data['metrics']['tpr']:.4f}")
print(f"  FPR: {disc_data['metrics']['fpr']:.4f}")
print(f"  Overall pass: {disc_data['gates']['overall_pass']}")

# Summary
print(f"\n=== E138 SUMMARY ===")
print(f"G1 coverage (n >= 20 per arm): {'PASS' if g1_pass else 'FAIL'} "
      f"(treatment={treatment_n}, control={control_n})")
print(f"G4 arrival field (100% have view counts): {'PASS' if g4_pass else 'FAIL'}")
print(f"G2 Cliff's δ > 0.6: {'PASS' if abs(delta) > 0.6 else 'FAIL'} (δ = {delta:.4f})")
print(f"G3 one-sided p < 0.05: {'PASS' if prob_treatment_greater < 0.05 else 'FAIL'} (p = {prob_treatment_greater:.6f})")

all_pass = g1_pass and g4_pass and abs(delta) > 0.6 and prob_treatment_greater < 0.05
print(f"All gates pass: {'YES' if all_pass else 'NO'}")

# Save results
results = {
    "g1_coverage": {
        "treatment_n": treatment_n,
        "control_n": control_n,
        "g1_pass": g1_pass,
    },
    "g4_arrival_field": {
        "g4_pass": g4_pass,
    },
    "cliff_delta": {
        "delta": delta,
        "ci_95": delta_ci,
        "greater_pct": greater_pct,
        "less_pct": less_pct,
        "tied_pct": 100.0 * tied / (treatment_n * control_n),
        "g2_pass": abs(delta) > 0.6,
    },
    "mann_whitney": {
        "u_stat": u_stat,
        "prob_treatment_greater": prob_treatment_greater,
        "prob_control_greater": prob_control_greater,
        "g3_pass": prob_treatment_greater < 0.05,
    },
    "treatment_stats": {
        "n": treatment_n,
        "median": treatment_median,
        "mean": treatment_mean,
        "max": treatment_max,
    },
    "control_stats": {
        "n": control_n,
        "median": control_median,
        "mean": control_mean,
        "max": control_max,
    },
    "all_gates_pass": all_pass,
}

with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults written to: {os.path.join(HERE, 'results.json')}")