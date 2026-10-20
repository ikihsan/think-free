<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E139 PROTOCOL — preflight adapter for modelscope/evalscope run output

Pre-declared 2026-10-14, before adapter was written. Commit order is the evidence.

## The question

E128 documented the modelscope/evalscope run output format (two-file: predictions + reviews, joined by `index` within task directories) and concluded "the tax is an adapter, not a library." E129 did the same for openai/evals (event stream). E130-E133 validated the adapter pattern on synthetic data for 4 serialization formats.

**This experiment**: Actually write and test the evalscope adapter against the documented format, and run all three preflight checks (C1, C2, C3) to confirm the pattern works for this two-file structure.

## Scope

- Format: modelscope/evalscope run output as documented in E128 RESULT.md
- Adapter: stdlib-only Python, ~10 lines counted schema mapping
- Checks: C1 concordance, C2 alternate-form FP, C3 control arm
- Test data: Synthetic (Python 3.8 `zoneinfo` incompatibility prevents real evalscope run)

## Declared rules

1. **Adapter tax convention**: Generic loading (read JSON, read JSONL, read CSV with header) is free. Counted lines: nested reshaping, custom serialization, schema mapping, join logic.

2. **Test cases** (declared before adapter written):
   - Clean run: no defects, all checks pass, exit 0
   - F121-style: key uses composite ID, output uses simple index → `NO_DISCRIMINATING_PAIRING`
   - Repaired key: both use composite ID → `OK`
   - F122-style: control arm contaminated with true positives → `CONTROL_NOT_EMPTY`
   - C2 alternate-form FP: flagger too strict on correct items → `ALTERNATE_FORM_FP`

3. **No real evalscope run**: Documented as limitation. The adapter is tested against the *documented format*, not live bytes.

## Gates

- **G1 adapter size**: Counted schema mapping lines ≤ 15 (E128/E129 established "a few lines" as the threshold)
- **G2 C1 detection**: F121-style defect produces `NO_DISCRIMINATING_PAIRING` or `SILENT_NO_MATCH`
- **G3 C2 detection**: Strict flagger on correct items produces `ALTERNATE_FORM_FP`
- **G4 C3 detection**: Contaminated control arm produces `CONTROL_NOT_EMPTY`
- **G5 clean run**: No-defect case produces exit 0 with all checks `OK`

## Kill gate

If G1 > 15, or G2/G3/G4 fail to detect their respective defects, or G5 fails: the adapter pattern does not hold for the evalscope two-file format, and the population coverage claim is not extended.

## Baseline

The strongest accessible alternative is the harness's own test suite for its scorer (E125 M5). E125 found this is typically `no_test` or `unprotected` for the join. Preflight adds a *per-run* measurement of the join, which the harness's static tests do not provide.

## What this does not show

- That a real evalscope run works (Python 3.8 blocker)
- That the adapter works on all evalscope benchmarks/tasks
- That anyone outside this repository would use it
- Prevalence of the defects in real evalscope runs