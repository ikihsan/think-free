# Experiment 051 — Claim Contradiction Detection in Literature

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

## Claim

**E051**: Given a research question and a set of paper abstracts on that topic, a rule-based claim extractor can identify contradictory directional claims (e.g., "X increases Y" vs "X decreases Y") about specific variable relationships better than manual reading alone, with sufficient precision to be useful as a triage tool.

**Scope**: Limited to directional claims in biomedical/social science abstracts where variables and relationships are explicitly stated. Not a general NLP claim — only the narrow pattern "X [increases/decreases/has no effect on] Y".

## Kill Gate

**Primary gate**: On a test set of 30 paper pairs with human-annotated directional contradictions, the extractor must achieve:
- **Recall ≥ 60%** (≥ 18 of 30 contradictions detected)
- **Precision ≥ 80%** (≤ 20% false positive rate on detected contradictions)

**Secondary gate**: The extractor's output must be rated by a blind human reviewer as "useful for triage" on ≥ 70% of a held-out set of 10 papers, where "useful" means the highlighted contradictions match the reviewer's own judgment.

If either gate fails, the claim is abandoned. No retry with modified rules.

## Strongest Baseline

**Manual annotation by a domain-naive reader**: A person unfamiliar with the topic reads the same abstracts and marks contradictions. This baseline is executed by the experimenter (who is domain-naive for the test topics) to measure the human ceiling.

**Comparison**: The extractor's contradictions are compared against the human's contradictions on the same abstracts. The human baseline is not "perfect" — it represents what a researcher would actually do without tool support.

## Inputs

1. **Test corpus**: 30 paper pairs (60 abstracts) from PubMed Central open-access subset, selected for:
   - Same research question (e.g., "Does vitamin D supplementation reduce depression?")
   - Explicit directional claims in abstracts (increases/decreases/no effect)
   - Known contradictions from prior systematic reviews or meta-analyses

2. **Held-out corpus**: 10 additional abstracts on a different question for the usefulness rating.

3. **Synthetic fixtures**: 10 constructed abstract pairs with planted contradictions and non-contradictions to verify the extractor's logic independently of NLP quality.

All abstracts are public domain (PMC open access). Selection is documented in `selection.csv` with PMCIDs, research questions, and ground-truth labels.

## Oracle

**Ground truth**: Human annotation by the experimenter (domain-naive) of directional claims and contradictions. Each abstract is read and claims are extracted as (variable X, relationship, variable Y) triples. Contradictions are pairs of triples with opposite relationships on the same X-Y pair.

**Agreement check**: A second independent annotation on 10% of abstracts to measure inter-annotator agreement (κ). If κ < 0.6, the oracle is unreliable and the experiment is invalid.

## Extractor Design (Rule-Based, stdlib Only)

1. **Sentence segmentation**: Split abstracts into sentences (stdlib `re`).
2. **Variable candidate extraction**: Find noun phrases preceding/following relationship verbs.
3. **Relationship classification**: Match verbs/phrases to directional categories:
   - INCREASE: increase, raise, elevate, enhance, improve, augment, boost, upregulate
   - DECREASE: decrease, reduce, lower, diminish, impair, worsen, attenuate, downregulate
   - NO_EFFECT: no effect, no significant, no difference, does not affect, unchanged
4. **Triple extraction**: (subject, relationship, object) where subject and object are noun phrases.
5. **Contradiction detection**: For each X-Y pair, if both INCREASE and DECREASE (or INCREASE and NO_EFFECT, etc.) appear across abstracts, flag as contradiction.
6. **Confidence scoring**: Based on verb strength, negation scope, hedge words (may, suggest, associated with).

## Negative Controls

1. **Random pairing control**: Shuffle abstracts across research questions; contradiction rate should drop to near zero.
2. **Non-directional control**: Abstracts with only correlational language (associated with, linked to, correlated with) should yield no directional contradictions.
3. **Broken extractor control**: Run with relationship verb lists shuffled; should perform at chance level.

## Thresholds and Resource Limits

- **Runtime**: < 30 seconds for 60 abstracts on this VM (Python 3.8, 2 CPUs)
- **Memory**: < 500 MB
- **No external dependencies**: stdlib Python only (`re`, `json`, `csv`, `pathlib`, `urllib`)
- **No network calls during extraction**: All abstracts pre-fetched and stored locally.

## Reproduction Command

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/051-claim-contradiction
python3 extractor.py --input abstracts.jsonl --output contradictions.jsonl
python3 evaluate.py --predictions contradictions.jsonl --ground-truth ground_truth.jsonl --output results.json
```

## Expected Outcome

**Most likely**: The rule-based extractor will have low recall because abstracts use varied language, hedging, and indirect phrasing that simple verb matching misses. Precision may be acceptable but recall will likely fall below 60%.

**If it passes**: The mechanism is technically feasible for triage. Next step would be testing with real researchers on their own literature reviews (requires authorization).

**If it fails**: The claim is abandoned. The negative result is recorded in FAILURES.md. The domain may still have value but a different mechanism is needed.

## Epistemic Limits

- Synthetic and open-access abstracts may not represent the full language diversity of paywalled literature.
- Domain-naive annotation may miss subtle contradictions a domain expert would catch.
- A triage tool that misses 40% of contradictions may be worse than useless (false confidence).
- This experiment tests technical feasibility only, not adoption or usefulness in practice.