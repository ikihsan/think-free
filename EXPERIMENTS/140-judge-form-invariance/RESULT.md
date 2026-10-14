<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 RESULT — is a shipped LLM judge form-invariant, and is a canonicalizer enough?

Run 2026-10-14. Protocol predeclared 2026-10-14 before any arm existed;
AMENDMENT-1 to -3 before any instrument ran; AMENDMENT-4 and -5 after
measurement, and neither changes a threshold. Raw evidence: `arms.jsonl`,
`p2.jsonl`, `judge_prompts/`, `judge_output/`, `gates.json`,
`misattribution.json`, and the session's `commands.log`.

**Short answer.** The cheap deterministic pass is enough for what it is scoped
to, and is now measured rather than argued. The incumbent mechanical checker it
replaces is not merely imprecise, it is *anti*-correlated with the property it
is used for. The shipped LLM judge is not falsified: it produced zero false
positives on 24 correct-but-reworded answers and found 6 of 7 swapped values.
What the experiment settles is that **the expensive check cannot be replaced,
only deferred** — because the weakness it covers is real and `observed`.

## Population

E114's committed corpus, reused and not re-harvested: **15 (document,
question, answer) triples over 5 real US Federal Register final rules**, 241
numeric values and 398 canonical values of every kind. Judge arm: **31 items in
7 batches** — 10 `V`, 10 `P`, 7 `C`, 4 `P2`.

Arms: `V` verbatim, `P` deterministic surface transforms, `P2` a blind writer's
re-authoring, `C` one value replaced by a plausible same-document value,
`K` one list item deleted, `X` one value transposed onto the wrong subject
(exploratory, AMENDMENT-5).

## The three instruments, one table

Every rate below is a false-positive rate on answers that are **correct by
construction** (K4-verified), except the last two columns, which are detection
on answers that are **wrong by construction**.

