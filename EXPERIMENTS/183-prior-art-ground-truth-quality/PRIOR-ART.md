<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E183: Prior-art check — ground-truth-quality axis

**Date:** 2026-10-18
**Question:** Do vote margin, corroboration count, and residualised prescriptive divergence carry answer-quality information beyond what known Stack Overflow quality predictors already carry?

## Prior art found

Searched three vocabularies (user's, academic, infrastructure). Web search was unavailable; used Crossref API and ACL Anthology directly.

| # | Paper | Year | Venue | What it does | Features used |
|---|---|---|---|---|---|
| 1 | Xu et al., "Preferred Answer Selection in Stack Overflow: Better Text Representations ... and Metadata, Metadata, Metadata" | 2018 | WNUT | Attention-based answer selection | Text + metadata (votes, reputation, etc.) |
| 2 | Lyu et al., "What We Vote for? Answer Selection from User Expertise View in CQA" | 2019 | WWW | Answer selection from voting signals | Vote-based + user expertise |
| 3 | Tehrani & Arjomand, "Finding The Potential Accepted Answer On Stack Overflow" | 2022 | Research Square | Predicts accepted answer | 13 text mining features from Q/A/comments |
| 4 | "Predicting best answer using sentiment analysis in CQA" | 2015 | SPIS | Best answer prediction | Sentiment + text |
| 5 | "Improving Quality of a Post's Set of Answers in Stack Overflow" | 2020 | SEAA | Answer quality improvement | Metadata + text |
| 6 | "Studying the Long-Term Value Answers on Stack Overflow" | 2022 | SSRN | Long-term answer value | Upvotes, revisions, tags |

## Findings

1. **Answer quality prediction on Stack Overflow is an established research area** with at least 6 papers using ML to predict answer quality/selection.

2. **Vote-based features are standard.** Papers #1 and #2 explicitly use vote scores and voting signals. Paper #6 uses upvotes as a quality measure.

3. **Metadata features are standard.** Paper #1's title literally emphasizes "Metadata, Metadata, Metadata" — metadata (votes, reputation, user features) is a core part of the state of the art.

4. **The three specific signals are NOT clearly present in the prior art in their specific formulation:**
   - **Vote margin** (difference between top and runner-up votes): not found as a specific feature; raw vote scores are used instead
   - **Corroboration count** (number of agreeing answers): not found in any paper
   - **Residualised prescriptive divergence** (answer disagreement after controlling for shared problem vocabulary): not found in any paper

5. **The question is empirical, not novelty.** The prior art uses raw vote scores and text similarity, but nobody has tested whether these three specific formulations add predictive power beyond what's already used.

## What this means

The prior-art-check **clears the screen**: the three signals are not already used in the prior art in their specific formulation. The next step is to test whether they add predictive power beyond a standard baseline (text + metadata features).

## Next experiment

**E184: Do the three signals add predictive power beyond standard features?**

Design:
1. Fetch ~200 Stack Overflow questions with answers and votes (Stack Exchange API)
2. Label: top-voted answer is "best" (consistent with E182)
3. Baseline: logistic regression with TF-IDF text features + standard metadata (vote count, answer count, user reputation)
4. Treatment: baseline + three signals (vote margin, corroboration count, residualised prescriptive divergence)
5. Compare: 5-fold cross-validated AUC, accuracy, F1
6. Kill gate: if treatment AUC − baseline AUC < 0.03, the signals don't add enough to be worth building

This is a small, reversible prototype. It's evidence-gathering, not product validation.
