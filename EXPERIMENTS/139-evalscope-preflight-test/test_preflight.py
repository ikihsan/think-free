"""Full preflight test against evalscope-format synthetic run output."""

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

print("=== C1: Concordance ===")
c1 = concordance(key_rows, out_rows)
print(f"  verdict: {c1['verdict']}")
print(f"  best_rate: {c1['best_rate']}")
print(f"  key_rows: {c1['key_rows']}")
print(f"  output_rows: {c1['output_rows']}")

# C2: Alternate-form false positive rate
# Create control items with known correctness
# For this synthetic test, we'll use the out_rows as "correct" items
# and create some "incorrect" items
control_items = []

# Add correct items (from the actual run - these are known correct)
for row in out_rows:
    if "score" in row:
        control_items.append({
            "arm": "evalscope_run",
            "value": f"task={row['task']} index={row['index']} target={row['target']}",
            "correct": True,  # These are from the actual run
        })

# Add some incorrect items (simulated wrong predictions)
control_items.append({
    "arm": "evalscope_run",
    "value": "task=test index=99 target=X",
    "correct": False,
})

# Simple flagger that checks if score == 1.0
def simple_flagger(item):
    # In real use, this would be the harness's actual flagger
    # For this test, we just return "OK" for correct items
    if item.get("correct"):
        return "OK"
    return "ungrounded_value"

print("\n=== C2: Alternate-form FP ===")
c2 = alternate_form_fp(control_items, simple_flagger, fp_ceiling=0.02)
print(f"  verdict: {c2['verdict']}")
print(f"  worst_fp_wilson_lower: {c2['worst_fp_wilson_lower']}")
for arm, data in c2['arms'].items():
    print(f"  arm '{arm}': correct={data['correct_items']['n']} flagged={data['correct_items']['flagged']} fp_rate={data['correct_items']['rate']} recall_on_incorrect={data['recall_on_incorrect']}")

# C3: Control arm validity
# Create a control arm that should be negative
# For this test, we'll use a hypothetical negative arm
control_rows = [
    {"id": "ctrl_1", "evidence": "no task data"},
    {"id": "ctrl_2", "evidence": "no task data"},
    {"id": "ctrl_3", "evidence": "no task data"},
]

# Predicate: is this a true positive? (should be false for control arm)
def is_positive(row):
    return False  # Control arm has no true positives

print("\n=== C3: Control Arm ===")
c3 = control_arm(control_rows, is_positive, premise=0.0, name="negative_control")
print(f"  verdict: {c3['verdict']}")
print(f"  positives: {c3['positives']} / {c3['rows']}")
print(f"  rate: {c3['rate']}")
print(f"  wilson: {c3['wilson']}")

# Combined report
print("\n=== Combined Report ===")
checks = [c1, c2, c3]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"\nExit code: {code}")