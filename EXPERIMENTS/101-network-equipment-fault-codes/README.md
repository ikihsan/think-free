<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E101 — Fresh observation in network equipment fault codes domain

**Session:** `2026-10-11-XXX`, VM `instance-20260717-0944`, observed 2026-10-11.
**Finding:** none allocated — this experiment produced no finding record. Its
G1–G4 "ALL GATES PASS" verdict uses the view-count screen that E110 withdrew
(F116), so it is `untested` rather than a finding.

## Summary

Measured the view-count principle (independent arrivals at a need via `view_count`) on three network equipment Discourse forums:

| Forum | Topics | Need | Served | Unserved-open-like | Need % | Unserved % | View+ % |
|-------|--------|------|--------|-------------------|--------|------------|---------|
| forum.mikrotik.com | 50 | 9 | 2 | 7 | 18.0% | 14.0% | 100% |
| community.cambiumnetworks.com | 50 | 2 | 0 | 2 | 4.0% | 4.0% | 100% |
| community.f5.com | 50 | 6 | 0 | 6 | 12.0% | 12.0% | 100% |
| **Aggregate** | **150** | **17** | **2** | **15** | **11.3%** | **10.0%** | **100%** |

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** Need prevalence | ≥ 15 need statements | **PASS** (17) |
| **G2** Control validity | Corpus ≥ 100 topics | **PASS** (150) |
| **G3** Unserved fraction | < 50%, CI95 upper < 60% | **PASS** (10.0%, CI95 [5.7%, 16.5%]) |
| **G4** view_count validation | ≥ 95% view_count > 0 | **PASS** (100%) |

**All gates PASS.**

## Key Findings

1. **view_count instrument generalizes to network equipment Discourse forums**: 100% view_positive_rate matches E077's finding on 7 non-software Discourse forums (100%) and E082's finding on 3 embedded Discourse forums (100%). The arrival instrument is platform-invariant across 7 platform types.

2. **Unserved-open-like fraction is comparable**: 10.0% aggregate unserved-open-like fraction (CI95 [5.7%, 16.5%]) is statistically consistent with E077's 11.7% across 7 non-software Discourse forums and E082's 15.3% across 3 embedded Discourse forums. The "unserved ≠ unserved" pattern holds across platform types.

3. **Sufficient need prevalence**: 17 vc_positive items (11.3% of topics) exceeds G1 threshold of 15.

4. **Domain variation**: forum.mikrotik.com has higher need prevalence (18%) and unserved fraction (14%) vs community.cambiumnetworks.com (4%/4%) and community.f5.com (12%/12%), reflecting community focus differences.

5. **Other forums inaccessible**: community.cisco.com (403), community.ui.com (parse error), forums.juniper.net (404) were not accessible via Discourse `/latest.json` API. This is consistent with E077 where 3 of 10 target forums failed.

6. **No candidate produced**: This is an evidence-gathering experiment per D083 (fresh observation in new domain). The validated instrument and consistent unserved fraction refine the instrument's documented limits but do not generate a product.

## Evidence Labels

- view_positive_rate = 100%: **observed** (measured on 150 topics across 3 Discourse forums)
- need_fraction = 11.3%: **observed**
- unserved_open_like_fraction = 10.0%: **observed**
- Consistency with E077/E082 baselines: **observed** (CI95 intervals overlap)
- Platform invariance of view_count instrument: **observed** (7th platform type confirmed)

## Reproduce

```bash
python3 EXPERIMENTS/101-network-equipment-fault-codes/run.py
```

## Artifacts

- `results.json` — full per-forum and aggregate results
- `raw/*.jsonl` — raw topic data and classified topics per forum
- `PROTOCOL.md` — pre-declared protocol with results appended