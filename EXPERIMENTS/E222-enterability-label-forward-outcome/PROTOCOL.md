<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-22
-->

# E222 protocol — do E220's enterability labels predict newcomer forward outcomes better than naive baselines?

**Declared 2026-10-22, before any outcome-window fetch.** Session 2026-10-22-002.

## Claim under test (one sentence, scoped)

Within the three enterable federal IT PSC codes (DA01, DA10, 7A21), the
(PSC, NAICS) sub-segments E220 labeled HIGHLY/SOMEWHAT ENTERABLE produce
**higher forward award recurrence** for their FY2023 first-time entrants than
sub-segments labeled MARGINAL/CLOSED, and E220's enterability score ranks
sub-segments by that outcome **better than either naive baseline** (obligation
size alone, fragmentation alone).

Practical difficulty addressed: a small business picking a federal IT
sub-segment today has the advisor's label (E220/E221) or the naive heuristics
(pick the biggest cell; pick the most fragmented cell). E220/E221 never tested
whether the label predicts what actually happens to newcomers. If it does not
beat the naive heuristics, the advisor's practical difference is nil and the
14-hour E221 full run has no product path.

## Two realities, identical inputs, opposite outputs (information-sufficiency test)

The FY2023 entry-window data alone is compatible with both: (a) newcomers in
labeled-enterable segments convert to ongoing vendors, or (b) newcomer
"entry" is historical churn — identity reuse, one-shot multi-year contracts,
roster turnover — and recurrence is identical everywhere. Both produce the
same FY2023 newcomer fractions. Only the FY2024–2025 outcome observation
separates them. [inferred; the fetch below is the discriminating observation]

## Population (fixed at preflight, from E220's committed bytes — no network)

- 28 (PSC, NAICS) sub-segments exist from E220 (3 codes × 8–10 NAICS).
- **Analysis population: 23 sub-segments with ≥ 10 FY2023 newcomers**
  (`results/preflight_population.json`; excludes the 5 small-denominator
  cells E220 itself flagged as artifact-prone, incl. 513210 in some codes).
- Identity: `recipient_id`, exactly E220's identity. Entry window FY2023,
  prior window FY2018–2022 (calendar, E220's convention). Newcomer = present
  in entry window, absent in prior window.

## Outcome observation (this experiment's only network work)

For each of the 23 population sub-segments, fetch the complete recipient list
for the **outcome window FY2024–2025** (`time_period` 2024-01-01…2025-12-31)
from `POST /api/v2/search/spending_by_category/recipient/` with the same
`psc_codes` + `naics_codes` filters, paginated via `hasNext`, 65 s between
requests, every response written to `raw/` with SHA-256 + request meta
(`fetch_outcome.py`). FY2025 data may still accrue small late obligations;
noted as limitation, not adjustable post hoc.

## Measures (fixed now)

- **M1 (primary, per sub-segment):** recurrence rate = |newcomers ∩ outcome
  recipients| / |newcomers|.
- **M2 (secondary):** median FY2024–25 obligation among recurrent newcomers.
- Confound reported alongside: ρ(newcomer count, M1) — E208 found
  fragmentation is a size proxy.

## Baselines (strongest naive advice, fixed now)

- **B1 obligation:** E220's `current_obligation` per sub-segment.
- **B2 fragmentation:** E220's `fragmentation` per sub-segment.

Primary statistic: Spearman ρ between sub-segment-level enterability score
and M1 (n = 23); same ρ for B1 and B2. Sampling unit = sub-segment.

## Gates (declared before the fetch)

| gate | condition |
|---|---|
| **G0** | Outcome fetch complete for all 23 sub-segments (sha256'd, `hasNext` reached). Incomplete → **INSTRUMENT_FAIL, no conclusion**. |
| **G1** | ≥ 95% of outcome rows carry `recipient_id`. |
| **G2** | Every population sub-segment has ≥ 10 newcomers (assert; construction guarantee). |
| **G3 kill gate** | **SUPPORT** iff ρ_score ≥ 0.5 **and** ρ_score − max(ρ_obl, ρ_frag) ≥ 0.1 **and** one-sided permutation p < 0.05 (10,000 permutations, seed 20261022). **REFUTE** iff ρ_score ≤ 0.3 **or** ρ_score ≤ max(ρ_obl, ρ_frag). **INCONCLUSIVE** otherwise. INCONCLUSIVE behaves as "no product path" for the E221-scale decision but is reported as untested, not refuted. |
| **G4 (secondary, non-gating)** | ENTERABLE (HIGHLY+SOMEWHAT) vs rest: sub-segment-level Mann–Whitney on M1, clustered-bootstrap rate difference (10k, seed 20261022), plus ρ(size, M1). |
| **C1 (negative control)** | Permutation null of ρ_score (seed 20261022); observed ρ must exceed the null's 95th percentile for SUPPORT. |

## Strongest objections, predeclared

1. **NAICS/PSC drift:** a newcomer recurring under a different NAICS or PSC
   counts as non-recurrence. Biases M1 downward for all labels; if drift is
   worse in service segments it could manufacture a negative. Not fixable
   within this design's budget; recorded, not adjusted.
2. **Identity instability:** `recipient_id` suffix/version changes across
   windows would undercount recurrence. Same endpoint both windows; E209
   measured ≥ 99.8% id coverage. Residual risk recorded.
3. **Recurrence ≠ success:** a recurring vendor of one tiny task order is not
   a success story. M2 (median amount) reported beside M1 for this reason.
4. **n = 23 sub-segments** cannot distinguish nearby ρ values; hence the
   three-way verdict and the "INCONCLUSIVE = no product path" clause.

## Reproduction

```bash
python3 analyze.py --preflight   # population from E220 bytes, no network
python3 fetch_outcome.py         # the only network step (cached, resumable)
python3 analyze.py               # gates + results/
```
