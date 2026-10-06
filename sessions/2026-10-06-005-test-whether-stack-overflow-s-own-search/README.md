# Session 2026-10-06-005-test-whether-stack-overflow-s-own-search

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-06T07:16:01+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether Stack Overflow's own search box already returns the E034 score-tail duplicate backlog, with a declared kill gate and a positive control

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/036-search-backlog/PROTOCOL.md | ac054fe67864 | 9679 |
| tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md | 8eb7367fe853 | 2495 |
| EXPERIMENTS/036-search-backlog/README.md | 379a3d3d44c6 | 7715 |
| EXPERIMENTS/036-search-backlog/harvest.py | 438964508e2f | 8510 |
| EXPERIMENTS/036-search-backlog/tally.py | 9275abb75f83 | 10466 |
| EXPERIMENTS/036-search-backlog/readout.py | db58f6cb0f9a | 2196 |
| EXPERIMENTS/036-search-backlog/raw/measures.jsonl | f1e2e884edbb | 256351 |
| EXPERIMENTS/036-search-backlog/raw/probe.jsonl | 1140daf532cc | 20177 |
| EXPERIMENTS/036-search-backlog/raw/tally.json | fc0f9a857c4d | 5058 |
| EXPERIMENTS/036-search-backlog/README.md | fd0868c92bc5 | 8531 |
| EXPERIMENTS/036-search-backlog/PROTOCOL.md | ac054fe67864 | 9679 |
| EXPERIMENTS/036-search-backlog/README.md | fd0868c92bc5 | 8531 |
| EXPERIMENTS/036-search-backlog/harvest.py | 438964508e2f | 8510 |
| EXPERIMENTS/036-search-backlog/raw/measures.jsonl | f1e2e884edbb | 256351 |
| EXPERIMENTS/036-search-backlog/raw/probe.jsonl | 1140daf532cc | 20177 |
| EXPERIMENTS/036-search-backlog/raw/tally.json | fc0f9a857c4d | 5058 |
| EXPERIMENTS/036-search-backlog/readout.py | db58f6cb0f9a | 2196 |
| EXPERIMENTS/036-search-backlog/tally.py | 9275abb75f83 | 10466 |
| DECISIONS-SCREENING-7.md | 267f5b3d8f39 | 4441 |
| FAILURES-findings-24.md | e94c76d7dc4d | 7388 |
| tests/test_e036_gate_handling.py | 48644643f9f9 | 6802 |
| tests/test_decision_files.py | 084a43220327 | 4408 |
| tools/originlib/paths.py | 1054bdffb234 | 4126 |
| tools/originlib/reconcile.py | 1015e2887767 | 8222 |
| STATE.md | 08d61a67cd12 | 36390 |
| STATE-next-actions.md | aa6e592ef84a | 18486 |
| STATE-next-actions-closed.md | 91c4b017a8a5 | 13824 |
| STATE-in-flight-3.md | 0663eedd9037 | 15694 |
| HYPOTHESES.md | f83320655d32 | 18722 |
| HYPOTHESES-results.md | f2cc2633bbff | 18181 |
| FAILURES.md | 233f93cd10ba | 31653 |
| FAILURES-findings-23.md | 91fa6ae85e98 | 12030 |
| DECISIONS.md | e0f00871e332 | 9851 |
| RELEASE-MANIFEST.md | c3ee3a504556 | 5398 |
| tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md | 8eb7367fe853 | 2495 |
| ROADMAP.md | d7434a2ec944 | 15713 |

## Commands

