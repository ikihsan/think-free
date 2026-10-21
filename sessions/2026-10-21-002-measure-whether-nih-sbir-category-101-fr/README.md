# Session 2026-10-21-002-measure-whether-nih-sbir-category-101-fr

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T07:34:27+00:00
- **Duration:** 2493.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Measure whether NIH SBIR category-101 fragmentation predicts newcomer entry: what fraction of FY2023 award-holding organizations had no prior award in that segment, compared across fragmented and concentrated categories, with gates declared before any fetch

## Summary

E208: measured whether NIH SBIR category fragmentation predicts newcomer entry. Complete R41/R42 census FY2014-FY2023 (3,407 rows, fetched = API meta.total per year), identity external_org_id, gates declared before the fetch. G0-G2 PASS (reproduces E207 exactly). G3 kill gate fired: rho(fragmentation, segment-newcomer fraction) = -0.2456, one-sided p = 0.9754 over 64 categories with >=10 awardees; nine-year sensitivity -0.2748. G4 PASS (cat 101 segment-entrant 0.5075, unremarkable vs median 0.538). Exploratory post-hoc: rho(fragmentation, category size) = 0.9711, so fragmentation is a size proxy here; entry itself is common (0.527 segment / 0.407 domain). F152, D129. The federal IT codes stay untested on entry.

## Next

E209: the same entrant measurement on the federal IT PSC codes (E196-E198), where the accessibility pattern was first claimed; per code, what fraction of FY2023 recipients were new to that code in the prior five years, gates declared before the fetch, with the award-volume confound measured alongside.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E208-sbir-entrant-share/PROTOCOL.md | 6b7052374c3e | 7215 |
| EXPERIMENTS/E208-sbir-entrant-share/fetch_prior.py | 8c81aab970ca | 2448 |
| EXPERIMENTS/E208-sbir-entrant-share/analyze.py | 7b131121a167 | 10395 |
| EXPERIMENTS/E208-sbir-entrant-share/RESULT.md | c2d2492a5ff8 | 6072 |
| EXPERIMENTS/E208-sbir-entrant-share/per_category.csv | 5e86548bd714 | 9988 |
| EXPERIMENTS/E208-sbir-entrant-share/raw/prior_years.json | 4d1338f6d6c8 | 37585276 |
| EXPERIMENTS/E208-sbir-entrant-share/AMENDMENT-1.md | 2b273be143c0 | 980 |
| EXPERIMENTS/E208-sbir-entrant-share/gates.json | 16eb013dd925 | 59792 |
| EXPERIMENTS/E208-sbir-entrant-share/RESULT.md | 33f901cb0d55 | 6070 |
| EXPERIMENTS/E208-sbir-entrant-share/analyze.py | 84899ff91745 | 10391 |
| DECISIONS-RECORDS-6.md | 2ed7549a7243 | 12654 |
| FAILURES.md | 64c1b9f1c733 | 118266 |
| FAILURES-findings-48.md | 16ec429c5175 | 13060 |
| DECISIONS.md | 144a46abeb6c | 36439 |
| HYPOTHESES.md | e7c913cb54a2 | 23418 |
| STATE-next-actions.md | 43320f36f3f9 | 11056 |

## Commands

3 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/E208-sbir-entrant-share/fetch_prior.py'] | 0 | 129864 |
| 6 | ['python3', 'EXPERIMENTS/E208-sbir-entrant-share/analyze.py'] | 0 | 7200 |
| 10 | ['python3', 'EXPERIMENTS/E208-sbir-entrant-share/analyze.py'] | 0 | 8379 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:34:27 | session_start | Measure whether NIH SBIR category-101 fragmentation predicts newcomer entry: what fraction of FY2023 award-holding organizations had no prior award in |
| 2 | 07:38:27 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/PROTOCOL.md |
| 3 | 07:41:39 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/fetch_prior.py |
| 4 | 07:41:42 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/analyze.py |
| 5 | 07:44:13 | command | $ python3 EXPERIMENTS/E208-sbir-entrant-share/fetch_prior.py |
| 6 | 07:48:04 | command | $ python3 EXPERIMENTS/E208-sbir-entrant-share/analyze.py |
| 7 | 07:51:50 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/RESULT.md |
| 8 | 07:51:53 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/per_category.csv |
| 9 | 07:52:22 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/raw/prior_years.json |
| 10 | 07:53:37 | command | $ python3 EXPERIMENTS/E208-sbir-entrant-share/analyze.py |
| 11 | 07:53:55 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/AMENDMENT-1.md |
| 12 | 07:53:58 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/gates.json |
| 13 | 07:54:00 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/RESULT.md |
| 14 | 07:54:02 | artifact | wrote EXPERIMENTS/E208-sbir-entrant-share/analyze.py |
| 15 | 07:55:38 | artifact | wrote DECISIONS-RECORDS-6.md |
| 16 | 07:56:24 | artifact | wrote FAILURES.md |
| 17 | 07:56:26 | artifact | wrote FAILURES-findings-48.md |
| 18 | 07:56:29 | artifact | wrote DECISIONS.md |
| 19 | 07:56:59 | artifact | wrote HYPOTHESES.md |
| 20 | 07:57:51 | artifact | wrote STATE-next-actions.md |
| 21 | 08:16:01 | doc_update | updated DECISIONS-RECORDS-6.md |
| 22 | 08:16:01 | doc_update | updated DECISIONS.md |
| 23 | 08:16:01 | doc_update | updated FAILURES.md |
| 24 | 08:16:01 | doc_update | updated HYPOTHESES.md |
| 25 | 08:16:01 | session_end | E208: measured whether NIH SBIR category fragmentation predicts newcomer entry. Complete R41/R42 census FY2014-FY2023 (3,407 rows, fetched = API meta. |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-002-measure-whether-nih-sbir-category-101-fr/events.jsonl
```
