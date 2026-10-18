<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E182 PROTOCOL — is the ground truth contestable where the assistant missed?

**Declared 2026-10-18, before any answer set was fetched.** Commit this file
first; `git log` is the evidence.

## 1. The question this record is carrying, and why it needs correcting first

E177 measured a free general assistant reaching the top-voted resolution on
26/30 = 0.8667 of self-contained Stack Overflow questions and 12/30 = 0.4000
of evidence-gated ones (F136, D118). E181 then measured that putting the
correct missing fact back (0.5714) and pasting the entire thread (0.6429) both
fail to move the assistant off a 0.5000 floor. E181's named next action is the
one explanation left: **the ground truth may be contestable.**

That question is stated in three documents — [`STATE.md`](../../STATE.md),
[`STATE-next-actions.md`](../../STATE-next-actions.md) and
[`EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md`](../181-fact-supply-closes-gap/RESULT.md)
— as *"is the accepted answer the best answer, or merely the accepted one."*

**It cannot be asked of this population.** Reading E177's committed
`rows.json` (`accepted_answer_id`, `key_is_accepted`):

| over | rows | `accepted_answer_id` non-null | key answer *is* the accepted one |
|---|---|---|---|
| E177's committed draw | 181 | **3** | — |
| rows carrying a key answer | 145 | **3** | **1** |
| **the 60 scored rows** | **60** | **0** | **0** |

The population is drawn from questions that were **unanswered when drawn**
(E175's screen). The asker has therefore accepted nothing. The key answer is
**the highest-scoring answer**, by a rule E177 declared in advance
([`AMENDMENT-2.md`](../177-evidence-gated-need/AMENDMENT-2.md)) precisely
*because* acceptance could not key the declared n. E177's own RESULT.md says
so at line 112.

So the executable question is one word different and materially harder:

> **Is the top-voted answer the best answer, or merely the top-voted one?**

**This is a record defect, not a finding about the world.** Three documents
carried a question whose subject is absent from the population they name. It is
corrected here and in the three documents, and the correction is what makes the
experiment runnable.

## 2. The instrument, and why it is not a reader

E181's proposed version of this question is *"one reader, reading the rows
every arm missed."* That is the wrong instrument twice over: it is the same
reader that E181's own G4 caught changing 4 of 10 verdicts on identical inputs
one day later, and it makes the answer to "is this ground truth good" a second
opinion rather than a measurement.

**The community already voted, and the vote vector is a measurement.**

For each row, fetch every answer's `score`. Then:

- `top` = the key answer's score (must reproduce `rows.json`);
- `runner_up` = the second-highest answer score, `None` where no second
  answer exists;
- `contested` ≡ **at least two answers AND `runner_up >= 0.5 * top`** — the
  ratio is scale-free, because scores here span two orders of magnitude
  (median key score 22.5) and any absolute threshold would be an artefact of
  that spread.

Four mutually exclusive, exhaustive states per row:

| state | rule | meaning |
|---|---|---|
| `uncorroborated` | exactly 1 answer | **no alternative exists to disagree with** |
| `unopposed` | runner_up ≤ 0 | alternatives exist; none drew support |
| `decisive` | 0 < runner_up < 0.5·top | alternatives drew some support, far less than the key |
| `contested` | runner_up ≥ 0.5·top | the community backed an alternative within a factor of two |

**`uncorroborated` and `contested` are different weaknesses** and must not be
merged. A single answer is not contested; it is unattested. Firing G3 without
distinguishing them is the mistake K1 exists to catch.

## 3. Gates, declared before the fetch

- **G4 (control, population stability).** The fresh fetch must reproduce
  `rows.json`'s `answer_count` **and** `key_score` on **≥ 57 of 60** rows.
  Disagreements are **reported row by row, never dropped.** E177 ran on
  2026-10-17 and this runs later, so answers can have arrived; a row whose
  count rose is population drift and is itself a reportable observation.
- **G1 (population measured).** A complete score vector for **≥ 55 of 60**
  rows. Below that, every gate below is `not_evaluated` — the third answer a
  numeric gate needs for "the population was not measured", required
  *before* the measurement so it cannot be added to make a result look better.
- **G2 (differential — the decisive gate).** On EVID rows: `contested` share
  on the **18 missed** against the **12 hit**. Fisher exact, two-sided.
  **Fires** at `p < 0.05` **and** a difference ≥ 0.20 in the same direction.
- **G3 (prevalence).** `contested` share over all 60 rows. **≥ 0.25** is the
  bar for "the ground-truth weakness is common rather than incidental".
- **K1 (kill for the disagreement framing).** If **≥ 0.50** of the 60 rows are
  `uncorroborated`, the disagreement framing is **wrong regardless of G2**,
  because on more than half the population there is no second position for the
  community to hold.
- **G5 (real-positive recovery).** Hand-read the answer bodies of the **5
  most `contested` and 5 most `decisive`** rows. The measure must be right on
  **≥ 8 of 10**. This is the instrument's own calibration; a statistic that
  only separates near-copies has not been shown to work.

## 4. Population, join, and leakage control

- Population: **the 60 rows E177 scored**, recovered by joining
  `score/verdicts.jsonl` (`pid` → `qid`) to `labels.json` (`arm`) and
  `rows.json`. Reproduces SELF 26/30 and EVID 12/30 exactly.
- The assistant's own answers are **never read** by this experiment and appear
  in no input. Arm labels enter only at the join, after the fetch.
- Every response body is written to `raw/se.jsonl` with its URL and remaining
  quota, so the cost and the bytes are auditable (D061).
- One reused draw, one venue: every rate here is **conditional on E177's pool**,
  not a prevalence estimate for Stack Overflow.

## 5. The decision this changes, stated before the measurement

1. **G2 fires.** Contestedness is differential and materially attributable.
   The SELF/EVID gap is then substantially **a disagreement about answers, not
   a deficit of context** — which is consistent with E181's two nulls and means
   **no context pipeline of any kind closes it**. The build direction stops
   being answer generation and becomes *knowing which resolutions are settled*:
   a ground-truth quality signal over a public corpus consumed as training and
   evaluation data. Next action becomes prior-art screen, then a **fresh-draw**
   prevalence run. **No product is proposed by this experiment** (brief §3).
2. **G2 does not fire, K1 does not.** Contestedness exists but is uniform:
   the EVID gap is a genuine reasoning deficit on evidence-gated questions.
   Both the EVID line and the ground-truth-quality direction close, and the
   mission returns to fresh exploration.
3. **K1 fires.** The disagreement framing is dead. The honest statement is
   that a large share of the ground truth is *unattested rather than
   contested* — which cannot explain the SELF/EVID **gap** but **does put a
   ceiling on every absolute service rate in this record**, because it weakens
   hit and miss rows alike. That is worth knowing and worth writing down; it
   is not a product.
4. **G4 fails.** The population moved between E177 and now. The rates are
   reported as drift-affected and no gate above is treated as clean.

## 6. Ceilings declared in advance

- n = 60, one reused draw, one venue, one sort rule (`view_count`).
- The four states measure **community voting behaviour**, which is a proxy for
  ground-truth quality and not the same thing. G5 is the only check on that
  gap and it is 10 rows.
- Vote margin is not correctness. A community can be confidently wrong; the
  instrument can only detect *disagreement*, which is the weaker and more
  defensible claim.
- No absolute level here may be compared with E177's 0.4000 / 0.8667 — E181's
  G4 voided that comparison across sessions.