# Session 2026-10-06-001-e032-test-whether-the-mission-s-three-ze

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T00:56:15+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E032: test whether the mission's three-zero recurrence result is a fact about public conversation or a fact about the single venue all three populations came from

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

34 captured, 10 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['bash', '-c', '\necho "=== E012 raw file header (the need corpus) ==="\nhead -c 400 EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl 2 | 0 | 997 |
| 5 | ['bash', '-c', '\necho "=== does E029 reuse E012s corpus? ==="\ngrep -rnoE "012-candidate-harvest[a-z/._-]*\|hn_needs_2026-10-04[a-z.]*\|raw/[a-z_0-9- | 0 | 371 |
| 6 | ['python3', 'EXPERIMENTS/032-venue-recurrence/harvest.py'] | 0 | 3132 |
| 7 | ['bash', '-c', '\npython3 - <<PY\nimport json, collections\nrows=[json.loads(l) for l in open("EXPERIMENTS/032-venue-recurrence/raw/harvest.jsonl")]\n | 0 | 186 |
| 8 | ['python3', 'EXPERIMENTS/032-venue-recurrence/harvest.py'] | 0 | 1511 |
| 9 | ['bash', '-c', '\npython3 - <<PY\nimport json,glob,os,collections\ndef ids(p):\n    s=set()\n    if not os.path.exists(p): return None\n    for line i | 0 | 404 |
| 10 | ['python3', 'EXPERIMENTS/032-venue-recurrence/extract.py'] | 0 | 203 |
| 11 | ['python3', 'EXPERIMENTS/032-venue-recurrence/extract.py'] | 0 | 184 |
| 12 | ['bash', '-c', '\npython3 - <<PY\nimport json\nman=json.load(open("EXPERIMENTS/032-venue-recurrence/sheets/MANIFEST.json"))\nrows=[json.loads(l) for l | 0 | 190 |
| 13 | ['python3', 'EXPERIMENTS/032-venue-recurrence/link.py'] | 0 | 1883 |
| 14 | ['python3', 'EXPERIMENTS/032-venue-recurrence/link.py'] | 0 | 611 |
| 16 | ['tools/origin', 'release', 'check'] | 2 | 103935 |
| 17 | ['python3', 'EXPERIMENTS/032-venue-recurrence/tally.py', '--check'] | 1 | 783 |
| 18 | ['python3', 'EXPERIMENTS/032-venue-recurrence/tally.py', '--check'] | 1 | 607 |
| 19 | ['python3', 'EXPERIMENTS/032-venue-recurrence/link.py'] | 0 | 624 |
| 20 | ['python3', 'EXPERIMENTS/032-venue-recurrence/tally.py', '--check'] | 0 | 119 |
| 21 | ['python3', '-'] | 0 | 96 |
| 22 | ['tools/origin', 'doc', 'lint'] | 2 | 12834 |
| 23 | ['tools/origin', 'doc', 'index'] | 0 | 2037 |
| 24 | ['tools/origin', 'doc', 'lint'] | 2 | 15268 |
| 25 | ['tools/origin', 'doc', 'lint'] | 0 | 19299 |
| 26 | ['tools/origin', 'doc', 'lint'] | 2 | 14333 |
| 27 | ['tools/origin', 'doc', 'lint'] | 2 | 12892 |
| 28 | ['tools/origin', 'doc', 'lint'] | 2 | 13199 |
| 29 | ['tools/origin', 'doc', 'lint'] | 0 | 13320 |
| 30 | ['tools/origin', 'doc', 'lint'] | 2 | 12882 |
| 31 | ['tools/origin', 'doc', 'lint'] | 0 | 14906 |
| 32 | ['tools/origin', 'release', 'check'] | 2 | 90362 |
| 33 | ['tools/origin', 'release', 'check'] | 0 | 84694 |
| 34 | ['tools/origin', 'doc', 'index'] | 0 | 1416 |
| 35 | ['tools/origin', 'doc', 'lint'] | 0 | 12016 |
| 36 | ['bash', '-c', 'PYTHONPATH=tools:tests timeout 900 python3 -m unittest discover -s tests -t tests 2>&1 \| tail -8'] | 0 | 485889 |
| 37 | ['bash', '-c', 'PYTHONPATH=tools:tests timeout 900 python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^(OK\|FAILED\|Ran [0-9]+ test)" \|  | 0 | 485643 |
| 38 | ['python3', 'EXPERIMENTS/032-venue-recurrence/tally.py', '--check'] | 0 | 218 |

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
| 1 | 00:56:15 | session_start | E032: test whether the mission's three-zero recurrence result is a fact about public conversation or a fact about the single venue all three populatio |
| 2 | 00:56:31 | task_rewrite | rewrote tasks/T-0076-e032-test-whether-the-mission-s-three-zero-recur.md (status: claimed) |
| 3 | 00:56:31 | task_rewrite | appended a claim record for T-0076 |
| 4 | 00:56:44 | command | $ bash -c  echo "=== E012 raw file header (the need corpus) ===" head -c 400 EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl 2 |
| 5 | 00:57:04 | command | $ bash -c  echo "=== does E029 reuse E012s corpus? ===" grep -rnoE "012-candidate-harvest[a-z/._-]*\|hn_needs_2026-10-04[a-z.]*\|raw/[a-z_0-9-]* |
| 6 | 00:58:31 | command | $ python3 EXPERIMENTS/032-venue-recurrence/harvest.py |
| 7 | 00:58:39 | command | $ bash -c  python3 - <<PY import json, collections rows=[json.loads(l) for l in open("EXPERIMENTS/032-venue-recurrence/raw/harvest.jsonl")] pr |
| 8 | 00:58:59 | command | $ python3 EXPERIMENTS/032-venue-recurrence/harvest.py |
| 9 | 00:59:15 | command | $ bash -c  python3 - <<PY import json,glob,os,collections def ids(p):     s=set()     if not os.path.exists(p): return None     for line in op |
| 10 | 00:59:45 | command | $ python3 EXPERIMENTS/032-venue-recurrence/extract.py |
| 11 | 01:02:22 | command | $ python3 EXPERIMENTS/032-venue-recurrence/extract.py |
| 12 | 01:03:01 | command | $ bash -c  python3 - <<PY import json man=json.load(open("EXPERIMENTS/032-venue-recurrence/sheets/MANIFEST.json")) rows=[json.loads(l) for l i |
| 13 | 01:03:31 | command | $ python3 EXPERIMENTS/032-venue-recurrence/link.py |
| 14 | 01:04:08 | command | $ python3 EXPERIMENTS/032-venue-recurrence/link.py |
| 15 | 01:04:33 | milestone | protocol declared, 60-row non-programming population harvested, two blinded readers at kappa 0.8344, linkage reachable at 32 candidates vs 1.19 chance |
| 16 | 01:06:46 | command | $ tools/origin release check |
| 17 | 01:06:52 | command | $ python3 EXPERIMENTS/032-venue-recurrence/tally.py --check |
| 18 | 01:07:03 | command | $ python3 EXPERIMENTS/032-venue-recurrence/tally.py --check |
| 19 | 01:07:24 | command | $ python3 EXPERIMENTS/032-venue-recurrence/link.py |
| 20 | 01:07:29 | command | $ python3 EXPERIMENTS/032-venue-recurrence/tally.py --check |
| 21 | 01:07:49 | command | $ python3 - |
| 22 | 01:09:54 | command | $ tools/origin doc lint |
| 23 | 01:10:40 | command | $ tools/origin doc index |
| 24 | 01:10:56 | command | $ tools/origin doc lint |
| 25 | 01:11:25 | command | $ tools/origin doc lint |
| 26 | 01:12:21 | command | $ tools/origin doc lint |
| 27 | 01:13:22 | command | $ tools/origin doc lint |
| 28 | 01:13:54 | command | $ tools/origin doc lint |
| 29 | 01:14:15 | command | $ tools/origin doc lint |
| 30 | 01:14:35 | command | $ tools/origin doc lint |
| 31 | 01:14:55 | command | $ tools/origin doc lint |
| 32 | 01:16:26 | command | $ tools/origin release check |
| 33 | 01:18:01 | command | $ tools/origin release check |
| 34 | 01:18:03 | command | $ tools/origin doc index |
| 35 | 01:18:16 | command | $ tools/origin doc lint |
| 36 | 01:28:36 | command | $ bash -c PYTHONPATH=tools:tests timeout 900 python3 -m unittest discover -s tests -t tests 2>&1 \| tail -8 |
| 37 | 01:36:52 | command | $ bash -c PYTHONPATH=tools:tests timeout 900 python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^(OK\|FAILED\|Ran [0-9]+ test)" \| ta |
| 38 | 01:37:03 | command | $ python3 EXPERIMENTS/032-venue-recurrence/tally.py --check |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-001-e032-test-whether-the-mission-s-three-ze/events.jsonl
```
