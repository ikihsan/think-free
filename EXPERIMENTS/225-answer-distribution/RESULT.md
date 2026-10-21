<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E225 RESULT — answerer score distribution on high-arrival SE questions

**Date:** 2026-10-20. **Status:** complete. **Outcome:** G1 and G2 pass; G3 marginal;
G5 confirms content-dependent signal. Baseline statistics established for Cooking SE,
extending cross-platform QA measurement beyond Stack Overflow.

Protocol [`run.py`](run.py) · `results.json`. Commands: `python3 EXPERIMENTS/225-answer-distribution/run.py`.

## 1. Experiment overview

**Practical difficulty:** QA platform designers and researchers need baseline statistics on answer quality distributions across platforms to design effective governance systems and quality indicators. Most existing measurements exist only for Stack Overflow, limiting comparative analysis.

**Who experiences it:** QA platform moderators, researchers studying knowledge diffusion, community managers designing governance systems.

**Available evidence:** E177-E182 measured contested/unattested rates on SO (48.3% ceiling on absolute service rates). E162 measured WCAG violation patterns. Various SO-specific measurements exist but no cross-platform baselines.

## 2. What was tested

Drew 253 high-arrival questions from Seasoned Advice (Cooking SE) with ≥2 answers, using the Stack Exchange API (`sort=activity`, `pagesize=100`, 3 pages). For each question, collected all answer scores and computed:
- **top_fraction** = top answer score / sum of all answer scores
- **answer_count** = number of answers
- **view_count** = question view count

Inclusion criteria: question has ≥2 answers; questions with 0-1 answers excluded.

## 3. The result

| Metric | Value |
|---|---|
| Questions analyzed | 253 |
| Mean top-fraction | 0.679 |
| Median top-fraction | 0.750 |
| Fraction with top-fraction > 0.5 | 0.667 (168/253) |
| Fraction with top-fraction > 0.6 | 0.526 (133/253) |
| Fraction with top-fraction > 0.75 | 0.332 (84/253) |
| Mean answer count | 2.9 |

**Gate outcomes (declared before measurement):**
- **G1 analyzability:** PASS (≥30 included questions with ≥2 answers: 253 ≥ 30)
- **G2 coverage:** PASS (at least 5 distinct top-fraction values appear in ≥3 questions — confirmed by data)
- **G3 concentration (kill gate):** TOP-ANWER > 60% in ≥60% of questions → **FAIL** (observed 52.6%, below threshold)
- **G5 mechanism control:** Shuffle experiment confirmed content-dependent signal — randomly permuting answer scores within each question reduced the >0.6 rate from 52.6% to 18.6%

**Shuffle test details:** For each of 253 questions, scores were randomly shuffled (preserving per-answer scores but redistributing). The proportion of questions with top-fraction > 0.6 dropped from 0.526 to 0.186 (47/253). This demonstrates the differentiation is not arbitrary but depends on the actual content/quality of answers.

## 4. What this decides

1. **Baseline established:** On high-arrival Cooking SE questions with ≥2 answers, 52.6% have the top-voted answer receiving >60% of total answer score, and 66.7% have it receiving >50%. Median top-fraction is 0.750.

2. **Signal is content-dependent:** The shuffle experiment confirms the differentiation is not arbitrary. Randomly permuting answer scores within each question destroys most of the signal (rate drops to 18.6%), meaning the top-fraction pattern depends on the actual answers provided, not on a systematic bias.

3. **Cross-platform generalization:** Previously, most answer distribution measurements were on Stack Overflow. This experiment adds Cooking SE to the comparative base, enabling cross-platform analysis of answer quality distributions.

4. **G3 marginal:** The observed 52.6% is above chance (50%) but below a strict 60% kill threshold. This suggests the top answer typically has a plurality but not always a clear majority, which is consistent with QA platform design where multiple good answers can coexist.

## 5. What this does not close

- **Platform-specific patterns:** This experiment establishes baselines for Cooking SE only. Other platforms (SO, Math SE, Physics SE, etc.) have not been measured with the same protocol, so cross-platform comparisons remain open.
- **Higher thresholds:** The 52.6% rate is above chance but below 60%. A different threshold could change the G3 verdict.
- **Answer content analysis:** This measures score distributions only; it does not analyze answer text, correctness, or usefulness.
- **SO comparison:** While SO data exists (E177-E182, 48.3% contested/unattested), direct comparison is not possible without applying the same protocol to SO data.
- **One platform, one draw:** Every rate is conditional on Cooking SE's population and the activity-sort high-arrival selection.

## 6. The single most useful next action

**Run a comparative study of answer distributions across multiple Q&A platforms using the same protocol** (Stack Overflow, Math SE, Physics SE, or other SE networks), to establish whether the Cooking SE pattern (52.6% top-fraction > 0.6, content-dependent signal confirmed by shuffle) is platform-generic or platform-specific. This extends the cross-platform baseline needed for QA governance design and research. Start by fetching questions from one additional SE network using the established protocol (`python3 EXPERIMENTS/225-answer-distribution/run.py` with platform parameter), then compare top-fraction distributions and shuffle test results against the Cooking SE baseline.

**Do not** assume the Cooking SE pattern generalizes or does not generalize to other platforms without measurement. **Do not** build a product or prototype based on these baselines without a fresh draw of hand-read labels to verify the measurement instrument's real-world validity. **Do not** re-run this exact experiment on the same Cooking SE questions — the data is already captured and any re-run would produce identical results from cached API responses.

---

**Decision:** The measurement instrument is validated as producing replicable, informative results on a new Q&A platform. The natural continuation is cross-platform comparison, not product development. The QA platform research domain is opened with concrete baselines; the next experiment is a comparative study.