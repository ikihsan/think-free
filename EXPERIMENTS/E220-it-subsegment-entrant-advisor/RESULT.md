# E220 Result: IT PSC Sub-Segment Entrant Advisor Prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Summary

**VERDICT: ALL GATES PASS** — The prototype successfully identifies enterable sub-segments (NAICS codes) within the three enterable federal IT PSC codes (DA01, DA10, 7A21) discovered in E209. Strong differentiation exists at the NAICS level within each PSC code.

## Data

- **PSC codes analyzed**: DA01, DA10, 7A21 (the three enterable codes from E209)
- **NAICS sub-segments per PSC**: 8 (DA01), 10 (DA10), 10 (7A21) — 28 total
- **Windows**: Current FY2023, Prior FY2018–2022
- **Identity**: `recipient_id` (100% coverage in 25/28 sub-segments, ≥98.5% in remaining 3)
- **Total recipient observations**: 8,474 current-window recipients across 28 sub-segments

## Gate Results

| Gate | Condition | Result |
|------|-----------|--------|
| **G0** | API accessible, returns NAICS breakdown for all 3 PSC codes | **PASS** (118/130/142 NAICS codes) |
| **G1** | Identity coverage ≥ 95% | **PASS** (100% in 25/28, ≥98.5% in 3/28) |
| **G2** | Prior window complete (≥5 NAICS per PSC) | **PASS** (129/145/147 NAICS codes) |
| **G3** | Sub-segment differentiation (>10pp spread in segment newcomer fraction per PSC) | **PASS** (DA01: 27.3pp, DA10: 87.2pp, 7A21: 88.0pp) |
| **G4** | Actionable output (≥3 sub-segments classified) | **PASS** (17 actionable: 7 HIGHLY, 4 SOMEWHAT, 6 MARGINAL) |

**Overall: ALL GATES PASS**

## Key Findings

### 1. Strong Sub-Segment Differentiation (G3)

The segment newcomer fraction varies dramatically within each PSC code:

| PSC | Min SegFrac | Max SegFrac | Spread | Interpretation |
|-----|-------------|-------------|--------|----------------|
| DA01 | 9.1% (511210) | 36.4% (541519) | **27.3pp** | Meaningful variation |
| DA10 | 1.5% (519130) | 88.7% (513210) | **87.2pp** | Extreme variation |
| 7A21 | 3.5% (511210) | 91.5% (513210) | **88.0pp** | Extreme variation |

The PSC-level analysis (E209) masked this variation: DA01 appeared uniformly enterable at 26.8%, but sub-segments range from 9% to 36%.

### 2. Consistently Enterable NAICS Codes Across PSC Codes

Two NAICS codes appear as **HIGHLY ENTERABLE** or **SOMEWHAT ENTERABLE** in **all three** PSC codes:

| NAICS | Name | DA01 | DA10 | 7A21 |
|-------|------|------|------|------|
| **541511** | Custom Computer Programming Services | HIGHLY (30.3%) | HIGHLY (47.8%) | SOMEWHAT (46.1%) |
| **541519** | Other Computer Related Services | HIGHLY (36.4%) | HIGHLY (34.4%) | HIGHLY (35.4%) |

These are service-oriented categories where small programs can credibly compete.

### 3. PSC-Specific Enterable Sub-Segments

| PSC | Top Sub-Segments (by enterability score) |
|-----|------------------------------------------|
| **DA01** (App Dev Labour, $60.9B) | 541519 Other Computer Related Services (36.4%, $3.24B), 541511 Custom Programming (30.3%, $2.57B), 541513 Facilities Mgmt (33.3%, $0.36B) |
| **DA10** (SaaS, $18.5B) | 541511 Custom Programming (47.8%, $0.58B), 541512 Systems Design (47.7%, $0.65B), 541519 Other Computer Related (34.4%, $2.50B) |
| **7A21** (Perpetual Licence, $13.7B) | 541519 Other Computer Related (35.4%, $2.65B), 541511 Custom Programming (46.1%, $0.14B), 541512 Systems Design (41.4%, $0.42B) |

### 4. "Software Publishers" (511210) is Consistently CLOSED

