# E078 — Need-Classification Prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Prototype experiment testing whether the need-classification and served-fraction
measurement framework from E077 generalizes to a new online community dataset.

## Quick test

```bash
python3 run.py --dataset data/sample_threads.jsonl --n 30
```

## Expected output

The script produces `results.json` with gate outcomes and a served-fraction
estimate. All four gates must pass for the framework to be considered generalizable
to the new dataset.

## Gates

| Gate | Criterion | Detail |
|---|---|---|
| G1 | Classification validity | Single-rater, well-defined rules |
| G2 | Need prevalence | ≥5% of sampled threads are need topics |
| G3 | Served fraction measurable | Wilson CI95 upper bound < 70% |
| G4 | Cross-platform signal | ≥2 of 3 sampled threads have tool-named replies |

## Design rationale

This experiment extends E077's framework from Discourse forums to a new dataset,
testing whether the same classification rules and served-fraction rubric produce
consistent results across different online communities. The 70% Wilson upper bound
gate allows the classification to be useful even when the served fraction is moderate,
while still flagging datasets where the classification may be broken.

## Results

Results are written to `results.json` and include:
- `need_fraction`: proportion of threads classified as needing a tool
- `unserved_fraction`: proportion classified as unserved-open-like
- `wilson_ci95_upper`: Wilson upper bound for the unserved fraction
- Per-gate pass/fail status
- `all_gates_pass`: whether every gate passed