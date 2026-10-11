<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Screening decisions, part 18

Split out of [`DECISIONS-SCREENING-14.md`](DECISIONS-SCREENING-14.md). This
part holds decisions taken when a **measured** capability or reach number
retires a build direction, or when a measurement's own instrument is found
wanting. Nothing was shortened to make room.

Decisions **D098, D099, D102, D103, D104**. Each entry records a choice that was
genuinely open, the options considered, and what was decided.

| id | decision |
|---|---|
| [`DECISIONS-SCREENING-18.md`](DECISIONS-SCREENING-18.md) | D098 — a prebuilt module→distribution index over a popular slice of PyPI is not a product; the conditional advantage over `pip install M` is 0.1877 and the reach is 0.3137 (E090, F111); D099 — the incumbent a gate is measured against must be the strongest one the protocol names, and E090 named three and ran one; D102 — the package-name line closes on demand: E091's 2.91% re-reads to 2–4 genuine of 858, under the 1% gate (F113); D103 — the Anova venue is closed as a route, and "unserved share" is redefined as a property of ownership composition: 13 of 20 highest-arrival appliance needs are vendor- or repair-bound, and the assistant's 5/20 is 4 of 7 answerable rows against 1 of 13 elsewhere (E091, F114); D104 — the appliance-fault-diagnosis line closes for good: on a multi-vendor knowledge venue the diagnosis population is real (44% of high-arrival unanswered rows) and 92% answerable-class, and a free general assistant serves that class at 0.81 with 0 of 40 program-shaped remedies (E092, F115) |

## D098 — The reverse index is retired; what E090 measured instead

**Decision.** Do not build a module→distribution index over PyPI, at any K.
`pyprovides/README.md`'s *what is not measured* bullet becomes **measured, and
negative**, and is corrected in place. The forward direction is untouched.

**Why.** E090 built the index over the 15 000 most-downloaded projects — 13 920
wheels read, 14 387 distinct top-level modules indexed — and it resolves **618
of 1 970** module names that real Python repositories import: **0.3137**. The
K-curve is 0.100 / 0.140 / 0.200 / 0.255 / 0.295 / 0.314, so tripling K from
5000 to 15000 bought +0.058 and 15 000 is 2.5% of the namespace. Per
`PROTOCOL.md` the run stopped there instead of looking for a K that passes.

**The number that retires it is not the coverage, it is the union.** `pip
install <module>` alone reaches 0.3305. **Together, name matching answers
0.3893** of real imported names; **0.6107 of the population is answered by
neither**. A prebuilt index can only ever redistribute that 0.3893.

**What is kept.** G3 passed at 0.0589, and in the conditional form that a
developer meets — one failing import, one module name — **among the 618 names
the index covers, `pip install M` misses 116, 0.1877**; at ≥ 2 repositories
importing a name, coverage is 0.7724 and the addition over `pip install` is
0.1655. The mechanism is confirmed cheap at 2 requests and a mean 351 KB per
project. A **query-time** reverse answer, if anyone wants one, is a different
artifact from an index and is not ruled out here; what is ruled out is paying
5.3 GB and 30 000 requests to precompute 0.31 of a name space.

**Consequences.** `pyprovides` stays a prototype, unreleased, `status: draft`.
Its remaining case rests on the forward direction (0.931, E085) and on the
conditional value above — **not** on the index.

**Reopening condition.** A reach measurement on a query-time mechanism against
the *general assistant* baseline, not against `pip install`. See D099.

## D099 — Name every baseline you declare, then run the strongest one

**Decision.** A gate's baseline is the strongest alternative **the protocol
itself names**. If the protocol lists three ways a developer could answer the
question and measures one, the result is reported as an upper bound on the
advantage and the missing arm is named in the verdict, not in a footnote.

