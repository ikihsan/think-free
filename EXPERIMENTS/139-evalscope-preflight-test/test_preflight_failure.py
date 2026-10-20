"""Preflight test demonstrating failure detection on evalscope-format data with injected defects."""

import sys
sys.path.insert(0, 'EXPERIMENTS/124-eval-harness-preflight')
sys.path.insert(0, 'EXPERIMENTS/139-evalscope-preflight-test')

from preflight import concordance, alternate_form_fp, control_arm, render
from evalscope_adapter import adapt_evalscope

# Load the evalscope run output
key_rows, out_rows = adapt_evalscope(
    'EXPERIMENTS/139-evalscope-preflight-test/predictions_dir',
    'EXPERIMENTS/139-evalscope-preflight-test/reviews_dir'
)

# Inject F121-style defect: change key_rows index to string while out_rows keeps int
key_rows_defective = [{"task": kr["task"], "index": str(kr["index"])} for kr in key_rows]
out_rows_defective = out_rows  # keeps int index

print("=== Test 1: F121-style type conflict (index: str vs int) ===")
c1 = concordance(key_rows_defective, out_rows_defective)
print(f"  verdict: {c1['verdict']}")
print(f"  best_rate: {c1['best_rate']}")
print(f"  type_conflicts: {c1['type_conflicts']}")
print(f"  reason: {c1['reason']}")

# Test 2: Control arm with true positives (F122-style)
print("\n=== Test 2: F122-style control arm contamination ===")
control_rows = [
    {"id": "ctrl_1", "evidence": "monthly recurring payment of 50.00"},
    {"id": "ctrl_2", "evidence": "no task data"},
    {"id": "ctrl_3", "evidence": "monthly identical amount 100.00"},
]

def is_positive(row):
    # Predicate independent of key: looks for recurring payment patterns
    evidence = row.get("evidence", "").lower()
    return "monthly" in evidence and ("recurring" in evidence or "identical amount" in evidence)

c3 = control_arm(control_rows, is_positive, premise=0.0, name="bank_extract_control")
print(f"  verdict: {c3['verdict']}")
print(f"  positives: {c3['positives']} / {c3['rows']}")
print(f"  rate: {c3['rate']}")
print(f"  wilson: {c3['wilson']}")
print(f"  reason: {c3['reason']}")

# Test 3: Alternate-form FP with a flagger that condemns correct items
print("\n=== Test 3: C2 alternate-form FP (flagger too strict) ===")
control_items = []
for row in out_rows:
    if "score" in row:
        control_items.append({
            "arm": "evalscope_run",
            "value": f"task={row['task']} index={row['index']} target={row['target']}",
            "correct": True,
        })

# Flagger that requires exact string match (too strict for alternate forms)
def strict_flagger(item):
    # This flagger only passes if the value contains "target=A" exactly
    # But our test data has various targets
    if "target=A" in item["value"]:
        return "OK"
    return "ungrounded_value"

c2 = alternate_form_fp(control_items, strict_flagger, fp_ceiling=0.02)
print(f"  verdict: {c2['verdict']}")
print(f"  worst_fp_wilson_lower: {c2['worst_fp_wilson_lower']}")
for arm, data in c2['arms'].items():
    print(f"  arm '{arm}': correct={data['correct_items']['n']} flagged={data['correct_items']['flagged']} fp_rate={data['correct_items']['rate']}")

# Combined report for Test 1 (type conflict)
print("\n=== Combined Report: Type Conflict ===")
checks = [c1]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"Exit code: {code}")

# Combined report for Test 2 (control contamination)
print("\n=== Combined Report: Control Contamination ===")
checks = [concordance(key_rows, out_rows), c3]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"Exit code: {code}")

# Combined report for Test 3 (alternate-form FP)
print("\n=== Combined Report: Alternate-form FP ===")
checks = [concordance(key_rows, out_rows), c2]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"Exit code: {code}")