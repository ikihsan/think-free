<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E181 RESULT — supplying the missing fact does not move the assistant

**Date:** 2026-10-18. **Status:** complete. **Outcome: K1 fired. The mechanism
is not there, and the strongest accessible alternative does not work either.**

## The question

E177 measured a free general assistant reaching the accepted resolution on
**26/30 = 0.8667** of high-arrival Stack Overflow questions whose resolution
follows from the question's own text, and **12/30 = 0.4000** on those whose
resolution depends on a fact the question never states (F136, D118). It also
measured **abstention at 0 of 30**: the assistant answers confidently on exactly
the questions whose deciding evidence is absent.

This experiment asked the next question, which is the one a product would have
to answer: **what happens to the 0.4000 when the missing fact is put back?**

Four arms, same 14 rows, all answered in one session, scored blind by one
reader in a shuffled set with no arm label in any filename:

| arm | input to the assistant | reached | rate | Wilson 95% |
|---|---|---|---|---|
| **A0** | the question only | 7/14 | **0.5000** | [0.2680, 0.7320] |
| **A1** | + the one extracted missing fact | 8/14 | **0.5714** | [0.3259, 0.7862] |
| **B1** | + **every comment on the question and on its accepted answer, verbatim** | 9/14 | **0.6429** | [0.3876, 0.8366] |
| **C1** | + a fact extracted from a *different* row (placebo) | 4/10 | 0.4000 | [0.1682, 0.6873] |
| **P** | E177's committed answer for the same row (drift check) | 3/10 | 0.3000 | [0.1078, 0.6032] |

**Every paired comparison is null.**

| comparison | discordant pairs | McNemar exact, two-sided |
|---|---|---|
| A1 vs A0 | 2 for, 1 against | **p = 1.0** |
| A1 vs B1 | 0 for, 1 against | **p = 1.0** |
| A1 vs C1 | 1 for, 1 against | **p = 1.0** |
| A0 vs B1 | 0 for, 2 against | **p = 0.5** |

## What this decides

**The 0.4000 is not a missing-input failure that an elicitation step closes.**
A free general assistant given the *correct* missing fact, extracted blind from
the thread's own comments and never from the accepted answer, lands at 0.5714
against a 0.5000 floor. And the strongest accessible alternative — **paste the
whole discussion**, which costs nothing and needs no new tool — lands at
0.6429 against 0.5000, with McNemar p = 0.5 and **zero rows where B1 beat A0**.

So the population gap F136 measured is real and still unexplained, but neither
of the two things a person or a tool could do about it — supply the fact, or
supply the thread — moves this assistant off its baseline on these rows. The
"ask the assistant to ask" product direction this protocol was written to test
has no measured support behind it.

**The cost result survives the null, and it is the one number a reader should
keep.** Median tokens of *added* context: **A1 15.5, B1 232.5, C1 14.5** — a
correctly extracted fact is **6.7%** of the thread it came from. If targeted
elicitation were the mechanism it would be fifteen times cheaper than pasting,
which is a real product shape. It is not the mechanism.

## G4 failed, and it changes what may be compared to what

The drift control re-scored **E177's own committed answers** on ten of these
rows against E177's own verdicts on the same rows: **6 agree, 4 disagree.**
G4's declared tolerance was 3, so **G4 fires.**

What that does and does not invalidate:

- **Void:** any comparison between a number here and E177's 0.4000 or 0.8667.
  This session's A0 = 0.5000 is *not* a re-measurement of E177's 0.4000 and
  must not be read as a drift-corrected version of it.
- **Intact:** every within-session paired comparison, because all five arms
  were produced and scored by the same instrument on the same day in one
  shuffled set. A1-vs-A0 is A1-vs-A0 whatever the absolute level is.

The drift is itself the finding worth recording: **the same reader re-scoring
the same answers a day later changed four of ten verdicts.** A reach rate from
a single reader on this population is not a stable instrument at ±0.4.

## K1 fired, so the gate table is empty

`EXT` read all 30 of E177's scored EVID rows against a pre-declared rule — the
one fact or artefact the thread's comments supply that the question does not,
absent from the question, with identifiers copied verbatim, `null` when the
comments carry the remedy instead or another reporter's observations instead.
**14 of 30 = 0.4667**, Wilson 95% [0.3023, 0.6386], carried a fact. K1's
declared floor was 16, so K1 fired and **G1, G2, G3 and G5 are reported as
`not evaluable`** rather than as passes or failures. AMENDMENT 2 declared in
advance what this means: on 14 paired rows an exact McNemar reaches p < 0.05
only if the treatment wins essentially every discordant pair, so **a null here
means "no near-perfect effect detected", not "no effect"**.

### The yield, which is what survives K1

**The round trip runs on two thirds to nine tenths of these rows (E178 0.6739,
F138 0.9000) and names the deciding fact on 46.67% of them.** The other 53% is
not random:

