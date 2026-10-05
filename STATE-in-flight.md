<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# In flight — open readings, with their evidence

Split out of [`STATE.md`](STATE.md) on 2026-10-05, which was at the 300-line cap.
**This file holds material that is still open** — a reading the record has not
closed, and what would close it. The reload point keeps a pointer to the live
item and the finding number; the reasoning lives here so a rewrite of one does not
force a rewrite of the other, which is the same reason
[`STATE-next-actions.md`](STATE-next-actions.md) exists.

Read a finding number and go to the file it is defined in. Identifiers are stable
across findings files.

**Closed readings that an open item still leans on are in
[`STATE-in-flight-2.md`](STATE-in-flight-2.md)**, split out at the 300-line cap
on 2026-10-05: what actually killed the candidates (F044), and the
undecidability question F034 opened (F034, F037, F041).

## What became of the 1401 stated needs?

**Status: closed, and it narrows item 0 rather than opening it. F042, with its
third number withdrawn by F043. `EXPERIMENTS/022-need-outcomes/`,
`EXPERIMENTS/023-served-baseline/`.**

The one asset no failure in this record has touched — 1250 named people who each
wrote down, publicly and unprompted, what was missing from their work — had never
been followed forward. **Nobody had measured what became of any of them.** This is
the fourth measurement in a row about the world rather than about this
repository's own instruments, and the first that answers a question about *people*.

| outcome | figure |
|---|---|
| need statements, and their readability | 1401, **100.0%** (gate A1 requires ≥95%) |
| **answered** (≥1 reply) | **812 / 1401 = 0.580**, CI95 [0.554, 0.605] |
| **served** — a reply names an artifact serving the clause | **15 / 39 = 0.385** — **withdrawn as a demand-side figure, F043** |
| **the same arm against a control** | **14 / 38 = 0.368**, CI95 [0.234, 0.527], ordinary comments in the same stories |
| **built by the requester** | **0 / 24**, CI95 [0.0, 0.138] — 6 candidates, all hand-checked, none related. **Read as a disclosure floor, then measured: 278/1250 = 0.222 of these authors have publicly shipped something (F045)** |
| **of which have shipped anything at all, vs a control** | **0.2224** CI95 [0.2002, 0.2463] against **0.2780** CI95 [0.2405, 0.3188] for ordinary commenters in the same stories — ratio **0.80×**, intervals overlap (F045, D057) |

**The withdrawal, in one paragraph.** `served` had no control; E022's C1 and C2
both measure `answered`, and its own protocol says "`answered` is not `served`".
T-0067 drew the missing arm — ordinary comments in the need arm's own stories,
matching none of the 23 trigger phrases, **restricted to answered** so both arms
share the "a reply exists" condition — and it reads 0.368 against the need arm's
0.395, intervals overlapping across nearly their whole width. **The rubric is not
the cause: two readers labelled the identical 39 rows at κ = 0.9226.** So the
0.385 describes how Hacker News conversations go and the record read it as a
description of needs. What is left of E022 is the two cells that were measured
properly, and the sentence they support is the weaker one: the corpus records
needs the world **absorbed in conversation**.

**The build arm's own ceiling has now been measured (F045, D057).** `0 of 24` was
declared a floor on disclosure, and `STATE-next-actions.md` item 0 then carried it
as *"the people who state a need are not the people who build it"* — the one thing
the floor cannot say. Reading the missing channel over 1750 authors with zero
refusals: **22.2% of the 1250 have publicly shipped something on HN**, against
**27.8%** of control commenters from the need arm's own stories. So the corpus
**does** contain builders, in a fifth of its members, who build **less** than their
neighbours — and item 0d's closure is **confirmed by measurement rather than
withdrawn by caveat.** The rate at which they build *what they asked for* is
unchanged. Evidence: `EXPERIMENTS/025-need-staters-builderhood/`. D057 generalises
the lesson: an absence declared by an instrument is a candidate for measurement.

**Gate A2 fired as declared, before the first fetch.** The within-thread lift is
**0.703** (Mantel-Haenszel, CI95 [0.176, 2.814]) against a declared floor of 1.0:
carrying a need trigger does not make a comment more likely to be replied to. At
depth 0 need comments are answered *less* often than their thread neighbours
(0.599 vs 0.728) and at depth 1 not differently (0.575 vs 0.565). **The interval
spans 1.0, so "answered less" is not established** — what is established is that
the lift is not greater than 1.0, which is all the gate claimed. **F043's +0.026
on `served` is the same result in the neighbouring cell**, and together they say
one thing: **a trigger vocabulary finds people who state needs and is invisible
to what happens to those needs afterwards.**

**What this changes about item 0, in one direction.** The asset is **not** a
population of unmet needs awaiting a builder. It is a population of needs the
world **absorbed conversationally**: answered in the majority, served in about a
third of those, and self-built essentially never. That is a real demand-side
population and no failure in this record has touched it — but on this evidence it
contains no standing unmet need, and it still cannot supply a candidate. F029's
0-of-50 and F035's coverage measurement are untouched by this.