| | FP on `V` | FP on `P` | FP on `P2` | detects a swapped value | detects an omission | detects a misattribution |
|---|---|---|---|---|---|---|
| **M1** `ground.py` (E114's, unchanged) | 139/373 = **0.3727** | 173/372 = **0.4651** | 65/108 = **0.6019** | 9/11 = 0.818 | not gated | 6/6 |
| **M2** `valueset.py` (the canonicalizer) | 0/398 = **0.0000** | 0/398 = **0.0000** | 0/133 = **0.0000** | **11/11 = 1.000** | 11/11 items | **0/6** |
| **J1** shipped `inspect_ai` `model_graded_fact` | 0/10 | 0/10 | 0/4 | 6/7 = **0.857** | not run | not run |

Wilson 95% intervals: M2's three zeros are 0.0000–0.0096 (n=398), 0.0000–0.0096
(n=398) and 0.0000–0.0281 (n=133). J1 pooled on the 24 correct answers,
0/24 = 0.0000, CI95 **[0.0000, 0.1380]**; on the 7 corrupted answers 6/7 =
0.8571, CI95 **[0.4869, 0.9743]**. M1's paired detection is 9/11 = 0.8182,
CI95 [0.5230, 0.9486]. M2's 11/11 is CI95 [0.7412, 1.0000].

## Gates, as declared

| gate | declared | observed | verdict |
|---|---|---|---|
| **G0** J1 detection on `C` | ≥ 0.667 | 6/7 = 0.8571 | **PASS** |
| **K1** M2 recall on `C` | ≥ 0.95 | 11/11 = 1.0000 | **PASS** |
| **K2** M2 FP on `P` | ≤ 0.02 | 0.0000 | **PASS** |
| **K3** M2 FP on `V` | ≤ 0.02 | 0.0000 | **PASS** |
| **K4** `P`, `P2` multiset equals `V` | per item | 15/15 and 4/4 | **PASS** |

**The build trigger fires.** M2 survives faithful rephrasing at 0 false
positives in **929** values, detects every substitution and every omission built,
and every arm it was measured on passed the gate that E114's verifier failed.

## What the numbers say, in the order they matter

**1. The incumbent is not a paraphrase detector; it is a paraphrase *detector
of the wrong thing*, and rephrasing makes it worse.** M1 flags 0.3727 of the
correct verbatim values, 0.4651 after surface transforms, 0.6019 after a writer
re-authored the same answer in different words. Every one of those flags is
wrong: K4 guarantees the values are identical. E114 recorded 0.3717 and a
false-positive rate of 1.00 on faithful paraphrase (F118); this run reproduces
the 0.3717 independently and shows the rate rising monotonically with how far
the text has moved from the expert's words. **A rate quoted on one arm does not
transfer, and here the transfer is not random — it is a function of
rephrasing depth.** That is F123 sharpened from a warning into a curve.

**2. M1's detection is not evidence, because it is not separable from its own
false positives.** It finds 9 of 11 swapped values. It also flags 37 per cent of
correct values. A flag from M1 is worth roughly as much on a correct answer as
on a corrupted one, which is why E114's conclusion that the verifier was dead
stands: it was not weak, it was the wrong instrument. This run's contribution is
that the diagnosis is now *quantified* rather than asserted, and the paired
measurement — was the swapped value itself the flagged one? — is what produced
9/11, where differencing aggregate flag counts would have produced 6/11. The
paired measurement is the one worth repeating on any future instrument.

**3. The shipped judge is not the problem.** `model_graded_fact`, verbatim, in
seven separate blind agent sessions: **0 false positives in 24 correct answers**,
including 10 mechanically reordered, 4 re-authored by a writer, and 10 verbatim.
It found 6 of 7 swapped values, including a transposition inside a telephone
number and a four-digit change in a date. The upper bound of 0.138 does not
establish invariance; it establishes that the obvious failure mode — a judge
that fails a correct answer because it lost its thousands separator — **was not
observed here**, at n = 24, on this rubric, from this judge model.

**4. And its one miss is the most useful sentence in the run.** Batch 0, item 5
is a corrupted answer whose only defect is a billing code changed from
`4915-01-P` to `1247-01-P`. The judge **found it**, wrote "This is a factual
discrepancy in a data value, not a style or punctuation difference" — and then
graded it **C**, because the question asked for CFR, U.S.C., docket and FR
document numbers, and a billing code is none of those. The failure is not
perception and not the rubric's silence; it is the rubric's *scope clause*
outvoting evidence in front of it. A practitioner reading this should know that
`model_graded_fact` asks "does the submission contain the expert's content?"
and that a grader can decide a real error is out of scope and be right about the
question it was actually asked. This is a different defect class from everything
in F118/F123, and it is the one a re-run would not fix.

**5. The declared weakness is now `observed`, and it is the whole problem.** On
6 misattribution arms where every value is present, correctly written and
correctly attached to the wrong subject, **M2 detected 0 of 6** and M1 flagged 6
of 6. So the cheap pass is blind to binding, by construction and now by
measurement, while the check that sees binding is unusable as a gate. M2 is not
a replacement for a faithfulness check; it is a **pre-pass that removes the
cases a faithfulness check should never have to look at** — omissions and
substitutions, which are 22 of 22 of the wrongness built here — and hands on
only the binding question.

## What this changes

The decision that changes is the one PROTOCOL.md made conditional: **`valueset.py`
is no longer a module inside an experiment. It is a candidate artifact**, and the
protocol's own next action — a second document genre — is now the binding
constraint on it rather than an optional extra. Its scope statement is fixed by
measurement rather than by hope: *value correspondence under rephrasing*, never
faithfulness.

The second change is to `preflight`. E124 shipped a tool whose declared gates
included a false-positive arm; E137 then closed `preflight` on demand grounds
while it still carried the arm this experiment shows is not reachable by a
mechanical checker. M2 is the cheap, deterministic, zero-false-positive way to
carry the **value** arm, and `ground.py`'s value arm should be described by the
curve in row 1 rather than by a single quoted rate.

## What remains unknown

- **Generalisation.** One genre, five documents, one reader, one day. The
  extractor was written against this corpus's value shapes, so a pass here is
  evidence of mechanism, not of generality. This is the declared next action.
- **The judge's invariance is not established.** 0 of 24 is an interval with an
  upper bound of 0.138, not a measurement of invariance. Repeating it at n = 100
  would cost about four times this run and is the only way to turn it into a
  number a team could gate on.
- **Panel and reducer.** One judge model, no majority vote, uncontrolled model
  variation between the seven batches (AMENDMENT-2 §3's declared cost).
- **Binding in prose.** `X` transposes values mechanically. A binding that is
  wrong in words rather than by transposition is `untested`.
- **Instruments outside this shape** — anything not reducible to values —
  are untouched by this result.

## The single most useful next action

Run `valueset.py` unchanged against a **second document genre** with a real
value population, and report K1/K2/K3 at that genre's own denominators. That is
the protocol's declared next action, it is the only thing standing between a
measured mechanism and a candidate artifact, and every number in this RESULT is
about a corpus where the extractor was already known to work.
