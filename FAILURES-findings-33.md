<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-08
-->

# Findings 33 — a rubric that rejected its own treatment arm, and the
# instrument this mission never had

`observed` 2026-10-08, session 2026-10-08-006, VM `instance-20260717-0944`.
Evidence: [`EXPERIMENTS/062-nonsw-need-shape/`](EXPERIMENTS/062-nonsw-need-shape/README.md).

Split out of [`FAILURES-findings-32.md`](FAILURES-findings-32.md) on 2026-10-08.
**Identifiers are stable across all findings files.**

## F095 — a rubric clause written for a software venue disqualified a physical domain's needs, and its null branch would have closed a route permanently

**What happened.** E062 was declared to answer whether the mission's empty
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

**What it buys.** D083, below. G3 is not merely unfavourable; its null branch is
**permanently disarmed** and unavailable to any later session, and the
find-a-new-venue route is **deferred with the reason recorded** — a different
standing from closed, and the only honest one available.

## F096 — "the requester never came back" was never evidence that the need went unserved

**What happened.** F039 measured, on 794 requesters in one corpus, that 1 replied
again and that 0 of 77 whose need drew a link followed up, and read the result
as the absence of demand. E062 read the whole no-remedy population of a second
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
sat unanswered for 9.0 years at 15,635 views. D084 below.

## F097 — the population that resists a program resists it because the data was never recorded

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

The two rules this experiment's reading produced are **D083** (a rubric clause
that cannot recover a positive on its own domain disarms its own null branch,
permanently) and **D084** (arrival at a need is a different quantity from a
statement of need). Both are recorded in
[`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md), which is where a rule
belongs: this file holds findings, and no other findings file defines a
decision.

## F098 — the mission's need corpus selects statements that are already served, and it has no unserved tail

**What happened.** E063 ran the E062 instrument on the two corpora every
candidate screen in this repository consumed. G1 control 10 of 10 served
recovered, 9 of 10 unserved recovered (the one miss, `C08`, reported rather
than relabelled). G2 remedy verification 22 of 23 after a declared channel
correction (the first round resolved 18 of 23 — five artifacts on the wrong
channel or owner, kept in `raw/remedy-verification.json`). G3 was a same-reader
pass and would have measured memory, so it was replaced by a declared
sensitivity analysis (AMENDMENT-1, A3).

**The measurement.** Arm A (71 HN need rows): **served share 0.676** (48 of 71,
CI95 0.561–0.773); over the 59 rows that state a need at all, 0.814. Arm B (32
`stg` demand issues): **0.969** (31 of 32). **`unserved-open` — the only label
that can open a candidate — is 0 of 103 rows.** The resistant rows resist
because the data was never recorded (F097's shape), because the remedy is human
work or an institution, or because the row states no need at all. 12 of 71 arm A
rows carry a trigger phrase and state nothing requestable: trigger filtering is
not a need filter. Arm B's 0.969 is mostly already-met work — 25 of 32 rows were
closed when read, including one GUI that shipped the exact line-level staging
`stg` was built for — so it is not an independent confirmation of arm A.

**What it buys.** Seven emptiness measurements in this repository (F029, F039,
F051, F059, F081, F084, F085) were not wrong about the domains they sampled;
they were reading a route that selects served statements. A trigger-phrase
harvest over HN/GitHub is now retired as a candidate source without a
candidate. This does not measure demand or difficulty, and a low served share
on it would not have opened one either.

## F099 — "it exists" is a materially insufficient answer: 16% of plausible near-miss names resolve to a real, different artifact

**What happened.** E064-A1 (session 2026-10-08-014) measured the
failure mode complementary to the hallucinated-package-name rate the
literature publishes (Krishna et al., arXiv:2501.19012, ICML 2025:
0.22 %–46.15 % per ecosystem, whose remedy is "resolve the name
against the registry"). Ground truth is definitional, so no labeller
is involved: mutate a real package name the way a model does when it
half-remembers one (suffix/prefix/synonym families, fixed before any
registry was read), and the intended artifact of every mutation is the
original — so any mutation that resolves is a **false accept by
construction**. 37 seeds in 5 ecosystems, 576 mutations, checked
against the registries themselves (`registry.py`, model-free, 13
ecosystems).

**The measurement.** **93 of 576 mutations resolve: 0.1615, Wilson
CI95 [0.1337, 0.1937]** — npm 0.278, PyPI 0.167, crates 0.156,
RubyGems 0.063, Packagist 0.000 (its `vendor/pkg` shape makes a
same-vendor collision the only way to fail). Zero `unknown` verdicts,
so no missing observation sits in the denominator. The declared
discriminability rule (downloads < 1 000; badge/empty description;
newest release > 3 years old; no repository URL — clauses dropped,
never zeroed, when a registry does not carry the field, D082) **failed
its recall arm**: it flags 69 of 93 false accepts (0.742, gate 0.90)
while correctly leaving 29 of 30 real registry-listing names alone
(0.967). The 24 it misses are healthy, popular, maintained projects —
`jinja2-cli` (11.2 M downloads/yr), `sqlalchemy-utils`, `django-click`
(1.7 M), gem `async-redis` (863 K) — indistinguishable from the real
class on every declared signal. Some are the seeds' de-facto companion
libraries, which is why the failure is silent: the install succeeds and
the package does something adjacent.

**What it buys.** The existence bit that every installer, IDE, and
existence checker returns is necessary and, 16% of the time on this
population, insufficient — and the cheap deterministic repair this
protocol fixed in advance does not work, because the residual is
semantic ("does this package do what was asked"), which is the named
alternative's job (a model call) and takes the cost and determinism
advantage with it. The original E064 candidate — a deterministic
cross-ecosystem pre-install checker — would have *confirmed* 16% of
the wrong names it was asked about; its success case is the failure
case. No candidate opened, no prototype written (D086). The instrument
(`registry.py`, `meta.py`) is reusable, and the rate recomputes from
committed bytes via `outcome.py`. Ceiling: one author's idea of
plausible mutation, 37 fame-selected seeds, five ecosystems, one day;
the real near-miss distribution of model output is a different sample
(the withdrawn G2 — the non-existent tail is already published).
