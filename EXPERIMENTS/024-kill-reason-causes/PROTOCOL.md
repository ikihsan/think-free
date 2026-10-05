<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# 024 — protocol: what killed the candidates, declared before any reason is read

**Date declared:** 2026-10-05, before any row of the candidate inventory was
classified. **Task:** T-0068. **Proposed findings/decision ids:** F044, D056.

## The belief under test

The sentence **"twelve candidates, twelve prior-art deaths"** is load-bearing in
this record. It appears in [`STATE.md`](../../STATE.md) ("Every candidate has
substantial prior art, and none has passed prior-art review"), in
[`HYPOTHESES.md`](../../HYPOTHESES.md) (standing caution 2), and it is the
stated premise of four experiments and of the top item in
[`STATE-next-actions.md`](../../STATE-next-actions.md): E015/F034 measured
whether "prior art exists" means "the need is served", E016/F035 re-adjudicated
the verdict, E017/F037 read the artifact types, E021/F041 measured the copy
channel. Item 0 rests on the claim that novelty cannot be the selection filter
*because it killed everything*.

**The claim has two separable parts, and only the first has ever been checked.**

1. **the count** — that there were twelve, and
2. **the cause** — that all twelve died of prior art.

Neither has a gate. Both are restated from summaries rather than counted from
the primary records.

## Why this is worth a measurement

If part 2 is false, then the apparatus built on top of it answers a question
that was not load-bearing. **Prior art would have killed a minority of the
candidates**, and the dominant kill reason would be something else — most likely
that the candidates' own mechanisms failed their own falsification tests
(F001, F006, F008) or were information-insufficient (D's executed witnesses).

That is a different diagnosis with a different repair. "The world already has
this" cannot be fixed by a better prior-art search; "the claim did not survive
its own test" can be fixed by not promoting an untested mechanism to candidate
status. **The two diagnoses imply opposite next steps**, and the record asserts
one of them in four places without a count behind it.

This is falsifiable, cheap, and needs no network.

## Population rule, fixed now

The population is **every row of the candidate inventory table in
[`RESEARCH/SYNTHESIS.md`](../../RESEARCH/SYNTHESIS.md)**, which that document
calls "Every candidate any report proposed, promoted or parked", **plus
`tools/origin`** (F026), which the record counts as a candidate and the
inventory does not list.

No candidate may be added from any other source, and no row may be dropped. If
a row has no recorded reason in its primary source it is classified
`unrecorded` and reported — that is the finding, not a gap to be filled by
inference.

**Primary source** for each row is, in this order: the sealed report that
proposed it (`RESEARCH/A.md`–`F.md`), then the experiment record that tested it
(`EXPERIMENTS/*/README.md`, `FAILURES-findings*.md`). **Summaries are never the
primary source**: `SYNTHESIS.md`, `STATE.md`, `STATE-next-actions.md` and
`HYPOTHESES.md` are the objects under test, so citing them to settle the
question is circular.

## Classification rule, fixed now

Four mutually exclusive categories, assigned by **precedence** so that a row
with two stated reasons gets one answer:

| order | category | assigned when the primary source states that |
|---|---|---|
| 1 | `unrecorded` | no kill reason is stated in the primary source at all |
| 2 | `information_insufficient` | no available observation could separate the claim from an alternative — an executed witness, non-identifiability, or an unfalsifiable universal |
| 3 | `falsified_mechanism` | a test of the candidate's own claim was run and the claim failed |
| 4 | `prior_art` | existing software or artifact already does the thing, and that is the stated reason not to advance |

**Precedence runs 1→4 and the first match wins.** A row whose source says both
"prior art exists" and "the coordination cost dominates" is `prior_art`, and the
secondary reason is recorded beside it. This ordering is a choice, it is declared
before reading, and the report states which rows it decided.

Every row also carries the **verbatim deciding sentence** from its primary
source, because a category assigned without quoting the deciding text is not
evidence.

## The two gates, declared now

- **H1 (the cause), `observed`.** Prior art is the decisive kill reason for a
  **majority** of the population. **Killed if ≤ 50%; survives if > 50%.** The
  threshold is half because the claim under test is that prior art is
  *dominant*, and half is the weakest population that can carry the word.
- **H2 (the count), `observed`.** The population is **twelve**. Reported as a
  bare number against the stated twelve, in both directions, with **no gate**:
  the count is a fact to be established, not a hypothesis to be supported.

## The control, declared now

A classifier with four hand-assigned categories can produce any answer its author
wants. So the same rule is run over a population whose true cause split is
**already recorded by a different instrument at a different time**:
`EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl`, whose 50 rows carry
F029's own cause table — **19 `prior_art`, 15 no mechanism, 12 not software, 4
hardware**.

**The control passes only on an exact match of all four categories.** A near
match does not pass: it means the rule is not reproducing a known cause split,
so H1 is reported `not evaluable` rather than answered.

## What each outcome would change

| result | what follows |
|---|---|
| H1 killed | prior art killed a minority. The four experiments measuring the screen answered a question that was not load-bearing, and item 0's premise is wrong. The dominant kill reason is named from the table, and it is not fixable by a better prior-art search. |
| H1 survives | the premise stands. The four experiments are answering the right question and item 0 is correctly posed. Recorded as a confirmation, with the count corrected if H2 disagrees. |
| control fails | H1 is `not evaluable`. No claim about the cause is made in either direction. |

## Limits, declared now

- **Every row was assigned by one reader.** There is no second coder, so this
  has exactly the defect E023 measured on its own labels before it fixed them
  with a κ. The deciding sentences are recorded so a disagreeing reader can
  re-derive every category and name the single sentence they disagree about.
- **The categories are the record's own vocabulary**, not the world's. A
  candidate killed by two reasons at once is assigned by precedence, which is a
  convention and can move a row across the 50% line.
- **This measures a cause table, not a world.** No statement about what exists in
  the world is made or implied here, and nothing here is a novelty claim.
- **It is a count over the record as written.** If the record's summaries are
  wrong, this reports that the summaries disagree with the primary sources — it
  does not repair them.