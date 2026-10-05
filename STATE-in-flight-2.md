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