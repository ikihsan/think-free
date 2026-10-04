<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

<<<<<<< HEAD
# Failures — recorded findings, part 10 (F030)
=======
# Failures — recorded findings, part 10 (F029)
>>>>>>> E011: a live corpus of unmet needs is not a candidate generator


Source: session `2026-10-04-044`. A prior-art verdict drawn from a single search
query is wrong in both directions, demonstrated three times on one day.
<<<<<<< HEAD
Runnable evidence: `EXPERIMENTS/012-candidate-harvest/prior_art_probe.py`.

## F030 — A prior-art verdict from one query is unreliable in both directions

Source: session `2026-10-04-044`, 2026-10-04. All counts re-runnable from
`EXPERIMENTS/012-candidate-harvest/prior_art_probe.py` and
=======
Runnable evidence: `EXPERIMENTS/011-candidate-harvest/prior_art_probe.py`.

## F029 — A prior-art verdict from one query is unreliable in both directions

Source: session `2026-10-04-044`, 2026-10-04. All counts re-runnable from
`EXPERIMENTS/011-candidate-harvest/prior_art_probe.py` and
>>>>>>> E011: a live corpus of unmet needs is not a candidate generator
`prior_art_probe2.py`. Not a claim about any candidate.

## What happened

Screening 50 harvested needs killed 19 of them with the verdict "a tool already
owns this". That verdict decides candidates, so it was checked against
GitHub's public search rather than left as memory — and the first pass was
wrong twice, in opposite directions.

**False pass: 502 hits that were not prior art.** The query carried
`in:name,description,readme`. The phrase matched the README of `awesome-go`
(186917 stars), a self-hosting guide (22973) and a Discord bot (11277). The
count said "this space is well populated" and the population was three list
repositories.

**False gap: 0 hits that meant nothing.** The query for URL popularity scoring
returned `total=0`. That reads as nobody has built one. Re-asked with
`in:name,description` and ordinary phrasings, the same idea returns
`url popularity` 29 repositories (top: `evansims/socialworth`, 120 stars),
`link popularity` 83, `url citation graph` 4. And the cluster that looked
emptiest of all — agent memory portability, 14 hits with no serious project in
the top three — returns **40027** for `agent memory` and **1137** for
`ai agent memory server`.

## The observation

**A single search query decides a prior-art verdict, and it decides it wrongly
in both directions.** One phrasing produced a false kill, another produced a
false pass, and a third produced a false gap. Nothing in the count distinguishes
them, so the count cannot be the property.

This is the shape defect 22 records, arriving from the other end. There, a gate
asked "does this number occur anywhere in the artifact" and was green on a false
record. Here, a check asks "does a search return hits" and is green on a false
kill. Both are **a check that reads a proxy for the property it claims to read.**
MISSION.md already says absence of a hit is not originality; what is new here is
that the *presence* of 502 hits is no more evidence than the absence of 0, and
that a full-text index makes an unrelated hit indistinguishable from a real one.

## Falsification, both directions

- The multi-phrasing rule changes the answer on the cases tested: probe 1 said 0
  and probe 2 said 29-83 for URL popularity; probe 1 said 14 with nothing serious
  and probe 2 said 40027 for agent memory. The rule is not decorative.
- The rule is not a novelty check either, and does not become one. Every count
  here is GitHub's repository index: a tool on PyPI, npm or a commercial
  service reads as zero. It can refute; it cannot establish.

## What it changes

A prior-art verdict now needs **more than one phrasing, on more than one
corpus, with the phrasing written down** — the same requirement
`docs/policy/gate-falsification.md` places on a gate: read the property, do not
read a proxy for it. `verify_prior_art.py` in
<<<<<<< HEAD
`EXPERIMENTS/012-candidate-harvest/` is written to that rule, and its four
=======
`EXPERIMENTS/011-candidate-harvest/` is written to that rule, and its four
>>>>>>> E011: a live corpus of unmet needs is not a candidate generator
`revise` rows are the honest output of following it, not a shortfall.

## What it does not show

It does not show that any of the four revised items is a real gap; they are
unverified, which is where they started. It does not show the mission's prior
rejections were wrong — `RESEARCH/PRIOR-ART-KNITTING.md` and F009 rest on opened
sources, not on a query. It is one agent's six queries against one index, on one
day, and a search index is a hostile instrument for the question being asked of
it.