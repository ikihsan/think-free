<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E140 — is a shipped LLM judge form-invariant, and is a canonicalizer enough?

Declared 2026-10-14, **before any arm was built and before any judge output
exists**. Nothing below may be edited after the first judge call except by an
amendment file that names what it changed and why.

## The practical difficulty

Scoring open-ended model output with an LLM judge is the default in every major
evaluation framework, and it is used almost entirely as a **gate**: a score goes
down, CI goes red, someone opens a ticket. That gate is only as trustworthy as
its stability under rewording. If a judge flips a correct answer because the
number lost its thousands separator, or the list ran in a different order, or the
sentence was split in two, then a team's regressions and its improvements are
partly judge noise, and neither is diagnosable after the fact.

Two facts from this repository's own record make this concrete:

- **F118 (E114).** The mechanical value-grounding checker had a false-positive
  rate of **1.00** on faithful paraphrase of real correct answers. It was not
  weak; it was the exact inverse of a detector on that arm.
- **F123 (E124).** One verifier, five arms, false-positive rates
  **0.0069 / 0.1970 / 0.6667 / 0.9346 / 1.0000**. A quoted rate does not
  transfer between arms, so "the judge is 95% accurate" is not a usable claim
  about a judge.

E114 §"What would reopen this" named the missing number and said it was not
cheap to get: *the false-positive rate of a verifier whose comparison step
tolerates faithful paraphrase, on faithful paraphrase*. This experiment gets it,
twice — once for a **shipped judge rubric**, once for a **deterministic
canonicalizer** — on the same items, with the arms declared first.

## What this is not

It is not a benchmark of model graders, and it makes no claim that any judge is
better than any other. **One rubric from one framework, one judge model, ten
items.** The number that comes out is a number *about that rubric on that arm*,
which is exactly the unit F123 said rates belong to.

## Population — reused, not re-harvested

**E114's committed corpus**: 15 (document, question, answer) triples over 15
real Federal Register final rules, read in full by the E114 session's agent.
Nothing is refetched and no new answer is written, so every input to this
experiment is already in git and independently re-readable.

The **expert answer** the judge is given is the original answer. It is
model-produced, not gold, and that is declared as a ceiling: this measures
whether a submission matches *a real correct answer*, not whether either is
correct. E114 measured the latter separately (0 of 374 values fabricated).

**Ceiling, stated before the run:** one document genre (US federal rulemaking),
one reader, one day, and an expert answer that is not independently
authoritative.

## Arms

Every arm is a transformation of the same 15 real answers. The **corrupt** arm
reuses E114's own seeded corrupter (`EXPERIMENTS/114-value-grounding/controls.py`),
which draws the replacement from the same document so it is confusable rather
than absurd.

| arm | construction | correct verdict |
|---|---|---|
| **V** verbatim | unchanged | C |
| **P** paraphrase | deterministic surface transforms only (§Arm construction) | C |
| **P2** paraphrase, re-authored | a fresh writer rewrites the answer in different words, keeping every value | C |
| **C** corrupted | one value replaced by a plausible same-shape value from the same document | I |
| **K** truncated | one item deleted from a semicolon-delimited list, rest intact | I |

**P is the cheap arm and P2 is the arm that broke E114.** They are kept apart
because they are not the same test. P varies formatting, unit spelling, clause
order and sentence boundaries by rule. P2 varies vocabulary, by a writer. If a
verifier survives P and fails P2, the finding is that **mechanical invariance was
the wrong measurement** — which is the most useful result this experiment could
produce, and the one that most changes what a practitioner should do.

**Arm-construction gate (K4), declared before measurement.** For every item,
the canonical value multiset of P and of P2 must equal that of V. A difference
means the arm is invalid and the item is dropped, counted, and reported — it is
not evidence about any instrument.

**P2 size.** P2 is built for the 5 judge items with the shortest verbatim
answer, by a stated rule, because rewriting long answers costs more than the
measurement is worth at this sample size. P2 is therefore reported as
**illustrative, with an interval and no gate**. That is a declared limit of the
run, not a result.

## Instruments

**J1 — the shipped judge.** `inspect_ai`'s `model_graded_fact` scorer, with its
default template, its default instructions and its default grade pattern, copied
verbatim into `judge_rubric.txt`
(`RUBRIC_SHA256 6733f1db73c180db57845b5bbfcdbf5ab4c44eb962a17bbe41643962793e53b5`).
No line edited, no criterion added, no system message added. The library's own
prompt-injection neutralisation of `[BEGIN DATA]` / `[END DATA]` is reproduced.

Three deviations from how `inspect_ai` runs it, each because this session has no
API credentials, and each a cost:

1. **The judge is the session's agent, not an API model.** Labelled by model,
   not by version, because the session cannot introspect its own weights.
