<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Findings — failures and negative results, part 41

Split out of [`FAILURES-findings-40.md`](FAILURES-findings-40.md), which held
F119-F124 and was at 281 of 300 lines. See [`FAILURES.md`](FAILURES.md) for the
index. **Identifiers are stable across all findings files.**

## F125 — the verifier question is two questions, and only one of them is solvable cheaply

**Observed 2026-10-14**, session `2026-10-14-001`,
[`EXPERIMENTS/140-judge-form-invariance/`](EXPERIMENTS/140-judge-form-invariance/RESULT.md).

E114 closed with: the subject was fine (0 of 374 values fabricated) and the
**verifier was dead** — a checker that passed every declared gate had a
false-positive rate of 1.00 on faithful paraphrase, and named as the missing
number *"the false-positive rate of a verifier whose comparison step tolerates
faithful paraphrase"*, adding that it was not cheap to get. E140 got it, three
times, on one corpus, with the arms declared before the instruments ran.

**Population.** E114's 15 committed (document, question, answer) triples over 5
real Federal Register final rules; 241 numeric and 398 canonical values. Judge
arm 31 items in 7 batches: 10 verbatim, 10 surface-transformed, 4 re-authored by
a blind writer, 7 corrupted.

| instrument | FP on verbatim | FP on surface-paraphrased | FP on re-authored | detects a swapped value | detects an omission | detects a misattribution |
|---|---|---|---|---|---|---|
| M1 `ground.py` (E114's) | 0.3727 | 0.4651 | 0.6019 | 9/11 | — | 6/6 |
| M2 `valueset.py` (canonicalizer) | **0.0000** | **0.0000** | **0.0000** | **11/11** | 11/11 | **0/6** |
| J1 shipped `inspect_ai` `model_graded_fact` | 0/10 | 0/10 | 0/4 | 6/7 | not run | not run |

Every rate in the three false-positive columns is a *false*-positive rate because
K4 machine-verifies that each arm carries the identical value multiset as the
verbatim answer. J1's 0/24 correct answers is Wilson CI95 [0.0000, 0.1380]; its
6/7 detection is [0.4869, 0.9743].

**What is disproved.** Not the judge: it produced zero false positives on 24
correct-but-reworded answers and found 6 of 7 swapped values, including a
transposition inside a telephone number. The **incumbent mechanical verifier is
disproved as a gate, and this time quantitatively**: its false-positive rate is
not a constant that transfers between arms (F123) but a **monotone function of
how far the input has been reworded** — 0.3727 verbatim, 0.4651 after mechanical
surface transforms, 0.6019 after a writer re-authored the same answer in
different words. E114's 0.3717 reproduces here independently, and the 1.00 of
F118 is the far end of a curve rather than an outlier.

**The finding that changes a build decision.** The paired measurement — *was the
swapped value itself the flagged one?* — gives M1 **9/11**, where differencing
aggregate flag counts gives **6/11**. M1 detects most substitutions while
flagging 37–60% of correct values, so a flag from it is worth about as much on a
correct answer as on a wrong one: it is not a paraphrase detector, it is a
paraphrase detector of the wrong thing, and its detection is inseparable from its
noise. **E114's "the verifier is dead, not the subject" stands, and is now a
measurement rather than an assertion.**

**What survives, and is the first positive build trigger this line has produced.**
`valueset.py` — canonicalise each value (separators, decimal trailing zeros,
currency placement, `per`/`each`, percent sign or word, case, whitespace, list
order) and compare multisets — passes every declared gate: **zero false
positives in 929 values** across three correct arms, 11/11 substitutions, 11/11
omissions, K4 15/15 and 4/4. G0 passed first (6/7 ≥ 0.667), so the comparison
was not void.

**And the weakness the protocol declared, now `observed` rather than inferred.**
PROTOCOL.md named M2's blind spot before the run: comparing multisets binds
nothing to what a value is said to be about. Six mechanical misattribution arms
were built (one value transposed onto the wrong subject, K4-preserving) and **M2
detected 0 of 6**; M1 flagged 6 of 6. So the cheap pass is blind to binding by
construction *and by measurement*, while the only instrument here that sees
binding is the one twice measured unusable as a gate. **The expensive check
cannot be replaced, only deferred** — M2 is a pre-pass that removes omissions and
substitutions (22 of 22 of the wrongness built) and hands on the binding
question, which is now the open problem rather than an assumption.

**One practitioner finding with no counterpart in F118/F123.** J1's single miss
was a corrupted billing code, `4915-01-P` → `1247-01-P`. The judge **found the
discrepancy in writing** — "This is a factual discrepancy in a data value, not a
style or punctuation difference" — and then graded it **correct**, because the
question asked for CFR, U.S.C., docket and FR-document numbers and a billing
code is none of those. The failure is the rubric's *scope clause outvoting
evidence in front of it*: a different defect class from context-word mismatch,
and one that a re-run at larger n does not fix.

**Ceilings, all declared before the run.** One genre, five documents, one reader,
one day; expert answers are model-produced, not gold. One rubric, one judge
model, no panel, no majority reducer, uncontrolled model variation between the
seven batches. Misattribution by transposition only — a binding wrong in prose is
`untested`. **Generalisation is the declared next action and is not done**: the
extractor was written against this corpus's value shapes, so a pass here is
evidence of mechanism and not of generality.

**Corroborates** F118, F123. **Consumes** the number E114 named as the one it
could not afford. **Produces** a candidate artifact (`valueset.py`) whose scope
is fixed by measurement: *value correspondence under rephrasing*, never
faithfulness.
