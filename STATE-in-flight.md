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

## The third axis: is the young vocabulary served by copies rather than installs?

**Status: closed, negative (F041, D053). `EXPERIMENTS/021-copied-artifact-serving/`.**

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

## Is a screen whose premise is unmeasurable four times in five a screen?

**Status: closed as an open reading, with one question left (F034, F037, F041).**
Was item 0c of `STATE-next-actions.md`, moved here when F041 made the ranked list's
entry redundant.

F034 could read serving evidence for **57% of the incumbents its own population
contained and 22% of the young arm** — which is a statement about the world's
distribution rather than about this repository's tooling. F037 measured the
fraction and it is **high exactly where the candidates live: 14 of 18 young rows
undecided, 13 of them tools, and 43% of the mature arm.** It also showed
undecidability does **not** track artifact class — 10 of the 14 unreadable young
rows are executable — so "this is just a document" never explains an unreadable row.
F041 then found the missing channel is a *smaller* one, and that its own blind spot
is the placebo arm.

**What remains open is whether the unmeasurable fraction predicts anything about the
need**, and its falsifier is a population where that fraction is near zero.

**Ceiling, and it is the reason this is a reading rather than a verdict:** 015's
`placebo.py` shows the instrument *can* read unpopular projects when it looks for
readable ones, so "unmeasurable" is partly an artefact of which channels were
consulted. **A follow-up must state its channel set or it measures the
instrument.** That is now also the fifth condition of
[`docs/process/experiment-protocol.md`](docs/process/experiment-protocol.md)'s
prior-art rule.

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