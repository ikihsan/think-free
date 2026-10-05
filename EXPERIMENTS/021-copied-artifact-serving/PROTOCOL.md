# 021 — the protocol as declared, in full

<!-- origin-meta
owner: EXPERIMENTS/021-copied-artifact-serving/README.md
status: active
last-verified: 2026-10-05
-->

Written 2026-10-05, **before any count on the population was read**. The
hypothesis, both gate arms, all four controls, the thresholds and the instrument's
own limits are fixed here so that the run cannot be read as narration.

## What was read before this file existed, and what was not

**Read:** the instrument's shape. Sourcegraph's public streaming search API
answers unauthenticated, takes a `file:` path pattern and `select:repo`, and
returns a `progress` event carrying `repositoriesCount`. Probes were run against
four **calibration anchors unrelated to this population** — `package-lock.json`,
`node_modules/.package-lock.json`, `.github/workflows/ci.yml`, and one
deliberately absent path — to establish saturation behaviour, fork and archive
exclusion, and the shape of a zero. Results in `README.md` §calibration.

**Not read:** no count, no repository list and no per-repository existence check
was taken against the young arm, the mature arm, the placebo arm, or any of
F037's four documents, before this declaration. No reading of any file inside
this population was done for this experiment.

**The leak this does not cover:** this session knew F037's conclusion — that four
young-arm documents tell the reader to copy a directory — before designing
anything. That is prior reading of another experiment's *result*, not of the
population, and it is the reason H1 is phrased about volume rather than about
attribution.

## The instrument premise in the record is wrong, and that is a finding already

`STATE-next-actions.md` item 0 says the cheapest honest proxy for "was this
copied" is a repository count that **"no public API serves"**, and that the
first move is therefore to decide whether forks, dependents or templates are an
adequate stand-in. **A public unauthenticated API does serve it.** This is
`observed` on 2026-10-05 and it removes the blocker that item was written
around; it does not by itself settle which signal is right, which is what the
arms below are for.

Three properties of that API are fixed here as **the ceiling on every number in
this experiment**, before any is read:

1. **It is a floor, not a census.** The index is a subset of GitHub and its
   coverage of any population is unknown until measured. Every count is
   reported as *at least*.
2. **Forks and archived repositories are excluded by default.** A copy that was
   made by forking would be invisible; a copy that was made by `cp -r` into a new
   repository is visible. Both are excluded and included respectively by the
   default and by `fork:yes archived:yes`.
3. **The pattern is a path glob over indexed files, so a repository counts once
   no matter how many of its files match.** A field with one copied directory and
   a field with fifty are the same row.

## H1 — the serving signal in a young vocabulary is copies, not installations

**Claim, in one sentence.** If F037's reading is right — the artifact a coding-
agent user puts in their repository is a directory they copy rather than a
package they install — then counting repositories that contain a coding-agent
configuration directory should return a figure large enough that the young arm's
install-channel readings are a rounding error against it, and the prior-art
screen's premise failing in young vocabularies is instrument blindness rather
than the world.

**Declared gate.** H1 **survives** if the count of indexed repositories
containing a coding-agent configuration directory **with at least one hook
declared** is **≥ 20× the young arm's total monthly install readings summed over
all four channels**, summed across every channel 015 and 017 read. It is **dead**
at **≤ 5×**. Between 5× and 20× is `inconclusive`, and the gate does not round
up in the hypothesis's favour.

The 20× and 5× are chosen because of what the competing reading needs. If the
copy channel is only a few times the install channel, the screen was reading the
dominant channel and F037's "used and invisible" is wrong. If it is one or two
times, the installs were telling the truth. Twenty times is the smallest factor
at which "the channel we counted is not the channel the field uses" is not
arguable.

**A floor is not required for this gate and none is declared.** The mission has
no absolute threshold for "used"; it has relative ones, and inventing an absolute
one here would be a number with no source. The comparison is against a measured
figure this repository already holds.

## H2 — forks and dependents are an adequate stand-in for copies