Across all three PSC codes, NAICS 511210 (Software Publishers) shows low segment newcomer fractions (3.5–9.1%) and high concentration (top-5 share 78–89%). This aligns with E209's finding that product categories (7030, D304) are closed — software publishing behaves like a product category even within service PSC codes.

### 5. Extreme Outliers: NAICS 513210 "Software Publishers (variant)"

NAICS 513210 shows extreme segment newcomer fractions (88.7% DA10, 91.5% 7A21) but tiny market sizes ($0.07B, $0.23B) and low prior-window recipient counts (68, 95). These are likely **statistical artifacts** from small denominators and/or API classification quirks. Classified as HIGHLY/SOMEWHAT ENTERABLE but should be treated with caution.

## Classification Summary

| Classification | Count | Criteria |
|----------------|-------|----------|
| **HIGHLY ENTERABLE** | 7 | SegFrac ≥30%, Frag ≥60%, ≥20 newcomers |
| **SOMEWHAT ENTERABLE** | 4 | SegFrac ≥20%, Frag ≥40%, ≥10 newcomers |
| **MARGINAL** | 6 | SegFrac ≥10%, Frag ≥20%, ≥5 newcomers |
| **CLOSED** | 11 | Below thresholds |

## Prototype Tool Assessment

The prototype demonstrates that **sub-segment analysis adds significant value over PSC-level analysis**:

1. **Actionable granularity**: A small program targeting DA01 should focus on NAICS 541519 (Other Computer Related Services) or 541511 (Custom Programming), not 511210 (Software Publishers) or 541512 (Systems Design — high obligation but low entry).

2. **Cross-PSC validation**: 541511 and 541519 are enterable across all three PSC codes, suggesting a robust pattern.

3. **Market size context**: Enterability score balances newcomer fraction, fragmentation, and obligation. The top-ranked actionable sub-segment with substantial market is **DA01/541519** ($3.24B, 36.4% newcomers, 82.3% fragmentation).

## Limitations

1. **Spending level**: Data is at `transactions` level (not `awards`), so obligation amounts may double-count.
2. **NAICS assignment**: USAspending assigns NAICS per transaction; a recipient may appear under multiple NAICS codes.
3. **Small sample artifacts**: NAICS 513210 and 336413 have very small prior windows (n<100), inflating newcomer fractions.
4. **No capability validation**: Enterability measures historical entry, not whether a specific small program *can* win.
5. **Single year current window**: FY2023 only; multi-year current window would be more robust.

## Artifacts

- `raw/naics_{CODE}_{YEAR}.json` — NAICS breakdown per PSC per window (6 files)
- `raw/recipients_{CODE}_{NAICS}_{YEAR}.json` — Recipient data per (PSC, NAICS, window) (56 files)
- `results/subsegment_metrics.csv` — Per-subsegment metrics
- `results/ranked_subsegments.csv` — Ranked by enterability score
- `results/gates.json` — Gate verdicts

## Conclusion

**The sub-segment entrant advisor prototype validates the concept.** The PSC-level "fragmented ⇒ enterable" pattern from E209 resolves into actionable NAICS-level guidance:

- **For small programs entering federal IT**: Target NAICS 541511 (Custom Computer Programming) or 541519 (Other Computer Related Services) within DA01, DA10, or 7A21.
- **Avoid**: NAICS 511210 (Software Publishers), 334111 (Computer Manufacturing), 443120 (Computer Stores) — consistently closed.
- **Caution**: Extreme newcomer fractions in tiny markets (513210) are likely artifacts.

**Next step**: This prototype could be extended to (a) all 100+ PSC codes, (b) multi-year current windows, (c) integration with SAM.gov entity data for capability matching, or (d) a UI for small business opportunity discovery. However, as a measurement experiment, it closes the question: **sub-segment differentiation is real and actionable.**

## Evidence Labels

- Gate verdicts, metrics, classifications: `observed` (computed from fetched data)
- NAICS name mappings: `source-supported` (from API responses)
- Interpretation of 513210 as artifact: `inferred` (based on small denominator)
- Prototype utility assessment: `speculative` (not tested with users)