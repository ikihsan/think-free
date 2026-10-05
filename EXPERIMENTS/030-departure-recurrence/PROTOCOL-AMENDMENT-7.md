# E030 — Amendment 7

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the diagnostic in AMENDMENT-6 §4 was read and before the
third run.** It withdraws the statistic both previous runs produced.

## 1. Withdrawn: every cluster-level number from this experiment

`AMENDMENT-6`'s diagnostic exists to say whether the declared statistic means what
it says. It does not.

The treatment arm's largest connected component holds **259 of 919 accounts**
across **241 authors, 214 artifacts and 249 stories** — **28% of the arm in one
blob**. Its linking tokens, taken from `raw/clusters_treatment.jsonl`, are:

```
2014   2022   anyways   appreciated   aspect   coded
```

**Years and filler.** Nothing there is a clause. Single-linkage clustering over a
graph with ~8 500 rare tokens chains into a giant component almost regardless of
content: a token with document frequency ≤ 5 contributes up to 10 pairs, and
union-find joins everything that is reachable. So `R_shared = 0.349` against
`0.215` — and the first run's `R_c = 0.000` — are **measurements of
chain-reachability**, not of two strangers failing at the same task.

This is F033's failure in a new costume: a cluster that looked strong because of
how it was built. The declared rule said *"two accounts recur when they share ≥ 2
rare tokens"* and then *"a cluster is a maximal set of accounts joined by that
relation"*. **"Joined by" was ambiguous between connected and mutual linkage, I
implemented connected linkage, and connected linkage is the wrong one.** Every
cluster-level figure from runs 1 and 2 is withdrawn, not restated.

## 2. The correction: read the declared pair rule literally

The declared unit was always the **pair**. The statistic becomes the pair-level one:

> **`R_pair` = accounts with at least one recurring partner ÷ |arm|.**

No components, no chaining. Two accounts recur when they share **≥ 2** signature
tokens each occurring in **≤ 5** accounts of the arm, by **different authors**, and
— in the declared variant only — naming **different departing artifacts**. Identical
rule in both arms in the matched variant, per `AMENDMENT-6` §2.

**Direction, declared before the run and not established.** Removing chaining
removes edges, so both arms' rates fall. Which arm falls further is not known in
advance and is the thing the run measures.

**Nothing else moves.** The rare-token rule, the common-token cutoff, the
author-distinctness requirement, the control arm's missing artifact field, the
B1/B2 thresholds in `AMENDMENT-6` §3, and the `≥ 3` multi-artifact cluster count
are all unchanged. The `≥ 3` count is now computed over **mutual groups** rather
than components.

## 3. Mutual groups, reported, feeding no gate

`R_pair` says whether an account shares its clause vocabulary with anyone. It does
not say **how many** people share it, and "two" is a much weaker claim than "six
organisations". So a **greedy mutual group** is also computed:

- vertices in ascending `objectID` order; start from the first unassigned vertex;
- repeatedly adjoin the candidate adjacent to **every** current member, breaking
  ties by the larger number of remaining candidates, then by `objectID`;
- stop when no candidate qualifies; mark members assigned and record the size.

Deterministic, and it is the honest form of "shared clause": every pair in a
mutual group shares the vocabulary, so no chain is involved. Sizes are reported as
a distribution, and the **largest** groups are printed with their members' author,
artifact and opening words so the linkage can be read rather than trusted.

**The count of accounts in a mutual group of ≥ 3 is also reported**, because a
shared clause among three or more people who never met is the claim the mission
has never been able to make about any corpus.

## 4. Why this is a conformance fix and not a new gate

The protocol's recurrence definition is a statement about **pairs**, and the only
thing I chose was the linkage used to assemble them. Correcting connected linkage
to the literal pair rule does not change a threshold, does not change a direction,
and cannot be chosen to favour an outcome: a pair-level rate under single linkage
is not a pair-level rate at all. The withdrawn numbers stay in the session record
and in this file.
