<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E124 — a preflight check on the instrument that produces an evaluation number

Pre-declared 2026-10-13, before any adapter was written and before `preflight`
existed. Commit order is the evidence: this file precedes `run.py`.

## The question

This repository has now lost three results to defects in the *harness* that
produced the number, each of which was found by hand, after the fact, by reading
output until something looked wrong:

| finding | the harness reported | what was true |
|---|---|---|
| F118 (E114) | verifier recall 1.0000, false-alarm rate 0.0069, `instruments_valid: true` | it flagged 0.3717 of 374 values in correct answers; **false-positive rate 1.00 on its own flags** |
| F121 (E116) | a scorer printing TP/FP/FN for 80 accounts | key held integer `account_id`, answers held `"R001"`; **every answer scored against nothing** |
| F122 (E116) | `G0_C_precision = 0.0` — reader hallucinates | the gate's premise was false: 4 "control" accounts hold real standing orders outside the key's positive set, so **every reader, including the incumbent, scored 0.0** |

Each was a *silent* failure: no exception, a number printed, no gate red.

**The practical difficulty.** Anyone who measures whether a model did a task
over a corpus they built themselves runs this gauntlet. The three failures are
not three unlucky bugs; they are the three places where such a harness can be
structurally incapable of telling a correct answer from a wrong one, and each
one is invisible to a gate declared by the same person who wrote the scorer.

**Proposed practical difference.** A small stdlib-only tool that answers one
question before the number is reported: *may this instrument report a rate at
all?* It makes three measurements and refuses to print the headline figure
unless all three hold.

## The three checks

Each is a measurement over files the harness already has. None requires a model.

### C1 — concordance (key ↔ output identifiers)

The scorer joins output rows to key rows on an identifier. If the two files
name the same entities in different **types** or different **compositions**,
the join matches nothing, every lookup returns the empty case, and the harness
reports a number (usually 0.0000) that describes its own plumbing.

Reported: matched/total for every shared field name, matched/total for every
pairwise and composed concatenation of up to two shared fields, and the verdict
`SILENT_NO_MATCH` when **no** candidate pairing reaches a nonzero match rate
while both files are non-empty. The check never asserts *which* pairing the
harness uses; it reports the space and lets the reader see the zero.

### C2 — false-positive rate on correct output in a different surface form

A verifier is nearly always validated on controls whose surface form matches its
key: a value copied verbatim, or a value corrupted from the key's own string.
F118's rule, operationalised: **the control set must include the case where the
subject is right and the form is different.**

Input: control items carrying an independent correctness label and a flagger.
Output: FP rate on the correct items (Wilson 95% CI), recall on the incorrect
ones, and the verdict `ALTERNATE_FORM_FP` when the Wilson **lower** bound on the
FP rate exceeds the declared ceiling. Reported per arm, so a verifier that is
sound on the easy form and broken on the alternate form is visible as two
numbers on one instrument rather than one aggregate.

### C3 — control-arm validity

A gate whose negative arm is not negative cannot separate a reader that
hallucinates from a reader that reads correctly; it fails every subject
identically, which reads as a clean result about the subject.

Input: rows of the declared control arm, plus a predicate over a field
**independent of the key** that says whether a row carries a true positive.
Output: observed positive rate in the control arm with a Wilson CI, and the
verdict `CONTROL_NOT_EMPTY` when the observed rate exceeds the gate's declared
premise (by default: the premise is that the arm holds no positives).

### Refusal

`preflight` exits **0** only when all three checks pass. Otherwise it exits
**3** and prints the offending check with its measurement. A harness may call
`report()` and get a headline rate only on exit 0. This is the whole proposal:
**a rate that is not accompanied by the instrument's validity is withheld.**

## Cases — declared before the tool existed

The tool is not told which defect a case carries, and no case is hand-tuned.

| case | harness | committed source | expected |
|---|---|---|---|
| **A** | E116 scorer, key as committed (integer ids) | `116-berka-service-test/key.jsonl`, `answers.jsonl` | **C1 fires.** 0/80 raw match; ≥1 composed pairing recovers >0 |
| **B** | E116 scorer, key as repaired | same files, composed ids | **C1 silent.** Every pairing > 0 |
| **C** | E114 value-grounding verifier, **easy form** | values copied verbatim from `raw/text/*.txt`, independent label = present | **C2 silent.** FP ≤ 0.02 |
| **D** | E114 verifier, **alternate form** | `flags-verified.jsonl`, 24 hand-read rows with `all_parts_present: true` | **C2 fires.** FP ≥ 0.50 |
| **E** | E116 `G0_C_precision` control arm | the C arm of `key.jsonl` + the answer `detail` patterns | **C3 fires.** Observed positive rate > 0 where the premise is 0 |

Cases C and D are the pair that matters: **the same verifier, one instrument,
two arms, opposite verdicts.** A checker that cannot tell those apart is
measuring the arm, not the instrument.

## Gates

| gate | declared | meaning |
|---|---|---|
| **K1** | ≥ 4 of 5 cases produce the declared verdict | sensitivity on real committed harnesses |
| **K2** | cases B and C produce the declared *silent* verdict, and case D's measured FP rate is ≥ case C's + 0.40 | the instrument discriminates, rather than firing everywhere |
| **K3** | all 4 injected defects (key type flip, key field drop, verifier normalisation removed, control arm contaminated) are caught on a sound fixture, and the sound fixture alone is clean | generality beyond the two memorized cases |
| **K4** | `preflight` exits 3 on A, C, D, E and 0 on B, and on the injected-sound fixture | the refusal is what actually ships |

**Kill gate.** K2 < 0 or K4 failing on any case: the tool cannot be trusted to
withhold a rate, so it is not a candidate. K1 < 4 with K2 and K3 passing: it
works only on the cases it was designed on, which is evidence about this
repository's own defects rather than about anything reusable — **recorded and
not pursued.**

## Baseline — the strongest accessible alternative

What a practitioner actually does today, measured on the same inputs:

1. **the harness's own declared gates** (E114's `KG-C1`/`KG-C2`,
   E116's `G0_*`/`K1`/`K2`) — the incumbent, and the thing the tool must beat;
2. **a hand read of a sample of flags** — what F118 did, 50 rows, after the run.

Baseline 1 is the strong one: it is free, it is always available, and on all
three cases above it returned green or a clean-looking number. The experiment
records both outputs side by side. A preflight that adds nothing over baseline 1
has no use, whatever its gates say.

## Ceilings declared now

- Cases A–E are **this repository's own harnesses**. They are real and
  committed, and they are still a sample of two: one verifier, one scorer.
- C2's alternate-form arm uses labels produced by one reader (the F118 hand
  read). A different reader may disagree.
- The E114 verifier was repaired twice *after* its controls passed, while
  looking at the treatment arm's output, so its flagged rate is a record of a
  repair sequence, not a clean measurement. E124 measures the verifier **as
  committed**, which is the only version anyone would run.
- The tool validates three specific structural properties. It cannot tell a
  biased sample from a fair one, cannot tell a stale key from a fresh one, and
  has nothing to say about whether the population is representative.

## What would make this a candidate

Not the gates. The gates only say the tool works on five cases. The candidate
case is: prior art does not already do this in one command (PRIOR-ART.md), and
someone other than this repository could point it at their own harness. Both are
recorded here as requirements, and neither is established by a passing gate.