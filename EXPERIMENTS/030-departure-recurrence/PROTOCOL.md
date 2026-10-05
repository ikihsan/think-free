# E030 — do departure accounts supply a recurring unmet clause?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Declared 2026-10-05, before any account was read and before any rate was
computed.** Task T-0074. What follows is fixed in advance; a threshold that moves
after seeing which side of it the data fell on is a rationalisation, and
[`DECISIONS-SCREENING-4.md`](../../DECISIONS-SCREENING-4.md) D058 forbids it.

## The question, and the evidence class this mission has never read

Twenty-nine experiments have looked outward at exactly two things:

| class | instrument | what it can carry |
|---|---|---|
| **what people say they lack** | trigger-vocabulary harvest of Hacker News comments (E012, E022, E026, E029) | a wish. F039: 1250 people, median one comment each. F029: **0 of 50** survived |
| **what exists, and how much of it is used** | repository counts, registry names, install and copy counts (E011, E014, E015, E020) | existence and popularity. D060: **use is not fit** |

There is a third class, available in public and never read here: **an account of
leaving**. "We moved off X because it cannot do Y", "what are you using instead of
X", "I replaced X with Z after it broke on W". It differs from both of the above in
the property that matters — the clause is stated **by someone who actually depended
on the thing**, and the account exists **because they paid for it in time, money or
migration**. A need statement imagines the missing thing; a departure account
describes the moment the thing was found wanting.

Two things follow, and they are why this is worth an experiment rather than a
method note.

1. **It is the demand-side recurrence axis, from a population that cannot inherit
   the need corpus's failure.** F033 collapsed the strongest need cluster by >100×
   under a relevance filter and F039 then found the corpus is 1250 individuals each
   asking once, with **no need-level recurrence inside it**. So the mission has
   never observed two people who never met failing at the same task. A departure
   account population is a *different* population, not a re-read of the same one:
   the events are independent, and two organisations naming the same missing
   capability is a fact about the world rather than about a shared vocabulary.
2. **It targets the gap E028 left open.** D060's ceiling states it exactly:
   *"it does not license treating absence of documented fit as demonstrated
   absence of fit — a product that does the thing without saying so is invisible in
   both directions."* E028's two blind readers both returned `partial` for the row
   with the strongest use evidence in the whole record, because no document states
   the clause. **A use account is fit evidence that a document is not**, and the
   mission has never tested whether it can carry a verdict.

**H1.** Among public accounts of leaving a named artifact, the rate at which an
account shares a *rare* vocabulary cluster with an account written by a **different
author** about a **different departing artifact** is materially higher than the
same rate over ordinary comments drawn from the same stories.

**H2 (pilot).** For a clause stated in departure accounts, an account in which a
named person says a named artifact does that clause identifies fit at a rate above
the rate for artifact–clause pairs drawn at random. If so, use accounts are a
fit-adjudicating instrument that this record does not have.

## The strongest existing alternative, and it cannot be executed here

The strongest existing alternative to mining public departures is **asking people
who left**: churn interviews, win/loss reviews, exit surveys. That is what the
industry does, it is funded, and it returns the same information with the reporting
bias removed. **It is labelled unperformed**: it needs people, and this mission
has none and is not authorised to contact anyone.

The strongest **executable** alternative is the corpus this mission already holds.
Its recurrence was measured and it is zero (F039), and E029 measured its
need-to-build link at CI95 [−0.0156, +0.1125] (F049). H1 is therefore a genuine
contrast and not a second reading of a known null.

The **rival explanation W-A** is that recurrence in the treatment arm is story
topic, not clause. The control is drawn from the **same stories**, and the
signature removes the story title's tokens and the departing artifact's tokens, so
a shared topic cannot survive as a shared clause.

## Corpus, and the two probes that chose it

One corpus: **Hacker News via the public Algolia API**, comments created after
2024-01-01. It is already this mission's instrument of record (E012, E022, E029),
it needs no token, it costs nothing, and its field set is machine-readable.

The framing phrases were fixed **before** the corpus was chosen, by asking what a
departure account says rather than what a need statement says. Ten phrases were
probed for volume and the counts are recorded so the choice is visible:

| framing phrase | comments since 2024-01-01 |
|---|---|
| `"what are you using instead of"` | 8 |
| `"looking for a replacement"` | 94 |
| `"moved off"` | 359 |
| `"migrating from"` | 529 |
| `"switched from"` | 2637 |
| `"alternatives to"` | 3500 |
| `"alternative to"` | 11045 |
| `"replaced"` | 73853 |
| `"instead of"` | 124240 |
| `"insteadof"` | 14 |

These counts are a **power** decision, not an outcome decision: no rate, no
cluster and no clause was computed from them, and none can be. The eight
high-precision framings give ~6 500 comments before filtering; the two vague ones
are excluded because `"replaced"` and `"instead of"` are ordinary English.

**Channels declared as unread**, per rule 5 of
[`docs/process/experiment-protocol.md`](../../docs/process/experiment-protocol.md):
GitHub issues and pull requests, package-registry dependents, support forums,
Reddit, and the open web. GitHub issue text is the largest of these and the most
template-contaminated (migration guides and changelogs copy the phrase), so its
absence is a limit on this result and not a neutral fact. The public Stack Exchange
API answers Superuser with a 300-request daily unauthenticated quota, which is
enough to state the channel and not enough to power a rate from it.

## Population and extraction, fixed before the data

1. Every comment created after 2024-01-01 containing one of the eight framing
   phrases, one pass per phrase, deduplicated by comment id.
