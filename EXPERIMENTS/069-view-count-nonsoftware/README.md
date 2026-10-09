<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E069 — non-software arrival measurement: the arm stands, its headline does not

**Date:** 2026-10-08 · **Session:** 2026-10-08-021 · **Status:** complete —
**`CONFIRMED` verdict WITHDRAWN by E071 (F101, D088)**

Landed 2026-10-09 (session 2026-10-09-002) from an unlanded tree. No protocol
was written before the run; the thresholds are the two in
`EXPERIMENT-RESULT.json` (VC-positive ≥ 1 row, unserved-open ≥ 1 row), and both
were met by the numbers as computed.

## What was asked

E062 adopted `view_count` as the mission's arrival measure (D084). E063 and
E066 found `unserved-open` = 0 across 103 rows of software corpora. E069 asks
whether the instrument generalizes outside software: 50 rows from 13
non-software Stack Exchange sites, one API call per site.

## Results as run (observed)

| measure | value |
|---|---|
| rows | 50 across 13 sites |
| `view_count` > 0 | **50/50** (1.000) |
| `unserved-open`-like | 7/50 (0.140) |
| `served`-like | 37/50 (0.740) |

Its reported headline — the instrument is not software-narrow, because
non-software shows 100% VC-positive against 0% in software — is **withdrawn**.

## What was wrong with it, and what is not

**`observed` (E071):** the software comparison is a **missing observation**. The
E063/E066 corpora were harvested from the Hacker News and GitHub issues APIs,
and **neither returns any arrival/view field** — 0 of 60 HN items and 0 of 8
GitHub issue objects carry one, while Stack Exchange, the surface E062 actually
measured, returns a positive `view_count` on 80 of 80 items. E069 read those
absences as zeros and built a "diametrically opposed" contrast on them. That is
D082 committed a second time.

**Unaffected:** the non-software arm itself. `view_count` is a field Stack
Exchange does return, so **50/50 VC-positive is a real measurement**, and the
**7/50 unserved-open-like** share is a real measurement on that surface. Those
are the numbers this experiment actually establishes, and they are the ones that
make E070's CFPB arm worth running.

**Corrected verdict:** the instrument is **Stack-Exchange-shaped**. It measures
arrivals where a platform publishes them and is unmeasurable on the two APIs
the software corpora came from — so the domain contrast E069 reported cannot be
drawn from those corpora at all.

## Reproduction

```bash
python3 -c "import json;print(len(json.load(open('raw/api-responses.json'))))"   # 50
```

The 50 captured responses are in `raw/api-responses.json`; no script was written
to produce them, so the classification is **not** re-derivable from committed
bytes — a limitation of this landing, recorded here rather than silently carried.