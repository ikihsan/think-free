# Session 2026-10-16-004-e169-measure-whether-the-error-string-in

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T03:49:55+00:00
- **Duration:** 5636.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E169: measure whether the error string in each version-pinned failure reaches the linked resolution source through the mechanism-native search a developer actually uses (tracker search + direct fetch), which decides whether the class is served or has a search-resistant residue

## Summary

E169 ran E168's named cheap measurement of the incumbent's ceiling and withdrew it: the search arms' own positive control failed (treatment 1/13, control 3/13 then 13/13; a target's own quoted title returns 17,033,706 hits). Replaced by containment, a deterministic instrument needing no search engine: median term coverage 0.625, 9 of 13 at >= 0.5, 0 of 13 sharing a 3-word run with the fix, and >= 0.8 coverage against the whole thread on 12 of 13. The thread is the delivery mechanism; the tracker link is a citation. Fourteenth served closure, first with the mechanism measured. Corrects two E168 figures that do not reproduce and reports G1 as vacuous as declared.

## Next

E170: test ranked reachability on an index that is reachable from this host. GitHub issue search is live here (api.github.com 200, unauthenticated 10 req/min), so the ceiling E169 could not measure is measurable as a top-10 hit rate, with a positive control designed so it can pass (a verbatim run from the target's own text) and a query-syntax verification suite, because E169 recorded that quoted phrases, OR and sort=best-match are not honoured. Arms: the error string (E168's incumbent) against symptom+component (E169's design rule). Queries committed before any fetch. Replication on a fresh blinded sample is blocked by the Stack Exchange daily quota (7 of 300 remaining).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/169-version-pinned-reach/PROTOCOL.md | bf973d684e38 | 6755 |
| EXPERIMENTS/169-version-pinned-reach/PROTOCOL-AMENDMENT-1.md | 61bcbaffe235 | 2955 |
| EXPERIMENTS/169-version-pinned-reach/PROTOCOL-AMENDMENT-2.md | e0369f8c5048 | 4511 |
| EXPERIMENTS/169-version-pinned-reach/RESULT.md | 7d680d67c126 | 8625 |
| EXPERIMENTS/169-version-pinned-reach/containment.py | b7464cf6e4eb | 9971 |
| EXPERIMENTS/169-version-pinned-reach/controls.py | b07d5f1e911d | 7856 |
| EXPERIMENTS/169-version-pinned-reach/arms.py | e65cb3400475 | 6544 |
| EXPERIMENTS/169-version-pinned-reach/run.py | f6357e97f018 | 8044 |
| EXPERIMENTS/169-version-pinned-reach/literals.py | 857cc2bbb267 | 3415 |
| EXPERIMENTS/169-version-pinned-reach/reach.py | 3c7984b6042f | 4340 |
| EXPERIMENTS/169-version-pinned-reach/fetch_missing.py | 51e28395ed86 | 2811 |
| EXPERIMENTS/169-version-pinned-reach/g0_recount.py | 5a78afcacc39 | 2575 |
| EXPERIMENTS/169-version-pinned-reach/hand-queries.jsonl | baf52ab6e4bb | 3773 |
| EXPERIMENTS/169-version-pinned-reach/g1-labels.jsonl | 55d0717b24f5 | 2563 |
| EXPERIMENTS/169-version-pinned-reach/threads-all.json | a82de2f2d238 | 468439 |
| FAILURES-findings-41.md | 214c1fe38475 | 17150 |
| DECISIONS-RECORDS-2.md | a94cec0aba17 | 11785 |
| DECISIONS.md | cc78cc6e3700 | 25846 |
| FAILURES.md | f812a7a239cd | 85844 |
| EXPERIMENTS/README.md | 16705fde926b | 9917 |
| EXPERIMENTS/169-version-pinned-reach/raw/containment.json | 283ffe873005 | 15280 |
| RELEASE-MANIFEST.md | c506cdb54845 | 7825 |
| STATE.md | 711fcb04f39a | 20257 |
| STATE-dashboard.md | 53a640241437 | 17611 |
| docs/INDEX.md | f5dda15def1a | 56004 |
| EXPERIMENTS/169-version-pinned-reach/raw/g0-recount.json | 000f8a451554 | 2664 |
| EXPERIMENTS/169-version-pinned-reach/raw/arms-summary.json | cf883da32208 | 982 |
| EXPERIMENTS/169-version-pinned-reach/raw/controls-summary.json | 46240545fd84 | 524 |
| EXPERIMENTS/169-version-pinned-reach/raw/fetch.json | 502ab07669cb | 384 |
| EXPERIMENTS/169-version-pinned-reach/raw/target-titles.json | 9306696465dc | 3208 |
| EXPERIMENTS/169-version-pinned-reach/raw/controls.json | 9b286bf448f9 | 5835 |
| EXPERIMENTS/169-version-pinned-reach/raw/query-results.json | 8e990f395a1b | 20988 |
| EXPERIMENTS/169-version-pinned-reach/RESULT.md | 3c5ce876e059 | 9176 |
| STATE.md | 0780aad8818a | 20257 |
| STATE-next-actions.md | 2d369c2ead61 | 17085 |

## Commands

9 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/g0_recount.py'] | 0 | 110 |
| 3 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/fetch_missing.py'] | 0 | 106371 |
| 4 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/arms.py'] | 0 | 323738 |
| 5 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/controls.py'] | 0 | 191590 |
| 6 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/controls.py'] | 0 | 369882 |
| 7 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/containment.py'] | 1 | 1993 |
| 8 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/containment.py'] | 0 | 118741 |
| 9 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/containment.py'] | 0 | 8512 |
| 10 | ['python3', 'EXPERIMENTS/169-version-pinned-reach/containment.py'] | 0 | 126116 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 6 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/arms-progress.txt |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/containment-progress.txt |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/containment-summary.json |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/controls-progress.txt |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/g1-sample.json |
|   undeclared | EXPERIMENTS/169-version-pinned-reach/raw/query-plan.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 03:49:55 | session_start | E169: measure whether the error string in each version-pinned failure reaches the linked resolution source through the mechanism-native search a devel |
| 2 | 03:53:08 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/g0_recount.py |
| 3 | 03:55:01 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/fetch_missing.py |
| 4 | 04:03:48 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/arms.py |
| 5 | 04:07:33 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/controls.py |
| 6 | 04:14:18 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/controls.py |
| 7 | 04:15:15 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/containment.py |
| 8 | 04:17:34 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/containment.py |
| 9 | 04:18:31 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/containment.py |
| 10 | 04:31:09 | command | $ python3 EXPERIMENTS/169-version-pinned-reach/containment.py |
| 11 | 04:32:43 | milestone | E169 measured: containment 9/13 >= 0.5, 0/13 share a 3-word run with the fix, thread coverage >=0.8 on 10/13; search arms withdrawn by their own contr |
| 12 | 04:32:45 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/PROTOCOL.md |
| 13 | 04:32:46 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/PROTOCOL-AMENDMENT-1.md |
| 14 | 04:32:47 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/PROTOCOL-AMENDMENT-2.md |
| 15 | 04:32:49 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/RESULT.md |
| 16 | 04:32:50 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/containment.py |
| 17 | 04:32:52 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/controls.py |
| 18 | 04:32:53 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/arms.py |
| 19 | 04:32:54 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/run.py |
| 20 | 04:32:56 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/literals.py |
| 21 | 04:32:57 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/reach.py |
| 22 | 04:32:58 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/fetch_missing.py |
| 23 | 04:33:00 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/g0_recount.py |
| 24 | 04:33:01 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/hand-queries.jsonl |
| 25 | 04:33:02 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/g1-labels.jsonl |
| 26 | 04:33:04 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/threads-all.json |
| 27 | 04:33:09 | artifact | wrote FAILURES-findings-41.md |
| 28 | 04:33:10 | artifact | wrote DECISIONS-RECORDS-2.md |
| 29 | 04:33:12 | artifact | wrote DECISIONS.md |
| 30 | 04:33:13 | artifact | wrote FAILURES.md |
| 31 | 04:33:14 | artifact | wrote EXPERIMENTS/README.md |
| 32 | 04:53:29 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/raw/containment.json |
| 33 | 04:53:34 | artifact | wrote RELEASE-MANIFEST.md |
| 34 | 04:53:38 | artifact | wrote STATE.md |
| 35 | 04:53:44 | artifact | wrote STATE-dashboard.md |
| 36 | 04:53:50 | artifact | wrote docs/INDEX.md |
| 37 | 04:54:10 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/raw/g0-recount.json |
| 38 | 04:54:19 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/raw/arms-summary.json |
| 39 | 04:54:28 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/raw/controls-summary.json |
| 40 | 04:54:33 | artifact | wrote EXPERIMENTS/169-version-pinned-reach/raw/fetch.json |
| 48 | 05:23:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/169-version-pinned-reach/raw/containment-progress.txt |
| 49 | 05:23:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/169-version-pinned-reach/raw/containment-summary.json |
| 50 | 05:23:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/169-version-pinned-reach/raw/controls-progress.txt |
| 51 | 05:23:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/169-version-pinned-reach/raw/g1-sample.json |
| 52 | 05:23:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/169-version-pinned-reach/raw/query-plan.json |
| 53 | 05:23:52 | doc_update | updated DECISIONS-RECORDS-2.md |
| 54 | 05:23:52 | doc_update | updated DECISIONS.md |
| 55 | 05:23:52 | doc_update | updated FAILURES.md |
| 56 | 05:23:52 | doc_update | updated STATE.md |
| 57 | 05:23:52 | session_end | E169 ran E168's named cheap measurement of the incumbent's ceiling and withdrew it: the search arms' own positive control failed (treatment 1/13, cont |

_7 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-004-e169-measure-whether-the-error-string-in/events.jsonl
```
