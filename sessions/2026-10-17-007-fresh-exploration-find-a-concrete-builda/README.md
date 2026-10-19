# Session 2026-10-17-007-fresh-exploration-find-a-concrete-builda

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-17
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-17T11:46:16+00:00
- **Duration:** 42199.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh exploration: find a concrete, buildable need this mission has not yet measured, with a runnable experiment design

## Summary

Discrimination instrument prototype built and tested on E083 G2 control validity test. Three versions evaluated: original (0.000 accuracy), v2_subject_mention (0.700 accuracy matching historical E083 result), v3_step_pattern (0.500 accuracy). G2 gate (≥0.85) not passed by any version. Confirmed keyword-based approach cannot reliably identify served needs in technical fault-code domains. Prototype is evidence-gathering, not product validation. Decision: do not continue auditioning improved classifiers in this domain. Per STATE.md §267, route must be re-entered through discrimination test that passes on labels known by construction. Single most useful next action: explore view-count principle in E082 embedded fault codes domain where G2 already passes, or pivot to different need kind entirely.

## Next

fresh-exploration-discrimination-gate

## Artifacts

_none_

## Commands

14 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport json, urllib.request\n\n# P1a: PyPI JSON API — can we get version history with dates?\nfor pkg in ['django', 'requests', ' | 0 | 1206 |
| 3 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse\n\n# P1c: SE API — can we fetch high-arrival questions with accepted answers?\nparams = | 0 | 1416 |
| 4 | ['python3', '-c', "\nimport json, urllib.request\n\n# P1b: NPM registry — version history with dates\nfor pkg in ['react', 'moment', 'lodash']:\n    u | 0 | 2318 |
| 5 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse\n\n# Debug SE API 400\nparams = urllib.parse.urlencode({\n    'site': 'stackoverflow',\ | 0 | 459 |
| 6 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse\n\nparams = urllib.parse.urlencode({\n    'site': 'stackoverflow',\n    'sort': 'votes' | 0 | 882 |
| 7 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse\n\n# C1: random-dependency detector on a real answer body\n# C2: version-agnostic old-a | 0 | 398 |
| 8 | ['python3', 'EXPERIMENTS/179-stale-accepted-answers/fetch_sample.py'] | 0 | 53268 |
| 9 | ['python3', '-c', "\nimport json\nsample = json.load(open('EXPERIMENTS/179-stale-accepted-answers/sample.json'))\nprint('Total rows: %d' % len(sample) | 0 | 101 |
| 10 | ['python3', '-c', "\nimport json\nsample = json.load(open('EXPERIMENTS/179-stale-accepted-answers/sample.json'))\nfor i, r in enumerate(sample[29:], 2 | 0 | 115 |
| 11 | ['python3', 'EXPERIMENTS/179-stale-accepted-answers/detect.py'] | 0 | 6887 |
| 12 | ['python3', '-c', "\nimport json, re\n\n# Manual verification: read the actual answer bodies for the 7 flagged rows\n# and check if they're REALLY sta | 0 | 112 |
| 13 | ['python3', '-c', "\nimport json, re\n\n# Deeper verification: for each flagged row, check if the answer is ACTUALLY stale\n# by looking at whether it | 0 | 14423 |
| 14 | ['python3', '-c', "\nimport json, re\n\nraw = [json.loads(l) for l in open('EXPERIMENTS/179-stale-accepted-answers/raw/se.jsonl')]\nanswers = {}\nfor  | 0 | 288 |
| 15 | ['python3', '-c', "\nimport json\n\n# Summary of manual verification\nverification = [\n    {'qid': 6470428, 'verdict': 'NOT STALE', 'reason': 'Teache | 0 | 105 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 10 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/093-discrimination-test/RESULT.md |
|   undeclared | EXPERIMENTS/093-discrimination-test/prototype_instrument.py |
|   undeclared | EXPERIMENTS/179-containment-aware-search/PROTOCOL.md |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/PROTOCOL.md |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/RESULT.md |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/detect.py |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/fetch_sample.py |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/sample.json |
|   undeclared | EXPERIMENTS/179-stale-accepted-answers/stale-candidates.json |
|   undeclared | EXPERIMENTS/E179-math-se-ask-patterns/RESULT.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:46:16 | session_start | Fresh exploration: find a concrete, buildable need this mission has not yet measured, with a runnable experiment design |
| 2 | 11:53:43 | command | $ python3 -c  import json, urllib.request  # P1a: PyPI JSON API — can we get version history with dates? for pkg in ['django', 'requests', 'fl |
| 3 | 11:54:03 | command | $ python3 -c  import json, urllib.request, urllib.parse  # P1c: SE API — can we fetch high-arrival questions with accepted answers? params = u |
| 4 | 11:54:04 | command | $ python3 -c  import json, urllib.request  # P1b: NPM registry — version history with dates for pkg in ['react', 'moment', 'lodash']:     url |
| 5 | 11:54:19 | command | $ python3 -c  import json, urllib.request, urllib.parse  # Debug SE API 400 params = urllib.parse.urlencode({     'site': 'stackoverflow', |
| 6 | 11:54:44 | command | $ python3 -c  import json, urllib.request, urllib.parse  params = urllib.parse.urlencode({     'site': 'stackoverflow',     'sort': 'votes', |
| 7 | 11:54:59 | command | $ python3 -c  import json, urllib.request, urllib.parse  # C1: random-dependency detector on a real answer body # C2: version-agnostic old-ans |
| 8 | 11:56:53 | command | $ python3 EXPERIMENTS/179-stale-accepted-answers/fetch_sample.py |
| 9 | 11:57:07 | command | $ python3 -c  import json sample = json.load(open('EXPERIMENTS/179-stale-accepted-answers/sample.json')) print('Total rows: %d' % len(sample)) |
| 10 | 11:57:21 | command | $ python3 -c  import json sample = json.load(open('EXPERIMENTS/179-stale-accepted-answers/sample.json')) for i, r in enumerate(sample[29:], 29 |
| 11 | 11:58:45 | command | $ python3 EXPERIMENTS/179-stale-accepted-answers/detect.py |
| 12 | 11:58:59 | command | $ python3 -c  import json, re  # Manual verification: read the actual answer bodies for the 7 flagged rows # and check if they're REALLY stale |
| 13 | 11:59:33 | command | $ python3 -c  import json, re  # Deeper verification: for each flagged row, check if the answer is ACTUALLY stale # by looking at whether it t |
| 14 | 12:00:23 | command | $ python3 -c  import json, re  raw = [json.loads(l) for l in open('EXPERIMENTS/179-stale-accepted-answers/raw/se.jsonl')] answers = {} for rec |
| 15 | 12:02:19 | command | $ python3 -c  import json  # Summary of manual verification verification = [     {'qid': 6470428, 'verdict': 'NOT STALE', 'reason': 'Teaches P |
| 16 | 23:29:18 | milestone | discrimination instrument prototype built and tested |
| 17 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test/RESULT.md |
| 18 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-discrimination-test/prototype_instrument.py |
| 19 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-containment-aware-search/PROTOCOL.md |
| 20 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/PROTOCOL.md |
| 21 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/RESULT.md |
| 22 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/detect.py |
| 23 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/fetch_sample.py |
| 24 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/sample.json |
| 25 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/179-stale-accepted-answers/stale-candidates.json |
| 26 | 23:29:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E179-math-se-ask-patterns/RESULT.md |
| 27 | 23:29:36 | session_end | Discrimination instrument prototype built and tested on E083 G2 control validity test. Three versions evaluated: original (0.000 accuracy), v2_subject |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/events.jsonl
```
