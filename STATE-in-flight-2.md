<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# In flight, part 2 — closed readings kept for their bearing on open ones

Split out of [`STATE-in-flight.md`](STATE-in-flight.md) on 2026-10-05, which was
at the 300-line cap with two further readings to add. **This file holds readings
that are closed but whose reasoning a later reader of an open item will need**;
the live readings stay in the file this one was split from, so that a rewrite of
one does not force a rewrite of the other. Identifiers are stable across the two.

Read a finding number and go to the file it is defined in.

## What actually killed the candidates

**Status: closed for the count, open for the reliability (F044, T-0068).
`EXPERIMENTS/024-kill-reason-causes/`.** Kept here because item 0's premise was
carried by four summaries and had never been counted from a primary source.

| | |
|---|---|
| population | **20 rows**, not the twelve four files stated |
| `prior_art` | **10 of 18 eligible = 0.556** — survives a 50% floor by one row |
| `falsified_mechanism` | 4 — A1 (F006), B1 (F001), C2 (F008), E3 (F012) |
| `information_insufficient` | 3 — D1, D2, D5 |
| `unrecorded` | 1 — B2, promoted then parked with no reason stated |
| excluded | 2 — E1, E2 were never candidates |

**The sensitivity is the finding.** Every one of the 10 prior-art rows, moved to
any other declared category, puts the share at 9/18 = 0.500 and kills the
majority reading. Six rows are contested by the declared precedence and moving
all six also kills it. So the sentence "prior art is the dominant kill reason" is
a **plurality with a one-row margin**, not a majority.

**Seven of the 18 died of something else**, in three distinct shapes: a
mechanism its own test refuted or confirmed into uselessness (E3's mechanism
*worked*, which is why there was nothing to build), a claim no available
observation could establish, and one promoted then parked with no reason at all.
F006 is the sharpest: A1's mechanism passed a count budget and failed 6/6 under a
walking-distance budget its own report never priced — a gate missing at report
time, not a search failure.

**Why it matters for item 0.** The record's implicit model was that every
candidate died because the world already had it, which makes the problem "our
ideas are not novel." For at least 7 of 18 that diagnosis is wrong, and the
repair differs: **promote fewer claims and price each one's gate before
promoting it.** That is now an option for the owner decision with a count behind
it, alongside the axes item 0 already named.

**What is still open, and it is the same shape as E023's.** One reader, no
second coder — at a one-row margin, **κ on the same 18 rows by an independent
reader is what would settle whether the record's sentence is a fact or a
coin-flip.** Not run.

**Ceiling.** A count over the record as written. It falsifies no prior-art
verdict and reopens no candidate — F035 already measured that separate question
on F029's population and found 3 of 12 adjudicable kills had no prior art.

## Is a screen whose premise is unmeasurable four times in five a screen?

**Status: closed as an open reading, with one question left (F034, F037, F041).**
Was item 0c of `STATE-next-actions.md`, moved here when F041 made the ranked
list's entry redundant.

F034 could read serving evidence for **57% of the incumbents its own population
contained and 22% of the young arm** — which is a statement about the world's
distribution rather than about this repository's tooling. F037 measured the
fraction and it is **high exactly where the candidates live: 14 of 18 young rows
undecided, 13 of them tools, and 43% of the mature arm.** It also showed
undecidability does **not** track artifact class — 10 of the 14 unreadable young
rows are executable — so "this is just a document" never explains an unreadable
row. F041 then found the missing channel is a *smaller* one, and that its own
blind spot is the placebo arm.

**What remains open is whether the unmeasurable fraction predicts anything about
the need**, and its falsifier is a population where that fraction is near zero.

**Ceiling, and it is the reason this is a reading rather than a verdict:**
015's `placebo.py` shows the instrument *can* read unpopular projects when it looks
for readable ones, so "unmeasurable" is partly an artefact of which channels were
consulted. **A follow-up must state its channel set or it measures the
instrument.** That is now also the fifth condition of
[`docs/process/experiment-protocol.md`](docs/process/experiment-protocol.md)'s
prior-art rule.

## The demand-side absence of recurrence survives a change of venue (F039, F049, F051, F053, F054)

**Status: closed, and now on two venue classes instead of one.** Item 0d's last
standing question. **F053** counted what the closure stood on and found one
platform; **F054** changed the venue and nothing else. Full reading below; raw
evidence in [`EXPERIMENTS/032-venue-recurrence/`](EXPERIMENTS/032-venue-recurrence/README.md).

**What the two populations now say.** F039 found the need corpus is **1250
individuals each asking once**, with no need-level recurrence inside it. E031
reached the same reading from a **structurally different** population — 919
departure accounts from people who had depended on the thing, 326 of them framed
as seeking an alternative — and found **0 recurring requirements in 63 clauses**,
against a reader-adjudicated random-pair control at 0.

**Why this is a change and not a repetition.** Until now the recurrence null had a
single alternative explanation available: F043 showed the trigger vocabulary is
blind to outcomes, so the need corpus's zero could have been the instrument's. A
second corpus, harvested by **different phrases about a different event**, with
its own reader question and its own controls, gives the same zero. The absence is
therefore **not an artefact of any vocabulary this mission chose** — and it is a
fact about **what people write on Hacker News about tools they have left**, which
is what F053 leaves it as.

**The premise that failed is the useful part.** E031's hypothesis was that
accounts seeking an alternative state a requirement the artifact failed. They
state a missing capability at **twice** the base rate of ordinary comments — and
**exactly as often as accounts that named a successor** (0.347 against 0.347).
**What a departure account lacks is not a missing capability; it is a named
successor.** The population is people reporting friction, not people holding an
unfilled slot. That is why recurrence is zero, and it is why this closes a
generator rather than merely failing to open one.

**What this makes cheap to believe, and what it does not license.** It is cheap to
believe that **a cross-author recurring requirement will not be found by mining
Hacker News comments** — two corpora, five readings, five zeros, and the
vocabulary varied each time. That part is earned and it is the stronger claim.
It licenses **no** claim about other venues, and **not** one that unmet
requirements do not exist, that none recur, or that they cannot recur: F042's
0-of-24 and F049's CI95 [−0.0156, +0.1125] are disclosures and bounded
intervals, not zeros, and E031's own sample is **63 clauses** with its ceiling
declared before the adjudication (AMENDMENT-4).

> **Corrected 2026-10-06 (F053).** This paragraph used to read "mining public
> conversations — three populations, three instruments, three zeros". **The venue
> was never varied.** All 3,856 comment ids behind F039, F042, F043, F049 and
> F051 come from `hn.algolia.com` / `hacker-news.firebaseio.com`, and E019, E022,
> E026 and E029 all re-read E012's single 1401-comment file at **100% identifier
> overlap** — so there are two corpora, one of them read four times, not three
> populations. F051's own ceilings already said as much ("One corpus and one
> channel set"); the summary sentence was where the bound was dropped.
> [`EXPERIMENTS/032-venue-recurrence/`](EXPERIMENTS/032-venue-recurrence/PROTOCOL.md)
> tests the venue as the single changed variable.

**The transferable instrument lesson is D062.** A linkage rule is part of the
instrument: state the candidate count it produces against the count chance alone
produces, before reading any adjudication. E031's declared rule produced **4
pairs against a chance expectation of 4.9** — unreachable, the mirror of F010's
gate that could not fail — and **fixing F050's coincidence problem caused it**,
because a ≥ 2-rare-token rule tuned for 90-word comments does not transfer to
11-word clauses. The control is **reader-adjudicated random pairs from the same
arms through the same filters**, not a permutation of the candidate set, which is
F043's missing control in a second instrument.
