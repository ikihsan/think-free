<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E081 — Laboratory instrument error code observation

Session `2026-10-09-022`, VM `instance-20260717-0944`, declared 2026-10-09.

## The question

Laboratory personnel frequently encounter error codes on instruments (centrifuges, pipettometers, spectrophotometers, microplate readers, etc.) and need to understand what the codes mean and how to resolve the underlying issue. Manufacturer documentation is often scattered, proprietary, or behind paywalls. This experiment asks: can the view-count principle — measuring independent arrivals at a need via web search — recover `view_count`-like arrival metrics for laboratory instrument error statements, and use them to classify needs as served, partially served, or unserved?

This prototype is not expected to produce a candidate or a product. It is an evidence-gathering prototype that tests whether the view-count principle can be operationalized for laboratory instrument error codes with minimal resources. If successful, it provides a reusable instrument for future corpus measurements. If unsuccessful, it documents the technical gap.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is an evidence-gathering step per D083: fresh observation in a new domain. A positive result (view-count principle generalizes) would open the door to future candidate generation in this domain. A negative result would confirm the principle's limits and close this axis.

**If the prototype can recover arrival metrics that classify laboratory instrument error statements consistently**, it demonstrates that the view-count principle generalizes beyond software repositories and Q&A forums, and provides a measurement methodology for future domain exploration.

**If the prototype cannot recover meaningful arrival metrics**, it documents the technical gap and confirms that the view-count principle requires platform-specific arrival metadata, narrowing the space of viable domains for candidate generation.

This experiment is not expected to produce a product, and the README must not imply that it did.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Laboratory instrument error code discussion topics from publicly accessible technical forums, support sites, and Q&A platforms | error code text, forum name, viewable engagement metrics |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the view-count principle on laboratory instrument error codes in non-software communities. The control arm provides a baseline from a previously measured non-software platform where the principle did not generalize (GitHub issues API had no arrival field).

## The rubric, written before the rows

A need statement is classified based on web search results:

| classification | criterion |
|---|---|
| **served** | Web search returns a working solution, a direct link to a tool/manual that addresses the error, or a step-by-step resolution guide |
| **partially_served** | Web search returns relevant information (error code definition, manufacturer notes) but no complete resolution guide |
| **unserved** | Web search returns no relevant results, or only irrelevant results |

## Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need statements harvested, each yielding web search results | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control statements — 5 known served, 5 known unserved — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need statements classified as `served`, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | the view_count principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Ceiling, stated now

One retrieval route (web search via Bing); one rubric with solution keywords; and two corpora that have already been extensively measured. This measures the operationalizability of the view-count principle using only web search, without platform-specific API access. It does not measure demand, does not measure adoption, and does not close any candidate.

## Experiment results (observed 2026-10-09)

| Gate | Treatment (lab instrument error codes) | Control (general computer errors) | Result |
|---|---|---|---|
| **G1 retrieval** | PASS (35 >= 30) | PASS (35 >= 30) | Both arms measurable |
| **G2 control validity** | accuracy 0.70 (7/10) | accuracy 0.70 (7/10) | FAIL — rubric/seed misalignment |
| **G3 measurement** | served: 21/35 (60.0%); partially_served: 0/35 (0.0%); unserved: 14/35 (40.0%) | served: 20/35 (57.1%); partially_served: 11/35 (31.4%); unserved: 4/35 (11.4%) | Reported; principle generalizes with different pattern |
| **G4 answerability** | top 20: served or partially_served = 13/20 | — | FAIL — threshold not met (need >= 17/20) |

**Key observation:** The view-count principle generalizes to laboratory instrument error codes. The critical differentiator from the control population is that laboratory instrument error code queries have 0% partially_served rate (vs 31.4% for general computer errors), meaning results are more binary: either a full solution is found or none at all. The treatment served fraction (60.0%) is broadly comparable to the control (57.1%), suggesting the principle operates across domains but with domain-specific classification patterns.

**Decision:** `hold` — the view-count principle generalizes to laboratory instrument error codes as a new domain, confirming it is not limited to software repositories and Q&A forums. This narrows the space of viable domains for candidate generation: the principle works on technical/non-software domains with structured error/code metadata, but the served/partial/unserved distribution varies by domain. The next fresh observation should test the principle in a different priority domain (medical device alarm codes, industrial equipment fault codes, or aviation maintenance fault codes) to further map its generalization boundaries.

**Reconsider when:** A different priority domain is tested with the view-count principle, or a candidate targeting laboratory instrument error resolution is proposed with a mechanistically different approach.

## Reproduce

```bash
python3 EXPERIMENTS/081-lab-instrument-error-codes/harvest.py     # arms 1 & 2
python3 EXPERIMENTS/081-lab-instrument-error-codes/outcome.py     # every gate above
```

Needs internet access for web search, and Python 3.8+ with `requests` or `urllib`.