**Claim, in one sentence.** Item 0's proposed first move was to decide whether
forks, dependents or templates can stand in for a copy count. If they can, the
instrument question is closed with the tools already owned; if they cannot, the
copy count is required and is worth its cost.

**Declared gate.** H2 **survives** if, among configurations whose copy count is
demonstrably high, **at most 25%** have a repository that is neither forked nor
a template — that is, if fork and template counts separate the copied
configurations from the uncopied ones well enough to rank them. It is **dead** at
**≥ 50%**. Between 25% and 50% is `inconclusive`.

A configuration's copy count is *demonstrably high* when it clears **≥ 100
indexed repositories**; *demonstrably low* at **≤ 5**. Rows between the two are
not used, because a band this wide cannot order anything and including it would
manufacture a separation. This is the record's own named falsifier — "a
known-copied configuration whose repository has neither" — turned into a rate
rather than a single counterexample.

## Controls, all four declared before the run

| control | what it is | what it decides |
|---|---|---|
| **C1 calibration** | four unrelated anchors: a saturated path, a rare path, a moderate path, an absent path | whether the instrument can distinguish 0 from few from many, and where it saturates |
| **C2 index coverage** | what fraction of the **61 repositories 017 already read** the index contains at all, by arm | whether any count below is a fact about the world or a fact about the index. **If the young arm's coverage is near zero, H1 is not evaluable and is reported so** |
| **C3 the mature arm** | the same copy measurement applied to mature-vocabulary configuration anchors | whether a large young count is about coding agents or about configurations in general. The strongest available baseline, not a weak one |
| **C4 the absent path** | a path that cannot exist, run in every configuration shape a real path is run in | that a zero from this instrument is a zero and not a refusal — F032's defect class, which has already bitten this repository twice |

**C2 is the load-bearing control and it can refuse the whole experiment.** The
index's coverage of this population class is unknown, and a large count on a
thin index is still a floor — but a *small* count on a thin index is not a
finding about the field. If the young arm's coverage comes back low, H1's
direction is reported with that caveat attached and no gate is declared met on
the strength of it.

## Limits, stated before the numbers are read

- **Every count is a lower bound.** A floor can exceed a threshold and support
  H1; a floor below a threshold cannot refute anything, only fail to support.
  H1's *dead* verdict therefore rests on the ratio being small, which is a
  statement about two floors and is correspondingly weak. This asymmetry is
  declared rather than discovered.
- **Attribution is not measured.** Whether a counted repository copied *this*
  artifact or independently wrote a similar one is not decidable from a path
  count. H1 is a statement about a channel's volume, not about any incumbent's
  adoption. Anyone reading `survives` as "these incumbents are serving" is
  overreading it, and the README says so again at the result.
- **One young vocabulary, one index, one moment.** The arm is coding-agent
  guardrails, chosen by 015 because its cluster recurred. The finding is about
  that vocabulary.
- **A pattern's specificity is a judgement.** Deciding which paths count as "a
  coding-agent configuration directory with hooks" is the one non-mechanical step,
  it is written down here, and every pattern used is reported next to its count
  so a reader who disagrees can see what the disagreement is worth.
- **This validates nothing about a candidate.** H1 surviving would mean the
  screen's blind spot is larger than measured. That is a method result. It does
  not reopen any of the twelve prior-art deaths by itself, because "prior art
  exists" and "the need is served" are different claims and only the first has
  been in question.

## Method

`copycount.py` performs every query and writes each raw capture to `raw/` before
parsing, so a figure in `results.json` can be traced to bytes on disk.
`coverage.py` reads the 61 repositories from `017`'s committed artifacts — no
network call to GitHub is needed for the population list. `tally.py` computes
both gates, all four controls, and refuses to report a gate met when C2 shows
the arm was not in the index.

Every query is issued unauthenticated. A refused, truncated or HTTP-error answer
is recorded as `refused` and is never counted as a zero, and a query whose
`skipped` list names a limit is reported with that limit attached rather than as
its number.