2. **An account enters the treatment arm** when all three hold:
   - a framing phrase occurs in the comment, case-insensitively;
   - a **departing artifact candidate** resolves immediately after the phrase —
     the span to the first punctuation or 40 characters, whichever is shorter — and
     contains a token matching `^[A-Z]` or `^[a-z0-9]+[._-][a-z0-9]`. This is a
     syntax test, decided without reference to any corpus frequency;
   - the comment has **≥ 40 stripped words** after HTML removal.
3. The **control arm** is drawn from the **same stories**: comments on those
     stories, by authors not in the treatment arm, containing **no** framing
     phrase, ≥ 40 stripped words, and not a reply to a treatment account. Sampled
     to the treatment arm's size, seeded (`random.Random(3004)`), story-stratified
     so no story contributes more than its treatment share.
4. **Exclusions applied blind to every rate:** a comment by an author who also has
   a treatment account is dropped from both arms; the reason is printed.

## The recurrence rule, declared

For each account in an arm:

- **signature** = the set of lowercased word tokens of length ≥ 4 in the comment,
  minus the story title's tokens, minus the departing artifact candidate's tokens,
  minus every token occurring in **more than 2%** of that arm.
- **Two accounts recur** when they share **≥ 2** signature tokens that each occur
  in **≤ 5** accounts of the arm (a *rare* shared token), they have **different
  authors**, and they name **different departing artifacts**. A token in more than
  5 accounts is topic, not clause — this is the rule F033 needed and did not have.
- A **cluster** is a maximal set of accounts joined by that relation.
- A **multi-artifact cluster** is a cluster whose accounts name ≥ 2 distinct
  departing artifacts and come from ≥ 2 distinct authors.

**Primary statistic.** `R` = accounts in a multi-artifact cluster ÷ |arm|. `R_t`
and `R_c` are reported with Wilson CI95 and their difference with the same
interval method. `stats.py` computes them from `raw/` and writes `results.json`;
nothing below is typed from memory.

## Gates, all declared now

| gate | declared rule |
|---|---|
| **A1**, fetch validity | ≥ 90% of attempted comment ids return a body; ≥ 90% of framing-phrase pages fetched without error |
| **A2**, positive control | **5 of 6** planted framing+artifact probes return ≥ 1 account. Declared as E029's A2 did: a known-answer control on the instrument, not a self-report |
| **A3**, nonsense control | the same probes with a nonsense artifact name return **0** accounts |
| **A4**, population | treatment arm ≥ 300 accounts and control arm ≥ 300 accounts, else the rates are not reportable and the verdict is `inconclusive` |
| **B1**, survive | `R_t − R_c` ≥ **0.10**, its CI95 excludes **0**, and **≥ 3** multi-artifact clusters exist → **H1 survives** |
| **B2**, kill | `R_t` CI95 overlaps `R_c`'s, **or** fewer than 2 multi-artifact clusters exist → **H1 dies** |
| **B3** | between the two → `inconclusive` |
| **C1**, H2 pilot | for the ≤ 3 largest multi-artifact clusters, the rate at which a named artifact has a use account naming the clause exceeds the shuffled-pair rate by ≥ 0.10 with CI95 excluding 0 → H2 supported; otherwise `not_evaluated` or refuted, whichever the numbers say |

**A4 and the two arms are the floor.** 300 accounts per arm gives a Wilson
half-width near 0.03 at `R ≈ 0.1`, which resolves the declared 0.10 margin; below
300 the declared margin is not resolvable and the experiment says so instead of
reporting a rate.

## What each outcome changes

- **B1 (survives).** Item 0d's seat stops being empty for a measured reason. The
  mission would hold its first **cross-organisation recurrence of a stated
  capability clause**, which is the demand evidence F033 and F039 measured to be
  absent from the corpus the mission had. That is a lead, and it still owes a
  mechanism, a differentiation and an adoption path — none of which this supplies.
- **B2 (dies).** A **third** generator closes, from a population structurally
  different from the first two, and the closure of demand-side generation stops
  depending on the trigger vocabulary that F043 showed is blind to outcomes. That
  is a real narrowing of item 0's owner decision: it would say the absence of
  recurrence is a fact about public accounts, not an artefact of the harvest.
- **A2/A3/A4 failure.** The instrument is named as blind and no rate is reported.
  E028's outcome, and a real result.
- **C1 supported.** E028's named gap closes in the direction that *use accounts are
  fit evidence*, and D060's rule acquires the one evidence type it has lacked.

## What this cannot decide

- **It is not a measurement of need.** It says nothing about how many unmet needs
  exist, nothing about F029's 0-of-50, and nothing about the 1250 people in the
  existing corpus, none of whom are re-read here.
- **It is not a usefulness or adoption claim.** No person is contacted and no
  artifact is used. H2's "use account" is a *statement about* a use, which is
  evidence and not the use.
- **A surviving H1 is a lead, not a candidate.** It names a clause, not a product.
- **The population is self-selected into public technical argument**, and
  departure accounts over-represent tools with loud unhappy users. Both arms carry
  that.
- **The departing-artifact syntax test misses lowercase brand names** and counts
  any capitalised word in the span as a candidate, so artifact identity is noisier
  than a reader would make it. It is deliberately mechanical, and its error rate is
  reported rather than repaired by judgement.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/harvest.py
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/extract.py
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/recurrence.py
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/use_accounts.py
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/stats.py
python3 -m unittest discover -s EXPERIMENTS/030-departure-recurrence -p 'test_*.py' \
  -t EXPERIMENTS/030-departure-recurrence
```
