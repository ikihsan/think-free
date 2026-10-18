<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Failure findings 44 - the missing fact is not what is missing

Continued from [`FAILURES-findings-43.md`](FAILURES-findings-43.md), split
at the 300-line cap on 2026-10-18. Carries F137, F138, F139 and F140.

## F137 — The round trip's failure is uniform across evidence buckets, and the genuinely unserved residue is tiny

**Date:** 2026-10-17. **Kind:** exploratory re-analysis of E178's committed
data (no new fetch, no gate). **Decides:** whether the "automated ask" route
has a buildable sub-population inside the E177 EVID class.

E178 measured `has_ask` (the thread contains a request for the missing fact)
as an aggregate over the 46 EVID rows and did not store it per row. The
cross-tab of `has_ask` against the M2 bucket was computed by replicating
`score.py`'s exact `is_ask` lexicon and joining on `qid`:

| bucket | round trip failed | round trip worked | total | failure rate |
|---|---|---|---|---|
| asker_only | 7 | 14 | 21 | 0.3333 |
| third_party | 6 | 14 | 20 | 0.3000 |
| none | 2 | 3 | 5 | 0.4000 |
| publishable | 0 | 0 | 0 | — |
| **all** | **15** | **31** | **46** | **0.3261** |

**The round trip's failure is not concentrated in `asker_only`.** It is uniform
at ~30–33% across both non-empty buckets, so there is no special sub-population
of asker-held facts that an automated ask would uniquely serve. The failure is
a low-engagement failure, not a bucket-specific one: 5 of the 7
`asker_only`+failed rows have **zero** comments, meaning no commenter engaged
at all.

On the 30 scored EVID rows (the subset E177's `verdicts.jsonl` covers), the
joint with the free assistant's verdict:

| | assistant reached | assistant missed |
|---|---|---|
| round trip worked | 8 | 11 |
| round trip failed | 4 | 7 |

**The genuinely unserved residue — round trip failed AND assistant missed — is
7 of 30 = 0.2333**, and all 7 carry a key answer: they were served by a
mechanism other than the free assistant or the visible round trip (asker edit,
expert answer, or self-answer — `rows.json` does not record which). Fisher
exact on `has_ask` × `reached` gives p = 1.0, which is expected: the E177
assistant saw only the question body, so a comment ask cannot affect its
verdict.

**What this decides.** The "automated ask" route has no buildable
sub-population on Stack Overflow. The round trip fails uniformly because of low
engagement, not because the missing fact is the wrong kind; and the 23% residue
it does leave is a population that was eventually answered anyway. The EVID
class is served by the assistant (0.40), the visible round trip (0.67), and
invisible mechanisms (the residue). **The EVID line is closed, and the
"unserved need" hypothesis is dead for every population this mission can
measure on this venue.**

**Ceiling.** The cross-tab is post-hoc over reused rows, not a pre-declared
experiment; it decides a route, not a rate.

## F138 — The round trip is stronger, not weaker, when the missing fact is personal

**Date:** 2026-10-17. **Kind:** fresh observation, second venue, hypothesis declared
before the run. **Decides:** whether F137's conclusion (the EVID class is served by
the venue's own round trip) is a Stack Exchange property or a general one.

F137 left one untested boundary: on Stack Overflow the missing fact is often a version
number, which is easy to elicit. The hypothesis, declared before any fetch, was that
on a venue where the missing fact is **personal** — income, debt, jurisdiction, age —
the asker is less willing to supply it and the round trip should fail *more*.

On Personal Finance Stack Exchange (`money.stackexchange.com`, chosen by a stated rule:
the largest non-software SE site where high-arrival questions routinely turn on a
personal fact the asker may not volunteer), the top 30 highest-vote questions with
answers were fetched and scored with E178's own `is_ask` lexicon:

| measure | money SE | Stack Overflow (E178) |
|---|---|---|
| lacks a specific personal fact | **9/30 = 0.3000** | 46/100 = 0.46 (E177 EVID) |
| carries a round-trip ask | **27/30 = 0.9000** | 31/46 = 0.6739 |

**The hypothesis is disconfirmed in the direction that matters.** The round trip is
*stronger* where the missing fact is more personal (0.9000 against 0.6739), not
weaker. The venue asks more readily, not less, when the fact is sensitive.

**What this decides.** F137's conclusion is not a Stack Exchange property. The EVID
class — questions whose resolution depends on a fact the asker holds but did not post
— is served by the venue's own round trip across two venues of very different
personal-fact sensitivity, and the genuinely unserved residue is small and eventually
answered in both. The "unserved need" hypothesis is dead for money SE as it was for
Stack Overflow. **Ceiling:** one reader, one venue, 30 rows, votes as a proxy for
arrival; the fact-presence lexicon is a heuristic, not a blind re-key.

## F139 — The measured "missing fact" is not what is missing, and the strongest accessible alternative does not work either (E181)

E177 measured a free general assistant reaching the accepted resolution on
0.8667 of self-contained high-arrival questions and **0.4000** of the ones whose
resolution needs a fact the question never states, with **abstention at 0 of
30** (F136, D118). The obvious reading is that the 0.4000 is a *missing input*:
ask for the fact, supply it, close the gap. E181 ran that as four paired arms on
one population, all answered and scored in one session.

| arm | added context | reached | Wilson 95% |
|---|---|---|---|
| A0 | nothing (question only) | 7/14 = 0.5000 | [0.2680, 0.7320] |
| A1 | the one extracted missing fact | 8/14 = 0.5714 | [0.3259, 0.7862] |
| B1 | **every comment on the thread, verbatim** | 9/14 = 0.6429 | [0.3876, 0.8366] |
| C1 | a fact from a different row (placebo) | 4/10 = 0.4000 | [0.1682, 0.6873] |

**Every paired comparison is null.** A1 vs A0: 2 discordant for, 1 against,
McNemar exact **p = 1.0**. A1 vs B1: 0 for, 1 against, **p = 1.0**. A0 vs B1:
0 for, 2 against, **p = 0.5** — *pasting the entire thread never once beat
answering the question alone*. So neither of the two things a person or a tool
could do about this population moves the rate, and the product direction this
session was written to test has no measured support behind it.

**What does survive is a cost ratio and a yield.** A correctly extracted fact is
a median of **15.5 tokens against the 232.5 tokens of the discussion it came
from - 6.7%**. If targeted elicitation were the mechanism it would be fifteen
times cheaper than pasting; it is not the mechanism. And on 30 of E177's EVID
rows the comments named the deciding fact on **14 = 0.4667**
[0.3023, 0.6386]: **10 of the 16 nulls carry the remedy itself** (`:host`
styling, "run as administrator", `langchain_classic`) and 6 carry another
reporter's observation. F137's and F138's "the round trip serves the class"
needs one clause: **the round trip runs to the solution, not to the fact, and on
more than half of these rows the solution is what it delivers.**

**Two things this record should carry forward as rules.**

1. **G4 caught the instrument, and the thing it caught was the reader.** The
   drift control re-scored E177's *own committed answers* on ten of these rows
   against E177's own verdicts: **6 agree, 4 disagree**, against a declared
   tolerance of 3. **The same reader re-reading the same answers one day later
   changed four of ten verdicts.** So a reach rate from one reader on this
   population is not stable at plus or minus 0.4, and every absolute level this
   session produced is barred from comparison with E177's 0.4000 and 0.8667 -
   only its within-session paired comparisons survive. **Rule: a reader protocol
   that has never re-scored its own past verdicts has an unmeasured error bar,
   and the cheapest check for it is re-scoring answers that were already
   graded.**
2. **A comment saying "my machine at home" inside someone else's thread is not
   the reporter's machine.** One of the fourteen extracted facts (row 18, the
   `uv` case) was exactly that, and the accepted answer says the opposite - the
   reporter's `uv` was `pip install`ed under Python 3.13.2. Every arm scored
   that row `not_reached`. **Rule: a round-trip extraction must mark *whose*
   environment a comment describes, and a third party reproducing a problem
   inside the reporter's thread is a class the naive rule does not anticipate.**

