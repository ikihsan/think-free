<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E099 — Medical device fault code discrimination test

Session `2026-10-10-004`, VM `instance-20260717-0944`, declared 2026-10-10.

## The question

Can the E098 discrimination test instrument (Aviation Stack Exchange API metadata classifier: view_count, answer_count, accepted_answer, fault_code_specific) generalize to the medical device fault code domain? This is a fresh observation per D083, testing the instrument outside the domain where it was originally validated (aviation), without using `classify_served` over Bing (using Stack Exchange API metadata instead).

If the instrument passes G2 on medical device queries, it demonstrates that the discrimination instrument generalizes across platforms with exposable metadata. If it fails, it suggests the instrument is platform-specific and the view-count principle's measurement problem in fault-code domains is harder to solve.

### The candidate decision this changes

This prototype is not expected to produce a candidate or change any candidate decision directly. It is an evidence-gathering step per D083 (fresh observation in a new domain). A positive result (instrument passes G2 on medical device queries) would demonstrate that the discrimination instrument generalizes across platforms with exposable metadata, opening the door to population measurement in medical device domains. A negative result would suggest the instrument is platform-specific, and a different approach would be needed for each domain.

**If the instrument passes G2**: It demonstrates that the view-count principle's discrimination gap can be generalized with the right platform-specific instrument, and population measurement can proceed in medical device domains.

**If the instrument fails G2**: It confirms the discrimination instrument is platform-specific, and the mission's 10+ measurements showing the seat is empty (F029, F051, F039, F059, F081, F084, F085, E075, E079, F106) reflects fundamental limitations that cannot be solved by iterating the same instrument across domains.

### Population and arms

| arm | source | what it carries |
|---|---|---|
| **1 (treatment)** | Medical device fault code discussions from publicly accessible medical device forums, support sites, and Q&A platforms (e.g., MedWrench, patient forums) | fault code text, device type, viewable engagement metrics |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows) | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why these populations.** The treatment arm tests the E098 discrimination instrument on medical device fault codes using Stack Exchange API metadata. The control arm provides a baseline from a previously measured non-software platform.

### Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 30 need statements harvested, each yielding API results | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 10 seeded control statements — 5 known served, 5 known unserved — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the fraction of need statements classified as `served`, with Wilson CI95, over ≥ 30 rows; and the same fraction over the control arm's rows | this is the result; no gate |
| **G4 answerability sub-test** | 17 of 20 top-arrival need statements classified as `served` or `partially_served` | the view_count principle does not serve the top-arrival need population |

**Denominators.** Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

### Ceiling, stated now

One retrieval route (Stack Exchange API); one classifier using platform metadata (view_count, answer_count, accepted_answer, fault_code_specific); two corpora that have been partially measured. This measures the generalizability of the E098 discrimination instrument to the medical device fault code domain. It does not measure demand, does not measure adoption, and does not close any candidate.

### Reproduce

```bash
python3 harvest.py     # harvest both arms via Stack Exchange API
python3 outcome.py     # evaluate all gates with E098 classifier
```

Needs internet access for Stack Exchange API, and Python 3.8+ with `requests`.

### Harvest notes

The harvest uses the Stack Exchange API to search for medical device fault code queries. The API returns structured metadata including view_count, answer_count, accepted_answer_id, and title/snippet text. The classifier logic (classify_fault_code) is applied in the outcome step.