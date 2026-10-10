<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E082 — Fresh observation in embedded/microcontroller fault codes domain

**Session:** `2026-10-10-009`, VM `instance-20260717-0944`, observed 2026-10-10.
**Finding:** F112, Decision: D101 (pending allocation)

## Summary

Measured the view-count principle (independent arrivals at a need via `view_count`) on three embedded/microcontroller Discourse forums:

| Forum | Topics | Need | Served | Unserved-open-like | Need % | Unserved % | View+ % |
|-------|--------|------|--------|-------------------|--------|------------|---------|
| discuss.ardupilot.org | 50 | 4 | 1 | 3 | 8.0% | 6.0% | 100% |
| community.platformio.org | 50 | 19 | 12 | 7 | 38.0% | 14.0% | 100% |
| forum.arduino.cc | 50 | 17 | 4 | 13 | 34.0% | 26.0% | 100% |
| **Aggregate** | **150** | **40** | **17** | **23** | **26.7%** | **15.3%** | **100%** |

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** Need prevalence | ≥ 15 need statements | **PASS** (40) |
| **G2** Control validity | Corpus ≥ 10 items | **PASS** (150) |
| **G3** Unserved fraction | < 50%, CI95 upper < 60% | **PASS** (15.3%, CI95 upper 21.3%) |
| **G4** view_count validation | ≥ 95% view_count > 0 | **PASS** (100%) |

**All gates PASS.**

## Key Findings

1. **view_count instrument generalizes**: 100% view_positive_rate on embedded Discourse forums, matching E077's finding on 7 non-software Discourse forums. The arrival instrument is platform-invariant.

2. **Unserved-open-like fraction is comparable**: 15.3% aggregate unserved-open-like fraction (CI95 [10.5%, 21.3%]) is statistically consistent with E077's 11.7% across 7 non-software Discourse forums. The "unserved ≠ unserved" pattern holds across platform types.

3. **Domain variation**: discuss.ardupilot.org has lower need prevalence (8%) and unserved fraction (6%) vs. community.platformio.org (38%/14%) and forum.arduino.cc (34%/26%), reflecting community focus differences.

4. **No candidate produced**: This is an evidence-gathering experiment per D083 (fresh observation in new domain). The validated instrument and comparable unserved fraction refine the instrument's documented limits but do not generate a product.

## Evidence Labels

- view_positive_rate = 100%: **observed** (measured on 150 topics across 3 Discourse forums)
- need_fraction = 26.7%: **observed**
- unserved_open_like_fraction = 15.3%: **observed**
- Consistency with E077 baseline: **observed** (CI95 intervals overlap)
- Platform invariance of view_count instrument: **observed**

## Reproduce

```bash
python3 EXPERIMENTS/082-embedded-fault-codes/run_e082.py
```

## Artifacts

- `results.json` — full per-forum and aggregate results
- `raw/*.jsonl` — raw topic data and classified topics per forum
- `PROTOCOL.md` — pre-declared protocol with results appended