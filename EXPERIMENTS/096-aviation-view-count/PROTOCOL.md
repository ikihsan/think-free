<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E096 — Aviation maintenance fault code view-count measurement

Session `2026-10-11`, VM `instance-20260717-0944`, declared 2026-10-11.

## The question

Aviation maintenance personnel frequently encounter fault codes on aircraft maintenance systems, ground support equipment, and avionics. Understanding these codes is critical for flight safety, but manufacturer documentation is often proprietary, technical, and scattered across different aircraft types and systems. This experiment asks: can the view-count principle — measuring independent arrivals at a need via `view_count` metadata — recover `view_count`-like arrival metrics for aviation maintenance fault code statements, and use them to classify needs as served, partially served, or unserved?

This prototype is not expected to produce a candidate or a product. It is an evidence-gathering prototype that tests whether the view-count principle can be operationalized for aviation maintenance fault codes using the platform's native `view_count` metadata, avoiding the keyword-classifier approach that failed in E083.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is an evidence-gathering step per D083: fresh observation in a new domain. A positive result (view-count principle generalizes with platform metadata) would open the door to future candidate generation in this domain. A negative result would confirm the principle's limits for this type of platform and close this axis.

**If the prototype can recover arrival metrics that classify aviation maintenance fault code statements consistently using the platform's `view_count` metadata**, it demonstrates that the view-count principle generalizes beyond software repositories and Q&A forums with explicit view counts, and provides a measurement methodology for future domain exploration using platform APIs.

**If the prototype cannot recover meaningful arrival metrics**, it documents the technical gap and confirms that the view-count principle requires platform-specific arrival metadata, narrowing the space of viable domains for candidate generation.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Aviation maintenance fault code discussion topics from Aviation Stack Exchange, tagged with fault-related terms | topic id, view_count, answer_count, score, tags, title, body, accepted_answer_id |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the view-count principle on aviation maintenance fault codes using the Stack Exchange platform's native `view_count` metadata. The control arm provides a baseline from a previously measured non-software platform where the principle did not generalize (GitHub issues API had no arrival field).

## The rubric, written before the rows

A need statement is classified based on the topic's metadata and content:

| classification | criterion |
|---|---|
| **served** | Accepted answer provides a working solution/step-by-step resolution guide for the specific fault code, or a direct link to a tool/manual |
| **partially_served** | Topic has answers with relevant information (error code definition, manufacturer notes) but no complete resolution guide, OR view_count indicates interest but no accepted answer |
| **unserved** | No relevant answers, or only irrelevant answers; view_count > 0 but no useful content |

## Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need statements harvested, each having view_count > 0 | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control statements — 5 known served, 5 known unserved — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need statements classified as `served`, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | the view_count principle does not serve the top-arrival need population |

## Denominators

Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Reproduce

```bash
python3 EXPERIMENTS/096-aviation-view-count/harvest.py     # arms 1 & 2
python3 EXPERIMENTS/096-aviation-view-count/outcome.py     # every gate above
```

Needs internet access for the Stack Exchange API, and Python 3.8+ with `requests`.
