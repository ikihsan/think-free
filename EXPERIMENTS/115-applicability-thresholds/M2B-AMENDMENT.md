<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E115 M2b — AMENDMENT 1, declared after M2's result and before M2b was run

M2 returned **14/14 = 1.0000**, kill gate met. Before closing the line on
that number I have to ask whether the test could fail at all, and the honest
answer is that it might not have: **I wrote the cases and I answered them.**

The specific defect: M2 handed the assistant the exact clause that decides each
case. A person asking a real compliance question does not have the clause in
front of them; they have the facts and the question, and the clause has to be
*found*. M2 therefore measured **application of a quoted counting rule**, and
the real workflow requires **finding it first**. Those are different tasks and
the second is the one a tool would have to help with.

So M2's number is an **upper bound on service**, not a measurement of it.

## M2b, declared now

Same 14 cases, same committed key at `ab5f9de8`. **One change: no clause text
is supplied.** The arm is given the facts, the question, and nothing else —
no verbatim regulation text, no citation, no pointer to a section. It may
consult the committed `parts-title29.jsonl` harvest, which is the same public
data any person would have.

The discriminating quantity is **the counting-rule subset only** (P2, P4, P6,
P8, P10, P7b). The other eight are the cases a search engine answers and they
are reported for context, not as evidence.

### Declared outcome before running

- **M2b ≥ 0.95 on the counting-rule subset** → the population is served
  end-to-end, the line closes, and the honest statement is that a free
  assistant finds *and* applies the counting rule on cases a tool could serve.
- **M2b < 0.95** → the interesting case. It would mean the service in M2 came
  from being handed the clause, which is evidence about the *workflow*, not
  about the model. It does **not** on its own make a tool: a tool must beat
  the incumbent, and the incumbent here is a person with the CFR open.

### The defect this amendment does not repair

**Both arms are still one reader.** M2b removes the clause from the prompt; it
does not give me an independent mind that has not already read every one of
these sections during M1. I have read 825.104, 825.105, 825.111, 1904.1,
1904.2 and 1910.38 in full in this session, so recall of the rule is available
to me whether or not the prompt quotes it. **M2b is a weak instrument against
exactly the effect it is meant to expose**, and any result from it is reported
as `single-reader, prompt-ablation`, not as a measurement of the population.

What would actually repair it is a second agent that has not read the
harvest. That is not available in this session, and the honest report is that
**the line closes on the M2 number with a stated ceiling, not on a
cross-population measurement.**