**K1 fired and the gate table is therefore empty, and that is reported rather
than dressed up.** `EXT` read all 30 rows and only 14 carried a fact, against a
declared floor of 16, so G1, G2, G3 and G5 are `not evaluable`. AMENDMENT 2
declared in advance what n = 14 can see: **a null here means "no near-perfect
effect detected", not "no effect"** - an exact McNemar on 14 paired rows
reaches p < 0.05 only if the treatment wins essentially every discordant pair.
G5's blind re-read was **partially** executed: one row was found during scoring
and the rest were not re-read, which is recorded rather than smoothed.

**Ceilings.** One venue, one reused draw, so conditional rather than prevalence.
`ANS` had no retrieval, inherited from E177's incumbent. One reader behind all
three roles, with disjoint inputs and a committed order - and G4 is the number
that says how much that costs. A0's 0.5000 is **not** a re-measurement of
E177's 0.4000 and must not be read as one.

**What this closes.** The elicitation route for the EVID class: supplying the
correct fact, and supplying the whole thread, both measured, neither working.
**What this does not close.** F136's population gap stands and is still
unexplained; abstention is untouched; nothing here says anything about any other
venue.

**What reopens it.** A discriminating test on the rows every arm missed, asking
whether the accepted answer is the *best* answer or merely the *accepted* one.
That is one reader, no new fetch, and the only remaining explanation this
population has. See
[`EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md`](EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md).

## F140 — the repository could not track its own raw evidence, and two readers of this record have been quoting capture paths that were never committed

Found while recording E181's evidence and repaired in the same commit.

`.gitignore` line 46 excluded **`EXPERIMENTS/*/raw/` as a directory**, and git
cannot re-include a file whose parent directory is excluded, so the negations
at lines 47-54 have **never** had effect. The same file's trailing `raw/` rule,
unanchored, was a later matching pattern and re-excluded everything regardless.
Consequence: **every `EXPERIMENTS/*/raw/*.jsonl` in this repository is
untrackable**, while E177's and E178's protocols each state in their own text
that the raw capture is what makes the quota cost auditable. That is D061's
exact shape - a claim tied to no bytes - sitting in the two experiments this
mission's only positive result came from. **109 raw files, 199 MB, were sitting
untracked**; 5,295 were force-added before or despite the rule. Repaired by
`raw/` -> `raw/**` (excluding the contents rather than the directory) and by
anchoring the root-level rule, verified by `git add` succeeding with no `-f`.
**The 109 are left in place and named as a known gap.**

A second defect, in the evidence rather than in the configuration: **E178's
committed `raw/se.jsonl` holds each `comment_id` up to three times** - 1,307
items, 649 distinct, 306 appearing exactly 3x - because its paging appended
every page of the same URL to one file. Unnoticed, it would have tripled E181's
whole-thread arm and turned a declared token-cost comparison into a measurement
of a duplication artifact. **Rule: a raw capture assembled by appending pages of
the same URL is a set, not a log, and the first thing any reader of it should do
is count distinct ids against item count.**
