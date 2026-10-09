# Session 2026-10-09-003-run-the-install-test-falsification-of-e0

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T01:04:20+00:00
- **Duration:** 24807.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Run the install-test falsification of E068's spec generator against the repo's own declared spec and an agent arm, on real repos

## Summary

E069 ran the install-test falsification of E068's spec generator: 16 of 20 repositories measured (VM hit 95% disk; all 4 unmeasured carry pins pip refuses, so gates are determined), GEN installs cleanly in 3 of 16 and all three name nothing, verified imports 0 of 16, K1 passes vacuously and the direction closes on K3 (F101, D088). Six instrumentation defects found and fixed (analyze.py reading a file the run writes at the end; installed counting untested environments; a pip timeout charged to the mechanism; README headline reporting 15 measured as 20; a near-miss count of 149-of-383 no rule reproduces, recomputed as 132 of 383 = 34.5% in pin_compatibility.py). doc lint was hanging on 3.6GB of un-gitignored third-party checkouts - added EXPERIMENTS/068-arxiv-spec-generator/repos/ and cache/pypi/ under the established re-fetchable-inputs clause. Landing repairs: duplicate F093 renumbered to F102 (two VMs allocated it), F101/F102 defined in FAILURES-findings-35.md, EXPERIMENTS/**/raw/*.tsv added to the declared-exemption class, and three files split at the 300-line cap with byte-identical re-verification (harness.py into config.py+venvinstall.py, extract.py into declared_files.py, STATE-history into -2/-3).

## Next

E069's lesson is the standing one: the next candidate's kill gate must have its reachable set enumerated before the run (a gate whose only passing values are vacuous cannot fail), and its analyzer must read bytes that exist before the run ends. The one open question E064 names is untested and is the next observation: the 24 healthy-metadata false accepts are exactly the population the installers' own guards (keyed on names that do NOT resolve) cannot see - observe whether that silent wrong-project failure occurs anywhere in the wild, per D080 starting from observation, not a prototype. Per D083, if that closes, start a fresh observation in a new domain.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/069-install-test/README.md | 38d6827f812d | 13939 |
| EXPERIMENTS/069-install-test/results.json | b40d75a6be07 | 29096 |
| EXPERIMENTS/069-install-test/analyze.py | bab232bea6d7 | 13968 |
| EXPERIMENTS/069-install-test/pin_compatibility.py | 813718f49ddd | 11757 |
| EXPERIMENTS/069-install-test/PROTOCOL.md | bb0d1de6d5c2 | 10205 |
| EXPERIMENTS/069-install-test/interpreter.json | bb9024ef54bb | 325 |

## Commands

