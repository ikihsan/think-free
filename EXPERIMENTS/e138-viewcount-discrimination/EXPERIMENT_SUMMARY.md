<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E138 — view-count discrimination on HA Discourse forum data (KILL GATE FIRED)

**Date:** 2026-10-14

**Experiment:** E138 — testing the view-count principle on the Home Assistant Discourse forum corpus
(23 topics from `raw/population_measurement_results.json`).

**Kill gate:** G1 coverage fired — 13 `served` (need-related) + 10 `unserved` (control) = 23 total,
below the ≥20 per arm threshold. Experiment marked `untested` per protocol; no further
gates evaluated.

## Raw data summary

| Metric | Value |
|---|---|
| Total topics | 23 |
| Need-related (`served`): | 13 topics, median views 509, max 2721 |
| Control (`unserved`): | 10 topics, median views 37, max 1577 |
| View counts present: | 100% (all topics have `views` field) |

## Gate results

| Gate | Status | Details |
|---|---|---|
| **G1 coverage** | **FAIL** (kill gate) | 13/10 topics per arm < required ≥20 per arm |
| **G4 arrival field** | PASS | 100% of topics have `views` metadata |
| **G2 Cliff's δ** | Not exercised | Kill gate fired first |
| **G3 effect significance** | Not exercised | Kill gate fired first |

## Key finding

The 23-topic Home Assistant Discourse corpus is **insufficient** for the view-count
measurement suite's G1 coverage gate (≥20 per arm). While view counts are available
for all topics, the sample size is too small to reliably detect an effect size (Cliff's δ)
or test for significance. This closes this corpus as a viable domain for the view-count
measurement suite without collecting additional data.

## Comparison with prior results

- E077 (non-software Stack Exchange): 20 topics, G1 met, view-count principle supported
- E082 (embedded microcontroller Discourse): 150 topics, G1 met, all gates PASS but
  unserved fraction consistent with baseline (15.3%)
- E101 (network equipment Discourse): 150 topics, G1 met, all gates PASS, unserved
  fraction 10.0% consistent with baseline
- E138 (this experiment): 23 topics, G1 FAIL — corpus too small

The pattern is clear: the view-count principle requires sufficient corpus size for
the G1 gate. Below ~20 per arm, the measurement cannot proceed. Above ~50 per arm,
the principle shows varying results across domains.

## Decision

**Experiment marked `untested`** per the kill gate. No candidate generated from this
corpus. The next action is to either (a) collect a larger corpus for this domain, or
(b) pursue a fresh observation in a new domain with sufficient scale.

---

*Raw evidence committed: `EXPERIMENTS/e138-viewcount-discrimination/run_e138.py`,
`EXPERIMENTS/e138-viewcount-discrimination/results.json` (to be written on next run),
`raw/population_measurement_results.json`, `raw/discrimination_test_results.json*.*