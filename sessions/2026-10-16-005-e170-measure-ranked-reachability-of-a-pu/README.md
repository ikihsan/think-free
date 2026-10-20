# Session 2026-10-16-005-e170-measure-ranked-reachability-of-a-pu

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-16T05:24:30+00:00
- **Duration:** 3445.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E170: measure ranked reachability of a published fix on a live index — the error string (E168's incumbent mechanism) against a component+symptom query (E169's design rule) — on the 13 tracker-linked rows, with a positive control that can pass and a query-syntax verification suite

## Summary

E170 measured the one question E168 and E169 both left open -- is a published fix reachable by the query a developer types -- on two live ranked indexes with queries committed before any fetch. Capability controls pass on both surfaces (in:title returns the target at rank 1 on 11/13 via api.github.com/search/issues and 10/13 via github.com/search?type=issues), so the arms are readable. On the web surface the developer's quoted error string reaches the fix on 1 of the 8 rows that have a literal and component+symptom keywords on 2 of 13 = 0.1538 (paired McNemar p = 1.0); the declared kill does not fire and the declared 0.30 bar for building anything is not met, so the class closes. Mechanism, now measured: a failure report names the symptom and the environment, a fix states the cause and the change, and 0 of 13 rows share a 3-word run with their fix (E169) while the thread carries it at >= 0.8 on 12 of 13 -- the responder's prose is the bridge, and that semantic step is the strongest accessible alternative. No retriever proposed, so no prior-art screen run. F131 (control lesson plus five reproducible index defects), F132 (the closure), D115 (an index is declared as a surface with its query semantics).

## Next

