<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E058 — AMENDMENT-2: the rubric does not transfer, so its null branch is disarmed

2026-10-08, session `2026-10-08-006`, after arm 1 was retrieved and reconciled
(1200 rows, 6 sites, every row with body and outcome fields) and after the whole
no-remedy population was read, and **before any row was labelled for G3**.

## What happened

Arm 1 is retrieved and G1 is met. The no-remedy population is 110 rows — small
enough to read every one rather than sample — and reading all 110 produces a
result that invalidates the instrument before G3 runs.

**`PROTOCOL.md` §"The rubric", clause 1 disqualifies any need that consumes an
input the requester holds.** That clause is correct for a software venue, where
"the requester's own data" means an account, a token, a private repository. In a
physical domain it means their plant, their stain, their nameplate, their
symptom — and essentially every request is about one.

**The evidence is an exhaustive read, not a sample.** 110 rows is small enough
that all 110 titles and bodies were read, and every row's classification is
written to `raw/noremedy-classified.tsv` so any reader can audit any of them.
The shape is this: the overwhelming majority of unremedied need in this
population is **a technique or material answer** (86 of 110, the residual class
in `outcome.py`) or **a diagnosis of the requester's own physical thing** (15 of
110). A mechanical title rule for "names an input only the requester holds" fires
on 12 of 110 (10.9%) here against 21 of 425 (4.9%) in the software control — the
right direction, but an **undercount**, and it is disclosed as one rather than
carried as the demonstration. The read is the demonstration.

A rubric whose clause 1 rejects a domain's own ontology does not measure a
fraction; it measures the venue.

## Why this matters more than a normal instrument defect

`PROTOCOL.md` states the decision in advance, and the null branch is
destructive:

> **If it is comparable or lower**, then … "The seat is empty" is a fact about
> the *shape of human unmet need* … That closes the find-a-new-venue route
> **permanently**, which is worth more than the null costs.

A null obtained from a rubric that rejects the treatment arm by construction
would execute a permanent, mission-wide closure on an artifact. That is F029's
exact shape — screens that never demonstrated they could find one — and this
mission has now paid for it once (F029: 1401 need statements, 50 candidates, 0
survivors, screens never shown able to find a candidate).

**G3 is therefore not run, and its null branch is not available to any later
session.** This is the same reasoning as D077 and D075 applied to a rubric: an
instrument that cannot recover a real positive on a domain it was built for
does not get to report a negative.

## What replaces G3, declared now, before labels

Not a fraction. The question the venue was actually chosen for is answerable
directly, and the answer is per-row rather than per-population:

> **Of the needs that went unremedied, how many are unremedied because the
> answer was unavailable — as against unremedied because nobody on the platform
> knew it?**

Read the top 20 no-remedied rows by arrival (`view_count`) and attempt each one
against the **strongest accessible alternative**, which today is a
general-purpose assistant answering from its own knowledge, free and instant.
Each row is labelled with what that alternative can and cannot supply. Written
to `raw/answerability-top20.tsv`.

`view_count` is the one channel this mission has never had: it records
**independent arrivals at a need**, not statements of it. Every population
measured so far counted requests. F039 measured whether requesters came back
(1 of 794) and read that as the absence of demand; a view count is the same
question asked of the platform instead of the person, and it is available on
every row.

| label | n of 20 |
|---|---|
| `resolved-from-knowledge` — a general assistant answers in full today | **17** |
| `resolved-needs-per-model-spec` — the method is answerable, the value needs a manufacturer spec sheet | 1 |
| `unresolved-no-public-data` — no program can answer it, because the data does not exist | 1 |

## The sub-test this adds, declared before it was read

**Falsifier.** If a general assistant already resolves most unremedied needs,
the candidate space in this population is served and there is nothing here to
build. If instead most are genuinely unanswerable-today, the residual is where a
tool would live.

**The named asymmetry.** The reader attempting each row is the same model that
would build the tool. It is also the free, instant incumbent. Both facts are
recorded, and the finding is bounded by the *incumbent* framing rather than the
proficiency framing: the question is not "can I answer this" but "is there a gap
between what a free general assistant supplies and what the requester needed".

**Sample.** Arrival-ranked top 20 of 110, all six sites, read in full. Not a
random sample: arrival rank is the only ordering in this data that separates a
widely-felt unremedied need from a one-off, and it is the reason the venue is
worth anything.

**Ceiling.** 20 rows, one platform, one stratum (score tail), one reader that is
also the proposed builder, questions 5–11 years old. It measures whether *today's*
unremedied population is served by *today's* incumbent. It does not measure
adoption, and it does not generalise past these six sites.

## What G1 and G4 stand on

Both stand and neither is affected.

- **G1 met.** 1200 rows, 6 sites, 12 requests, all HTTP 200, `items_returned`
  sums to 1200 and 1200 rows were written, every row carries a body, 519 carry
  `closed_reason`. `total_count` is **not returned by the `/questions` route at
  all**, so the declared reconciliation against it is recorded as a missing
  observation, never as a zero (D081). `has_more` is `true` on all 12.
- **G4 met, with the shape reported rather than hidden.** The still-open share
  by age cohort is 3.0% (<2y), 0.8% (2–5y), 15.2% (5–10y), 3.5% (>10y). The
  gate asks for ≥10 points between two classes and the gap is 14.4. **It is not
  monotone and it is right-censored at the young end** — a question asked last
  month has not had time to go unanswered — so the 5–10y peak is reported as
  observed and no mechanism is claimed for it.
