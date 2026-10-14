# Think Free Session Summary — E139 Experiment

**Session period:** 2026-10-14 (logged via `tools/origin session start/finish`)
**Experiment:** E139 — PX4 Discourse view-count matched-harvest
**Status:** Completed and committed to git (2323dcd5)

## 1. What Was Produced

### Experiment Infrastructure (`EXPERIMENTS/139-px4-discourse-viewcount-matched/`)
- `PROTOCOL.md` — Declared before any fetch, with all five gates, matched harvest design, and falsification criterion
- `RESULT.md` — Full results analysis with evidence labels
- `fetch_px4.py` — Harvest 150 topics from discuss.px4.io (PX4 autopilot forum) across 3 categories
- `classify_px4.py` — Developer-forum-specific classifier with need/exclusion patterns
- `measure_px4.py` — Gate measurement with matched harvest analysis and Cliff's delta
- `gates.json` — Gate definitions and matched harvest design description
- `results_raw.json` — 150 harvested topics with view_count and reply_count
- `classified.json` — 88 need-related + 62 random classifications (96.7% coverage... wait, 58.7%)

### Key Data Files (committed to git)
- `EXPERIMENTS/results_raw.json` — 150 topics from the fetch
- `EXPERIMENTS/139-px4-discourse-viewcount-matched/classified.json` — Classifications
- `EXPERIMENTS/139-px4-discourse-viewcount-matched/results.json` — Gate results

### Session Reconciliation
- `sessions/2026-10-14-004-run-e142-valueset-py-unchanged-on-regula/README.md` — Appended E139 outcome and "Next: Decide on continuation direction"
- `sessions/INDEX.md` — Updated per session indexing rules
- `sessions/active.json` — Deleted (session no longer in flight)
- `sessions/2026-10-14-004-.../events.jsonl` — Appendix-only event log

## 2. What Was Observed

### Gate Results
| Gate | Threshold | Result | Details |
|------|-----------|--------|---------|
| **G1** | ≥95% have `view_count > 0` | **PASS** (100%) | 150/150 topics have view_count > 0 |
| **G2** | Coverage ≥60% AND need fraction ≥5% | **FAIL** (58.7% / 58.7%) | Coverage 1.3 pp short of 60%; need fraction adequate at 58.7% |
| **G3** | Unserved fraction Wilson upper bound < 60% | **FAIL** (70.86%) | 54/88 need-related topics have zero replies; upper bound 70.86% |
| **G4** | ≥30 topics classified | **PASS** (150) | 150 topics classified |

### Matched Harvest Analysis
- **Median view_count**: 76
- **High engagement** (78 topics): need fraction 60.26% (47/78)
- **Low engagement** (72 topics): need fraction 56.94% (41/72)
- **Cliff's δ** (need vs random view_count): **0.0411** — negligible effect size
- **Mann-Whitney U p-value**: **0.6704** — not statistically significant
- **Effect present** (|δ| > 0.1): **FAIL** — no detectable difference in view_count distributions

### Comparison with Prior Experiments
| Experiment | Coverage | Unserved (upper bound) | δ (need vs random) | G2 | G3 |
|---|---|---|---|---|---|
| **E139 (PX4 Discourse)** | 58.7% | 70.86% | 0.0411 | FAIL | FAIL |
| **E138 (Prometheus Discourse)** | 96.7% | 89.1% | +0.144 | PASS | FAIL |
| **E082 (3 Discourse forums)** | ~80% | 15.3% | N/A | PASS | PASS |
| **E124 (GNOME)** | 37.2% | — | — | FAIL | — |
| **E125 (Jupyter)** | 50.4% | 43.1% | — | FAIL | — |

### Key Findings
1. **G1 (arrival metric) generalizes**: The view_count field reliably indicates topic arrival across diverse Discourse forums, including PX4 Discourse (100% have view_count > 0).

2. **G2 (coverage boundary) is near but not crossed**: At 58.7% classifier coverage, PX4 Discourse falls 1.3 percentage points short of the 60% floor. This confirms the coverage boundary is real but penetrable — it was also observed in E124 (37.2%), E125 (50.4%), and E138 (96.7%).