E171: E168's unrun G3 -- does an attempt grounded in the component's published version history recover rows the unaided attempt fails, declared bar >= 0.60 -- is now the only experiment left on this record where the candidate mechanism is not the incumbent, and E170 has removed its search arm. It needs a fresh blinded version_pinned sample; this host has 7 of 300 Stack Exchange requests remaining today, so the draw waits for the daily reset. E172 (fresh observation in an untouched domain, by a stated rule) needs no quota and can run in parallel. E170's own replication gate is deliberately not run: a replication of a near-zero effect teaches nothing this record lacks.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-1.md | f67b28caa2d6 | 3415 |
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-2.md | d95a2fcf4878 | 3326 |
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL.md | 1fc9cc0cbc25 | 7380 |
| EXPERIMENTS/170-fix-reachability-rank/RESULT.md | 58162180fd93 | 6957 |
| EXPERIMENTS/170-fix-reachability-rank/controls.py | ef320bc874c1 | 3565 |
| EXPERIMENTS/170-fix-reachability-rank/ghsearch.py | da743edac796 | 5386 |
| EXPERIMENTS/170-fix-reachability-rank/html_probe.py | 8317ca40008e | 1203 |
| EXPERIMENTS/170-fix-reachability-rank/html_run.py | b278e30a8ac5 | 4762 |
| EXPERIMENTS/170-fix-reachability-rank/queries.json | 1f728ada0309 | 14513 |
| EXPERIMENTS/170-fix-reachability-rank/run.py | 198fcb5a6339 | 5248 |
| EXPERIMENTS/170-fix-reachability-rank/summarize.py | e69a9fed7bcf | 3985 |
| STATE.md | 321f069fd63c | 18613 |
| STATE-next-actions.md | 863077d74e69 | 18561 |
| FAILURES.md | f3583342be49 | 89108 |
| FAILURES-findings-41.md | deeb743f677f | 14470 |
| FAILURES-findings-42.md | 32c92fc1075a | 5593 |
| DECISIONS.md | f8c1cc66a860 | 25852 |
| DECISIONS-RECORDS-2.md | 74683662073f | 14462 |
| EXPERIMENTS/README.md | 715349dbc948 | 10661 |
| RELEASE-MANIFEST.md | babaad5e7c3f | 7851 |
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-1.md | f67b28caa2d6 | 3415 |
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-2.md | d95a2fcf4878 | 3326 |
| EXPERIMENTS/170-fix-reachability-rank/PROTOCOL.md | 1fc9cc0cbc25 | 7380 |
| EXPERIMENTS/170-fix-reachability-rank/RESULT.md | 58162180fd93 | 6957 |
| EXPERIMENTS/170-fix-reachability-rank/controls.py | ef320bc874c1 | 3565 |
| EXPERIMENTS/170-fix-reachability-rank/ghsearch.py | da743edac796 | 5386 |
| EXPERIMENTS/170-fix-reachability-rank/html_probe.py | 8317ca40008e | 1203 |
| EXPERIMENTS/170-fix-reachability-rank/html_run.py | b278e30a8ac5 | 4762 |
| EXPERIMENTS/170-fix-reachability-rank/queries.json | 1f728ada0309 | 14513 |
| EXPERIMENTS/170-fix-reachability-rank/raw/controls-g0rt.json | 2b6315027471 | 10874 |
| EXPERIMENTS/170-fix-reachability-rank/raw/controls-summary.json | 4993b323be6f | 142 |
| EXPERIMENTS/170-fix-reachability-rank/raw/html-arms.json | af19ac94b6ec | 15858 |
| EXPERIMENTS/170-fix-reachability-rank/raw/html-summary.json | e125c9edc0ef | 227 |
| EXPERIMENTS/170-fix-reachability-rank/raw/rawlog.json | 88b9d8654018 | 56198 |
| EXPERIMENTS/170-fix-reachability-rank/raw/rows.json | 6a2a49eb10a8 | 17430 |
| EXPERIMENTS/170-fix-reachability-rank/raw/summary.json | d287d05485a2 | 3375 |
| EXPERIMENTS/170-fix-reachability-rank/raw/targets.json | 054eabd06dff | 59039 |
| EXPERIMENTS/170-fix-reachability-rank/raw/verify.json | 9a920d551fd0 | 243 |
| EXPERIMENTS/170-fix-reachability-rank/run.py | 198fcb5a6339 | 5248 |
| EXPERIMENTS/170-fix-reachability-rank/summarize.py | e69a9fed7bcf | 3985 |
| FAILURES-findings-42.md | ee068d0f44c1 | 9228 |

## Commands