8 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/069-install-test/repos_manifest.py'] | 0 | 495 |
| 3 | ['python3', 'EXPERIMENTS/069-install-test/repos_manifest.py'] | 0 | 539 |
| 4 | ['python3', 'EXPERIMENTS/069-install-test/harness.py'] | 1 | 863 |
| 5 | ['python3', 'EXPERIMENTS/069-install-test/harness.py'] | 1 | 54395 |
| 6 | ['python3', 'EXPERIMENTS/069-install-test/harness.py'] | 1 | 66588 |
| 7 | ['python3', 'EXPERIMENTS/069-install-test/harness.py'] | 0 | 67987 |
| 8 | ['python3', 'EXPERIMENTS/069-install-test/controls.py'] | 1 | 986713 |
| 9 | ['python3', 'EXPERIMENTS/069-install-test/controls.py'] | 1 | 1514579 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 82 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-SCREENING-14.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/067-arxiv-code-repro/generate.py |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/README.md |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/cache/extracted.json |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_Profluent-Internships_MMDiff.txt |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_deeplearning-wisc_args.txt |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_illidanlab_inversion-influence-function.txt |
|   undeclared | EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_qzhb_BSSARD.txt |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:04:20 | session_start | Run the install-test falsification of E068's spec generator against the repo's own declared spec and an agent arm, on real repos |
| 2 | 01:10:26 | command | $ python3 EXPERIMENTS/069-install-test/repos_manifest.py |
| 3 | 01:10:43 | command | $ python3 EXPERIMENTS/069-install-test/repos_manifest.py |
| 4 | 01:13:31 | command | $ python3 EXPERIMENTS/069-install-test/harness.py |
| 5 | 01:14:42 | command | $ python3 EXPERIMENTS/069-install-test/harness.py |
| 6 | 01:16:18 | command | $ python3 EXPERIMENTS/069-install-test/harness.py |
| 7 | 01:17:58 | command | $ python3 EXPERIMENTS/069-install-test/harness.py |
| 8 | 01:37:33 | command | $ python3 EXPERIMENTS/069-install-test/controls.py |
| 9 | 02:03:27 | command | $ python3 EXPERIMENTS/069-install-test/controls.py |
| 10 | 03:28:12 | milestone | E069 protocol written; oracle controls P2 passed; static pin-compatibility arm shows 17 of 20 generated specs carry a pin pip refuses on E068's own de |
| 11 | 05:56:58 | milestone | Server restart survived; harness still measuring repo 16/20 (JHW2000/JARNet GEN arm, 27min, 5.8GB venv). Verified E069 README does NOT reproduce from  |
| 12 | 06:07:31 | milestone | E069 analysis pipeline repaired so the verdict regenerates from the durable per-repo files: analyze.py read raw_results.json (written only at end of a |
| 13 | 06:25:28 | milestone | E069 result bounded. Measuring the one unmeasured repo with an empty spec (google-research) moved GEN installs 2->3 and flipped analyze.py's own label |
| 14 | 06:30:37 | artifact | wrote EXPERIMENTS/069-install-test/README.md |
| 15 | 06:30:40 | artifact | wrote EXPERIMENTS/069-install-test/results.json |
| 16 | 06:30:43 | artifact | wrote EXPERIMENTS/069-install-test/analyze.py |
| 17 | 06:30:45 | artifact | wrote EXPERIMENTS/069-install-test/pin_compatibility.py |
| 18 | 06:30:48 | artifact | wrote EXPERIMENTS/069-install-test/PROTOCOL.md |
| 19 | 06:30:52 | artifact | wrote EXPERIMENTS/069-install-test/interpreter.json |
| 20 | 06:43:30 | milestone | doc lint was hanging (9min, no output): it walked EXPERIMENTS/068-arxiv-spec-generator/repos/, 3.6GB of third-party shallow clones including a 510MB m |
| 21 | 07:36:24 | milestone | Landing E069 clean: doc lint exits 0 and all four tests that failed on the in-progress tree (identifier collision F093/F102, link escape, stale index, |
| 22 | 07:57:46 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 23 | 07:57:46 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-14.md |
| 24 | 07:57:46 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 25 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-arxiv-code-repro/generate.py |
| 26 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/README.md |
| 27 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/extracted.json |
| 28 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_Profluent-Internships_MMDiff.txt |
| 29 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_deeplearning-wisc_args.txt |
| 30 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_illidanlab_inversion-influence-function.txt |
| 31 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A1_qzhb_BSSARD.txt |
| 32 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A2_Itaymanes_K-QA.txt |
| 33 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_AmitRozner_domain-generalizable-multiple-doma |
| 34 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_DrLuo_RTM.txt |
| 35 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_EternityYW_Gemini-Commonsense-Evaluation.txt |
| 36 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_Goallow_Mini-Hes.txt |
| 37 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_JHW2000_JARNet.txt |
| 38 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_LPMP_BDD.txt |
| 39 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_ambroiseodt_tsim.txt |
| 40 | 07:57:46 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/068-arxiv-spec-generator/cache/generated_specs/A3_cvblab_Mitosis-UTS.txt |
| 99 | 07:57:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-029-analyze-python-package-importability-pat/events.jsonl |
| 100 | 07:57:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-001-record-decision-and-continuation-for-e06/events.jsonl |
| 101 | 07:57:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-002-record-artifact-for-e067-generate-py/events.jsonl |
| 102 | 07:57:47 | unlogged_change | changed but never declared as an artifact: tasks/T-0087-e055-build-a-tool-neutral-git-index-postconditio.md |
| 103 | 07:57:47 | unlogged_change | changed but never declared as an artifact: vendor/MANIFEST.md |
| 104 | 07:57:47 | doc_update | updated DECISIONS-SCREENING-14.md |
| 105 | 07:57:47 | doc_update | updated DECISIONS.md |
| 106 | 07:57:47 | doc_update | updated FAILURES.md |
| 107 | 07:57:47 | doc_update | updated STATE.md |
| 108 | 07:57:47 | session_end | E069 ran the install-test falsification of E068's spec generator: 16 of 20 repositories measured (VM hit 95% disk; all 4 unmeasured carry pins pip ref |

_58 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-003-run-the-install-test-falsification-of-e0/events.jsonl
```
