<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Fresh observation in aviation maintenance fault codes domain

Session `2026-10-10-014`, VM `instance-20260717-0944`, declared 2026-10-10.

## The question

Per D083: fresh observation in a new domain. Per D095: must not start from `classify_served` over Bing in an eighth domain. The `classify_served` instrument (Bing search + solution-keyword rubric) has been shown to fail discrimination in every technical domain tested (E088, E083, E090). This experiment uses the "read by hand" approach — classifying actual practitioner discussion threads by hand, with a rubric written before viewing results — which successfully passed the discrimination test on forum listings (E090, E097).

**Aviation maintenance personnel frequently encounter fault codes on aircraft maintenance systems, ground support equipment, and avionics. Understanding these codes is critical for flight safety, but manufacturer documentation is often proprietary, technical, and scattered. This experiment asks: can the view-count principle's rubric generalizable across domains be validated by hand classification of actual practitioner discussion threads, and what is the served/partial/unserved distribution?**

## Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Aviation maintenance practitioner discussion threads from publicly accessible forums/Q&A platforms (Aviation Stack Exchange, type-rated pilot forums, maintenance support forums) | fault code text, aircraft type, engagement metrics, solution links |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the view-count principle's rubric generalization to aviation maintenance fault codes using the "read by hand" approach (labels known by construction). The control arm provides a baseline from a previously measured platform where the principle's instrumentation differences are documented.

## The rubric, written before viewing results

| Classification | Criterion |
|---|---|
| **served** | A working solution, direct link to tool/manual, or step-by-step resolution guide for the specific fault code appears in the thread. The solution must address the query's distinctive subject (excluding chrome words like "error", "code", "fault", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages"). **Key criterion**: the query's distinctive subject term must appear in the solution text (not just in the query itself). |
| **partially_served** | Relevant information (error code definition, manufacturer notes, general guidance) appears in the thread but no complete resolution guide for the specific fault code. The thread mentions the fault code and provides helpful information but no working solution. |
| **unserved** | No relevant results, or only irrelevant results (chrome/boilerplate, unrelated topics). The thread does not meaningfully address the fault code. The query's distinctive subject does not appear in any retrieved text. |

Additionally: does any retrieved text actually mention the query's distinctive subject (excluding chrome words like "error", "code", "fault", "meaning", "how", "the", "for", "and", "with", "manual", "guide", "messages")?

## Gates, declared before any row is read

| gate | condition | if not met |
|---|---|---|
| **G1 discrimination** | `served(known-unserved) ≤ 0.30` **and** the Newcombe 95% CI of `served(known-served) − served(known-unserved)` excludes 0 | Instrument reports needs as served when no such thing exists; every served fraction is uninterpretable. This is the gate that killed E081-E087 and E090's automated classifier runs (which all had ~0.80 FPR on known-unserved). |
| **G2 control validity** | Separate 5 known-served + 5 known-unserved at ≥ 0.85 accuracy | Rubric is not usable; fraction is not measurable. |
| **G3 measurement** | Fraction classified as `served`, with Wilson CI95, over ≥ 30 rows | Reporting gate; no pass/fail but documents arrival metrics. |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | View-count principle does not serve the top-arrival need population. |

## Denominators

Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Ceiling, stated now

One retrieval route (hand reading of practitioner discussion threads); one rubric written before viewing results; and two corpora that have already been extensively measured. This measures the operationalizability of the view-count principle's rubric using hand classification, without automated search or classification. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
# This experiment requires manual reading of practitioner discussion threads.
# The collect_practitioner_rows.py script reads threads and outputs classified results.
# Run: python3 EXPERIMENTS/091-fresh-observation-aviation-fault-codes/collect_practitioner_rows.py
```