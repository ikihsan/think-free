<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E182 RESULT — the fourth explanation is gone; the gap is a capability limit, and the ground truth has a measured ceiling

**Date:** 2026-10-18. **Status:** complete. **Outcome: G2 does not fire on an
instrument that passed its own declared calibration bar, so E181's named next
action closes the last testable explanation of F136's gap. Two instrument
results survive, and one of them is a ceiling on every absolute service rate in
this record.**

Protocol [`PROTOCOL.md`](PROTOCOL.md) · [`AMENDMENT-1`](AMENDMENT-1.md) ·
[`AMENDMENT-2`](AMENDMENT-2.md). Commands: `fetch.py`, `analyse.py`,
`g5_fetch.py`, `bodies.py`, `overlap.py`, `overlap.py --power`.

## 1. A question three documents asked that this population cannot answer

E177's population is drawn from questions that were **unanswered when drawn**.
The asker has therefore accepted nothing. Reading E177's committed `rows.json`:

| over | rows | `accepted_answer_id` non-null | key answer **is** the accepted one |
|---|---|---|---|
| E177's committed draw | 181 | **3** | — |
| rows carrying a key answer | 145 | **3** | **1** |
| **the 60 scored rows** | **60** | **0** | **0** |

[`STATE.md`](../../STATE.md), [`STATE-next-actions.md`](../../STATE-next-actions.md)
and [`E181's RESULT`](../181-fact-supply-closes-gap/RESULT.md) all carried the
next action as *"is the **accepted** answer the best answer, or merely the
**accepted** one."* **0 of 60 rows have an accepted answer to inspect.** The key
answer is the *top-voted* one, by a rule E177 declared in advance because
acceptance could not key the declared n.

So the runnable question is one word different: **is the top-voted answer the
best answer, or merely the top-voted one?** (F141.)

## 2. Vote margin: cheap, pre-declared, and it does not measure the construct

The community already voted, so the instrument is the score vector — no reader.

| gate | result |
|---|---|
| G4 population stable | **PASS** 59 of 60; one row (`79408101`) drifted 9 → 10 votes, real movement in a day |
| G1 population measured | **PASS** 60 of 60 complete score vectors |
| G3 contested ≥ 0.25 | **FAIL** 13/60 = **0.2167**, Wilson [0.1312, 0.3362] |
| K1 uncorroborated ≥ 0.50 → kill | **not fired** 16/60 = 0.2667 |
| G2 differential | **did not fire** — EVID missed 4/18 = 0.222 vs EVID hit 3/12 = 0.250, diff **−0.0278**, Fisher p = **1.0**, OR 0.857 |
| **G5 real-positive recovery** | **FAILED — 4 of 10, bar was 8 of 10** |

G5 read the answer bodies of the 5 highest-ratio `contested` rows and the 5
highest-ratio `decisive` rows and asked the question that matters: **do the two
answers state the same resolution?** — which is what E177's own scorer measured
(`same_resolution`). Three of five `contested` rows state the *same* resolution;
three of five `decisive` rows state *different* ones. Errors run **in both
directions at similar rates**, so vote margin is not a noisy proxy for
resolution divergence, it is not a proxy at all. Two legible shapes:

- **Implementation competition reads as disagreement.** "How do I do X" rows
  collect several working implementations of one fix — `zip_transform` against
  a `zip` loop, two mirrors of the same `.aar`.
