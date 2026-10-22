# Session 2026-10-21-020-gsa-elibrary-cross-ref-validation-and-se

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T14:29:43+00:00
- **Duration:** 2726.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

GSA eLibrary cross-ref validation and SEWP catalog deep dive for Fedmarket

## Summary

E213 completed: GSA MAS SIN/SEWP validation using USAspending ground truth. Official GSA eLibrary and SEWP catalog APIs are inaccessible. Validated E210's description-based inferences against 25,000 USAspending awards across 5 PSC codes. Key findings: G1 FAIL (PIID-SIN consistency 34-53% - large resellers hold 8-14 SINs per PIID); G2 FAIL (description-SIN alignment 5-36% - descriptions too generic); G3 MIXED (E210 affinity scores falsified for 7030/7A21/DA01 - small vendors have LOWER share in software SINs than services SINs; DA10 is exception with 37.1% in software SINs); G4 PASS (SEWP holders span 4-5 categories); G5 FAIL (aggregation bug). Core conclusion: E210 SIN metrics are heuristic; DA10 remains ONLY viable GSA MAS path for small software vendors. 7030 strategy confirmed: direct sales (88.7%), not GSA MAS. Updated fedmarket.py with E213-corrected caveats.

## Next

E208 field test (requires authorization); update documentation index

## Artifacts

_none_

## Commands

