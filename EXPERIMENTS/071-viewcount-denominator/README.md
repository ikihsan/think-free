<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E071 — The software arm's `view_count` zero was a missing observation

**Date:** 2026-10-09 · **Session:** 2026-10-09-002 · **Status:** complete —
**kill condition met**

Protocol (predeclared before any result was read):
[`PROTOCOL.md`](PROTOCOL.md). Re-derivation:
`python3 outcome.py` reads only `raw/probe.json`, exit 0 on the gates.

## What was asked

Four experiments (E067, E067b, E069 ×2) and `MISSION-OUTCOME.json` were
sitting unlanded on the tree, all resting on E069's headline:

> 100% of non-software need statements have `view_count` > 0 …
> **This directly contradicts the E063/E066 finding** … `view_count` is
> **0% in software need corpora**. The instrument's domain scope is **not
> software-narrow**.

E069 had read the software cells as **measured zeros**. The question here is
whether those cells are zeros at all.

## Results (observed)

| arm | platform | rows | carrying an arrival/view field |
|---|---|---|---|
| A | Hacker News (Firebase `item` objects) | 60 | **0** |
| B | GitHub issues (`GET /repos/{o}/{r}/issues/{n}`) | 8 | **0** |
| C | Stack Exchange `/2.3/questions` — **control** | 80 items | **80 positive** |

Keys probed, not one spelling: `view_count`, `views`, `viewCount`, `viewed`,
`viewed_count`, `impressions`, `hits`, `pageviews`.

| gate | threshold | observed | verdict |
|---|---|---|---|
| G1 control (Stack Exchange) | ≥ 95% of items carry a positive `view_count` | **80/80** (1.000) | ✅ |
| G2 Hacker News | 0% carry an arrival field | **0/60** (0.000) | ✅ |
| G3 GitHub issues | 0% carry an arrival field | **0/8** (0.000) | ✅ |

**Kill condition met.** The instrument can say no: its classifier returns
`zero`, `positive`, `absent` and `not_an_object` correctly on all five
fabricated cases, so `absent` is a distinction the code actually draws rather
than a default. Arm C is what makes arms A and B interpretable — the harness
reads `view_count` when the platform returns it, so its absence elsewhere is a
platform property, not a parsing artifact.

## What this establishes

- `observed`: **neither the Hacker News API nor the GitHub issues API returns
  any arrival/view field** on any sampled object. The E063/E066 corpora were
  harvested from exactly those two surfaces.
- Therefore **the software-arm "0% view_count" in E063, E066, E069 and E070 is
  a missing observation, not a measured zero** — exactly the D082 error this
  record already wrote down ("an arm that produced no observation is a missing
  observation, never a zero and never a denominator"), committed a second time
  by a run that read its own rule and then harvested a field the platform does
  not serve.
- **E069's `CONFIRMED` verdict is withdrawn.** Its non-software arm is
  unaffected — 14% `unserved-open-like` on non-software Stack Exchange measured
  a field Stack Exchange does return — but the "diametrically opposed" contrast
  that made it a confirmation compares a real measurement against a non-measurement.
- **`MISSION-OUTCOME.json` cannot be recorded as observed.** `vc_always_100_percent`
  and `instrument_validated_outside_software` were both derived from that
  contrast.

## The corrected statement

The E062 arrival instrument is **measurable only where a platform publishes
one**. Stack Exchange does; Hacker News and the GitHub issues API do not. So
the instrument is **Stack-Exchange-shaped**, and every software-arm reading of
it in this record is missing. **The instrument is not falsified — it was never
measured there**, and it remains a real and useful arrival measure on the
surface that serves it.

This also retires a route rather than opening one. E062's `view_count` was
going to be carried into software corpora to find arrivals that E063/E066 could
not see; that is now known to be impossible from those APIs, not merely
unmeasured. Per D080/D083, a fresh observation has to come from a surface that
publishes arrivals.

## Ceiling

Scoped to the **public documented API response objects** — the only surface
E063/E066 harvested from and the only one a reproduction can use. This does
**not** claim Hacker News or GitHub expose no view counters anywhere; a web UI
or an undocumented endpoint is untested. GitHub's per-issue `reactions` block
returns `total_count` and was probed for (and is not an arrival count), but a
full impressions metric would need a different product. The claim is the narrow
one that blocks the landing: **the corpora carry no arrival field, so the
software-arm cell cannot be a measured zero.**

## Reproduction

```bash
cd EXPERIMENTS/071-viewcount-denominator
python3 probe.py     # 3 network arms -> raw/probe.json
python3 outcome.py   # gate table -> results.json, exit 0 on the gates
```

Environment: Python 3.8.10, stdlib only. Runtime ≈ 40 s (network-bound).
GitHub's anonymous rate limit was hit once during development on a 429 body;
that row is recorded as an error and excluded from the denominator by
`outcome.py` rather than counted as a zero.