# E031 — do unfilled departure requirements recur?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Declared 2026-10-05, after E030 closed and before one account in this
experiment was read and before any rate was computed.** Task T-0075. Fixed in
advance; D058 forbids moving a threshold after seeing which side of it the data
fell on.

## The question, and what E030 left on the table

E030 established a **real population** — departure-framing comments are
distinguishable from ordinary same-story comments (held-out separation 0.64 vs
0.036) — and **falsified its own ruler** (F050): the declared statistic read
coincidence between long comments, its permutation null explained the arm
difference, and length matching reversed the sign (F050, AMENDMENT-9).

F050's own closing instruction is this experiment's design constraint:

> *Any recurrence claim built on such a statistic needs A9's null wired in from
> the start, and its linking tokens printed, or it will fire on coincidence.*

E030 also never read the population **for what it says about the gap rather than
the move**. 326 of its 919 accounts carry a *seek* framing — "alternative to",
"what are you using instead of" — which asks for something and therefore names
no successor. Those are unfilled by construction rather than by measurement, and
that is the one demand-side population in this record stated by someone who had
depended on the thing.

This is the **second independent test of task-level recurrence** in public text,
after the need corpus (F033 collapsed its strongest cluster >100×; F039 found
1250 individuals each asking once, no recurrence). If it also finds none, the
absence stops being a property of a trigger vocabulary and starts being a
statement about public accounts. If it finds some, the mission holds its first
cross-author recurrence of a stated clause — a lead, not a candidate.

**The unit is a reader-extracted clause.** Not a shared rare token. E030 proved
what a token-overlap statistic measures, and the only instrument left that can
carry "the same requirement" is one that reads what the account says is missing.

## H1 — the population rates

Among seek-framed departure accounts, the rate at which the account states a
capability something the author relies on cannot do is materially higher than
among ordinary comments in the same stories.

## H2 — recurrence, which is the experiment

Among reader-extracted clauses, the rate at which two accounts by **different
authors**, departing from **different artifacts**, on **different stories**,
state the same requirement, exceeds what the same procedure finds under a
permutation null that preserves each clause's length and each arm's size.

H2 is the claim E030 could not evaluate. Its kill gate is the null, not the
point estimate.

## Corpus — no new fetch

E030's captures, already on disk and digest-recorded: `raw/treatment.jsonl`
(919) and `raw/control.jsonl` (2687) under
[`../030-departure-recurrence/`](../030-departure-recurrence/raw/). `recount.py`
restratifies them and writes the digests it read. No network access is used and
`session verify` shows the commands that ran.

## Strata, declared before any reading

The split is **by E030's framing phrase**, a field in its raw captures, not by
anything read here:

| arm | framings | rows |
|---|---|---|
| **A1** seek | `alternative to`, `alternatives to`, `looking for a replacement`, `what are you using instead of` | 326 |
| **A2** move | `switched from`, `migrating from`, `moved off` | 593 |
| **A3** ordinary | control arm, no framing phrase | 2687 |

A1 is the unfilled population; A2 is a population that named a successor by the
same lexical event, so it bounds how much of any A1−A3 difference is the framing
at all; A3 is the base rate of the same question in the same stories. The
stratum is a **hypothesis about successors, not a measurement of one** — the
reader adjudicates it on every row and the disagreement is reported.

## The reader question — one wording, three arms

Identical text for every arm, in [`RUBRIC.md`](RUBRIC.md):

> **q1** Does this comment state a **capability that something the author relies
> on cannot do**? `yes` / `no` / `unclear`.
> **q2** *(only if q1 = yes)* Copy, **verbatim and from inside this comment**,
> the shortest phrase that states the missing capability.

One wording is the point. A control question reworded for the control arm is the
defect E029 found by collision (its control was the treatment arm renamed).
`verify_labels.py` checks that all three arm views contain the byte-identical
question block, so the wording cannot differ by arm, and it checks that every
q2 phrase is a **verbatim substring** of that row's own text — a clause no reader
copied is rejected before any rate is computed.

**Reader blindness.** No arm label, no stratum name, no author, no story title,
no departing artifact, no word count in any view. `verify_labels.py` fails if
the string `A1`/`A2`/`A3`/`seek`/`move` appears in a view.

**Sample.** 72 rows per arm, seeded (`random.Random(3101)`), sorted by
`objectID` first. Plus **24 nonsense rows**: A3 rows whose content tokens are
deterministically shuffled (seed `3102`), kept in the views so the instrument is
exercised on text that carries no clause, and excluded from every rate.

## Reliability, before any gate decides

