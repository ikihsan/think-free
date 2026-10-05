# 022 — what becomes of a publicly stated unmet need?

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

**Date:** declared and run 2026-10-05. **T-0066.** The declaration is in
[`PROTOCOL.md`](PROTOCOL.md), written before any outcome was read.
**Gate A1 met, gate A2 fires, gate A3 evaluable.** F042 is the instrument bug
this session repaired; the result below is unchanged by that repair, and the
repair is reported because the earlier session's `verify` output said otherwise.

## The result in one sentence

**A stated need is answered about 58% of the time, and — when a reply exists —
something serving it is named in 38% of a hand-labelled sample, and in 0 of 24
cases did the requester go and build it themselves.** The corpus is therefore
mostly a record of needs the world *absorbed conversationally* rather than
unserved ones.

## Population, read at 100%

| | figure |
|---|---|
| need statements | 1,401 |
| readable item records | **1,401 (100.0%)** — gate A1 requires ≥95% |
| distinct requesters | 1,250 |
| distinct threads | 1,276 |
| replies below the needs | 1,860 |
| **answered (≥1 reply)** | **812 / 1401 = 0.580**, CI95 [0.554, 0.605] |

`answered` is not `served`. The two are reported separately on purpose, because a
reply count cannot tell a reply that answers a need from a reply that ignores it
— F036's shape, where an instrument answered the easier question confidently.

## The served cell is hand-labelled, and the automatic rule is not the headline

A 40-comment sample of the 812 answered comments was drawn at seed 20261005 and
labelled by hand (`raw/labels.tsv`, every row carries its own note):

| label | n |
|---|---|
| `served` — a reply names an artifact serving the clause | 15 |
| `partial` — something adjacent, incomplete | 10 |
| `not_served` — replies exist, none addresses the need | 14 |
| `unreadable` | 1 |

**served = 15/39 = 0.385, CI95 [0.249, 0.541].** Restricted to comments whose
clause was about software, 12/26 = 0.462. The over-inclusive lexical rule fires
on 39 of the 40 and agrees with the labels on 16 — it is reported beside the
labels and never alone, exactly as the protocol required.

## The build arm: 0 of 24, and that is a floor on disclosure

Of the 24 `not_served` + `partial` rows, all 24 author histories were read.
**Six requesters posted a story after the need. All six were hand-checked and
none was related** (`raw/build_check.tsv`, one note per row: a browser
sustainability need answered by a story about moving ReadMe to Git, an SSD
power-need answered by financial data rendered as paintings, and so on).

Rate **0.0, CI95 [0.0, 0.138]**. The arm cannot see a build posted to GitHub
rather than HN, so this is a floor on *disclosure*, not an estimate of building.

## Gate A2 fires: a trigger phrase does not mark a comment the thread answers

This is the arm that tests the protocol's strongest named alternative — that
thread popularity, not the need, drives replies.

| depth | need | control | lift |
|---|---|---|---|
| 0 | 384/641 = 0.599 | 8110/11134 = 0.728 | **0.822×** |
| 1 | 183/318 = 0.575 | 6226/11018 = 0.565 | **1.018×** |

**Mantel-Haenszel common odds ratio 0.703, CI95 [0.176, 2.814].** The declared
floor was 1.0, so **A2 fires**: carrying a need trigger does not make a comment
more likely to receive a reply. At depth 0 need comments are answered
*markedly less* often than their thread neighbours; at depth 1 the difference
vanishes.

**The honest reading of that interval: it spans 1.0, so "need comments are
answered less" is not established.** What is established is that the lift is not
greater than 1.0, which is what the gate declared in advance.

**Ceiling, stated rather than buried:** the control arm holds depths 0 and 1
only. **442 need comments at depth ≥2 have no depth-matched control**, so the
deep tail is unmeasured rather than measured at zero. The odds ratio is computed
over the two strata where both arms exist.

## F042 — the walk that reported 434 comments as unreadable

`need_depth.py --verify` was red for this whole experiment: 434 of 1401 need
comments carried `depth: null`. `need_depth_walk.py` was written to resolve them,
fetched 432 ancestors with status `ok`, resolved **none**, printed "no new
ancestors" for 29 rounds, and **exited 0**.

The loop re-appended each chain's *current* node with a larger hop count instead
of the node's parent, so `node == sid` was never true for a chain longer than one
hop. All three sampled chains resolve live at 4, 2 and 3 hops. After the repair:
**1401 of 1401 depths resolve**, including a tail to depth 20.

Three things make this worth more than the 434 rows:

1. **The first diagnosis was wrong and said so with confidence.** The walk's own
   docstring read the residue as "unreadable but fetchable" and blamed a
   one-hop-per-round limit. Every one of those 432 ancestors was already in
   `parent`, so "no new ancestors" was *correct*. The docstring is corrected.
2. **The direction of the error was the convenient one.** Unresolved rows were
   excluded from the strata, and they were the *deeply nested* rows — dropping
   them reweights toward depth 0, the stratum with the highest reply rate. The
   bug inflated nothing here, but it would have hidden the tail entirely.
3. **A gate that reads the artifact is the only thing that caught it**, because
   the walk's own exit code was 0. `tests/test_need_depth_gate.py` holds the
   defect's shape as an explicit assertion so the loop cannot be restored by an
   edit that looks equivalent.

The **reported result did not move**: the odds ratio was 0.701 before the repair
and 0.703 after, because the two strata the arm uses were never affected.

## What this licenses, and what it does not

The protocol said this experiment produces a population statistic, not a
candidate, and it was right about that. **It changes item 0's reasoning in one
specific direction.** The asset of "1,250 named people who each wrote down what
was missing" is **not** a population of unmet needs awaiting a builder. It is a
population of needs that were, in the large majority, **met in conversation** —
58% answered, 38% of those served by something named, and essentially nobody
building it themselves.

That is a real demand-side population, and it is the one no failure in this
record has touched. But it is a population of *acknowledged* needs. It does not
contain, on this evidence, a standing unmet one, and **it cannot supply a
candidate**: F029's 0-of-50 and F035's coverage measurement are untouched by
this.

**What would make it actionable is the inverse filter, and this experiment names
it without running it:** the ~42% of statements that drew **no reply at all** are
the only sub-population the outcome data marks as unserved, and the build arm says
their requesters did not self-serve either. That is a *next* measurement, not this
one — it needs the same two APIs and no new instrument.

## Honest limits, carried from the protocol unchanged

- **One community.** Hacker News commenters, self-selected, technical. No figure
  here generalises beyond it.
- **A corpus drawn for a prior purpose**, harvested by trigger phrase rather than
  sampled from needs. A2's stratification is the mitigation, not a fix.
- **One observation window** (2026-10-05), two APIs, neither snapshotted. A reply
  added later is invisible.
- **Labels are one reader's.** 40 rows, no second coder, so the served interval
  is a sampling interval over a single judgement.