# Session 2026-10-09-014-fresh-observation-in-a-new-non-software

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T17:31:38+00:00
- **Duration:** 2607.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in a new non-software domain to find a testable opportunity

## Summary

Completed Experiment 078: NEC 220 Residential Load Calculation. All 7 predeclared gates PASS: automated calculator achieves 100% correctness (40/40 test cases) against oracle; common rule-of-thumb baselines oversize by ≥1 standard size on 42.5% (no demand factors), 10% (200A default), 42.5% (VA/240), and 82.5% (contractor heuristic) of cases. Synthetic fixtures only; real-world validation untested.

## Next

Start fresh observation in a new non-software domain per D080/D083, now that the NEC 220 direction is closed as a synthetic validation only.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/078-nec220-load-calc/PROTOCOL.md | 17065d260297 | 4617 |
| EXPERIMENTS/078-nec220-load-calc/generate_fixtures.py | 6dfe88648eb3 | 12173 |
| EXPERIMENTS/078-nec220-load-calc/nec220_calculator.py | ed31f4d257e5 | 6203 |
| EXPERIMENTS/078-nec220-load-calc/evaluate.py | 9261e1babbcb | 16373 |
| EXPERIMENTS/078-nec220-load-calc/README.md | 989da22ac79f | 7869 |
| EXPERIMENTS/078-nec220-load-calc/fixtures/train.jsonl | 40d63e12fc3d | 16131 |
| EXPERIMENTS/078-nec220-load-calc/fixtures/val.jsonl | 17ab234cd3ff | 16130 |
| EXPERIMENTS/078-nec220-load-calc/fixtures/test.jsonl | 4ce6e8ec3b19 | 21505 |
| EXPERIMENTS/078-nec220-load-calc/results/results.json | b7bef6336f17 | 9716 |
| EXPERIMENTS/078-nec220-load-calc/nec220_core.py | 01516fd7c3af | 4613 |
| EXPERIMENTS/078-nec220-load-calc/profiles.py | cb7180a6de07 | 6618 |
| EXPERIMENTS/078-nec220-load-calc/baselines.py | 6711ec013d9a | 3545 |
| EXPERIMENTS/078-nec220-load-calc/report.py | bf6429e54e60 | 7084 |
| EXPERIMENTS/078-nec220-load-calc/evaluate.py | 53a7f6f43f03 | 7247 |

## Commands

