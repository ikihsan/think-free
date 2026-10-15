# Session 2026-10-15-001-prior-art-and-demand-evidence-for-a-dete

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-15T00:16:50+00:00
- **Duration:** 4803.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

prior-art and demand evidence for a deterministic CSV type-coercion checker, then measure real spreadsheet round-trip corruption on real CSVs

## Summary

Prior-art and demand probes returned weak for a CSV coercion linter (a handful of high-vote reports; 0-to-1-star tools that already do parts of it). E161 then measured the mechanism on real files with a real engine: 1,206,342 cells through LibreOffice Calc 6.4.7.2 headless, cell-level diff against source text. 36,697 leading-zero GEOID cells damaged in the US Census 2023 Gazetteer (9.5% of that file); 0 damaging cells in 818,222 cells of analyst exports and public-body registers; 13 of 78 folklore controls damaged. csvsafe.py (200 lines, stdlib, 10 tests) reproduces the engine at precision 1.0 and recall 1.0 on two real frames and flags 36,697 TP / 0 FP / 0 FN; csvsafe write takes the census file to 0 damaging cells. Not a candidate: the frame where damage is common is machine-produced tables whose publishers already ship .xlsx. Kept unreleased at status: draft, plus the round-trip instrument the four synthetic-fixture experiments lacked.

## Next

Not this line. E161's load-bearing claim (that the exposed population already knows) is untested but low-stakes; the prevalence measurement it names would not change the build decision. Move to a fresh population with a real, independent oracle.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/161-csv-spreadsheet-coercion/RESULT.md | c7e48b633698 | 9332 |
| EXPERIMENTS/161-csv-spreadsheet-coercion/instrument-test.json | 7764cce6dc0c | 6292 |
| EXPERIMENTS/161-csv-spreadsheet-coercion/csvsafe.py | 1658783d9b24 | 8411 |

## Commands

5 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '/tmp/opencode/priorart_probe.py'] | 0 | 22103 |
| 3 | ['python3', '/tmp/opencode/demand_probe.py'] | 0 | 13576 |
| 6 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/161-csv-spreadsheet-coercion', '-t', 'EXPERIMENTS/161-csv-spreadsheet-coercion', '-v'] | 1 | 608 |
| 7 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/161-csv-spreadsheet-coercion', '-t', 'EXPERIMENTS/161-csv-spreadsheet-coercion'] | 1 | 509 |
| 8 | ['python3', '-m', 'unittest', 'discover', '-s', 'EXPERIMENTS/161-csv-spreadsheet-coercion', '-t', 'EXPERIMENTS/161-csv-spreadsheet-coercion'] | 0 | 524 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 148 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/049-lockfile-closure/RESULT-PART-B.md |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/anyio-4.5.2-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/certifi-2026.7.22-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/charset_normalizer-3.5.2-cp37-abi3-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/exceptiongroup-1.3.1-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/h11-0.16.0-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/httpcore-1.0.9-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/httpx-0.28.1-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/idna-3.15-py3-none-any.whl |
|   undeclared | EXPERIMENTS/049-lockfile-closure/part_b_rerun/markdown_it_py-3.0.0-py3-none-any.whl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:16:50 | session_start | prior-art and demand evidence for a deterministic CSV type-coercion checker, then measure real spreadsheet round-trip corruption on real CSVs |
| 2 | 00:17:32 | command | $ python3 /tmp/opencode/priorart_probe.py |
| 3 | 00:18:01 | command | $ python3 /tmp/opencode/demand_probe.py |
| 4 | 00:19:04 | task_rewrite | appended a create record for T-0096 |
| 5 | 00:19:48 | milestone | prior-art probe (GitHub/PyPI/npm, 8 vocabularies) and demand probe (Stack Exchange, 6 sites) run for a CSV type-coercion checker: no adopted prior art |
| 6 | 01:07:57 | command | $ python3 -m unittest discover -s EXPERIMENTS/161-csv-spreadsheet-coercion -t EXPERIMENTS/161-csv-spreadsheet-coercion -v |
| 7 | 01:08:06 | command | $ python3 -m unittest discover -s EXPERIMENTS/161-csv-spreadsheet-coercion -t EXPERIMENTS/161-csv-spreadsheet-coercion |
| 8 | 01:08:15 | command | $ python3 -m unittest discover -s EXPERIMENTS/161-csv-spreadsheet-coercion -t EXPERIMENTS/161-csv-spreadsheet-coercion |
| 9 | 01:25:50 | artifact | wrote EXPERIMENTS/161-csv-spreadsheet-coercion/RESULT.md |
| 10 | 01:25:56 | artifact | wrote EXPERIMENTS/161-csv-spreadsheet-coercion/instrument-test.json |
| 11 | 01:25:59 | artifact | wrote EXPERIMENTS/161-csv-spreadsheet-coercion/csvsafe.py |
| 12 | 01:26:35 | milestone | E161 measured: 1,206,342 cells through LibreOffice Calc; Census GEOIDs lose 36,697 leading zeros (9.5%); analyst and public-body frames lose nothing;  |
| 13 | 01:29:25 | task_rewrite | rewrote tasks/T-0096-e161-measure-how-often-a-real-spreadsheet-engine.md (status: done) |
| 14 | 01:29:31 | task_rewrite | appended a complete record for T-0096 |
| 15 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/RESULT-PART-B.md |
| 16 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/anyio-4.5.2-py3-none-any.whl |
| 17 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/certifi-2026.7.22-py3-none-any.whl |
| 18 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/charset_normalizer-3.5.2-cp37-abi3-manylinux1_x86_64.manylinu |
| 19 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/exceptiongroup-1.3.1-py3-none-any.whl |
| 20 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/h11-0.16.0-py3-none-any.whl |
| 21 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/httpcore-1.0.9-py3-none-any.whl |
| 22 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/httpx-0.28.1-py3-none-any.whl |
| 23 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/idna-3.15-py3-none-any.whl |
| 24 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/markdown_it_py-3.0.0-py3-none-any.whl |
| 25 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/mdurl-0.1.2-py3-none-any.whl |
| 26 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/pygments-2.19.2-py3-none-any.whl |
| 27 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/requests-2.32.3-py3-none-any.whl |
| 28 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/rich-13.9.4-py3-none-any.whl |
| 29 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/sniffio-1.3.1-py3-none-any.whl |
| 30 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/typing_extensions-4.13.2-py3-none-any.whl |
| 31 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/part_b_rerun/urllib3-2.2.3-py3-none-any.whl |
| 32 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/generate_spec.py |
| 33 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/results.json |
| 34 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/079-arxiv-reproducibility/verdict.json |
| 35 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 36 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 37 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 38 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 39 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 40 | 01:36:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 155 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-034-check-state-next-actions-md-for-planned/events.jsonl |
| 156 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-035-fresh-observation-test-discriminating-ob/events.jsonl |
| 157 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-036-fresh-observation-discriminating-observa/events.jsonl |
| 158 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-037-investigate-t-0093-discriminating-observ/events.jsonl |
| 159 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-038-investigate-recurring-payment-detection/commands.log |
| 160 | 01:36:53 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-038-investigate-recurring-payment-detection/events.jsonl |
| 161 | 01:36:53 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 162 | 01:36:53 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 163 | 01:36:54 | doc_update | updated STATE.md |
| 164 | 01:36:54 | session_end | Prior-art and demand probes returned weak for a CSV coercion linter (a handful of high-vote reports; 0-to-1-star tools that already do parts of it). E |

_114 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-001-prior-art-and-demand-evidence-for-a-dete/events.jsonl
```