13 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', '\nimport json, urllib.parse, urllib.request, time\ndef q(s, **kw):\n    p = {\'q\': s, \'per_page\': 10}\n    p.update(kw)\n    url | 0 | 19138 |
| 3 | ['python3', '-c', '\nimport json, urllib.parse, urllib.request, time\ndef q(s, **kw):\n    p = {\'q\': s, \'per_page\': 5}\n    p.update(kw)\n    url  | 0 | 31166 |
| 4 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/run.py'] | 1 | 61498 |
| 5 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/run.py'] | 1 | 45297 |
| 6 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/run.py'] | 1 | 44294 |
| 7 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/run.py'] | 0 | 797088 |
| 8 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/summarize.py'] | 1 | 575 |
| 9 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/summarize.py'] | 0 | 98 |
| 10 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/controls.py'] | 0 | 186608 |
| 11 | ['python3', '-c', "\nimport urllib.request, re\ndef get(url):\n    r = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_ | 1 | 1106 |
| 12 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/html_probe.py'] | 0 | 929 |
| 13 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/html_probe.py'] | 0 | 353 |
| 14 | ['python3', 'EXPERIMENTS/170-fix-reachability-rank/html_run.py'] | 0 | 386708 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:24:30 | session_start | E170: measure ranked reachability of a published fix on a live index — the error string (E168's incumbent mechanism) against a component+symptom query |
| 2 | 05:24:56 | command | $ python3 -c  import json, urllib.parse, urllib.request, time def q(s, **kw):     p = {'q': s, 'per_page': 10}     p.update(kw)     url = 'htt |
| 3 | 05:25:37 | command | $ python3 -c  import json, urllib.parse, urllib.request, time def q(s, **kw):     p = {'q': s, 'per_page': 5}     p.update(kw)     url = 'http |
| 4 | 05:28:16 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/run.py |
| 5 | 05:29:16 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/run.py |
| 6 | 05:30:33 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/run.py |
| 7 | 05:44:17 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/run.py |
| 8 | 05:44:41 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/summarize.py |
| 9 | 05:44:57 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/summarize.py |
| 10 | 05:48:44 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/controls.py |
| 11 | 05:49:53 | command | $ python3 -c  import urllib.request, re def get(url):     r = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_6 |
| 12 | 05:50:08 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/html_probe.py |
| 13 | 05:50:32 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/html_probe.py |
| 14 | 05:57:37 | command | $ python3 EXPERIMENTS/170-fix-reachability-rank/html_run.py |
| 15 | 06:01:58 | milestone | E170: capability controls pass on both GitHub surfaces (title at rank 1, 11/13 API and 10/13 web); neither the quoted error string (1/8) nor component |
| 16 | 06:02:00 | decision | An index is declared as a surface with its query semantics, and a positive control reports its own total_count — because GitHub's API and web surfaces |
| 17 | 06:02:02 | experiment_result | neither lexical query form reaches a published version-pinned fix on a live ranked index; fifteenth served closure, second with the mechanism measured |
| 18 | 06:02:09 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-1.md |
| 19 | 06:02:10 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-2.md |
| 20 | 06:02:11 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL.md |
| 21 | 06:02:12 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/RESULT.md |
| 22 | 06:02:13 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/controls.py |
| 23 | 06:02:14 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/ghsearch.py |
| 24 | 06:02:16 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/html_probe.py |
| 25 | 06:02:17 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/html_run.py |
| 26 | 06:02:18 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/queries.json |
| 27 | 06:02:19 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/run.py |
| 28 | 06:02:20 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/summarize.py |
| 29 | 06:02:21 | artifact | wrote STATE.md |
| 30 | 06:02:22 | artifact | wrote STATE-next-actions.md |
| 31 | 06:02:24 | artifact | wrote FAILURES.md |
| 32 | 06:02:26 | artifact | wrote FAILURES-findings-41.md |
| 33 | 06:02:27 | artifact | wrote FAILURES-findings-42.md |
| 34 | 06:02:29 | artifact | wrote DECISIONS.md |
| 35 | 06:02:30 | artifact | wrote DECISIONS-RECORDS-2.md |
| 36 | 06:02:32 | artifact | wrote EXPERIMENTS/README.md |
| 37 | 06:02:33 | artifact | wrote RELEASE-MANIFEST.md |
| 38 | 06:03:21 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-1.md |
| 39 | 06:03:22 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL-AMENDMENT-2.md |
| 40 | 06:03:23 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/PROTOCOL.md |
| 55 | 06:03:39 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/raw/verify.json |
| 56 | 06:03:40 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/run.py |
| 57 | 06:03:41 | artifact | wrote EXPERIMENTS/170-fix-reachability-rank/summarize.py |
| 58 | 06:21:45 | artifact | wrote FAILURES-findings-42.md |
| 59 | 06:21:56 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 60 | 06:21:56 | doc_update | updated DECISIONS-RECORDS-2.md |
| 61 | 06:21:56 | doc_update | updated DECISIONS.md |
| 62 | 06:21:56 | doc_update | updated FAILURES.md |
| 63 | 06:21:56 | doc_update | updated STATE.md |
| 64 | 06:21:56 | session_end | E170 measured the one question E168 and E169 both left open -- is a published fix reachable by the query a developer types -- on two live ranked index |

_14 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-16-005-e170-measure-ranked-reachability-of-a-pu/events.jsonl
```