- **Genuine contradiction hides under a wide margin.** `qid 79556333`'s
  runner-up sits at 44% of the top and flatly contradicts it ("you can't, closed
  Shadow Root" / "you can add CSS, see the docs"); `qid 79843062` carries three
  different fixes at 23/10/7.

**G2's null was therefore withdrawn rather than reported.** A null from an
instrument that does not measure its construct reads exactly like a closure,
and the next reader of this record would have written "the EVID gap is not a
disagreement about answers" on the strength of a threshold G5 had already
falsified.

## 3. Two overlap instruments, two declared rejections, one acceptance

The construct is available lexically: E171 measured the vocabulary contrast on
an adjacent corpus (*a failure report names the symptom and the environment; a
fix states the cause and the change*), and E169 measured that a fix shares
**0 of 13** three-word runs with the report. So two answers to one question
overlap on **prescriptive tokens** when they state one fix.

> `divergent` ≡ `overlap ≤ τ`, with
> `overlap = |P(A0) ∩ P(A1)| / |P(A1)|` over prescriptive tokens — identifiers
> in code spans plus snake_case, mixedCase and dotted-path tokens.

τ was fitted on the **same 9 hand-read rows**, balanced accuracy was the
criterion, and the bar was **0.80**, all declared before either run.

| instrument | balanced acc | sensitivity | specificity | verdict |
|---|---|---|---|---|
| raw overlap (AMENDMENT 1) | **0.6500** | 0.8000 | **0.5000** | **rejected** — specificity at chance |
| residualised against the question (AMENDMENT 2) | **0.8000** | 0.6000 | 1.0000 | **accepted**, τ = 0.05 |

The raw instrument's three errors were one mechanism: **shared problem
vocabulary counted as shared prescription.** `qid 79791886`'s runner-up shares
`rand`, `RAND_MAX`, `sqrt`, `R` with the top answer, so a 0.91 overlap records
that both discuss the same program, not that both propose the same fix.
Residualising (`P(A) \ P(question)`) removes exactly that and nothing else.

**The accepted detector is narrow and that is a stated cost:** it fires only
where the runner-up shares essentially *no* residual prescriptive token. It has
**specificity 1.0000 and sensitivity 0.6000**, so it under-detects divergence by
roughly that factor, and its bound on the missed side (0.74) straddles the hit
side's (0.83) — too loose to inform, which is itself the honest statement about
power.

## 4. G2′ on the accepted instrument: no differential divergence

| | EVID missed | EVID hit | SELF hit (reference) |
|---|---|---|---|
| rows labelled | 13 | 8 | 15 |
| `divergent` | 6/13 = 0.4615 | 4/8 = 0.5000 | 4/15 = 0.2667 |
| after excluding the 9 calibration rows | **4/9** | **3/6** | — |

**Fisher exact p = 1.0, OR 0.80, diff −0.0556. G2′ does not fire.**

Because the gate is a 0/1 label on 9 versus 6, a better-powered check on the
*same* accepted instrument and the *same* rows was run as a post-hoc exact
permutation test on the continuous statistic — median residual overlap **0.054
missed against 0.083 hit**, **U = 27.0 which is exactly `n₁n₂/2`**, **p =
1.0000**. Not a near-null: exactly null.

**Coverage, stated because it is the real ceiling.** Of 60 rows, 16 are
`single_answer`, 2 have a runner-up scoring ≤ 0, and 5 more are conceptual rows
whose runner-up contains no prescriptive token at all (`qid 79537353` is a
C-standards question with nothing to prescribe). **37 of 60 rows are labelled,
and 21 of the 30 EVID rows.** The disagreement explanation is closed on 70% of
the arm it was about and is `untested` on the other 9.

## 5. A defect in my own arithmetic, caught before it was reported

The first version of the permutation test compared observed U against **0**
instead of against `n₁n₂/2`. It returned **p = 0.0004 for an observed U sitting
exactly at the midpoint** — the largest possible deviation from a null that was
in fact perfect. It is F136's own error, the Fisher tail summed from the wrong
term, made once more in a different function and caught by the case that matters
most. Fixed, re-run, committed; `--power` reproduces the corrected value.

Also recorded rather than smoothed: **the Stack Exchange answers endpoint does
not forward `x-ratelimit-remaining`** through the CDN in front of it (every
response carries `CF-Cache-Status` instead), so the first fetch's
`quota_remaining` was `None` on every row. Storing the whole header set records
the *absence*, which is the finding; the quota audit runs through `/info`
instead (231 → 227 for the whole experiment).

**One secret-scanner false positive, declared rather than worked around.** One
public answer in this corpus assigns an environment-variable *name* to a config
key in a code sample — it carries no value — and the scanner's generic
`assigned-credential` rule matches the value position. The raw capture
`raw/se-bodies.jsonl` and the derived `bodies.json` both carry the tool's own
per-file suppression directive, which is **recorded in the session log rather
than applied silently**. The derived dump is now rebuilt from the raw capture
by `bodies.py --rebuild-from-raw` — **zero requests** — so the two cannot drift
apart; the rebuild was checked to reproduce the committed 203 answers
byte-for-byte, and the deduplication it needs is by `(question_id,
answer_id)`, because the raw capture holds two independent fetches that
overlap.

## 6. What this decides

**F136's SELF/EVID gap has no testable explanation left.** Four candidates, four
verdicts:

| explanation | verdict | where |
|---|---|---|
| the missing fact is not in anything published | closed — publishable **0/46** | E178 |
| the venue's own round trip already supplies it | closed — `has_ask` 0.6739, 0.9000 on a second venue | E178, F137, F138 |
| supplying the correct fact (or the whole thread) moves the rate | closed — McNemar **p = 1.0**, and 0 rows for pasting | E181 |
| **the ground truth is contested where the assistant missed** | **closed — p = 1.0 on the gate and p = 1.0000 on the continuous test** | **E182** |

What remains is the reading that costs the most to accept: **the assistant
reasons worse on questions whose resolution needs a fact the question omits.**
That is a capability limit, not a context deficit, and it is not something a
context pipeline closes. **The EVID line closes with the reason measured rather
than unexamined** — which is what distinguishes this closure from the six before
it (D120).

**And one number in this record is now a ceiling on all the others.** The ground
truth behind every service rate here is:

| state | share |
|---|---|
| `contested` — a runner-up within a factor of two of the top answer | 21.7% |
| `uncorroborated` — one answer, no alternative exists to disagree | 26.7% |
| **contested or unattested** | **48.3%** |

E177's scorer asks whether the assistant states the same resolution as the
**top-voted** answer. On **48.3% of this population that answer is either
disputed or has no corroboration at all.** This weakens hit rows and missed rows
alike, so it explains **no** part of the SELF/EVID *gap* — but it puts a
measured ceiling on every absolute *level* this mission has reported, including
0.8667 and 0.4000 themselves.

## 7. What this does not close

- **9 of 30 EVID rows.** Single answer, no positive runner-up, or no
  prescription to compare. Untested on those, by construction.
- **Sensitivity 0.6000.** A more sensitive accepted detector could find
  divergence this one misses. The bound it implies straddles both arms and
  carries no information.
- **One venue, one reused draw, one sort rule** (`view_count`). Every rate is
  conditional on E177's pool.
- **Vote margin is not correctness.** A community can be confidently wrong; this
  instrument detects disagreement, which is the weaker and more defensible claim.
- **Nothing about any other venue**, and nothing about abstention.
- **One reader.** The ten hand-read labels are the only judgement here. E181's
  G4 already measured that one reader's verdicts move 4 of 10 on identical inputs
  one day later. These judgements are about two answers agreeing with each other,
  a narrower task, and the ceiling is not re-measured.

## 8. The single most useful next action

**Not more EVID work — that line is closed.** The one thing this experiment found
that is *not* an unserved-need question, that is not closed, and that has a
mechanism measured today rather than assumed:

> A public corpus consumed as ground truth has **48.3%** of its high-arrival
> resolutions contested or unattested, and a three-signal filter for that
> condition now has a **calibrated** discrimination estimate (0.8000 balanced
> accuracy, specificity 1.0000) and a **measured** prevalence.

Anyone building RAG corpora, evaluation sets or fine-tuning data from answered
questions is what that is about. It is a different axis from every hypothesis
this record has closed six times, and it is the first candidate in that many
sessions whose supporting measurement is *the finding itself*.

**Do that prior-art-check before any product code** — answer-quality prediction
on Stack Overflow is an established research area, and this record's rule is
that absence of a search hit is not originality but a crowded area is not
novelty either. The screen's first question is whether the three signals
(vote margin, corroboration count, residualised prescriptive divergence) carry
information a known quality predictor does not already carry.

If the screen clears, the next measurement is precision and recall of the
three-signal filter against a **fresh draw** of hand-read labels — not another
draw from E177's pool.