Two readers, same rubric, both blind, neither shown the other's labels.
**A3-agreement gate:** Cohen's **κ ≥ 0.6** on the three-label q1 scheme. Below
it, the verdict is `not_evaluated` and no recurrence number is reported. This is
the floor E029 missed at κ = 0.5004, declared here so the miss is a gate result
rather than a footnote. Reader 2 reads a **disjoint 40-row re-read sample** for
an independent check on clause text.

## Recurrence, declared

For every pair of q1-`yes` accounts in the same arm:

- **linkage candidate** when the normalised clauses share ≥ 2 content tokens,
  after lowercasing, stripping punctuation and stopwords, and dropping the
  departing artifact's own tokens. Normalisation and stoplist are in
  `common.py` and are fixed here.
- **independent** when authors differ, departing artifacts differ, and story ids
  differ. Same-author, same-artifact and same-story pairs are dropped and
  counted.
- **adjudicated same** only when a reader, shown both printed clauses and told
  nothing else, marks them `same requirement` / `different` / `unclear`.
- **P2** = adjudicated-same independent pairs ÷ all independent candidate pairs.
  Reported with Wilson CI95 per arm and the difference by Newcombe.

**The null is A9, wired in before the first pair is read.** 200 permutations of
clause→account assignment **within arm**, preserving each clause's token count,
each arm's size and the author/artifact/story structure. H2 survives only if
P2 exceeds the null's 95th percentile and the observed count of adjudicated-same
pairs is ≥ 2 independent pairs. A single pair cannot clear this gate and the
protocol says so now.

**Length.** Because the unit is a reader's clause rather than a comment, the
E030 length trap is mostly closed by construction; the length-matched
recomputation is still declared and run, matching arms on median clause token
count in bands, and reported whatever it says.

## Gates

| gate | declared rule |
|---|---|
| **A1** capture integrity | every arm's source file digest recorded; every view digest recorded and re-checkable; stratum row counts equal the table above |
| **A2** view hygiene | identical question bytes across the three arm views; no arm word in any view; every q2 phrase a verbatim substring of its own row |
| **A3** reader agreement | **κ ≥ 0.6** on q1 across both readers, computed before B1 or C1 is read |
| **A4** nonsense control | q1 `yes` rate on the 24 shuffled rows ≤ 0.25, else the instrument reports a clause where none exists |
| **A5** planted separation | the successor question — *"does the comment name the thing the author moved to?"* — separates A2 from A1 by **≥ 0.20** in q1 rate. The A2 arm's answer is known from the stratum definition, so a failure names a blind instrument |
| **B1** H1 | A1 q1 rate − A3 q1 rate ≥ **0.20** with CI95 excluding 0 |
| **C1** H2 | P2 above the null's 95th percentile **and** ≥ 2 adjudicated-same independent pairs **and** A3 passed **and** A5 passed |
| **D1** inconclusive | between the two readings |

## What each outcome changes

- **C1 fires.** The mission holds its first cross-author recurrence of a stated
  capability clause, from a population structurally independent of the need
  corpus, and D051's "no need-level recurrence" no longer generalises beyond the
  trigger vocabulary. It is a **lead**: it owes a mechanism, a differentiation
  and an adoption path, none of which this supplies.
- **B1 fires, C1 does not.** A1 states unfilled requirements more than ordinary
  comments do, and none of them repeat across independent authors. That splits
  the population: the demand is real and unshared. A **fourth** generator closes,
  and item 0's owner decision loses an axis rather than gaining one.
- **A3, A4 or A5 fails.** The instrument is named blind and the verdict is
  `not_evaluated` — E028's outcome and a real result. **The null's ceiling
  still applies**, so a failure to clear C1 on a valid instrument is evidence
  about the world and a failure of A3 is not.

## What this cannot decide

- **Not a measurement of need.** It says nothing about how many unmet needs
  exist, and re-reads none of the 1250 people in the need corpus.
- **Not usefulness or adoption.** No person is contacted. A clause is a
  statement about a need, which is evidence and not the need.
- **Not a candidate.** C1 names a clause, not a product.
- **Both arms over-represent public technical argument**, and A1's seek framings
  are ordinary English phrases a reader cannot always resolve to a departure.
- **Reader budget caps the resolution**: 72 rows per arm resolves a q1 rate to
  roughly ±0.11, and recurrence needs the observed count to clear a null built
  from the same arm, so a real-but-small recurrence will read as null. That
  ceiling is declared here, before the numbers.
- **A2 is a lexical stratum, not a verified fact** about who named a successor;
  A5 is the only check and it is one question.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recount.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/a2_reader.py
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py treatment
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py move
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/verify_labels.py ordinary
tools/x -- python3 EXPERIMENTS/031-unfilled-requirement/recurrence.py
```