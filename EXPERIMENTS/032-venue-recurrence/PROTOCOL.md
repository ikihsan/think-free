# E032 — protocol: does the recurrence zero survive a change of venue?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Declared 2026-10-06, before any fetch was made.** Task T-0076. No network
request was issued for this experiment before this file existed. The confound
this experiment exists to test was established from primary sources first, and is
recorded as F053; it is written up from the captures, not from this experiment.

## The question

F039 (E019), F042/F043 (E022), F049 (E029) and F051 (E030/E031) each returned zero
cross-author recurring requirements. `STATE-in-flight-2.md` line 120 draws the
conclusion that "a cross-author recurring requirement will not be found by mining
public conversations — three populations, three instruments, three zeros."

**Every one of those populations is Hacker News comments reached through
`hn.algolia.com`.** And the count of populations is two, not three: E019, E022,
E026 and E029 all re-read E012's single 1401-comment file, and E030's 2457-comment
harvest shares exactly 2 comment ids with it.

So the zero is a well-evidenced fact about **Hacker News comments**, and the
sentence that generalises it to public conversation is not carried by the
evidence behind it. This experiment changes one variable — the venue — and changes
nothing else in the instrument.

| | E031 (the run being compared against) | E032 (this one) |
|---|---|---|
| venue | Hacker News comments, Algolia | **declared below** |
| harvest rule | trigger vocabulary about an event | **structural: no requirement vocabulary** |
| clause reader | one question, three arms | one question, three arms |
| linkage rule | shared rare content token | **identical** |
| pair reader | `same` / `not same` / `unclear` | **identical** |
| control | length-matched random pairs, reader-adjudicated | **identical** |
| instrument gates | A3 κ ≥ 0.6, A4 nonsense, A5 separation, A6 pair positives | **identical, all four** |

E031's numbers are the declared baseline: candidate pairs 0 `same` of 100,
control pairs 0 `same` of 100, difference 0.0000 CI95 [−0.0370, 0.0370], on 63
clauses across three arms, with κ = 0.7189 and A6 at 20/20 and 0/10.

## Venue, declared with a substitution rule

**Primary:** Stack Exchange, sites `woodworking`, `outdoors`, `cooking`,
`boardgames`, `gardening` — public, unauthenticated, non-programming, and its
question bodies are long and self-contained where an HN comment is short and
anchored to a story. Unauthenticated budget is 300 requests/day per IP; the
declared harvest needs 6.

**Substitution, declared now so it cannot be chosen after seeing data:** if the
primary venue cannot supply the declared population — rate-limited, unreachable, or
fewer than 60 usable bodies — the fallback is Reddit long-form posts from
non-programming subreddits. Whichever venue is used is recorded in
`VENUE.md` with its reason, and the substitution is not made on the basis of
which venue returned more recurrences.

## Population, declared before the fetch

1. **All questions** in each site, `creation` inside 2025-01-01…2026-06-30,
   `sort=votes`, `filter=withbody`, pages until 40 per site are held.
2. Drop a question whose body has **fewer than 40 or more than 600 words**, and
   drop any question with no `owner.display_name` (author identity is required —
   F039's finding depends on knowing who is distinct).
3. **20 questions per site, 3 sites, 60 questions total** — deliberately the same
   clause scale as E031's 63, so the comparison is not a power comparison. **The
   three sites are the first three of the five declared above, in the declared
   order, that yield at least 20 usable bodies.** The rule is fixed before the
   fetch so the site cannot be chosen on which one returned more recurrences.
4. **No requirement vocabulary appears anywhere in the selection.** This is the
   F043 constraint in force: a trigger vocabulary must not define the population
   whose outcomes are being measured, and F043 measured that a trigger vocabulary
   finds people who state needs while being blind to what happened to them.

## The instrument, unchanged from E031

**q1 — clause extraction.** Given the question body, write the single capability
the author wants and does not currently have, as a clause of 5–30 words. Output
`none` if the body states no such capability. One clause per author.

**Linkage.** Two clauses pair when they come from **different authors** and
share **≥ 1 normalised content token**, where normalisation is E031's, imported
rather than reimplemented: lowercase, strip punctuation, keep tokens of length
≥ 4, drop E031's stoplist (`EXPERIMENTS/031-unfilled-requirement/common.py`
`normalise_clause`). E031's artifact and story exclusions have no counterpart
here and are not applied; the different-author exclusion is.

