<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E223 PROTOCOL — Award description term patterns across PSC codes

Declared 2026-10-20, session `2026-10-20-012`, before any API requests are made.
Seed **223**. Nothing below may be changed after `fetch.py` runs; any change is
an amendment with its own heading and reason, recorded before the run it affects.

## 1. Why this exists

E196 established the code-addressed shape of federal contract money, and E197
revealed that median funded fraction varies across codes (0.9667–0.9898). E223
divides into a fresh observation: instead of counting awards or reading
recipients, we analyze the *text* of award descriptions — a data source already
fetched in the course of earlier experiments but never systematically analyzed
for cross-code patterns. Understanding whether award language systematically
varies by code is a prerequisite for any natural-language–based classification
of federal spending.

## 2. The claim, in one sentence

PSC code account for systematic differences in award description term
frequency distributions — specifically, the dominant terminology differs
between codes whose awards tend to carry money (high funded fraction) and
codes whose awards often carry no money (low funded fraction), after controlling
for code type and award volume.

Scope: **mechanism and pattern only.** Not human usefulness, not adoption,
not novelty. The kill gate is the only build decision this experiment can change.

## 3. Data — award descriptions from USAspending.gov

| Parameter | Value |
|---|---|
| **PSC codes** | `DA01`, `DA10`, `7A21`, `7030`, `D304` (the five IT/software codes from E196) |
| **Award amount range** | $1–$100,000 (same as E197/E215/E216) |
| **Award type codes** | A, B, C, D |
| **Per-request fields** | `Description`, `Award ID`, `Award Amount`, `Awarding Agency` |
| **Per-page limit** | 100 (max per USAspending API) |

## 4. Arms, metric, sampling

| Arm | Prediction |
|---|---|
| **B0** `baseline` | word frequencies follow a Zipf–Mandelbrot distribution; a few high-frequency terms dominate |
| **B1** `code_effect` | PSC code is a significant predictor of word frequency distribution, after controlling for award volume |
| **B2` `funded_fraction_effect` | funded fraction (≥$1 per award) is a significant predictor of word frequency distribution |
| **Bshuf** | B0 with descriptions shuffled within a code (mechanism control: if the pattern is code-specific, shuffling should not produce the same dominant terms) |

Per request: record `description_word_count`, `description word list` (cleaned), `awarding agency`.

Per experiment: record the full sequence of per-code word frequencies, dominant terms, and gate outcomes.

## 5. Gates — all evaluated on the COLLECTED DATA, declared before the fetch

| Gate | Declared question | Threshold |
|---|---|---|
| **G1** analyzability | is the description sequence long enough to measure term frequencies? | ≥ **50** total descriptions across all codes, with ≥ **10** descriptions per code |
| **G2** coverage | did we observe term diversity? | at least **5** distinct terms appear in ≥ **3** different codes |
| **G3** code differentiation *(kill gate)* | does the word frequency distribution differ significantly between codes? | Kruskal–Wallis H test, p < 0.05 across the 5 codes |
| **G4** funded_fraction differentiation | do codes with funded fraction ≥ 0.98 have different term patterns than codes with funded fraction ≤ 0.97? | Mann–Whitney U test, p < 0.05 (two-group comparison) |
| **G5** mechanism control | after shuffling descriptions within each code, does the code-differentiation signal disappear? | after shuffling, Kruskal–Wallis p ≥ 0.05 (signal is content-dependent, not arbitrary) |

**Kill gate.** G3 failing ⇒ **the claim that code systematically shapes description language closes**: term patterns do not reliably differ across PSC codes, and the claim of code-specific terminology is not supported. G3 passing while G4 fails ⇒ code differentiates term patterns, but the funded-fraction split is not supported; the finding is that code matters but funded-fraction split does not. G3 passing while G4 passes ⇒ full pattern differentiation: code and funded fraction both carry systematic information in award language.

**Arithmetic control.** If description word counts cannot be reliably compared across codes (e.g., different average lengths), the verdict is `invalid_instrument`.

**Kill gate (alternative).** G3 failing on the successful-description count but passing on the total-attempts count ⇒ the term patterns are too sparse to support the claim, and the claim that "code shapes description language" is not supported.

**Secondary, reported not gated:** per-code dominant term lists; per-agency term distributions; the exact Kruskal–Wallis H statistic and Mann–Whitney U statistic; the per-code word count median and mean.

**Resource limits:** ≤ 200 USAspending API requests total (20 per code × 5 codes, with 10-page walk per code if needed); analysis ≤ 600 s; no credentials.

## 6. What this decides

If G3 passes and G4 passes: the GitHub unauthenticated Search API rate limits to ≤30 successful requests per 60-minute window, and the limit resets after W seconds (measured). This is a basic infrastructural fact that enables systematic GitHub data mining.

If G3 passes and G4 fails: the rate limit exists (≤30 successful requests) but does not reset after a waiting period (or resets after an unusually long wait). The finding is that the rate limit is a hard ceiling that does not self-reset.

If G3 fails: the rate limit is more generous than 30 successful requests per window, and the claim that "the rate limit is a practical constraint on systematic mining" closes.

**Next action.** The rate-limit characterization is recorded. If the rate limit is ≤30 requests per window, follow-up work can plan systematic mining within that budget. If the rate limit is more generous, the constraint is less binding than expected.

---

*This protocol is independent of any candidate selection. It is a measurement experiment only.*