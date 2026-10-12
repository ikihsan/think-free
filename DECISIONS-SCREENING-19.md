<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# Screening decisions, part 19

Split out of [`DECISIONS-SCREENING-18.md`](DECISIONS-SCREENING-18.md), which was
at 291 of 300 lines. This part holds the decisions taken when a candidate is
closed by **building the thing and measuring it**, rather than by screening a
population.

Decisions **D106**. Each entry records a choice that was genuinely open, the
options considered, and what was decided.

| id | decision |
|---|---|
| [`DECISIONS-SCREENING-19.md`](DECISIONS-SCREENING-19.md) | D106 — a verifier is validated on the population it will be used on, not on the populations it is convenient to construct: E114's checker passed both its declared controls (recall 1.0000 on corrupted answers, 0.0069 false alarms on verbatim spans) and then flagged 0.3717 of real values with a false-positive rate of 1.00, because the arm it was never tested on is faithful paraphrase with nothing invented; the value-grounding tool line is closed and the population is served at 0 of 374 fabricated (E114, F118) |

## D106 — a verifier is validated on the population it will be used on

**Date:** 2026-10-12. **Evidence:** E114, F118.
**Supersedes:** nothing. **Depends on:** D058 (a control is chosen on the
property being tested, not on use), D060 (a kill rests on the artefact doing what
the clause asked).

### The choice

E114 proposed a product: a cheap mechanical attestation that every number, date
and citation in an answer about a document came from that document. Before
building it, the mission had two options and the record says which to take.

1. **Screen the population.** Read documents, ask a free general assistant the
   questions people ask, and measure how often it reports values the document
   does not contain. If the rate is high, build the checker.
2. **Build the checker and validate it.** Write the verifier first, give it
   adversarial controls, and only then ask it about real answers.

Option 1 is what every candidate in this record has done, and E092 is the
closest precedent: run the strongest alternative on the real population and read
the result. It is cheaper and it tests the thing that matters. It was chosen
again here, and the product idea died at the measurement.

### What was decided

**Both, in that order, and the second one is the binding constraint.** The
verifier was built and given two declared controls. It passed both — recall
**1.0000** on corrupted answers across both corruption flavours, and a
**0.0069** false-alarm rate on verbatim document spans, against declared
ceilings of 0.90 and 0.02. It then flagged **0.3717** of the values in real
answers, and **every flag was wrong**: 24 of 24 `ungrounded_value` verdicts have
every part of the value present in the document, and 50 of 50 hand-read
`ungrounded_claim` flags are correct.

The verifier's false-positive rate on the population it exists to serve is
**1.00**, Wilson 95% lower bound 0.9286. A tool that cannot distinguish a
correct answer from a corrupted one is not a tool.

### The rule that follows

**A verifier's control must include the case where the subject is right and the
form is different.** Both of E114's controls were too easy, and they failed in
opposite directions:

- a *verbatim* negative control validates the case where the answer **is** the
  document, which is not what any user submits;
- a *corrupted* positive control validates the case where the value is wrong,
  which is not what a faithful reader produces.

Real answers are **faithful paraphrase with nothing invented**, and that arm was
not built until after the run had been scored. The instrument has no way to
notice that it is being asked the third question: verifying a paraphrase is a
semantic judgement, which is the cost the tool was built to avoid.

### Consequences

1. **The value-grounding tool line is closed.** Not "closed at this maturity" —
   closed, because the cheap verifier is the product and it does not work. A
   verifier that spends a language model on the paraphrase step is a different
   instrument with a different cost, and this run says nothing about it; that is
   named as open rather than claimed.
2. **The population is served on this property.** 0 of 374 fabricated values,
   Wilson 95% upper bound **0.0098**, against a declared kill gate of 0.02. This
   is the seventh measured instance of the mission's recurring result — an
   assistant the mission expected to fail on a class of work serves it — and it
   is now measured on the one property where a mechanical, judge-free check is
   possible.
3. **"LLMs invent numbers when reading documents" is withdrawn for this
   population.** It is a widely repeated claim. It was testable without a judge
   and it did not survive contact with 374 values from five real rules.
4. **A process rule for every future instrument in this record.** Before an
   instrument is run on a real population, name the arm that is *right but
   differently worded* and build it. AMENDMENT-2 is the worked example of what
   happens without one: the first checker was discarded at a 0.367 false-alarm
   rate rather than repaired into a result.

### What this decision does not claim

- **One rater.** The treatment arm is this session's agent, one document genre,
  one prompt style. `0 of 374` is a fact about that, not about assistants.
- **Not a measurement of the flag rate.** `ground.py` was repaired twice after
  its controls passed, while looking at arm A's output. The flag rate fell
  0.782 -> 0.684 -> 0.372 across those repairs, so it is a number produced by an
  instrument tuned on the arm it reports and is not an estimate of that arm. The
  hand-read of the flags is unbiased with respect to the instrument, and it is
  the number the decision rests on.
- **Not other genres.** Contracts, invoices, medical records and tabular
  spreadsheets put a different distance between a label and its value, and that
  distance is exactly the variable that decides this.