**The inverse filter is named here and deliberately not run**, because running it
would be the same population read a second time rather than a new question: **the
589 statements that drew no reply at all** are the only sub-population the outcome
data marks unserved, and the build arm says their requesters did not self-serve
either. That needs the same two public APIs and no new instrument.

**Ceiling on the whole thing:** one community, self-selected and technical; a
corpus harvested by trigger phrase rather than sampled from needs; one observation
window on 2026-10-05; and 40 labels from one reader with no second coder, so the
served interval is a sampling interval over a single judgement. The build arm
sees HN self-disclosure only, so 0-of-24 is a floor on disclosure and not an
estimate of building.

**F042 is the instrument defect, and the repaired number did not move.** The odds
ratio was 0.701 over the defective capture and 0.703 after — the two strata the
arm uses were never affected. That is only knowable *after* the repair, and
before it the record claimed 434 comments were unreadable when none were.

**The ceiling E023 added, and the ceiling it did not close.** One community, one
day, 38 rows per arm: a difference below roughly 0.2 is unresolvable, so **a small
need effect is not excluded** and the honest reading is that E023 could not find
one. The control arm is defined by *not matching the trigger vocabulary*, which may
still catch a need phrased unusually, making 0.026 a lower bound rather than an
estimate. And `served` is labelled, not measured — a reply naming an artifact is a
pointer — which both arms carry equally and which is why the comparison is fair and
the absolute numbers remain unusable.

## The third axis: is the young vocabulary served by copies rather than installs?

**Status: closed, negative (F041, D053). `EXPERIMENTS/021-copied-artifact-serving/`.**
Renumbered from F040/D052/`020-` on the unpushed side; see the collision note in
the finding.

F037 ended with exactly one reading standing for the prior-art screen's
young-vocabulary failure. The screen reads installation channels; the artifact a
coding-agent user commits is a **directory they copied**; so *1 of 18 incumbents
clears a floor while 14 of 18 have no readable channel* might mean the field is
**used and invisible to the instrument** rather than thin. `STATE-next-actions.md`
item 0 named the testable form and said the cheapest honest proxy was a count of
repositories containing a `.claude/` directory, **which no public API serves**.

**A public unauthenticated API does serve it** — Sourcegraph's streaming search
endpoint returns repository-level counts for a path pattern — and that correction
is itself part of the finding, because it removes the blocker the item was written
around. The count is **1,026** indexed repositories holding a `.claude/hooks/`
directory against **8,676** monthly installs across the young arm's four
channels. **Ratio 0.118**, where the gate declared in `PROTOCOL.md` needed ≥ 20×
to survive and ≤ 5× to be dead, the interval chosen so that "the channel we
counted is not the channel the field uses" would not be arguable.

**So the screen was reading the dominant channel**, F037's reading is withdrawn,
and the young side of F034's split is the world rather than the instrument.
**The twelve prior-art deaths stand** unless something other than the screen is
wrong, and the burden of argument moves to whoever would claim otherwise.

### The second finding, which is about the instrument rather than the field

C2, the coverage control, is the one the protocol declared able to refuse the
whole experiment. **It did not for the young arm** — 17 of 18 young repositories
are in the index, so the 1,026 is a count on the population rather than on a blind
spot. **But the placebo arm is 0 of 13.** 015 built those thirteen deliberately
unpopular repositories precisely so that a figure there would announce an
instrument defect, and this instrument cannot see a single one of them.

So it is not merely biased toward popular projects: it is **blind below whatever
threshold GitHub stars cross**, which is exactly where every candidate in this
mission lives. This is a *different* blind spot from the registry channels F037
ruled out, so the two do not compose into a working instrument.

### H2, the fork-and-template question, is `not evaluable`

The declared gate asks whether forks and templates separate heavily-copied
configurations from barely-copied ones. Nine configurations cleared the high band
(165 to 4,000 copies) and **none of their origin repositories is a fork or a
template**, which is the direction that would have supported the stand-in. The low
band is **empty**: the anti-bot challenge armed partway through that half, and this
session's own retry loop overwrote the five answers it had already obtained with
counts of 1, 1, 1, 1 and 2. **A rate over one band is not the rate the gate
declares**, so the verdict is `not_evaluated` and the missing half is a named cost.

The low band's twelve patterns are a **declared mechanical slice** — every 400th
hook path the index returned — so a rerun needs no new decisions, only a host the
endpoint will answer.

### Six instrument defects, recorded with the run

Two cost real data, and the second is the sharpest instance of a class this
repository already knows:

1. **A retry loop overwrote five good captures with refusals**, unrecoverably.
   Repaired: a capture holding an answer is never overwritten, and a refusal is
   written beside it.