55 captured, 12 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse, urllib.error, hashlib\nBASE='https://api.stackexchange.com/2.3'\ndef get(path, params) | 0 | 795 |
| 4 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse, urllib.error\nBASE='https://api.stackexchange.com/2.3'\ndef get(path, params):\n    ur | 0 | 972 |
| 5 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse, urllib.error\nBASE='https://api.stackexchange.com/2.3'\ndef get(path, params):\n    ur | 0 | 2123 |
| 9 | ['python3', 'EXPERIMENTS/036-search-backlog/harvest.py', '--probe'] | 0 | 5040 |
| 10 | ['python3', 'EXPERIMENTS/036-search-backlog/harvest.py', 'reach'] | 0 | 1875 |
| 11 | ['python3', 'EXPERIMENTS/036-search-backlog/harvest.py', 'retrieval'] | 0 | 7665 |
| 12 | ['python3', '-c', "\nimport json\nfor line in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl'):\n    r=json.loads(line)\n    print('%-22s %3d | 0 | 183 |
| 13 | ['python3', 'EXPERIMENTS/036-search-backlog/tally.py'] | 0 | 287 |
| 14 | ['python3', 'EXPERIMENTS/036-search-backlog/tally.py'] | 0 | 163 |
| 15 | ['python3', 'EXPERIMENTS/036-search-backlog/tally.py'] | 0 | 171 |
| 16 | ['python3', '-c', "\nimport json, collections\nrecs=[json.loads(l) for l in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl')]\nr0=[r for r in | 0 | 190 |
| 17 | ['python3', '-c', "\nimport json, collections\nrecs=[json.loads(l) for l in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl')]\nr0=[r for r in | 0 | 101 |
| 18 | ['python3', 'EXPERIMENTS/036-search-backlog/readout.py'] | 0 | 191 |
| 27 | ['python3', '-c', "\nimport re\np='RELEASE-MANIFEST.md'; s=open(p).read()\nold='`DECISIONS-SCREENING-6.md` `DECISIONS-GATING.md`'\nassert old in s, 'a | 0 | 100 |
| 28 | ['python3', '-c', "\np='RELEASE-MANIFEST.md'; s=open(p).read()\nold='`FAILURES-findings-22.md`, `FAILURES-findings-23.md`'\nassert old in s, 'anchor m | 0 | 210 |
| 29 | ['python3', '-c', "\np='FAILURES.md'; s=open(p).read()\nold='**No surface offers the ordering:** 409,639 bytes'\nassert old in s\nnew='**No *rendered  | 0 | 64 |
| 30 | ['python3', '-c', "\np='FAILURES-findings-23.md'; s=open(p).read()\nold='**No surface offers the ordering:**'\nassert old in s, [l for l in s.split(ch | 1 | 977 |
| 31 | ['python3', '-c', "\nimport io\nfor p,old,new in [\n ('STATE-in-flight-3.md','3. **No Stack Overflow page offers the ordering.**','3. **No rendered St | 0 | 104 |
| 32 | ['python3', '-'] | 0 | 94 |
| 33 | ['python3', '-'] | 0 | 38 |
| 34 | ['python3', '-'] | 0 | 92 |
| 35 | ['python3', '-'] | 1 | 590 |
| 36 | ['python3', '-'] | 1 | 559 |
| 37 | ['python3', '-'] | 1 | 601 |
| 38 | ['python3', '-'] | 0 | 58 |
| 39 | ['python3', '-'] | 0 | 35 |
| 40 | ['python3', '-'] | 0 | 38 |
| 41 | ['python3', '-'] | 0 | 48 |
| 42 | ['python3', '-'] | 1 | 677 |
| 43 | ['python3', '-'] | 0 | 100 |
| 44 | ['./tools/origin', 'doc', 'lint'] | 2 | 14260 |
| 45 | ['python3', '-'] | 0 | 199 |
| 46 | ['python3', '-'] | 0 | 35 |
| 47 | ['python3', '-'] | 0 | 64 |
| 48 | ['./tools/origin', 'doc', 'lint'] | 2 | 19340 |
| 49 | ['python3', '-'] | 0 | 98 |
| 50 | ['python3', '-'] | 0 | 88 |
| 51 | ['python3', '-'] | 0 | 92 |
| 52 | ['python3', '-'] | 0 | 94 |
| 53 | ['./tools/origin', 'doc', 'lint'] | 2 | 20395 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:16:01 | session_start | Test whether Stack Overflow's own search box already returns the E034 score-tail duplicate backlog, with a declared kill gate and a positive control |
| 2 | 07:16:08 | task_rewrite | appended a create record for T-0080 |
| 3 | 07:16:25 | command | $ python3 -c  import json, urllib.request, urllib.parse, urllib.error, hashlib BASE='https://api.stackexchange.com/2.3' def get(path, params): |
| 4 | 07:16:30 | command | $ python3 -c  import json, urllib.request, urllib.parse, urllib.error BASE='https://api.stackexchange.com/2.3' def get(path, params):     url |
| 5 | 07:16:48 | command | $ python3 -c  import json, urllib.request, urllib.parse, urllib.error BASE='https://api.stackexchange.com/2.3' def get(path, params):     url |
| 6 | 07:17:47 | artifact | wrote EXPERIMENTS/036-search-backlog/PROTOCOL.md |
| 7 | 07:17:48 | artifact | wrote tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md |
| 8 | 07:17:48 | milestone | E036 protocol declared before the second measurement request; one reachability probe already returned an E034 harvest id |
| 9 | 07:18:36 | command | $ python3 EXPERIMENTS/036-search-backlog/harvest.py --probe |
| 10 | 07:18:58 | command | $ python3 EXPERIMENTS/036-search-backlog/harvest.py reach |
| 11 | 07:19:29 | command | $ python3 EXPERIMENTS/036-search-backlog/harvest.py retrieval |
| 12 | 07:19:37 | command | $ python3 -c  import json for line in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl'):     r=json.loads(line)     print('%-22s %3d i |
| 13 | 07:20:11 | command | $ python3 EXPERIMENTS/036-search-backlog/tally.py |
| 14 | 07:20:25 | command | $ python3 EXPERIMENTS/036-search-backlog/tally.py |
| 15 | 07:20:31 | command | $ python3 EXPERIMENTS/036-search-backlog/tally.py |
| 16 | 07:20:40 | command | $ python3 -c  import json, collections recs=[json.loads(l) for l in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl')] r0=[r for r in |
| 17 | 07:20:48 | command | $ python3 -c  import json, collections recs=[json.loads(l) for l in open('EXPERIMENTS/036-search-backlog/raw/measures.jsonl')] r0=[r for r in |
| 18 | 07:21:10 | command | $ python3 EXPERIMENTS/036-search-backlog/readout.py |
| 19 | 07:22:01 | artifact | wrote EXPERIMENTS/036-search-backlog/README.md |
| 20 | 07:22:02 | artifact | wrote EXPERIMENTS/036-search-backlog/harvest.py |
| 21 | 07:22:02 | artifact | wrote EXPERIMENTS/036-search-backlog/tally.py |
| 22 | 07:22:03 | artifact | wrote EXPERIMENTS/036-search-backlog/readout.py |
| 23 | 07:22:04 | artifact | wrote EXPERIMENTS/036-search-backlog/raw/measures.jsonl |
| 24 | 07:22:04 | artifact | wrote EXPERIMENTS/036-search-backlog/raw/probe.jsonl |
| 25 | 07:22:04 | artifact | wrote EXPERIMENTS/036-search-backlog/raw/tally.json |
| 26 | 07:22:05 | milestone | KILL-R met: /search/advanced with sort=votes&order=asc returns 81 of E034's 100 git tail ids and closed_reason for 48 rows, unauthenticated |
| 27 | 07:23:04 | command | $ python3 -c  import re p='RELEASE-MANIFEST.md'; s=open(p).read() old='`DECISIONS-SCREENING-6.md` `DECISIONS-GATING.md`' assert old in s, 'anc |
| 28 | 07:23:11 | command | $ python3 -c  p='RELEASE-MANIFEST.md'; s=open(p).read() old='`FAILURES-findings-22.md`, `FAILURES-findings-23.md`' assert old in s, 'anchor mi |
| 29 | 07:23:33 | command | $ python3 -c  p='FAILURES.md'; s=open(p).read() old='**No surface offers the ordering:** 409,639 bytes' assert old in s new='**No *rendered ta |
| 30 | 07:23:40 | command | $ python3 -c  p='FAILURES-findings-23.md'; s=open(p).read() old='**No surface offers the ordering:**' assert old in s, [l for l in s.split(chr |
| 31 | 07:24:02 | command | $ python3 -c  import io for p,old,new in [  ('STATE-in-flight-3.md','3. **No Stack Overflow page offers the ordering.**','3. **No rendered Sta |
| 32 | 07:24:46 | command | $ python3 - |
| 33 | 07:25:42 | command | $ python3 - |
| 34 | 07:25:48 | command | $ python3 - |
| 35 | 07:26:04 | command | $ python3 - |
| 36 | 07:26:13 | command | $ python3 - |
| 37 | 07:26:20 | command | $ python3 - |
| 38 | 07:26:29 | command | $ python3 - |
| 39 | 07:26:37 | command | $ python3 - |
| 40 | 07:27:37 | command | $ python3 - |
| 90 | 08:18:13 | milestone | 799-test suite green after naming DECISIONS-SCREENING-7 in all three decision-file lists; the gate fired naming the file, a fifth time |
| 91 | 08:34:53 | command | $ bash -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests >/dev/null 2>&1 && python3 EXPERIMENTS/036-search-backlog/tall |
| 92 | 08:35:04 | task_rewrite | rewrote tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md (status: done) |
| 93 | 08:35:05 | task_rewrite | appended a complete record for T-0080 |
| 94 | 08:35:28 | command | $ python3 -c  p='ROADMAP.md'; s=open(p).read() old='''      first, in about two requests, before any population is measured for it. **D066**: |
| 95 | 08:35:44 | command | $ ./tools/origin doc lint |
| 96 | 08:35:54 | artifact | wrote ROADMAP.md |
| 97 | 08:37:33 | command | $ ./tools/origin release check |
| 98 | 08:37:34 | command | $ ./tools/origin skills check |
| 99 | 08:39:38 | command | $ ./tools/origin preflight |

_49 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-005-test-whether-stack-overflow-s-own-search/events.jsonl
```
