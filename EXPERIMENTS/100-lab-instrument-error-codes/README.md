<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E100 — Fresh observation in industrial automation/SCADA fault codes domain

**Session:** `2026-10-11-007`, VM `instance-20260717-0947`, observed 2026-10-11.
**Finding:** none allocated — this experiment produced no finding record. Its
"unserved 76.2%" figure is measured with the view-count screen that E113
withdrew (F116), so it is `untested` rather than a finding.

## Summary

Measured the view-count principle (independent arrivals at a need via `view_count`) on **forum.inductiveautomation.com** — an industrial automation/SCADA Discourse forum (Ignition SCADA platform). This is a fresh domain (industrial automation) not previously tested by the mission.

| Forum | Topics | Need | Served | Unserved-open-like | Need % | Unserved % | View+ % |
|-------|--------|------|--------|-------------------|--------|------------|---------|
| forum.inductiveautomation.com | 201 | 21 | 5 | 16 | 10.4% | 76.2% | 100% |

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** Need prevalence | ≥ 15 need statements | **PASS** (21 vc_positive) |
| **G2** Control validity | Control accuracy ≥ 0.85 | **PASS** (4/4 = 1.00) |
| **G3** Unserved fraction | < 50%, CI95 upper < 60% | **FAIL** (76.2%, CI95 [54.9%, 89.4%]) |
| **G4** view_count validation | ≥ 95% view_count > 0 | **PASS** (100%) |

## Key Findings

1. **view_count instrument generalizes to industrial automation Discourse forums**: 100% view_positive_rate matches E077's finding on non-software Discourse forums (100%) and E082's finding on embedded Discourse forums (100%). The arrival instrument is platform-invariant across 7 platform types.

2. **Classification rubric works**: 100% accuracy on seeded controls (G2) confirms the three-clause unserved-open-like rubric is operational in this domain.

3. **Sufficient need prevalence**: 21 vc_positive items (10.4% of topics) exceeds G1 threshold of 15.

4. **Unserved-open-like fraction is markedly higher**: 76.2% (CI95 [54.9%, 89.4%]) vs. E077's 11.7% (non-software Discourse) and E082's 15.3% (embedded Discourse). This suggests industrial automation fault code questions are substantially less well-served by existing code-based tools.

5. **Domain difference**: The high unserved fraction may reflect that industrial automation practitioners troubleshoot specific configuration/runtime errors (communication timeouts, driver issues, tag binding problems) rather than looking up standardized fault codes in databases. The "fault codes" here are often exception messages, error numbers, or internal codes (IGN-XXXX) rather than vendor-published standardized code tables.

6. **No candidate produced**: This is an evidence-gathering experiment per D083 (fresh observation in new domain). The validated instrument and distinct unserved fraction refine the instrument's documented limits but do not generate a product.

## Evidence Labels

- view_positive_rate = 100%: **observed** (measured on 201 topics on forum.inductiveautomation.com)
- need_fraction = 10.4%: **observed**
- unserved_open_like_fraction = 76.2%: **observed**
- Control accuracy = 100%: **observed**
- Platform invariance of view_count instrument: **observed** (7th platform type confirmed)
- Domain variation in unserved fraction: **observed** (industrial automation 76.2% vs embedded 15.3% vs non-software Discourse 11.7%)

## Reproduce

```bash
python3 EXPERIMENTS/100-lab-instrument-error-codes/harvest_ignition_fast.py
python3 EXPERIMENTS/100-lab-instrument-error-codes/classify.py
```

## Artifacts

- `results.json` — full per-forum and aggregate results
- `raw/topics.jsonl` — raw topic data
- `PROTOCOL.md` — pre-declared protocol with results appended