- **10 of the 16 nulls carry the remedy itself** — row 3's `:host` styling
  recipe, row 17's "run as administrator", row 19's `langchain_classic`, row
  7's "no public API". That is the answer, arriving after the fact is decided.
- **6 carry another reporter's observation** — row 4's .NET SDK 8, row 12's
  fork, row 21's opinion about the standards committee.

So F137's and F138's conclusion needs one clause added: **the round trip is a
round trip to the *solution*, not to the *fact*, and on more than half of these
rows the solution is what it delivers.**

## The one fact that was wrong, and it is the interesting one

Row 18 (`79665976`, uv): `EXT` recorded "uv on the home machine was installed
by the curl installer, not by pip install" — quoting a comment that says "my
machine at home is using the uv installed by curl". **The accepted answer says
the opposite:** that the reporter's uv was `pip install`ed under Python
3.13.2 and must be uninstalled and reinstalled standalone. Every arm on this
row scored `not_reached`, A1 included, because the supplied fact pointed the
wrong way.

A comment saying "my machine at home is…" was read as the reporter's machine
because the *thread* is theirs. **This is G5's check firing on one row of
fourteen, reported rather than recomputed: at least 1 of 14 = 7.1% of extracted
facts is not about the reporter, and this is a class the declared rule did not
anticipate — a third party reporting on their own environment inside someone
else's thread.**

## Controls, and what each one cost

- **Leak assertion (`prep.py`, `make_inputs.py`).** Every `EXT` input and every
  `ANS` input was re-read after writing and refused if a key-answer id or the
  first 120 characters of an accepted answer appeared in it. Passed both times.
- **Quote verification (`write_facts.py`).** Every `quote` proved a verbatim
  substring of the file the reader saw **and** proved absent from the question
  section, before `facts.jsonl` was written. Passed for all 14.
- **Placebo C1** ran on 10 rows and reached 4/10, below A0. At n = 10 this rules
  out nothing on its own, as declared.
- **Not run:** G5's full blind re-read of all 14 facts, which the protocol
  required after `answers.jsonl` was committed. The single row above was found
  while scoring. **G5 is therefore partially executed, not `not evaluable`, and
  the difference is recorded rather than smoothed.**

## A repository defect found and repaired on the way

`EXPERIMENTS/*/raw/` was listed in `.gitignore` at line 46 **as a directory**,
and git cannot re-include a file whose parent directory is excluded, so the
negations at lines 47–54 have never had effect. **Every `EXPERIMENTS/*/raw/*.jsonl`
was untrackable while E177's and E178's protocols state the raw capture makes
the quota cost auditable** — D061's shape, a claim tied to no bytes. 109 raw
files (199 MB) were sitting untracked; 5,295 were force-added before or despite
it. Repaired by `raw/` → `raw/**` plus anchoring the root-level `raw/` rule, and
verified by `git add` succeeding with no `-f`. The 109 are left alone and named
as a known gap.

A second defect, in evidence rather than configuration: **E178's committed
`raw/se.jsonl` contains each `comment_id` up to three times** — 1,307 items,
649 distinct, 306 appearing exactly 3× — because its paging appended every page
of the same URL to one file. Left in place it would have tripled the B1 arm and
made G2's token comparison a measurement of a duplication artifact. Every
comment set in E181 is de-duplicated, 240 → 80 question spans on the first 20
rows.

## Ceilings

- **n = 14 paired rows**, chosen by K1 firing, not by power. Only a
  near-perfect effect was detectable. Every p-value of 1.0 here means that.
- **One reader, one day, three roles.** The same reader produced the facts,
  wrote the answers and graded them, with disjoint inputs and a committed
  order — and G4 shows the reader's verdicts moved 4 of 10 on identical inputs
  one day later.
- **One venue, one reused draw.** E177's 30, so these are conditional numbers,
  not prevalence estimates.
- **Conditional claims.** "No near-perfect effect detected on 14 rows of one
  reused draw", not "supplying the fact does not help".
- **ANS had no retrieval**, inherited from E177's incumbent.

## What this does not close

- **F136's population gap stands.** EVID rows are still reached at roughly half
  the SELF rate. This experiment does not explain the gap; it removes the two
  explanations that were cheapest to reach for.
- **Nothing about money SE, Home Improvement SE, Anova, Cross Validated, or any
  non-Stack-Overflow venue.**
- **Nothing about the assistant abstaining.** F136's 0-of-30 abstention stands
  and untested here.

## The single most useful next action

**Stop treating the EVID gap as an input problem.** Two of the three obvious
interventions have now been measured and neither moves the rate, so the next
question has to be about the answer rather than the context: *is the failure a
retrieval-of-the-right-fact failure at all, or is it a disagreement with the
community's chosen resolution?* The cheapest discriminating test reads the six
rows every arm missed and asks whether the accepted answer is the *best*
answer or merely the *accepted* one — one reader, no new fetch, and it is the
only remaining explanation this population has.

Prior art: not screened, and not needed for a negative result. If a later
experiment revives the elicitation direction, the screen is owed first.