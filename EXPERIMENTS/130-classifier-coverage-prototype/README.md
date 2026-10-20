# E130 — Classifier coverage prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

## Quick test

```bash
python3 run.py \
  --need-titles "how do I install numpy","what is the best python package for data analysis" \
  --random-titles "how to format code","where is the best place to eat" \
  --view-counts '{"how do I install numpy": 1500,"what is the best python package for data analysis": 1200,"how to format code": 800,"where is the best place to eat": 600}' \
  --output results.json
```

## Expected output

The script produces `results.json` with gate outcomes and a coverage measurement.
All four gates must pass for the classifier to satisfy D083 reopening condition #1.

## Gates

| Gate | Criterion | Pass condition |
|---|---|---|
| G1 | Classification validity | Single-rater, well-defined rules (satisfied by design) |
| G2 | Need prevalence | ≥5% of sampled threads are need topics |
| G3 | Coverage floor | Classified fraction ≥ 60% of pool (declared floor) |
| G4 | Cross-platform signal | ≥2 of 3 sampled need threads classified as need |

## Design rationale

This experiment tests D083 reopening condition #1: "A classifier that covers its
population." The previous classifier (E078, used across the view-count domain sweep)
labelled only ~28% of a 700-row representative pool, with 458 of 700 rows matching
neither vocabulary due to unanchored substring matching (`ai` in `email`, `base` in
`database`). This coverage floor experiment uses word-boundary anchored patterns to
avoid substring collisions and achieve higher classification coverage.

If the 60% coverage floor is met, conditions #2 and #3 (declared coverage gate +
matched harvest design) can justify reopening the view-count line. If not, the
coverage constraint is confirmed and a different fresh observation is needed.

## Results

Results are written to `results.json` and include:
- `classified`: count of need / non-need / undetermined
- `coverage_rate`: fraction of pool classified
- `meets_coverage_floor`: whether coverage ≥ 60% floor
- Per-gate pass/fail status
- `all_gates_pass`: whether every gate passed
- `meets_reopening_condition_1`: D083 condition #1 status