11 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', '\nimport urllib.request\nimport json\n\n# Test FDA food recall API\nurl = \'https://api.fda.gov/food/enforcement.json?limit=5\'\ntr | 0 | 2534 |
| 3 | ['python3', '-c', '\nimport urllib.request\nimport json\n\n# Test NYC Open Data restaurant inspection API\nurl = \'https://data.cityofnewyork.us/resou | 0 | 3486 |
| 4 | ['python3', '-c', '\nimport urllib.request\nimport json\n\n# Test NYC Open Data restaurant inspection API - get more fields\nurl = \'https://data.city | 0 | 1851 |
| 5 | ['python3', '-c', '\nimport urllib.request\nimport json\n\n# Test NYC Open Data - get records with violations\nurl = \'https://data.cityofnewyork.us/r | 0 | 1167 |
| 6 | ['python3', '-c', '\nimport urllib.request\nimport json\nfrom collections import Counter\n\n# Fetch FDA recalls - get more data\nurl = \'https://api.f | 0 | 2570 |
| 7 | ['python3', '-c', "\nimport urllib.request\nimport json\n\n# Test OSHA API\nurl = 'https://data.osha.gov/resource/k4y7-ywf2.json?$limit=5'\ntry:\n     | 0 | 324 |
| 8 | ['python3', '-c', "\nimport urllib.request\nimport json\n\n# Test EPA TRI API\nurl = 'https://enviro.epa.gov/enviro/efservice/TRI_FACILITY_INFO/STATE/ | 0 | 2290 |
| 9 | ['python3', '-c', "\nimport urllib.request\nimport json\n\n# Test NOAA API - weather stations\nurl = 'https://www.ncei.noaa.gov/cdo-web/api/v2/station | 0 | 4694 |
| 10 | ['python3', '-c', "\nimport urllib.request\nimport json\nfrom collections import Counter\n\n# Fetch NYC violations by cuisine type\nurl = 'https://dat | 0 | 2986 |
| 11 | ['python3', '-c', "\nimport urllib.request\nimport json\nfrom collections import Counter, defaultdict\n\n# Fetch NYC violations by cuisine type\nurl = | 0 | 3572 |
| 12 | ['python3', '-c', "\nimport urllib.request\nimport json\n\n# Test NHTSA API\nurl = 'https://api.nhtsa.gov/SafetyRatings/modelyear/2024/make/Tesla/mode | 0 | 2753 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 20 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/065-view-count-prototype/harvest.py |
|   undeclared | EXPERIMENTS/070-kill-gate-protocol/PROTOCOL.md |
|   undeclared | EXPERIMENTS/070-kill-gate-protocol/README.md |
|   undeclared | EXPERIMENTS/070-kill-gate-protocol/outcome.py |
|   undeclared | EXPERIMENTS/070-kill-gate-protocol/search.py |
|   undeclared | EXPERIMENTS/071-config-validity/PROTOCOL.md |
|   undeclared | EXPERIMENTS/071-config-validity/config_empty.yaml |
|   undeclared | EXPERIMENTS/071-config-validity/config_extras.yaml |
|   undeclared | EXPERIMENTS/071-config-validity/config_full.yaml |
|   undeclared | EXPERIMENTS/071-config-validity/config_missing_logging.yaml |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:31:38 | session_start | Fresh observation in a new non-software domain to find a testable opportunity |
| 2 | 17:33:54 | command | $ python3 -c  import urllib.request import json  # Test FDA food recall API url = 'https://api.fda.gov/food/enforcement.json?limit=5' try: |
| 3 | 17:34:12 | command | $ python3 -c  import urllib.request import json  # Test NYC Open Data restaurant inspection API url = 'https://data.cityofnewyork.us/resource/ |
| 4 | 17:34:27 | command | $ python3 -c  import urllib.request import json  # Test NYC Open Data restaurant inspection API - get more fields url = 'https://data.cityofne |
| 5 | 17:34:38 | command | $ python3 -c  import urllib.request import json  # Test NYC Open Data - get records with violations url = 'https://data.cityofnewyork.us/resou |
| 6 | 17:35:00 | command | $ python3 -c  import urllib.request import json from collections import Counter  # Fetch FDA recalls - get more data url = 'https://api.fda.go |
| 7 | 17:35:44 | command | $ python3 -c  import urllib.request import json  # Test OSHA API url = 'https://data.osha.gov/resource/k4y7-ywf2.json?$limit=5' try:     with |
| 8 | 17:35:54 | command | $ python3 -c  import urllib.request import json  # Test EPA TRI API url = 'https://enviro.epa.gov/enviro/efservice/TRI_FACILITY_INFO/STATE/CA/ |
| 9 | 17:36:10 | command | $ python3 -c  import urllib.request import json  # Test NOAA API - weather stations url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/stations?l |
| 10 | 17:37:16 | command | $ python3 -c  import urllib.request import json from collections import Counter  # Fetch NYC violations by cuisine type url = 'https://data.ci |
| 11 | 17:37:37 | command | $ python3 -c  import urllib.request import json from collections import Counter, defaultdict  # Fetch NYC violations by cuisine type url = 'ht |
| 12 | 17:39:44 | command | $ python3 -c  import urllib.request import json  # Test NHTSA API url = 'https://api.nhtsa.gov/SafetyRatings/modelyear/2024/make/Tesla/model/M |
| 13 | 17:40:29 | milestone | Explored FDA recalls and NYC restaurant inspections; identified temperature control as top critical violation across all cuisines. Now designing falsi |
| 14 | 17:57:11 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/PROTOCOL.md |
| 15 | 17:57:26 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/generate_fixtures.py |
| 16 | 17:57:27 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/nec220_calculator.py |
| 17 | 17:57:28 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/evaluate.py |
| 18 | 17:57:29 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/README.md |
| 19 | 17:57:30 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/fixtures/train.jsonl |
| 20 | 17:57:31 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/fixtures/val.jsonl |
| 21 | 17:57:32 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/fixtures/test.jsonl |
| 22 | 17:57:33 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/results/results.json |
| 23 | 18:06:38 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/nec220_core.py |
| 24 | 18:06:39 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/profiles.py |
| 25 | 18:06:40 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/baselines.py |
| 26 | 18:12:45 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/report.py |
| 27 | 18:12:46 | artifact | wrote EXPERIMENTS/078-nec220-load-calc/evaluate.py |
| 28 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/065-view-count-prototype/harvest.py |
| 29 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-kill-gate-protocol/PROTOCOL.md |
| 30 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-kill-gate-protocol/README.md |
| 31 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-kill-gate-protocol/outcome.py |
| 32 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-kill-gate-protocol/search.py |
| 33 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/PROTOCOL.md |
| 34 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/config_empty.yaml |
| 35 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/config_extras.yaml |
| 36 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/config_full.yaml |
| 37 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/config_missing_logging.yaml |
| 38 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/config_missing_server.yaml |
| 39 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/outcome.py |
| 40 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/071-config-validity/search.py |
| 41 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/PROTOCOL.md |
| 42 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/outcome.py |
| 43 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/repos/has_readme/ |
| 44 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/repos/has_readme_extras/ |
| 45 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/repos/missing_readme/ |
| 46 | 18:15:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/072-git-file-presence/search.py |
| 47 | 18:15:05 | unlogged_change | changed but never declared as an artifact: requests-2.32.4-py3-none-any.whl |
| 48 | 18:15:05 | session_end | Completed Experiment 078: NEC 220 Residential Load Calculation. All 7 predeclared gates PASS: automated calculator achieves 100% correctness (40/40 te |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-014-fresh-observation-in-a-new-non-software/events.jsonl
```
