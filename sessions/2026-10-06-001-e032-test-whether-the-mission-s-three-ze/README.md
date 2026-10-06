# Session 2026-10-06-001-e032-test-whether-the-mission-s-three-ze

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T00:56:15+00:00
- **Duration:** 4309.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E032: test whether the mission's three-zero recurrence result is a fact about public conversation or a fact about the single venue all three populations came from

## Summary

F053 from primary sources: all 3,856 comment ids behind F039/F042/F043/F049/F051 are Hacker News, and four of five experiments re-read E012's single 1401-comment file at 100% id overlap, so 'three populations, three instruments, three zeros' was two corpora on one platform and the generalisation to public conversation was not carried by its evidence. E032 then changed the venue and nothing else - 60 long-form questions from three non-programming Stack Exchange sites, selected with no requirement vocabulary, against E031's own linkage rule imported from its module, its reader-adjudicated control and all four instrument gates - and got 0 of 32 candidate pairs and 0 of 60 control pairs, difference 0.0000 CI95 [-0.0602, +0.1072], with A2 reachable at 32 candidates against 1.19 chance, kappa 0.8344, 0/24 nonsense, 0/10 negatives, 20/20 positives. The zero is not Hacker News's length, unit, population or vocabulary selection; it is a bound of 0.0894 here and 0.0223 pooled with E031. Two of this run's own instrument defects were caught by running the step rather than by a reader's account. 796 tests green, doc lint, release check and preflight OK.

## Next

Item 0 is still an owner decision and is now the only thing blocking stage C: none of prior art, star-shaped adoption, or harvested recurrence can carry candidate selection (F034, F037, F041, F048), the demand side's recurrence zero is bounded at 0.0223 across two venue classes (F054), and F044 counted prior art as a plurality not a majority with a second option behind it - promote fewer claims and price each gate before promoting it. If a second venue class beyond long-form English Q&A is wanted, E032's ceiling names it: 28 clauses, one platform, one era.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/032-venue-recurrence/README.md | b4e5e7229625 | 7175 |
| EXPERIMENTS/032-venue-recurrence/PROTOCOL.md | ff82d98436ef | 8876 |
| EXPERIMENTS/032-venue-recurrence/VENUE.md | c91822459a86 | 2685 |
| EXPERIMENTS/032-venue-recurrence/raw/tally.json | 17b5b7b4ae52 | 1941 |
| FAILURES-findings-22.md | cb7bb2b80f9f | 9293 |
| EXPERIMENTS/032-venue-recurrence/README.md | b4e5e7229625 | 7175 |
| EXPERIMENTS/032-venue-recurrence/PROTOCOL.md | ff82d98436ef | 8876 |
| EXPERIMENTS/032-venue-recurrence/raw/tally.json | 17b5b7b4ae52 | 1941 |
| FAILURES-findings-22.md | cb7bb2b80f9f | 9293 |
| STATE-in-flight-2.md | 9d50285b56fb | 8842 |

## Commands

43 captured, 16 non-zero exit.

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
| 41 | ['tools/origin', 'doc', 'lint'] | 2 | 15026 |
| 42 | ['tools/origin', 'doc', 'lint'] | 2 | 14682 |
| 43 | ['tools/origin', 'doc', 'lint'] | 2 | 15072 |
| 44 | ['tools/origin', 'doc', 'lint'] | 2 | 15117 |
| 45 | ['tools/origin', 'doc', 'lint'] | 2 | 14429 |
| 46 | ['tools/origin', 'doc', 'lint'] | 2 | 13018 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 22 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/032-venue-recurrence/extract.py |
|   undeclared | EXPERIMENTS/032-venue-recurrence/harvest.py |
|   undeclared | EXPERIMENTS/032-venue-recurrence/labels/q1_nonsense.tsv |
|   undeclared | EXPERIMENTS/032-venue-recurrence/labels/q1_reader1.tsv |
|   undeclared | EXPERIMENTS/032-venue-recurrence/labels/q1_reader2.tsv |
|   undeclared | EXPERIMENTS/032-venue-recurrence/labels/q2_pairs.tsv |
|   undeclared | EXPERIMENTS/032-venue-recurrence/link.py |
|   undeclared | EXPERIMENTS/032-venue-recurrence/raw/fetch_log.jsonl |
|   undeclared | EXPERIMENTS/032-venue-recurrence/raw/harvest.jsonl |
|   undeclared | EXPERIMENTS/032-venue-recurrence/raw/link.json |

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
| 39 | 01:39:17 | task_rewrite | rewrote tasks/T-0076-e032-test-whether-the-mission-s-three-zero-recur.md (status: done) |
| 40 | 01:39:18 | task_rewrite | appended a complete record for T-0076 |
| 76 | 02:08:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/032-venue-recurrence/tally.py |
| 77 | 02:08:04 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 78 | 02:08:04 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 79 | 02:08:04 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 80 | 02:08:04 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 81 | 02:08:04 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 82 | 02:08:04 | doc_update | updated FAILURES.md |
| 83 | 02:08:04 | doc_update | updated ROADMAP.md |
| 84 | 02:08:04 | doc_update | updated STATE.md |
| 85 | 02:08:04 | session_end | F053 from primary sources: all 3,856 comment ids behind F039/F042/F043/F049/F051 are Hacker News, and four of five experiments re-read E012's single 1 |

_35 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-001-e032-test-whether-the-mission-s-three-ze/events.jsonl
```
