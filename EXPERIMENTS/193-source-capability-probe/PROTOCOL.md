<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E193 PROTOCOL — source capability probe for the demand axis

**Date declared:** 2026-10-19, before any request was sent.
**Host:** `instance-20260717-0947` (2 CPUs, Python 3.8.10).
**Status:** running.

## Why this exists

187 experiments in this record have measured *whether a need is served*
against public Q&A corpora. **No experiment has measured whether anyone
*pays* for a solution to it.** Money is the strongest demand evidence that
exists and it is a different signal from a question: a question costs a
person nothing, a purchase costs them money.

This probe does not measure demand. It establishes **which demand-bearing
sources are reachable from this host at all**, because a fresh observation
axis is only worth declaring after that is known. The record has been bitten
by exactly this before — E175's G0 runs were withdrawn as instrument-limited
after `403` responses, and the constraint "GitHub's unauthenticated core
budget is 60/hour" is a standing constraint — so the probe is the gate, not
the experiment.

## What is probed, and the bar

Ten sources in three roles. `control` sources are known-reachable from this
record's own history and must come back 200 — **if a control fails, every
other row is `not_evaluated`**, because the instrument is then broken rather
than the source being absent.

| # | Source | Role | Endpoint shape |
|---|---|---|---|
| 1 | Stack Exchange API | control | known used by E168–E185 |
| 2 | GitHub REST API | control | known used, 60/h unauthenticated |
| 3 | OpenAlex | control | known used by T-0015 |
| 4 | DuckDuckGo HTML | control | used by `RESEARCH/PRIOR-ART-KNITTING.md` |
| 5 | Reddit search JSON | demand | `reddit.com/r/<sub>/search.json` |
| 6 | Etsy search page | demand | `etsy.com/search?q=` |
| 7 | eBay sold/completed search page | demand | `ebay.com/sch/i.html` |
| 8 | Open Collective GraphQL | demand | `api.opencollective.com/graphql` |
| 9 | US Census CBP API | demand | `api.census.gov/data/2022/cbp` |
| 10 | data.gov CKAN API | demand | `catalog.data.gov/api/3/action/package_search` |

**Each row records:** HTTP status, `Content-Type`, body bytes, and — for
HTML pages — whether the body strips to more than 200 non-whitespace
characters. A `200` whose body strips to nothing is a **refusal, not a
capture** (`STATE-constraints.md`, the E028 lesson).

## Gates, declared before the run

- **G1 (control integrity).** 3 of 4 controls return a usable capture.
  **Fails → every non-control row is `not_evaluated` and the axis is
  declared unreachable from this host.**
- **G2 (at least one demand source is usable).** ≥2 of rows 5–10 return a
  capture. **Fails → the money axis cannot be measured here, and that is
  itself the finding to record.**
- **No gate can be met by a body the probe did not write.** Every row's
  bytes are hashed and the first 200 characters stored raw.

## Kill / continuation

This probe cannot kill a candidate. It decides only whether one further
experiment on this axis is *possible* from this host. If G1 and G2 both
pass, the next action is a declared harvest on the reachable demand sources.
If either fails, the axis is recorded as unreachable with the failing
statuses attached, and the next action is a different fresh observation.

## Raw data

`raw/probe.json` (written by `probe.py`), `probe.py` is the only script.
Reproduce with:

```bash
tools/x -- python3 EXPERIMENTS/193-source-capability-probe/probe.py
```