> **AMENDMENT-1, made before any pair was built and before any q2 adjudication.**
> This section originally said "≥ 1 content token rarer than the 200th most
> frequent token in this run's clause set". That is not E031's rule and would
> have changed a second variable at once. E031's final rule was `≥ 1` shared
> token after that normalisation, reached by relaxing `MIN_SHARED_TOKENS` from 2
> to 1 when the stricter form produced 4 candidate pairs against a chance
> expectation of 4.9 (its AMENDMENT-3). **With fewer than 60 clauses a rank-based
> cutoff also has no token at rank 200 to cut at.** The rule is now E031's, so
> the venue is the only thing that differs between the two runs.

E031's declared lesson (D062) applies before any adjudication: the count of
candidate pairs this produces is printed against the count chance alone
produces. If candidates ≤ chance, the linkage **cannot fire** and the run is
`not_evaluated` on A2 — F010's shape.

**q2 — pair adjudication.** Given two clauses from different authors, do they
state the same requirement? `same` / `not same` / `unclear`. Read blind to arm,
author, site and question.

**Control.** 60 length-matched random pairs drawn from the same clause set
through the same filters, adjudicated by the same reader on the same blinded
sheet. This is F043's missing control as fixed in E031 AMENDMENT-3 §3: a
permutation of the candidate set holds the selection fixed and cannot say what the
reader would answer about pairs nobody selected.

## Gates, declared before any adjudication

| gate | rule | fails ⇒ |
|---|---|---|
| **A1** | ≥ 95% of attempted rows answer; every held row re-readable from disk by digest | `not_evaluated` |
| **A2** | candidate pair count > the count chance alone produces | `not_evaluated` (rule cannot fire) |
| **A3** | reader κ ≥ 0.6 on ≥ 48 double-read rows | `not_evaluated` (labels not a measurement) |
| **A4** | nonsense: q1 returns a clause for ≤ 0.25 of 24 token-shuffled bodies; q2 returns `same` for ≤ 0.20 of 10 length-matched unrelated pairs | `not_evaluated` |
| **A5** | pair positive control: ≥ 16 of 20 synthetic positive pairs read `same` | `not_evaluated` |
| **B1 survive** | P_same(candidates) − P_same(control) ≥ **0.20**, CI95 excluding 0, **and** ≥ 2 `same` candidate pairs | — |
| **B2 kill** | 0 `same` candidate pairs, with A2, A3, A4, A5 all passing | — |

`B1` and `B2` are the same two numbers E031 declared, at the same margins, so
that the venue is the only difference between the runs.

## What each outcome decides, written before the run

- **B1 fires.** The zero is **venue-specific**. `STATE-in-flight-2.md`'s
  generalisation is withdrawn rather than softened, item 0d's "all three
  generators under this seat are closed" is withdrawn as venue-scoped, and a
  recurring requirement is written down with its authors, which is the first
  time this mission has held one.
- **B2 fires.** The zero **generalises past one venue class**. The mission's
  belief is strengthened from a venue statement to a general one, and
  E032's population becomes the second venue class behind it. The generator
  closes on evidence rather than on one corpus.
- **Any A-gate fails.** `not_evaluated`. No claim is made in either direction
  and nothing else in this repository moves.

**Ceilings declared now.** 60 clauses against E031's 63; two people needing the
same capability twice must both land in the sample; both readers are
sub-agent contexts of one model family, so κ is evidence the question is
answerable from the text and not evidence that two people would agree; one
platform, one language, one era. A positive result is a requirement recurring in
one venue class, not a market.

## Reproduction

    python3 harvest.py          # writes raw/harvest.jsonl + raw/fetch_log.jsonl
    python3 extract.py          # writes the clause sheet from raw/
    python3 tally.py --check    # re-derives every number in README.md from raw/