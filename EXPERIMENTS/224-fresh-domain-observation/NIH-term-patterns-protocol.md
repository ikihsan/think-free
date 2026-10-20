<!-- origin-meta
owner: EXPERIMENTS/224-fresh-domain-observation/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E224 PROTOCOL — Term pattern analysis across NIH research project activity codes

Declared 2026-10-20, session `2026-10-20-002`, before any API requests are made.
Seed **224**. Nothing below may be changed after `fetch.py` runs; any change is
an amendment with its own heading and reason, recorded before the run it affects.

## 1. Why this exists

E223 established that PSC code systematically shapes award description term
language in federal contracting. E224 divides into a fresh observation: instead
of federal contract awards, we analyze the *text* of NIH research project
abstracts — a data source already fetched in the course of earlier experiments
but never systematically analyzed for cross-activity-code patterns. Understanding
whether NIH activity code systematically shapes project abstract terminology is a
prerequisite for any natural-language–based classification of research funding.

## 2. The claim, in one sentence

NIH activity code account for systematic differences in research project
abstract term frequency distributions — specifically, the dominant terminology
differs between codes representing different types of funding (e.g., fellowships
vs. regular research) after controlling for award volume and ICD (Institute/Center)
group.

Scope: **mechanism and pattern only.** Not human usefulness, not adoption,
not novelty. The kill gate is the only build decision this experiment can change.

## 3. Data — NIH project abstracts from NIH RePORTER

| Parameter | Value |
|---|---|
| **Activity codes** | `F32` (Predoctoral Fellowship), `K01` (Career Development), `R01` (Research Project), `R03` (Small Research Grant), `U01` (Cooperative Agreement) |
| **Award amount range** | $100,000–$1,000,000 (typical NIH grant range) |
| **Per-request fields** | `Abstract Text`, `Project Title`, `Activity Code`, `IC Name`, `Funding Amount` |
| **Per-page limit** | 100 (max per NIH API per request) |
| **ICs (Institute/Centers)** | NIDDK, NCI, NHLBI, NINDS, NIGMS, NICHD, etc. |

## 4. Arms, metric, sampling

| Arm | Prediction |
|---|---|
| **B0 `baseline`** | word frequencies follow a Zipf–Mandelbrot distribution; a few high-frequency terms dominate |
| **B1 `code_effect`** | NIH activity code is a significant predictor of word frequency distribution, after controlling for award volume and ICD |
| **B2 `funded_fraction_effect`** | funded amount (≥$100K per award) is a significant predictor of word frequency distribution |
| **Bshuf** | B0 with abstracts shuffled within each activity code (mechanism control: if the pattern is code-specific, shuffling should not produce the same dominant terms) |

Per request: record `abstract_text`, `project_title`, `activity_code`, `ic_name`, `funding_amount`.

Per experiment: record the full sequence of per-activity-code term frequencies, dominant terms, and gate outcomes.

## 5. Gates — all evaluated on the COLLECTED DATA, declared before the fetch

| Gate | Declared question | Threshold |
|---|---|---|
| **G1** analyzability | is the description sequence long enough to measure term frequencies? | ≥ **50** total descriptions across all codes, with ≥ **10** descriptions per code |
| **G2** coverage | did we observe term diversity? | at least **5** distinct terms appear in ≥ **3** different codes |
| **G3** code differentiation *(kill gate)* | does the word frequency distribution differ significantly between activity codes? | Kruskal–Wallis H test, p < 0.05 across the activity codes |
| **G4** funded_fraction differentiation | do codes with funded amount ≥ $500K have different term patterns than codes with funded amount ≤ $300K? | Mann–Whitney U test, p < 0.05 (two-group comparison) |
| **G5** mechanism control | after shuffling abstracts within each activity code, does the code-differentiation signal disappear? | after shuffling, Kruskal–Wallis p ≥ 0.05 (signal is content-dependent, not arbitrary) |

**Kill gate.** G3 failing ⇒ **the claim that activity code systematically shapes abstract term language closes**: term patterns do not reliably differ across activity codes, and the claim of activity-code–specific terminology is not supported. G3 passing while G4 fails ⇒ activity codes differentiate term patterns, but the funded-fraction split is not supported; the finding is that activity code matters but funded-fraction split does not. G3 passing while G4 passes ⇒ full pattern differentiation: activity code and funded fraction both carry systematic information in project language.

**Arithmetic control.** If description word counts cannot be reliably compared across codes (e.g., different average lengths), the verdict is `invalid_instrument`.

**Kill gate (alternative).** G3 failing on the successful-description count but passing on the total-attempts count ⇒ the term patterns are too sparse to support the claim, and the claim that "activity code shapes description language" is not supported.

**Secondary, reported not gated:** per-code dominant term lists; per-IC term distributions; the exact Kruskal–Wallis H statistic and Mann–Whitney U statistic; the per-code word count median and mean.

**Resource limits:** ≤ 200 NIH API requests total (20 per activity code × 5 codes, with 10-page walk per code if needed); analysis ≤ 600 s; no credentials.

## 6. What this decides

If G3 passes and G4 passes: NIH activity codes show systematic term pattern differentiation in project abstracts, and funded fraction modulates the pattern — the claim is supported. If G3 passes and G4 fails: activity codes differentiate term patterns, but the funded-fraction split is not supported; the finding is that activity code matters but funded-fraction split does not. If G3 fails: the term patterns are too sparse to support the claim that "activity code shapes description language," and the claim closes.

**Next action.** The mechanism and pattern are recorded. If the claim is supported, follow-up work can explore which specific terms differentiate which activity codes and what this means for cross-code classification of research funding. If the claim is not supported, the project's knowledge of domain-specific terminology patterns expands with a null result.

---

*This protocol is independent of any candidate selection. It is a measurement experiment only.*