**Why.** `EXPERIMENTS/090-reverse-index/PROTOCOL.md` named three: `pip install
<name>`, a web search, and a general assistant. E090 ran the first and modelled
it rather than executing it. F096 had already measured the third at **17 of 20**
on a different population, so the arm E090 chose is the one the mission's own
record says is the weaker. G3's 0.0589 is therefore an upper bound on the
index's advantage over what a developer actually reaches for, and the coverage
number says nothing at all about the assistant arm.

**Relation to what already existed.** D088 required a gate's reachable set to be
enumerated before the run, because E069's K1 could only be met by a
specification that installs nothing. D095 required an instrument to pass
discrimination before its numbers were read, because E088's classifier called
40% of nonexistent entities `served`. **This is the third member of the same
family: the baseline is an instrument too, and it is never checked.** E090's
G3 passed and would have been read as a reason to build.

**Consequences.** The head-to-head is promoted from a footnote in
`EXPERIMENTS/090-reverse-index/VERDICT.md` to the next experiment: real failing
imports, three arms — `pip install M`, a free general assistant, and the
mechanism — on the same cases. It reuses E044's design, which is the only
precedent in this record for running agents against real cases.
## D102 — The package-name line closes on demand; a 46-second closure is replaced by a read one

**Decision.** Close the `pyprovides` package-name line on measured demand
grounds. Retire the "Decision: BUILD" the E086/E091 readings carried in
`STATE-next-actions.md`. `pyprovides` stays a prototype, unreleased,
`status: draft`. E087's usage measurement is superseded — there is no
measured demand for usage to confirm.

**Why.** E091's classifier passed its ≥1% gate at 25/858 (2.91%), and that
figure was recorded as a demand population. The re-read (`EXPERIMENTS/
091-import-error-population/REREAD.md`, F113) hand-judged all 25 rows against
their committed bodies: 2 genuine + 2 borderline of 858 (0.23–0.47%), both
under the gate, the strict reading's CI excluding it. Session 009's
"NONE genuine" closure reached the same verdict with no commands and no
artifact; this decision keeps its conclusion and replaces its evidence.

**Options considered.** (a) Keep the line open on E091's 2.91% — rejected:
the figure does not survive its own rows. (b) Keep it open on E086's 19.35%
(6/31) — rejected: no committed corpus or verdict for that sample exists in
this checkout, and the large-sample re-read supersedes it. (c) Narrow to the
2 genuine rows' shape (beginner what-to-install) — rejected: 2 of 858 is not
a population any artifact can be built for; a differently-situated population
(IDE telemetry, beginner venues) is a new measurement, not a narrowing.

**Reopening condition.** A new population measurement, on rows nobody has
read, clearing 1% genuine "which distribution provides X?" with committed
bodies — not a re-read of E091's rows and not a retrieval-failure G1.

## D103 — The Anova venue is closed, and "unserved share" is a property of what a community owns (E091, F114)

**Decision.** Close the Anova appliance forum as a candidate route.
Retire the premise under which E062, E077, E082 and E084 were
compared: an unserved-share number is a property of a population's
ownership mix, not of its community. Any future unserved-share screen
must screen vendor- and repair-bound needs out before computing a
share, or report the mix beside the rate.

**Why.** E091 ran E062's construction — the venue's highest-arrival
unremedied needs, attempted by a free general assistant — on the Anova
cooking forum, behind a block ("no GPT-4o or Claude API access") that
the protocol's own "or equivalent" clause, two prior runs, and the
writing agent had already met. G0 discrimination passed first (10/10
answerable probes answered, 10/10 unanswerable declined, labels known
by construction). The served share was **5 of 20 = 0.2500** (Wilson
CI95 [0.1119, 0.4687]), so K1 (≥ 0.50) failed and E062's 0.85 is
rejected for this venue. But the failure is compositional: classifying
each row by the remedy its thread converged on, **13 of 20 = 0.65 are
bound to a vendor or a screwdriver**, and the assistant served 4 of 7
answerable-class rows against 1 of 13 elsewhere (Fisher one-tailed
p = 0.0307). Arm A — remedies that are a self-contained program — is
**0 of 20**.

