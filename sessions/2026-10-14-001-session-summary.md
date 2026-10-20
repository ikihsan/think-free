<!-- origin-meta
owner: STATE-next-actions-sessions.md
status: active
last-verified: 2026-10-20
-->

# Session summary — 2026-10-14 (classification fresh observations)

## Session Summary — 2026-10-14

## Goal
Complete fresh observation experiments in classification domains, finish E049 Part B (lockfile registry drift), and attempt ArXiv reproducibility (E079).

## Completed Experiments

### 1. E150 — SQL Injection Technique Classification (FALSIFIED)
- **Protocol**: Predeclared kill gates with 16 synthetic fixtures (4 per category)
- **Results**: Keyword-only 81.2%, Structural 93.8% (Δ=12.5pp < 15pp gate)
- **Gates**: G1 FAIL (structural 93.8%), G2 FAIL (Δ < 15pp), G3 PASS, G4 PASS, G5 PASS
- **Finding**: Structural classifier outperforms keyword but not by required margin. Fixture keyword overlap partial (mainly `FROM`/`table`).

### 2. E160 — Medical Diagnosis Classification (FALSIFIED)
- **Protocol**: Predeclared kill gates with 17 synthetic fixtures
- **Results**: Keyword-only 94.1%, Structural 94.1% (Δ=0pp)
- **Gates**: G1 FAIL, G2 FAIL, G3 PASS, G4 PASS, G5 PASS
- **Finding**: Fixtures have mutually exclusive keyword signatures by construction — keyword matching is optimal. Structural logic redundant.

### 3. E122 — CI/CD Pipeline Failure Classification (FALSIFIED)
- **Protocol**: 140 synthetic fixtures (20 per 7 categories), KG1 threshold 80%
- **Results**: Classifier accuracy 52.1%
- **Finding**: Flaky tests confused with test failures (17/20), compile errors at 40%. Falsification criterion met.

### 4. E049 Part B — Registry-Side Drift of Pinned Requirements (FALSIFIED)
- **Protocol**: Re-resolve `requests==2.32.3`, `rich==13.9.4`, `httpx==0.28.1` one week after original snapshot
- **Results**: All 16 artifacts in transitive closure bit-identical (100% match)
- **Kill gate MET**: Bit-stable re-resolution falsifies registry-drift mechanism
- **E2 Line Status**: Fully tested — Part A shows projects rewrite lockfiles (10/11), Part B shows drift is from project edits, not registry mutation.

### 5. E079 — ArXiv Computational Reproducibility (ATTEMPTED, NOT VIABLE)
- **Results**: 0/3 install success due to implementation gaps
- **Gaps**: Import extraction fails on aliases (`import X as Y`), stdlib modules (`pickle`, `__future__`), CUDA deps (`selective_scan_cuda`), comment text
- **Witness**: Correctly predicted static analysis bound, but trial installation not robust enough

## Key Pattern Confirmed
Classification fresh observations (E147, E150, E160, E122) consistently fail due to synthetic fixture design: **clean keyword separation makes keyword matching optimal**. Structural advantage only emerges with substantial keyword ambiguity, which fixtures lack by construction. The 15pp gate correctly catches this.

## Files Modified
- `STATE-next-actions.md` — Added results for E150, E160, E122, E049 Part B, E079
- `STATE.md` — Updated experimental validation summary (6 invention claims tested)
- `EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py` — Fixed import extraction (stdlib exclusion, alias handling)
- Created `RESULT.md` for E150 and E160
- Created `RESULT-PART-B.md` for E049 Part B

## Tests Passing
- `test_doclint`: 20/20 OK
- `test_session`: 29/29 OK  
- `stage-lines`: 37/37 OK

## Next Actions
The pattern is clear: classification domains tested via synthetic fixtures with clean keyword separation will fail the 15pp structural advantage gate. Future fresh observations must either:
1. Use real-world data with natural ambiguity (not synthetic)
2. Design fixtures with deliberate keyword overlap and ambiguity
3. Accept that keyword matching may be optimal for the domain