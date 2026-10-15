"""Test preflight's C1 detection of the real F121 defect (genuinely different key values)."""

import sys
sys.path.insert(0, 'EXPERIMENTS/124-eval-harness-preflight')
sys.path.insert(0, 'EXPERIMENTS/139-evalscope-preflight-test')

from preflight import concordance, render
from evalscope_adapter import adapt_evalscope

# Load the evalscope run output
key_rows, out_rows = adapt_evalscope(
    'EXPERIMENTS/139-evalscope-preflight-test/predictions_dir',
    'EXPERIMENTS/139-evalscope-preflight-test/reviews_dir'
)

print("=== Test: Real F121 defect - key uses composite ID, output uses simple index ===")
# Simulate F121: key has composite IDs like "qwen-7b-000", "qwen-7b-001"
# but output has simple index like 0, 1, 2
key_rows_f121 = [{"task": kr["task"], "composite_id": f"{kr['task']}-{kr['index']:03d}"} for kr in key_rows]
out_rows_f121 = [{"task": or_["task"], "index": or_["index"]} for or_ in out_rows]

c1 = concordance(key_rows_f121, out_rows_f121)
print(f"  verdict: {c1['verdict']}")
print(f"  best_rate: {c1['best_rate']}")
print(f"  key_rows: {c1['key_rows']}")
print(f"  output_rows: {c1['output_rows']}")
print(f"  type_conflicts: {c1['type_conflicts']}")
print(f"  pairings: {c1['pairings']}")
print(f"  reason: {c1['reason']}")

# Combined report
print("\n=== Combined Report ===")
checks = [c1]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"Exit code: {code}")

# Now test with the correct composite key (like E116's score.py repair)
print("\n=== Test: Repaired key (composite ID matches output composite ID) ===")
out_rows_repaired = [{"task": or_["task"], "composite_id": f"{or_['task']}-{or_['index']:03d}", "score": or_.get("score"), "target": or_.get("target")} for or_ in out_rows]

c1_repaired = concordance(key_rows_f121, out_rows_repaired)
print(f"  verdict: {c1_repaired['verdict']}")
print(f"  best_rate: {c1_repaired['best_rate']}")
print(f"  pairings: {c1_repaired['pairings']}")

checks = [c1_repaired]
text, code = render(checks, rate="0.75", label="accuracy")
print(text)
print(f"Exit code: {code}")