**Options considered.** (a) Keep the venue open — rejected: 0 of 20
remedies is a program; the residual is a support queue, not a
knowledge gap. (b) Record 0.25 as a property of the community —
rejected: it conflates ownership classes, and every cross-venue number
in the record inherits the conflation. (c) Close the venue and correct
the instrument — adopted.

**Consequences.** The four structured-fault-code domain experiments
(E079, E082, E083, E084) and the Discourse baseline E077 are numbers
about populations, not communities; they are not compared against each
other or against E062 as drawn. Screens built on arrival counts
systematically over-represent broken products, because a broken product
is what generates arrivals.

**Reopening condition.** A venue whose ownership mix is reported
alongside its rate, whose answerable-class unserved share clears the
gate after vendor- and repair-bound rows are screened out, and whose
population contains a program-shaped remedy. The one class E091 leaves
open is diagnosis of a specific device from a described symptom — its
two answerable-class failures were wrong-kind diagnoses, not
refusals — and a runnable test of that class outside one vendor's own
forum is the named next action (`EXPERIMENTS/091-anova-answerability/
RESULT.md` §6).

## D104 — The appliance-fault-diagnosis line closes for good (E092, F115)

**Decision.** Close the appliance-fault-diagnosis
route, per the protocol's own K1 branch. Do not build
a diagnosis tool for appliance faults: the population
is real and reachable, the strongest accessible
alternative already serves it, and no program-shaped
remedy exists in it.

**Why.** E092 ran the test D103's reopening
condition named — a multi-vendor knowledge venue
(Home Improvement Stack Exchange, tag `appliances`)
with the ownership mix reported and vendor- and
repair-bound rows classified beside the rate. The
population is large: 44% of the 150 highest-arrival
unanswered questions are diagnosis-shaped, and 92% of
those are answerable-class — against 35% on E091's
Anova vendor forum (Fisher p = 4.7e-07). The
assistant served the answerable class at 30/37 =
0.8108, Wilson CI95 [0.6580, 0.9052]: the lower
bound clears the declared 0.50, and the share is
indistinguishable from E062's 17/20 on non-software
Stack Exchange (p = 0.764) and from Anova's own
answerable class, 4/7 (p = 0.182). Arm A is 0 of 40.

**The mechanism is composition, now measured twice.**
The overall served shares differ between venues
(0.80 vs 0.25, p = 0.000055) because the answerable
share of the population differs (92% vs 35%). Where
a venue's curation keeps vendor-bound rows out, the
assistant serves ~0.81 of what remains; where it
does not, the overall share falls — and the residue
is a support queue, not a knowledge gap. E091's
central claim survives its own "Steam" correction:
E062's 0.85 was measured on non-software Stack
Exchange (12 of its top-20 on `diy` itself), which
makes the E092/E062 agreement (p = 0.764) the
strongest cross-venue evidence the record has.

**Options considered.** (a) Reopen the line on the
7 answerable-class misses — rejected: they are
wrong-first-hypothesis errors at a 0.19 rate, not
an unserved population, and the misses are less-common
resolutions (chloramine attacking a molded
reservoir, defrost heaters stuck on), which is the
same failure shape a program would inherit. (b) Build
for the vendor- and repair-bound residue — rejected:
that residue is a support queue (D103), and it is
not a population a program can serve. (c) Close the
line — adopted.

**Consequences.** The diagnosis route is closed on
both of D103's limbs: the answerable-class unserved
share does not clear the gate, and the population
contains no program-shaped remedy. The fault-code
domain line (E079, E082, E083, E084) and the
diagnosis line (E091, E092) are both closed, on
population and on service respectively.

**Reopening condition.** A differently-situated
population — one where the answerable-class served
share clears the gate with a CI lower bound below
0.50, measured on rows nobody has read — or a
program-shaped remedy observed in a sampled
resolution. A second venue of the same shape (a
knowledge forum with curation) would be measuring
the same population twice; the record does not need
it.
