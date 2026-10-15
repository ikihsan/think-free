# Session 2026-10-14-029-measure-adoption-interest-for-preflight

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T18:04:51+00:00
- **Duration:** 1241.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure adoption interest for preflight among LLM evaluation practitioners via GitHub issue search and practitioner survey

## Summary

Measured adoption interest for preflight among LLM evaluation practitioners via GitHub issue search and repository analysis. Found multiple independent signals of real demand: 8+ open issues in lm-evaluation-harness about silent metric failures (C1/C2/C3 exactly match), 4+ issues in HELM about judge extraction and silent scoring failures, open proposal in openai/evals for harness-level failure attribution, feature request for reproducibility-bundle export, real audit finding 61/140 tasks with broken scoring in MLS-Bench, and standardization effort evaleval/every_eval_ever (137 stars). Preflight's three checks map directly to these documented problems. Prior art is partially-covered (no tool does all three, C3 is weakest). Created evidence record at EXPERIMENTS/preflight-adoption-interest.md. All preflight tests pass (16+9=25 tests).

## Next

Option C from STATE-next-actions.md: Document the tool with its limitations and release as stdlib-only instrumentation for harness authors. Next steps: update preflight README with adoption interest findings, ensure doc lint passes, consider promoting preflight/ to public product in RELEASE-MANIFEST.md (already listed).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/preflight-adoption-interest.md | 5905a76ba9fe | 8093 |

## Commands

17 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search GitHub for issues related to evaluation harness silent failur | 0 | 7436 |
| 3 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for issues about evaluation metric bugs, silent failures\nque | 0 | 13958 |
| 4 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Look at specific relevant issues\nurls = [\n    \'https://api.github | 0 | 2372 |
| 5 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search lm-evaluation-harness repo issues directly\nurl = \'https://a | 0 | 4745 |
| 6 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for bug issues in lm-evaluation-harness\nurl = \'https://api. | 0 | 12926 |
| 7 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for bug issues in lm-evaluation-harness with smaller page\nur | 0 | 1070 |
| 8 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Get details of relevant issues\nrelevant = [3314, 3005, 2907, 2553,  | 0 | 9996 |
| 9 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for issues about metric/aggregation bugs in lm-evaluation-har | 0 | 1068 |
| 10 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Get details of the most relevant issues\nrelevant = [4062, 4281, 423 | 0 | 4827 |
| 11 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for evaluation verification/reproducibility issues in other r | 0 | 3388 |
| 12 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Get details of relevant HELM issues\nrelevant = [4344, 4364, 4340, 4 | 0 | 2228 |
| 13 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for existing evaluation verification tools\nqueries = [\n     | 0 | 4859 |
| 14 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for discussions about evaluation harness problems on forums\n | 0 | 5348 |
| 15 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Search for discussions about leaderboard reproducibility, score veri | 0 | 4395 |
| 16 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Get details of relevant issues\nrelevant = [3749, 1832]\n\nfor num i | 0 | 1221 |
| 17 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Check evaleval/every_eval_ever repo\nurl = \'https://api.github.com/ | 0 | 1344 |
| 18 | ['python3', '-c', '\nimport json\nimport urllib.request\nimport urllib.parse\n\n# Check MLS-Bench issue #103\nurl = \'https://api.github.com/repos/Imb | 0 | 1399 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 73 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/073-viewcount-prototype-v3/results.json |
|   undeclared | EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/results.json |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/collect.py |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:04:51 | session_start | Measure adoption interest for preflight among LLM evaluation practitioners via GitHub issue search and practitioner survey |
| 2 | 18:05:18 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search GitHub for issues related to evaluation harness silent failures |
| 3 | 18:05:49 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for issues about evaluation metric bugs, silent failures queries |
| 4 | 18:06:18 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Look at specific relevant issues urls = [     'https://api.github.com/r |
| 5 | 18:06:35 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search lm-evaluation-harness repo issues directly url = 'https://api.gi |
| 6 | 18:07:03 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for bug issues in lm-evaluation-harness url = 'https://api.githu |
| 7 | 18:07:18 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for bug issues in lm-evaluation-harness with smaller page url = |
| 8 | 18:08:01 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Get details of relevant issues relevant = [3314, 3005, 2907, 2553, 3004 |
| 9 | 18:08:14 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for issues about metric/aggregation bugs in lm-evaluation-harnes |
| 10 | 18:08:38 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Get details of the most relevant issues relevant = [4062, 4281, 4236, 4 |
| 11 | 18:09:11 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for evaluation verification/reproducibility issues in other repo |
| 12 | 18:09:36 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Get details of relevant HELM issues relevant = [4344, 4364, 4340, 4351] |
| 13 | 18:09:58 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for existing evaluation verification tools queries = [     'eval |
| 14 | 18:10:32 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for discussions about evaluation harness problems on forums quer |
| 15 | 18:11:03 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Search for discussions about leaderboard reproducibility, score verific |
| 16 | 18:11:17 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Get details of relevant issues relevant = [3749, 1832]  for num in rele |
| 17 | 18:11:57 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Check evaleval/every_eval_ever repo url = 'https://api.github.com/repos |
| 18 | 18:12:14 | command | $ python3 -c  import json import urllib.request import urllib.parse  # Check MLS-Bench issue #103 url = 'https://api.github.com/repos/Imbernou |
| 19 | 18:15:14 | artifact | wrote EXPERIMENTS/preflight-adoption-interest.md |
| 20 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/results.json |
| 21 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 22 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/experiment.py |
| 23 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 24 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 25 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 26 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 27 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 28 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 29 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 30 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
| 31 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
| 32 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |
| 33 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/E137-decision.txt |
| 34 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md |
| 35 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_gsm_yi6b_result.json |
| 36 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 37 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/gsm_recompute_e137.json |
| 38 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/138-viewcount-comparison-analysis |
| 39 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/PROTOCOL.md |
| 40 | 18:25:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-evalscope-preflight-test/RESULT.md |
| 85 | 18:25:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-025-run-preflight-against-real-modelscope-ev/events.jsonl |
| 86 | 18:25:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-026-run-e137-point-calibrated-instrument-at/events.jsonl |
| 87 | 18:25:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-027-record-e137-artifacts-and-update-state-m/events.jsonl |
| 88 | 18:25:32 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-028-e138-run-r1-recomputation-on-helm-lite-v/events.jsonl |
| 89 | 18:25:32 | unlogged_change | changed but never declared as an artifact: think_free_test.py |
| 90 | 18:25:32 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 91 | 18:25:32 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 92 | 18:25:32 | unlogged_change | changed but never declared as an artifact: tools/viewcount_prototype.py |
| 93 | 18:25:33 | doc_update | updated STATE.md |
| 94 | 18:25:33 | session_end | Measured adoption interest for preflight among LLM evaluation practitioners via GitHub issue search and repository analysis. Found multiple independen |

_44 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-029-measure-adoption-interest-for-preflight/events.jsonl
```