19 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "import requests; print('requests available')"] | 0 | 430 |
| 3 | ['python3', '-c', '\nimport requests\n# Try GSA eLibrary API\nurl = \'https://api.data.gov/gsa/elibrary/2019/01/schedule/70/sins\'\ntry:\n    r = requ | 0 | 1727 |
| 4 | ['python3', '-c', "\nimport requests\n# Try different GSA eLibrary endpoints\nendpoints = [\n    'https://api.data.gov/gsa/elibrary/schedule/70/sins', | 0 | 5445 |
| 5 | ['python3', '-c', "\nimport requests\n# Check if the site resolves\ntry:\n    r = requests.get('http://elibrary.gsa.gov', timeout=10, allow_redirects= | 0 | 2844 |
| 6 | ['python3', '-c', "\nimport requests\nr = requests.get('https://api.gsa.gov/', timeout=10)\nprint(r.text[:2000])\n"] | 0 | 1719 |
| 7 | ['python3', '-c', "\nimport requests\n# Try different GSA eLibrary URLs\nurls = [\n    'https://www.gsa.gov/elibrary',\n    'https://www.gsa.gov/buyin | 0 | 4427 |
| 8 | ['python3', '-c', "\nimport requests\nr = requests.get('https://gsaelibrary.gsa.gov/', timeout=15)\nprint(f'Status: {r.status_code}')\nprint(f'Content | 0 | 2095 |
| 9 | ['python3', '-c', "\nimport requests\nr = requests.get('https://www.gsaelibrary.gsa.gov/ElibMain/home.do', timeout=15)\nprint(f'Status: {r.status_code | 0 | 5888 |
| 10 | ['python3', '-c', "\nimport requests\n# Try to find CSV exports or API endpoints\nurls = [\n    'https://www.gsaelibrary.gsa.gov/ElibMain/schedule/sch | 0 | 10059 |
| 11 | ['python3', '-c', '\nimport requests\nr = requests.get(\'https://www.gsaelibrary.gsa.gov/ElibMain/schedule/schedule.do?scheduleNumber=70&download=csv\ | 0 | 2969 |
| 12 | ['python3', '-c', "\nimport requests\n# Try SEWP catalog\nurls = [\n    'https://www.sewp.nasa.gov/',\n    'https://sewp.nasa.gov/',\n    'https://www | 0 | 9585 |
| 13 | ['python3', '-c', '\nimport requests\n# Check data.gov for GSA Schedule 70 SIN data\nurls = [\n    \'https://catalog.data.gov/dataset?tags=gsa+schedul | 0 | 3464 |
| 14 | ['python3', '-c', '\nimport requests\n# Try data.gov API\nurl = \'https://catalog.data.gov/api/3/action/package_search?q=gsa+schedule\'\nr = requests. | 0 | 1087 |
| 15 | ['python3', '-c', '\nimport requests\n# Try data.gov API with correct path\nurl = \'https://catalog.data.gov/api/3/action/package_search?q=gsa\'\nr =  | 0 | 1769 |
| 16 | ['python3', '-c', "\nimport requests\n# Check data.gov API base\nurl = 'https://catalog.data.gov/api/'\nr = requests.get(url, timeout=15)\nprint(f'Sta | 0 | 976 |
| 17 | ['python3', '-c', '\nimport requests\n# Try other data sources for GSA Schedule 70 SINs\nurls = [\n    \'https://www.gsa.gov/cdnstatic/GSASchedule70_S | 0 | 4377 |
| 18 | ['python3', '-c', "\nimport requests\n# Try to find GSA SIN reference data\nurls = [\n    'https://www.gsa.gov/system/files/Schedule_70_SIN_Crosswalk. | 0 | 2894 |
| 19 | ['python3', '-c', '\nimport requests\n# Try to find SIN reference data from other sources\nurls = [\n    \'https://raw.githubusercontent.com/GSA/sched | 0 | 2417 |
| 20 | ['python3', '-c', "\nimport requests\n# Try to find GSA MAS contract holder data\nurls = [\n    'https://www.gsa.gov/system/files/GSASchedule70_Contra | 0 | 4542 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 935 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 14:29:43 | session_start | GSA eLibrary cross-ref validation and SEWP catalog deep dive for Fedmarket |
| 2 | 14:30:05 | command | $ python3 -c import requests; print('requests available') |
| 3 | 14:31:26 | command | $ python3 -c  import requests # Try GSA eLibrary API url = 'https://api.data.gov/gsa/elibrary/2019/01/schedule/70/sins' try:     r = requests. |
| 4 | 14:32:13 | command | $ python3 -c  import requests # Try different GSA eLibrary endpoints endpoints = [     'https://api.data.gov/gsa/elibrary/schedule/70/sins', |
| 5 | 14:35:26 | command | $ python3 -c  import requests # Check if the site resolves try:     r = requests.get('http://elibrary.gsa.gov', timeout=10, allow_redirects=Tr |
| 6 | 14:35:49 | command | $ python3 -c  import requests r = requests.get('https://api.gsa.gov/', timeout=10) print(r.text[:2000]) |
| 7 | 14:38:08 | command | $ python3 -c  import requests # Try different GSA eLibrary URLs urls = [     'https://www.gsa.gov/elibrary',     'https://www.gsa.gov/buying-s |
| 8 | 14:38:42 | command | $ python3 -c  import requests r = requests.get('https://gsaelibrary.gsa.gov/', timeout=15) print(f'Status: {r.status_code}') print(f'Content l |
| 9 | 14:39:08 | command | $ python3 -c  import requests r = requests.get('https://www.gsaelibrary.gsa.gov/ElibMain/home.do', timeout=15) print(f'Status: {r.status_code} |
| 10 | 14:39:38 | command | $ python3 -c  import requests # Try to find CSV exports or API endpoints urls = [     'https://www.gsaelibrary.gsa.gov/ElibMain/schedule/sched |
| 11 | 14:39:56 | command | $ python3 -c  import requests r = requests.get('https://www.gsaelibrary.gsa.gov/ElibMain/schedule/schedule.do?scheduleNumber=70&download=csv', |
| 12 | 14:40:29 | command | $ python3 -c  import requests # Try SEWP catalog urls = [     'https://www.sewp.nasa.gov/',     'https://sewp.nasa.gov/',     'https://www.sew |
| 13 | 14:40:52 | command | $ python3 -c  import requests # Check data.gov for GSA Schedule 70 SIN data urls = [     'https://catalog.data.gov/dataset?tags=gsa+schedule+7 |
| 14 | 14:41:11 | command | $ python3 -c  import requests # Try data.gov API url = 'https://catalog.data.gov/api/3/action/package_search?q=gsa+schedule' r = requests.get( |
| 15 | 14:41:28 | command | $ python3 -c  import requests # Try data.gov API with correct path url = 'https://catalog.data.gov/api/3/action/package_search?q=gsa' r = requ |
| 16 | 14:41:43 | command | $ python3 -c  import requests # Check data.gov API base url = 'https://catalog.data.gov/api/' r = requests.get(url, timeout=15) print(f'Status |
| 17 | 14:42:04 | command | $ python3 -c  import requests # Try other data sources for GSA Schedule 70 SINs urls = [     'https://www.gsa.gov/cdnstatic/GSASchedule70_SINs |
| 18 | 14:42:30 | command | $ python3 -c  import requests # Try to find GSA SIN reference data urls = [     'https://www.gsa.gov/system/files/Schedule_70_SIN_Crosswalk.xl |
| 19 | 14:43:27 | command | $ python3 -c  import requests # Try to find SIN reference data from other sources urls = [     'https://raw.githubusercontent.com/GSA/schedule |
| 20 | 14:45:40 | command | $ python3 -c  import requests # Try to find GSA MAS contract holder data urls = [     'https://www.gsa.gov/system/files/GSASchedule70_Contract |
| 21 | 15:14:36 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 22 | 15:14:36 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 23 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 24 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
| 25 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
| 26 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
| 27 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
| 28 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
| 29 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 30 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 31 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 32 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 33 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 34 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 35 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 36 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.meta.json |
| 37 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.json |
| 38 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.meta.json |
| 39 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.json |
| 40 | 15:14:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.meta.json |
| 948 | 15:15:08 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 949 | 15:15:08 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket.py |
| 950 | 15:15:08 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket_dynamic.py |
| 951 | 15:15:08 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 952 | 15:15:09 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 953 | 15:15:09 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 954 | 15:15:09 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 955 | 15:15:09 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 956 | 15:15:09 | doc_update | updated STATE.md |
| 957 | 15:15:09 | session_end | E213 completed: GSA MAS SIN/SEWP validation using USAspending ground truth. Official GSA eLibrary and SEWP catalog APIs are inaccessible. Validated E2 |

_907 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-020-gsa-elibrary-cross-ref-validation-and-se/events.jsonl
```