2. **Falsifying the test for the overwrite defect executed the defect, and
   destroyed H1's raw capture.** The repair was untested against the repair.
   `COPYCOUNT_PROTECT` now refuses to touch a capture holding a value other than
   the one the run was asked to reproduce. The figure survives in this session's
   command log and in `forkstatus.json`; `results.json` states that the bytes are
   gone rather than presenting a recovered number as a live measurement.
3. A substring match on overlapping path patterns put a narrow pattern's count of 42
   on a broader one.
4. Two independent copies of one naming rule; when the capture format changed, all
   22 configurations became `no_origin`.
5. `copycount.json` was clobbered by every run, silently discarding nine counts.
6. A capture could not be traced to its query, because the slug is lossy.

**The pattern underneath them is worth more than any one.** The rate limit is
*positional*: it armed after ~30 requests from one host and every query after it
returned **HTTP 200 with an HTML challenge page** — F036's shape, in a different
instrument. The first coverage pass issued 61 queries unpaced and **33 rows,
including every young row and every placebo row, came back as HTML.** That reads
as "the index does not contain the young arm", which is a clean, confident, wrong
finding about the world. It was caught only because C2 was declared able to refuse
the experiment and the refusal was recorded as a refusal.

### What it does not open

- **Attribution.** Whether a counted repository copied *this* artifact or wrote
  something similar is not decidable from a path count. H1 is about a channel's
  volume, and reading `dead` as "these incumbents are not serving" overreaches.
- **The install channels are not thereby validated.** H1 compares two imperfect
  measures; dominance is not accuracy.
- **Nothing here reopens a prior-art death.** "Prior art exists" and "the need is
  served" remain different claims, and only the first has been in question.

Full text and the per-configuration table: `EXPERIMENTS/021-copied-artifact-serving/README.md`
and [`FAILURES-findings-16.md`](FAILURES-findings-16.md).

## Does a copied configuration go stale?

**Status: inconclusive, and it withdraws F037's *reconciliation* as well (F040, T-0065, other VM).**
`EXPERIMENTS/020-copied-config-drift/`. Recorded here because it is the mirror
image of the entry below, and the pair is the point.

F037 inferred from four documents that the reader **copies a `.claude/`
directory** into their own repository. That inference had a consequence nobody had
drawn: an artifact copied rather than installed has **no update channel**, so
near-zero install readings would be consistent with a field that is heavily used
and entirely invisible. **It does not hold, and it fails on its own terms rather
than on a limit.**

- **Copying is widely *instructed*** — `cp -r .claude` appears in **687** Sourcegraph
  content matches against a nonsense control of **0**.
- **and barely *duplicated*** — of **1,950** distinct configuration file contents
  across 31 repositories, **92 (4.7%)** are byte-identical across repositories, and
  **no two repositories from different authors overlap by half**.

So what readers do is **adapt** the configuration. **What is withdrawn is the
inference** that the copies accumulate as identical copies and therefore that the
near-zero install readings are an invisible distribution channel. **What is not
withdrawn is the documented practice**, which was measured.

**The drift rate itself is `drift_rate: null`, not 0**: 0 attributable
copy/upstream pairs exist in the measurable population, so the declared no-drift
gate fires on an unanswerable question — `inconclusive`, not evidence of low drift.

**Together with the entry below, F037's escape hatch is closed from both ends.**
Neither experiment is about this repository's own instruments, which is itself worth
noting: five consecutive experiments measured the quality of the mission's own
judgement before one asked a question about the world.

## The candidate generator is refuted as a generator

**Status: closed (F029, F033, F039, D049, D051).** Kept here because the item is
closed on a population measurement rather than a prior-art verdict, which is the
distinction a later reader is most likely to get wrong.

1401 practitioner need statements harvested from Hacker News comments since
2024-01-01; 50 drawn by a stated rule; **0 survived** — 38% prior art, 30% no
mechanism, 24% not software, 8% needing hardware, against the prior generator's
own 3-of-16. The corpus cannot supply recurrence: term recurrence returns only
function words. E014 applied the repository-signal half of D049 and the "5805
issues / 28 repositories" cluster collapsed to 15 issues across 9 agent-labeled
repositories — a complaint inside a dozen agent-project trackers, not a
cross-project problem (F033). F030: a prior-art verdict from one search query is
wrong in both directions.

**Then F039 measured the corpus's population, which is 1250 distinct authors** —
median one comment each, maximum eight, over 466 days, author recovered for 1401
of 1401 rows — so the narrow-audience explanation is disproved, and **no
need-level recurrence is detectable inside it**. The 0 of 50 was a fact about the
corpus's composition rather than about its screens. The recurrence instrument
failed its own controls (four of six positive controls returned 0 or 1 distinct
author), so that kill gate is recorded *not evaluable*.

**What the corpus holds is 1250 named people who each wrote down what was missing** —
a demand-side population this mission has never used, and the only one no failure
in this record has touched.
