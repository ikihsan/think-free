<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-08
-->

# Findings 33 — a rubric that rejected its own treatment arm, and the
# instrument this mission never had

`observed` 2026-10-08, session 2026-10-08-006, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/058-nonsw-need-shape/`](EXPERIMENTS/058-nonsw-need-shape/README.md).

Split out of [`FAILURES-findings-32.md`](FAILURES-findings-32.md) on 2026-10-08.
**Identifiers are stable across all findings files.**

## F090 — a rubric clause written for a software venue disqualified a physical domain's needs, and its null branch would have closed a route permanently

**What happened.** E058 was declared to answer whether the mission's empty
candidate seat is a property of *human unmet need* or of its *software sample
route*, by comparing a non-software population against the software corpus
already on disk. The decision was stated in advance, and the null branch was
destructive: comparable-or-lower was to be recorded as "the seat is empty is a
fact about the shape of human unmet need", closing the find-a-new-venue route
**permanently**.

Arm 1 retrieved 1200 rows across six non-software Stack Exchange sites. The
no-remedy population is 110 rows. **All 110 were read** — the population is small
enough that sampling adds nothing — and every row's classification is written to
`raw/noremedy-classified.tsv` so any of them can be audited.

**What was found. The rubric's clause 1 disqualifies any need that consumes an
input the requester holds.** That is right for a software venue, where the
requester's own data means an account, a token, a private repository. In a
physical domain it means their plant, their stain, their nameplate, their
symptom. The shape of the 110 rows is 86 technique-or-material answers and 15
diagnoses of the requester's own physical thing. A rubric whose disqualifying
clause rejects the treatment arm's ontology does not measure a fraction.

**A mechanical rule is disclosed as an undercount.** "Names an input only the
requester holds", applied to titles, fires on 12 of 110 (10.9%) in arm 1 against
21 of 425 (4.9%) in the software control — the right direction, far too small to
carry the argument. The **exhaustive read** is the demonstration; the regex is
reported because it was run and it undercounts.

**Why this is a failure rather than a fix.** G3 was declared as the measurement
and the gate that would produce the answer. It was not run, because a null from
this rubric would have executed a permanent mission-wide closure on an artifact
of the instrument. F029 is the same shape already paid for once: 1401 need
statements, 50 candidates, 0 survivors, and screens never demonstrated able to
find a candidate. The difference here is that it was caught **before** the
closure, by reading the population before labelling it — D077's rule, applied to
an instrument instead of a candidate.

**What it buys.** D082, below. G3 is not merely unfavourable; its null branch is
**permanently disarmed** and unavailable to any later session, and the
find-a-new-venue route is **deferred with the reason recorded** — a different
standing from closed, and the only honest one available.

## F091 — "the requester never came back" was never evidence that the need went unserved

**What happened.** F039 measured, on 794 requesters in one corpus, that 1 replied
again and that 0 of 77 whose need drew a link followed up, and read the result
as the absence of demand. E058 read the whole no-remedy population of a second
population (110 rows) and attempted the top 20 **by arrival** against the
strongest accessible alternative — a general-purpose assistant answering from
its own knowledge, free and instant.

| what the free alternative supplies today | n of 20 |
|---|---|
| a full answer | **17** |
| the method only; the value needs a manufacturer spec sheet | 1 |
| nothing reachable | 1 |

**What was found.** The 17 are not gaps. They are rows a forum left open because
nobody who knew the answer was on that forum between 2009 and 2016, and they
are now answered for free in seconds. **Unanswered on a platform is not
unserved.** Someone whose boiler question is answered by an assistant in 2024
does not post on a forum either way, so reply rate cannot distinguish "served
elsewhere" from "never served".

**Why this matters to the standing record.** Every population this mission has
measured counted **statements of need**. F039 measured whether requesters
returned. Neither measured **service**. The mission has been reading a count of
requests as a count of unmet service for the whole of its record, and this is
the first direct evidence that the two come apart by a factor of 17 in 20.

**What it buys.** The instrument: **`view_count` records independent arrivals at
a need**, on every row, and it is the channel this mission has never had. The
unremedied population here is 110 rows carrying 118,990 views, one of which has
sat unanswered for 9.0 years at 15,635 views. D083 below.

## F092 — the population that resists a program resists it because the data was never recorded

**What happened.** The 5% of the arrival-ranked top 20 that a free assistant does
not answer is not a software problem. The bike serial number `SNACEOSF18391`
decoded by no source I could reach. The nearest incumbent is Bike Index, a
501(c)(3) with over 1,844,000 cataloged bikes, tens of thousands of daily
searches and an API (`bikeindex.org/about`, fetched 2026-10-08) — and it is a
*registration* service, so an unregistered 2001 BMX is absent by construction.
The refrigerator capacitor is the same shape: the method is free knowledge, the
value is one of thousands of per-model spec sheets nobody made queryable.

**The ceiling on this claim.** My own lookup of that serial returned a
client-side, rate-limited page rather than a result. The label is "no free
source I could reach decoded it", **not** "no source exists".

**What it buys.** A boundary on where a tool can live at all: a need whose answer
is a record nobody kept is not buildable, and the tools that appear to serve it
are registration schemes — which move the burden of creating the record onto the
person who has the object. That is a design observation about the class, not a
candidate, and it is stated here so a later session does not re-derive it by
building one.

The two rules this experiment's reading produced are **D082** (a rubric clause
that cannot recover a positive on its own domain disarms its own null branch,
permanently) and **D083** (arrival at a need is a different quantity from a
statement of need). Both are recorded in
[`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md), which is where a rule
belongs: this file holds findings, and no other findings file defines a
decision.
