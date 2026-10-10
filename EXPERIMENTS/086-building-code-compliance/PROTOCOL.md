<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E086 — Building code compliance observation

Session `2026-10-11-001`, VM `instance-20260717-0944`, declared 2026-10-11.

## The question

Building code compliance officers and inspectors frequently encounter compliance codes, variance requests, and approval codes on building department websites and regulatory portals. Understanding these codes is critical for legal compliance, safety, and project approval, but municipal code databases are often scattered, poorly indexed, and difficult to search without knowing the exact code structure. This experiment asks: can the view-count principle — measuring independent arrivals at a need via web search — recover `view_count`-like arrival metrics for building code compliance statements, and use them to classify needs as served, partially served, or unserved?

This prototype is not expected to produce a candidate or a product. It is an evidence-gathering prototype that tests whether the view-count principle can be operationalized for building code compliance with minimal resources. If successful, it provides a reusable instrument for future corpus measurements. If unsuccessful, it documents the technical gap, particularly regarding whether the principle requires code-structured domains.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is an evidence-gathering step per D083: fresh observation in a new domain. A positive result (view-count principle generalizes) would open the door to future candidate generation in this domain. A negative result would confirm the principle's limits and close this axis, particularly regarding the question of whether the principle requires structured code metadata.

**If the prototype can recover arrival metrics that classify building code compliance statements consistently**, it demonstrates that the view-count principle generalizes beyond software repositories and across domain types (technical and regulatory), and provides a measurement methodology for future domain exploration.

**If the prototype cannot recover meaningful arrival metrics**, it documents the technical gap and confirms that the view-count principle requires platform-specific arrival metadata, narrowing the space of viable domains for candidate generation, and particularly confirming that code-structured domains are necessary for the principle to operate effectively.

This experiment is not expected to produce a product, and the README must not imply that it did.

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Building code compliance discussion topics from publicly accessible building department forums, support sites, and Q&A platforms | code text, building type, viewable engagement metrics |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the view-count principle on building code compliance in regulatory communities. The control arm provides a baseline from a previously measured non-software platform where the principle did not generalize (GitHub issues API had no arrival field).

## The rubric, written before the rows

A need statement is classified based on web search results:

| classification | criterion |
|---|---|
| **served** | Web search returns a working solution, a direct link to a tool/manual that addresses the code, or a step-by-step resolution guide |
| **partially_served** | Web search returns relevant information (code definition, manufacturer notes) but no complete resolution guide |
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

## Reproduce

```bash
python3 EXPERIMENTS/086-building-code-compliance/harvest.py     # arms 1 & 2
python3 EXPERIMENTS/086-building-code-compliance/outcome.py     # every gate above
```

Needs internet access for web search, and Python 3.8+ with `requests` or `urllib`.