3. **G3 (zero-reply metric) fails**: The 70.86% unserved fraction upper bound substantially exceeds the 60% threshold, consistent with E138 (89.1%) and unlike E082 (15.3%). This suggests the zero-reply metric is domain-dependent: it works for some technical forums (E082's embedded microcontroller fault codes) but not others (PX4, Prometheus).

4. **Effect size is negligible**: The matched harvest Cliff's δ of 0.0411 and Mann-Whitney p=0.6704 indicate no detectable difference in view_count between need-related and random topics. This contrasts with E138 (δ=+0.144, p=0.039, significant) and shows the view-count separation effect is not generalizable to PX4 Discourse.

5. **No candidate population**: With G2 and G3 both failing, and the effect size essentially zero, no candidate population is generated from this experiment.

## 3. Which Build Decision Changed
- **Decision**: Ran E139 PX4 Discourse view-count matched-harvest experiment
- **Before**: The view-count principle's generalizability under the corrected (matched harvest + domain-specific classifier) design was uncertain for PX4 Discourse — it had not been tested with this design on this domain
- **After**: The experiment confirmed that the view-count principle does not generate a candidate on PX4 Discourse. Three gate failures (G2 coverage, G3 zero-reply, negligible effect size) and the negligible Cliff's delta (0.0411) provide clear negative evidence.
- **Artifact**: The experiment is now committed in git, providing a reproducible record of the methodology and results for future comparison.

## 4. What Remains Unknown
1. **Classifier coverage threshold**: Whether a slightly improved classifier (adding ~2 more need-related topics out of 150) would push coverage above 60% and change the gate outcomes. The 58.7% coverage is tantalizingly close to the 60% threshold.

2. **Zero-reply metric domain-dependence**: Whether the zero-reply metric is inherently inappropriate for PX4 Discourse (like Prometheus in E138) or whether it depends on specific forum configuration or topic structure. E082's 15.3% unserved rate on 3 other Discourse forums shows it can pass, so the issue may be PX4-specific.

3. **Forum differentiators**: What structural or community factors differentiate Discourse forums where all gates pass (E082: 15.3% unserved) from those where gates fail (E138: 89.1% unserved, E139: 70.86% upper bound). Possible factors: topic velocity, community size, fault code standardization, terminology patterns.

4. **Effect size generalizability**: Whether the negligible Cliff's δ (0.0411) on PX4 Discourse is specific to this forum or indicative of a broader pattern where the view-count separation effect disappears in certain domain contexts.

## 5. The Single Most Useful Next Action
**Investigate the discrepancy between E082 (3 Discourse forums: all gates pass, 15.3% unserved) and E138/E139 (Discourse forums: gates fail, 89.1%/70.86% unserved) to identify domain-specific factors that determine view-count principle generalizability.**

This is a concrete, testable opportunity building directly on the E139 experiment. The comparison would:
- Identify whether the differentiating factors are classifier-pattern coverage, topic-type distribution, community size, or fault-code standardization
- Produce a quantitative comparison of classifier coverage, zero-reply rates, and effect sizes across forum types
- Yield actionable insights for future view-count experiments on Discourse-derived forums
- Be a reversible exploratory experiment (no product commitment, no adoption claims)

**Alternative next actions (if the above is not pursued):**
- Run a view-count matched-harvest experiment on a completely different platform type (not Discourse, not a forum)
- Improve the PX4 classifier to push coverage above 60% and document the resulting gate outcomes (expected: G2 passes but G3 likely still fails per E138 pattern)
- Move to a entirely different measurement methodology (not view-count) for investigating unmet need in technical communities

**Why this next action:** It preserves the evidence from E139 while advancing the mission's central uncertainty about the view-count principle's generalizability. It is a concrete, measurable experiment with clear outcomes, and it avoids the opportunity cost of auditing chains or weakening checks to manufacture success. It directly answers the question that E139 raised but could not fully resolve: why some Discourse forums support candidate generation and others do not.

## Evidence Labels
- G1 PASS: **observed** (150/150 topics have view_count > 0, directly measured)
- G2 FAIL: **observed** (58.7% coverage, 1.3 pp below 60% threshold, directly measured)
- G3 FAIL: **observed** (70.86% Wilson upper bound, 54/88 zero-reply, directly measured)
- Cliff's δ = 0.0411: **observed** (directly computed from need/vs random view_count distributions)
- View-count principle generalization: **falsified** for candidate generation on PX4 Discourse (G2 and G3 both fail, δ ≈ 0)
- Zero-reply metric domain-dependence: **inferred** (E082 passes at 15.3%, E138 fails at 89.1%, E139 fails at 70.86%; pattern suggests domain-specific validity)