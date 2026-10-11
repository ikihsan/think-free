# Session 2026-10-10-008-measure-the-rate-of-real-importerror-mod

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T11:06:32+00:00
- **Duration:** 2866.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure the rate of real ImportError/ModuleNotFoundError reports that name a module but no distribution, on Stack Overflow and GitHub issues

## Summary

E092 module-provider demand measurement completed. G1 FAIL (only 40 Stack Overflow questions harvested, target 200), G2 PASS (discrimination test 95% accuracy on 40 construction-labelled controls), G3 rate inconclusive (2/40 module-only, 5% raw, ~28% of classifiable but sample too small), G4 marginal (1/2 module-only have views). The population of practitioners asking 'which distribution provides this module?' on observable venues is too small to measure with current API access. The line closes on G1 failure.

## Next

Fresh observation in a new domain per D083. The package-name line (E064/E070/E085/E090/E092) is closed on measured grounds. Next session must start from fresh observation in a new domain with an instrument that passes discrimination test before population measurement.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/092-module-provider-demand/PROTOCOL.md | 60c9b1c2a14d | 9195 |
| EXPERIMENTS/092-module-provider-demand/controls.json | 13b989a548df | 12751 |
| EXPERIMENTS/092-module-provider-demand/DISCRIMINATION_TEST_RESULTS.json | 5aa4b00c1770 | 1100 |
| EXPERIMENTS/092-module-provider-demand/harvest_so.json | 6f88a45de46a | 137107 |
| EXPERIMENTS/092-module-provider-demand/RESULTS.md | fc7adbf56663 | 4298 |
| EXPERIMENTS/092-module-provider-demand/classifier.py | 2f669b769aac | 11135 |
| EXPERIMENTS/092-module-provider-demand/test_classify.py | 53b069e4d289 | 7744 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['mkdir', '-p', 'EXPERIMENTS/092-module-provider-demand'] | 0 | 4 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 30 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/measure_population.py |
|   undeclared | EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test_v2.py |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-2015682408449234324.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-3736331359080306124.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-6816885938114988197.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-8191367510348677309.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_5651601283028731923.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-1391194897386935960.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-2098477104287243660.json |
|   undeclared | EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-2836858676413196064.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:06:32 | session_start | Measure the rate of real ImportError/ModuleNotFoundError reports that name a module but no distribution, on Stack Overflow and GitHub issues |
| 2 | 11:06:56 | command | $ mkdir -p EXPERIMENTS/092-module-provider-demand |
| 3 | 11:26:30 | milestone | Completed E092: module-provider demand measurement. G1 fails (only 40 SO questions), G2 passes (95% accuracy), G3 inconclusive (small sample), G4 marg |
| 4 | 11:26:53 | artifact | wrote EXPERIMENTS/092-module-provider-demand/PROTOCOL.md |
| 5 | 11:26:54 | artifact | wrote EXPERIMENTS/092-module-provider-demand/controls.json |
| 6 | 11:26:55 | artifact | wrote EXPERIMENTS/092-module-provider-demand/DISCRIMINATION_TEST_RESULTS.json |
| 7 | 11:26:55 | artifact | wrote EXPERIMENTS/092-module-provider-demand/harvest_so.json |
| 8 | 11:26:56 | artifact | wrote EXPERIMENTS/092-module-provider-demand/RESULTS.md |
| 9 | 11:26:57 | artifact | wrote EXPERIMENTS/092-module-provider-demand/classifier.py |
| 10 | 11:26:57 | artifact | wrote EXPERIMENTS/092-module-provider-demand/test_classify.py |
| 11 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/measure_population.py |
| 12 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/090-fresh-observation-structured-faults/run_discrimination_test_v2.py |
| 13 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-2015682408449234324.json |
| 14 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-3736331359080306124.json |
| 15 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-6816885938114988197.json |
| 16 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_-8191367510348677309.json |
| 17 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/gh_5651601283028731923.json |
| 18 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-1391194897386935960.json |
| 19 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-2098477104287243660.json |
| 20 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-2836858676413196064.json |
| 21 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-293938269329985549.json |
| 22 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-5173110052057393772.json |
| 23 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-5767059578561439816.json |
| 24 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-670410225507507277.json |
| 25 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-6875238647147419649.json |
| 26 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_-8067677551562239189.json |
| 27 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_1288992901851251016.json |
| 28 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_1930554318371188534.json |
| 29 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_3535258719718082481.json |
| 30 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_5762727719346469638.json |
| 31 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_6404079325730572202.json |
| 32 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/.module-demand-cache/se_7991566340424433672.json |
| 33 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/CLASSIFICATION_RESULTS.json |
| 34 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/DISCRIMINATION_TEST.md |
| 35 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/classify_harvest.py |
| 36 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/classify_so.py |
| 37 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/harvest.py |
| 38 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/harvest_raw.json |
| 39 | 11:54:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-module-provider-demand/harvest_so.py |
| 40 | 11:54:18 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 41 | 11:54:18 | doc_update | updated STATE.md |
| 42 | 11:54:18 | session_end | E092 module-provider demand measurement completed. G1 FAIL (only 40 Stack Overflow questions harvested, target 200), G2 PASS (discrimination test 95%  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-008-measure-the-rate-of-real-importerror-mod/events.jsonl
```
