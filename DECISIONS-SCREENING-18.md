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

Decisions **D098, D099**. Each entry records a choice that was
genuinely open, the options considered, and what was decided.

| id | decision |
|---|---|
| [`DECISIONS-SCREENING-18.md`](DECISIONS-SCREENING-18.md) | D098 — a prebuilt module→distribution index over a popular slice of PyPI is not a product; the conditional advantage over `pip install M` is 0.1877 and the reach is 0.3137 (E090, F111); D099 — the incumbent a gate is measured against must be the strongest one the protocol names, and E090 named three and ran one |

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