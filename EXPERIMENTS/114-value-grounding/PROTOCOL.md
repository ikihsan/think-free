<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E114 — does a free general assistant ground the values it reports in a source document?

Declared 2026-10-12, before any document was fetched and before the checker
was written. Nothing below may be edited after the first fetch except by an
amendment file that names what it changed and why.

## The question, stated as one number

When a free general assistant is given a real document and asked a question
that turns on specific values, **what fraction of the values in its answer do
not occur in the document?**

This is not the model's general hallucination rate. Those are published for
factual QA. This measures one mechanical property that is decidable without a
judge: *can every number, date, money amount, count and identifier in the
answer be found in the source?*

## Why this population

E092, E091 and E062 already measured that a free general assistant **serves**
need-shaped questions better than the mission expected (0.81 on the answerable
class of a real repair venue). Screens looking for an "unserved need" are
exhausted. This experiment does not look for an unserved need. It looks at a
**task the assistant is already being asked, en masse, and doing silently** —
reading a document on someone's behalf — and asks whether the answer carries
values that are not in the document.

Documents chosen: **US federal court opinions from CourtListener**, because
they are (a) public domain and fetchable without an account, (b) non-software,
(c) numerically dense — docket numbers, filing dates, dollar amounts, page and
paragraph cites, counts, statute sections — and (d) consequential, which is the
regime where a silently wrong value costs something. This is a **convenience
sample of one document genre**, not a sample of documents.

## Design

**Unit:** one (document, question, answer) triple.

**Treatment arm (A).** The agent running this session is the free general
assistant. It reads a fetched document and answers a question about it, in
ordinary prose, without any tool. Every answer is **written to
`answers.jsonl` and committed before the checker exists**.

**Positive control (B).** For each answer, a script replaces exactly one value
with a plausible value of the same shape (same digit count, same unit, same
place in the sentence), seeded from the document so the corruption is
*confusable*, not absurd. A checker that cannot fire on B is not an instrument.

**Negative control (C).** For each answer, the same script builds a reply that
is a set of verbatim sentences from the document. A checker that fires on C is
measuring the wrong thing.

**Instrument.** `ground.py`, a mechanical checker. It extracts values from the
answer, normalizes the document, and reports each value as
`grounded` (occurs in the document), `ungrounded` (does not), or
`undecidable` (a class where the comparison is not well defined). It never sees
which arm a row came from.

## Kill gates, declared in advance

| gate | statement |
|---|---|
| **KG-A** | **If the treatment arm's ungrounded-value rate is below 2% of checked values, the class does not support a tool** and the line closes. The population is then served on this property, as E092's was on its own. |
| **KG-C1** | The checker must achieve **recall >= 0.90 on arm B** (corrupted values caught). Below that it is not an instrument. |
| **KG-C2** | The checker must achieve a **false-alarm rate <= 0.02 on arm C** (verbatim sentences not flagged). Above that it is measuring normalization noise, not hallucination. |
| **KG-D** | If KG-C1 or KG-C2 fails, the run returns **`not_evaluated`**. It does not return a rate for arm A, because an instrument that cannot separate B from C cannot be asked about A. |

## What this cannot establish, stated now

- **It is one rater.** The treatment arm is one agent, one document genre, one
  prompt style. A rate here is a rate *for that*, not for assistants in general.
- **The checker's ungrounded verdict is not a proof of error.** A value can be
  correct and absent from the document because it was derived (a sum, a
  conversion, an inference). Every ungrounded value is therefore hand-read and
  classified `fabricated` / `derived` / `ambiguous` before any rate is quoted.
  **The headline number is the fabricated rate, not the ungrounded rate.**
- **KG-A is a gate on the class, not on the agent.** Arm A failing KG-A closes
  the tool idea, not the reading that assistants are reliable here.

## What would make this worth building if it survives

Not the checker. The checker is 150 lines and a commodity. What would be worth
building is the thing the checker demonstrates is missing from every pipeline
that ships LLM document extraction today: **a cheap, complete, mechanical
attestation that the answer's values came from the document, with the failures
enumerated instead of summarized.**
