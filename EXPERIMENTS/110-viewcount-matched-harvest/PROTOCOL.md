# E110 — matched-harvest control for the view-count principle

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Origin

Session `2026-10-12-001`. Supersedes E109 (Pub.dev), which was written and
never run: another domain on the same instrument would have inherited the defect
this experiment tests for.

**The defect, found by reading committed bytes, not by running anything.**
`EXPERIMENTS/107-github-repos-viewcount/harvest.py` builds its two arms from
two *different* topics, each sorted by stars descending:

```python
NEED_TOPICS   = ["web-framework", "database", "orm", "cache", ...]
GENERIC_TOPICS = ["utils", "common", "core", "library", ...]
query = f"topic:{topic}"          # then sort=stars&order=desc, take first 80
```

Re-deriving from `raw_data.json` (160 rows, `observed`): **80 of 80** rows in the
intended need arm carry `web-framework`, and **80 of 80** rows in the intended
random arm carry `utils`. The classifier then reads those same topics, so
assignment is circular — it reproduces the harvest. The published
`Cliff's δ = 0.826` and "need median 8.6× random" therefore compare *the 80
most-starred web frameworks* against *the 80 most-starred utility libraries*.
That is true, and it is not the view-count principle: the arms differ in kind by
construction, and fame is the selection criterion.

`STATE.md` and `STATE-next-actions.md` also report E107 incompatibly (FAIL vs
ALL GATES PASS) for the same experiment id. Only one can be read.

## The decision this experiment changes

Named before any fetch: **whether the view-count principle is a usable discovery
instrument or a restatement of topic fame.** Roughly fifteen experiments
(E090, E095, E100–E103, E107, E108) report where it "generalizes". If the
effect is a harvest artifact, all of them measure their own sampling design and
the line closes. If it survives a matched harvest, the line stands and the
domain sweep becomes worth continuing.

## Question

With both arms drawn from **one identical pool** under **one identical
selection**, does a need-label predict arrival count?

## Hypothesis

- **H1 (confound):** the gap is produced by asymmetric harvest and by repo age.
  Under a matched harvest with age held in view, the effect shrinks toward the
  null and/or reverses.
- **H0 (principle):** a need-related repository accrues more arrivals than a
  non-need one *drawn from the same pool at the same age*, and the effect is
  not explained by age.

## Design — the matched harvest

| | value |
|---|---|
| Platform | GitHub code repositories (E107's platform, so this is a direct control of E107, not a new domain) |
| Pool query | `language:python stars:100..20000`, `sort=stars&order=desc` — **one** query, no topic filter, no need vocabulary in the query |
| Pool size | target 300 rows |
| Label source | `classify.py` — E107's `NEED_INDICATORS` / `GENERIC_TERMS` applied to description + topics **after** the row is already in the pool |
| Label arms | `need` (need-indicator, no generic-term) / `generic` (generic-term, no need-indicator) / `unlabelled` (both or neither — excluded, and counted) |

Asymmetry is removed by construction: identical query, identical sort, identical
star band, identical language filter applied to **both** arms. Only the label
differs.

## Gates

Declared before the first fetch. `untested` until run.

- **G0 — instrument discrimination (must pass first).** The labeler must
  recover independent real positives: seeded on the twenty E107 rows whose
  description contains an explicit technology noun (`postgres`, `kafka`,
  `tensorflow`, `sqlite`, `elasticsearch`, …) it must label `need` at ≥ 9/10
  and on twenty rows matching only generic vocabulary (`utils`, `boilerplate`,
  `example`, `helper`, …) at `generic` ≥ 9/10. **Kill: G0 below threshold stops
  the experiment** — a labeler that cannot find planted positives cannot be
  trusted to find natural ones, and the run reports `instrument_defect`.
- **G1 — population.** ≥ 100 `need` and ≥ 100 `generic` rows after labelling.
  *Kill:* under-powered; report `inconclusive`, not a null.
- **G2 — separation, cumulative (E107's metric).** Cliff's δ on cumulative
  stars, two-sided permutation p.
- **G3 — separation, age-controlled (the metric E107 never used).** Cliff's δ on
  **stars per year of existence** (`stargazers_count / max(years since created_at, 1)`),
  same permutation p. This is the confound E107 never controlled: a repository
  from 2013 has had a decade more to accumulate.
- **G4 — age balance, reported not gated.** Median age per arm, and the
  correlation between age and stars within each arm. If age separates the arms,
  G3 is the reading that matters and G2 is not.

## Failure condition, declared

**The principle is refuted as a discovery instrument if G0 passes and G3 fails**
(age-controlled δ CI includes 0, or reverses sign) **while G2 passes.** That is
the signature of a cumulative-count metric carrying age, not need.

**The confound is refuted — the principle survives — if G0 passes and G3 passes**
with δ in the direction the principle predicts.

Either verdict is informative and neither is a foregone conclusion.

## What this experiment cannot decide

- It does not measure demand for any product, or adoption of anything.
- It tests the *principle's* arithmetic on one platform, not usefulness.
- A pass here is a reason to keep the line, not a candidate. The line's purpose
  is to find populations no existing tool serves; this experiment can only say
  whether the screen is honest enough to look.

## Raw evidence

`raw_pool.json` — the full pool as fetched, before labelling, with the query
that produced each row. `results.json` — gate outcomes. `analyze.py` — the
labeler and the three statistics, re-runnable against the committed raw file.