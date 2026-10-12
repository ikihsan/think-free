<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E114 — RESULT: the population is served, and the verifier is the thing that fails

Run 2026-10-12. One rater (the agent running the session), one document genre
(US Federal Register final rules), one question style (enumerate the dollars,
the dates, the citations). `observed` for every number below; every count is
reproducible from the committed documents, answers and controls.

## The four gates

| gate | declared | measured | verdict |
|---|---|---|---|
| **KG-C1** recall on corrupted answers | >= 0.90 | **1.0000** (22 of 22; B1 from-document 11/11, B2 absent 11/11) | pass |
| **KG-C2** false alarms on verbatim document spans | <= 0.02 | **0.0069** (1 of 145 values, 15 spans) | pass |
| **KG-A** treatment arm's ungrounded rate | < 0.02 to survive | **0.0000** (0 of 374) | **class closed** |
| **KG-D** | instrument must pass C1 and C2 before A is scored | it did, after AMENDMENT-2's v0 failure | honoured |

## The instrument is perfect on both controls and useless in the field

The checker flags **139 of 374 values (0.3717)** in real answers.

| arm | what it is | what happened |
|---|---|---|
| `ungrounded_value` (24) | value reported absent from the document | **24 of 24 have every digit group and token present in the document.** Zero are fabrications. The document writes `49 CFR $2,600. 1150.31-1150.35`, `49 $64. per document. U.S.C. 11301`, `5 U.S.C. 552(a)(4)(A), (a)(6)(B), and 553`, and `Filed 10-9-26`; the checker needs the rendering it did not try. |
| `ungrounded_claim` (115) | value occurs, but not beside the words used to describe it | **50 of 50 read by hand against the document are correct.** |

**The checker's false-positive rate on real answers is 1.00** (95% Wilson lower
bound 0.9286 on the hand-read arm, and 24/24 with no missing parts on the other
arm). It cannot tell a correct answer from a corrupted one, even though it
catches corruption perfectly and passes verbatim text almost cleanly.

## The finding that generalizes

**Both controls were too easy, and the population that matters was in neither.**

- The verbatim control validates the case where the answer *is* the document.
- The corruption control validates the case where the value is wrong.
- Real answers to real documents are **faithful paraphrase with no invented
  values**, and that arm was never built until the run had already been scored.

That arm is where a checker built out of string containment and word overlap
fails completely. Verifying a paraphrase against a source is a semantic
judgement — the thing the tool was built to avoid paying for — and the
instrument has no way to notice that it is being asked.

## Limitations, stated rather than buried

1. **One rater.** The treatment arm is this session's agent, one genre, one
   prompt style. `0 of 374` is a fact about *that*, not about assistants.
2. **The flag rate is not an unbiased number.** `ground.py` was repaired twice
   after its controls passed, while looking at arm A's output (a sentence-unit
   window, then a dual-granularity rule plus light stemming). The flag rate
   fell 0.782 -> 0.684 -> 0.372 across those repairs. Any rate produced by an
   instrument tuned on the arm it reports is not an estimate of that arm. The
   hand-read of the flags **is** unbiased with respect to the instrument, and it
   is the number the decision rests on.
3. **The reader is the treatment arm.** 50 flags were classified by the same
   agent that wrote the answers. The mechanical check on all 24 `ungrounded_value`
   verdicts is independent of me, and it is the arm where a fabrication would
   have shown first.
4. **Small denominator in documents.** 5 documents, 15 answers, 374 values. The
   Wilson upper bound on 0 of 374 is **0.0098**, which clears the 2% gate with
   room, but a second genre could move it.

## What this closes and what it does not

- **Closed:** "a free general assistant invents the values when it reads a
  document for you." On this population it did not, once, across 374 values.
- **Closed:** "a cheap mechanical attestation that an answer's values came from
  the document" as a shippable product. The one built here flags more than a
  third of a faithful answer and every flag is wrong.
- **Not closed:** whether a verifier using a language model for the
  paraphrase step could work. That is a different instrument with a different
  cost, and this run says nothing about it.
- **Not closed:** other document genres. Contracts, invoices, medical records
  and tabular spreadsheets put a different distance between a label and its
  value, which is exactly the variable that decides this.

## Artifacts

| file | what it is |
|---|---|
| `PROTOCOL.md` | declared before any fetch, with all four gates |
| `AMENDMENT-1.md` | population changed to Federal Register rules, with the reason |
| `AMENDMENT-2.md` | checker v0 failed its negative control at 0.367; run `not_evaluated` |
| `fetch.py`, `raw/` | 30 final rules fetched, digests in `raw/manifest.jsonl` |
| `answers.jsonl` | the 15 treatment-arm answers, committed before `ground.py` existed |
| `ground.py` | the checker; deterministic, stdlib only |
| `controls.py`, `controls.jsonl` | the two control arms, seeded at 114 |
| `checked-controls-v1.jsonl`, `checked.jsonl` | verdicts |
| `sample-flagged.json` | the 50 hand-read flags with their answer fragment and document context |
| `verify_flags.py`, `flags-verified.jsonl` | the mechanical check on all 24 `ungrounded_value` verdicts |
| `score.py`, `gates.json` | the four gates, computed |
| `checked-v0.jsonl` | the failed instrument's run, kept |