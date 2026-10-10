<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E086 — View-count arrival metrics measurement

Session `2026-10-10-003`, VM `instance-20260717-0944`, declared 2026-10-10.

## The question

Can the view-count principle — measuring independent arrivals at a need via web search — produce meaningful arrival count distributions across technical fault-code domains, without relying on a classify_served classifier?

This experiment moves away from the classification gate framework (G2, G3, G4) that has consistently failed in fault-code domains, and instead focuses on the core view-count metric: the number of search arrivals per need statement. By reporting the raw arrival count distribution, we can assess whether the view-count principle has any measurable signal even when the classifier cannot separate served from unserved.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is a measurement step per D083 (fresh observation in a new approach): testing whether the view-count principle's core arrival metric has any distributional signal across domains, independent of classification accuracy.

**If the arrival count distribution shows a meaningful pattern** (e.g., different shapes for treatment vs control, or correlation with other metadata), it demonstrates that the view-count principle carries information beyond the failed classifier, and future work can build on this metric foundation.

**If the arrival count distribution is uniform/noisy across both arms**, it further confirms that the view-count arrival metric, as measured by simple web search result counts, does not carry discriminative information about need satisfaction — and the instrument's only valid use is as a raw counter, not as a served/partial/unserved signal.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Aviation maintenance fault code discussion topics from publicly accessible aviation technology forums, support sites, and Q&A platforms | fault code text, aircraft type |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, etc. |

**Why these populations.** The treatment arm tests the view-count arrival metric on aviation maintenance fault codes. The control arm provides a baseline from a previously measured non-software platform.

## Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need statements harvested, each yielding web search results | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 not applicable** | N/A — this experiment does not use a classifier discrimination test | — |
| **G3 measurement** | the fraction of need statements yielding ≥k search results, for k ∈ {1, 2, 3, 5, 10}, over ≥ 30 rows; and the same fractions over the control arm's rows | this is the result; no gate |
| **G4 not applicable** | N/A — this experiment does not have an answerability sub-test relying on classifier labels | — |

**Denominators.** Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Ceiling, stated now

One retrieval route (web search via Bing); no classifier rubric; two corpora that have already been extensively measured. This measures the operationalizability of the view-count principle's core arrival metric using only web search result counts, WITHOUT a served/partial/unserved classification. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 harvest.py     # harvest both arms
python3 outcome.py     # report arrival count distributions
```

Needs internet access for web search, and Python 3.8+ with `requests` or `urllib`.

## Harvest notes

The harvest uses the same Bing search infrastructure as E083. The key difference is that the outcome step does not attempt to classify each statement; it only records the number of search results per query (arrival count).