2. **Items are batched five to a generation.** The library sends one item per
   generation. Batching is the only way this session can afford the arm count,
   and it means position and cross-item effects are uncontrolled.
3. **Arm labels are withheld and item order is shuffled** by a seed fixed in
   this protocol, so the judge never learns which arm an item came from. This
   removes the worst confound at the cost of deviation 2.

**Seed, fixed before the run: `20261014`.** The judge subset is
`random.Random(20261014).sample(sorted(document_numbers), 10)`, and the
presentation order inside every generation is shuffled with a fresh
`random.Random(20261014)` seeded from the batch index. Both are reproducible from
`build_arms.py`, which is the only thing that chooses what the judge sees.

**M2 — the deterministic canonicalizer.** `valueset.py`: extract values with
E114's extractor, canonicalize each to a comparable form, compare multisets.
Canonicalization is the whole claim: thousands separators, decimal trailing
zeros, currency prefix or suffix, `per`/`each`, percent sign or word, case,
whitespace, and list order are all removed before comparison.

**M2's declared weakness, stated before the run.** Comparing value *multisets*
binds nothing to what the value is said to be about. An answer that lists every
right number attached to the wrong descriptions passes M2 and fails M1's
`ungrounded_claim` verdict. **M2 buys form-invariance by giving up the
claim-proximity property**, and it is not proposed as a replacement for M1; it is
proposed as the cheap pass that runs first, with M1's slower check behind it. A
pass on K1 and K2 is therefore a statement about *value correspondence under
rephrasing*, not about faithfulness.


**M1 — the incumbent.** E114's `ground.py`, run unchanged on the same arms, so
the new comparison sits beside the number it is meant to repair.

## Units, matched to denominators

This is F123 applied to this experiment's own design, and it is declared because
a gate that cannot fail is a gate that measures nothing (F010).

- **J1's unit is the answer**, n = 10 per arm. At n = 10 the smallest non-zero
  rate distinguishable from zero is 0.10, and 0 of 10 has a Wilson 95% upper
  bound of **0.278**. **J1 therefore carries no point gate.** Every J1 number is
  reported as an interval, and the decision it supports is stated as an
  interval.
- **M2's unit is the value**, n ≈ 374 across the corpus. This is where a ≤0.02
  gate is reachable, so this is where the gates are.

## Gates, declared before measurement

| gate | instrument | arm | unit | declared | meaning |
|---|---|---|---|---|---|
| **G0** | J1 | C | answer | grades I on **≥ 0.667** (10 of 15 judge items) | a judge that cannot find a swapped number is not an instrument; if G0 fails the comparison is void and the failure is the result |
| **K1** | M2 | C | value | recall **≥ 0.95** | detection |
| **K2** | M2 | P | value | false positives **≤ 0.02** | form-invariance — E114's own gate, on the arm E114 never built |
| **K3** | M2 | V | value | false positives **≤ 0.02** | the arm builder did not damage the control |
| **K4** | — | P, P2 | item | canonical multiset equals V | arm validity; failure drops an item and is reported |
| **J1-observed** | J1 | V, P, P2 | answer | *no gate* | false-positive rate on correct-but-reworded answers, with Wilson 95% interval |

**K2 on P only, not on P2.** K2 is a gate on a mechanism whose every input is
machine-checkable. P2 has n ≈ 120 values and a writer in the loop, and a
failure there would not distinguish "the canonicalizer is form-sensitive" from
"the rewrite drifted", which K4 is built to detect but can only bound. **P2 is
therefore reported beside K2 and never inside it.**

## Kill gate for the line, declared before measurement

**If M2 fails K1 or K2, no artifact is built and the line closes.** That result
would say: no cheap deterministic verifier of this shape survives faithful
rephrasing, which extends E114's "the verifier is dead, not the subject" from
a mechanical checker to the shape itself, and `preflight` must not ship a value
rate it cannot defend.

**If M2 passes K1, K2, K3 and K4,** the build trigger fires: `valueset.py`
becomes a candidate artifact and the *generality* test — a second document genre
— is the declared next action, not an optional extra. A pass on this corpus is
evidence of mechanism, not of generality, because the extractor was written
against this corpus's value shapes.

**J1 does not enter the kill gate.** It is underpowered by construction and
labelled so. It is the comparison the practitioners actually want, and the
honest form of that comparison at n = 10 is an interval.

## Ceilings, declared before measurement

- One genre, one reader, one day; expert answers are model-produced.
- One rubric from one framework, one judge model, no panel, no majority reducer.
- Five items per generation, order shuffled, arms unlabelled, but position and
  cross-item effects uncontrolled.
- P2 is five items and illustrative.
- K2's threshold of 0.02 is E114's gate, inherited rather than derived. It is a
  demanding bar, and a pass means "not merely a paraphrase detector" rather
  than "as good as a reader".
