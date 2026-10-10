<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E085 — Topic-matched classifier test

Session `2026-10-10-002`, VM `instance-20260717-0944`, declared 2026-10-10.

## The question

Can a topic-matched classifier — which checks whether search results share key topic terms with the query, rather than merely matching solution keywords incidentally — pass G2 control validity on labels known by construction (hand-classified ground truth from E083)?

The key improvement over E083's keyword classifier: instead of checking if solution KEYWORDS ('how to', 'fix', 'guide', etc.) appear incidentally in search results, check if the search result is TOPIC-MATCHED to the query — i.e., the result's main topic corresponds to the query's main topic (shares key terms like 'avionics', 'hydraulic', 'boeing', etc.).

If the topic-matched classifier passes G2, it demonstrates that the view-count principle's discrimination problem is solvable with a better instrument. If it still fails, it confirms that the discrimination problem is harder and hand classification is the only reliable method — population measurement must wait for a different breakthrough.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is an evidence-gathering step per D083 and D088: testing whether the discrimination instrument can be improved. A positive result (topic-matched classifier passes G2) would open the door to future candidate generation with a valid measurement instrument. A negative result would confirm that the keyword-based classifier's failure mode is fundamental, and the view-count principle's implementation requires hand-classification or a completely different approach.

**If the topic-matched classifier passes G2**: It demonstrates that the view-count principle's discrimination gap can be closed with a better instrument, and future candidates can rely on automated classification.

**If the topic-matched classifier fails G2**: It confirms that the discrimination problem is not solvable with simple keyword/topic matching, and the view-count principle as implemented (Bing search + textual classification) cannot reliably identify served needs in technical fault-code domains. Population measurement must wait for a different breakthrough.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Aviation maintenance fault code discussion topics from publicly accessible aviation technology forums, support sites, and Q&A platforms | fault code text, aircraft type, viewable engagement metrics |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the view-count principle on aviation maintenance fault codes using the topic-matched classifier. The control arm provides a baseline from a previously measured non-software platform where the principle did not generalize (GitHub issues API had no arrival field).

## The rubric, written before the rows

A need statement is classified based on search results:

| classification | criterion |
|---|---|
| **served** | Web search returns a working solution, a direct link to a tool/manual that addresses the fault code, or a step-by-step resolution guide |
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

One retrieval route (web search via Bing); one rubric with solution/info keywords; and two corpora that have already been extensively measured. This measures the operationalizability of the view-count principle using only web search, WITH a topic-matched classifier instead of a simple keyword matcher. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 harvest.py     # harvest both arms (same as E083, uses same raw corpora)
python3 outcome.py     # evaluate all gates with topic-matched classifier
```

Needs internet access for web search, and Python 3.8+ with `requests` or `urllib`.

## Harvest notes

The harvest uses the same raw corpora and same Bing search infrastructure as E083. The topic matching is only in the classifier (outcome.py), not in the harvest step.