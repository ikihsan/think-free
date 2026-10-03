# Session 2026-10-03-030-run-t-0017-attribute-every-differing-byt

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-03T21:41:36+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run T-0017: attribute every differing byte between repeated builds of one source under different SOURCE_DATE_EPOCH values, with the kill gate written before the run

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/paths.py | 8d470e1296d3 | 3359 |
| tools/originlib/reconcile.py | 8cef4d2e2b8e | 5213 |
| tests/test_doc_gaps.py | 243b1bcbce14 | 5133 |
| DECISIONS.md | 976f9647a377 | 1965 |
| DECISIONS-PRACTICE.md | 01e63fb9ea51 | 10603 |
| DECISIONS-GATING.md | 6187391ea08b | 8322 |
| STATE.md | bcf131bafc2c | 16735 |
| docs/reference/cli-reference.md | 255abcb6e0db | 5878 |
| docs/process/session-protocol.md | 57802211019b | 6259 |
| docs/process/experiment-protocol.md | 4e7fd3b44c3d | 5216 |
| docs/reference/repo-map.md | 2eaf7f7dcbf8 | 4535 |
| RELEASE-MANIFEST.md | 68973b268467 | 2751 |
| AGENTS.md | 6b69591613ec | 7952 |
| .agents/skills/evidence-record/SKILL.md | e48092f157eb | 5242 |
| .agents/skills/session-lifecycle/SKILL.md | 5b0a680e4806 | 5821 |
| HYPOTHESES-results.md | 28920498f636 | 12110 |
| EXPERIMENTS/008-build-timestamp-attribution/README.md | a075f2a413d8 | 8259 |
| EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py | e6e359d5c0c2 | 4056 |
| EXPERIMENTS/008-build-timestamp-attribution/README.md | a075f2a413d8 | 8259 |
| EXPERIMENTS/008-build-timestamp-attribution/attribute.py | 6fd912e4358e | 7099 |
| EXPERIMENTS/008-build-timestamp-attribution/builds.py | 4ca5145e6027 | 9202 |
| EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py | e6e359d5c0c2 | 4056 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/click-8.1.7.tar.gz | ca9853ad459e | 336121 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/idna-3.3.tar.gz | 9d643ff0a55b | 286689 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/packaging-21.3.tar.gz | dd47c42927d8 | 84848 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/six-1.16.0.tar.gz | 1e61c37477a1 | 34041 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/toml-0.10.2.tar.gz | b3bda1d108d5 | 22253 |
| EXPERIMENTS/008-build-timestamp-attribution/sources.json | 1aa354bb39a9 | 1693 |
| EXPERIMENTS/008-build-timestamp-attribution/zipdiff.py | 2b188cb735d6 | 8848 |
| EXPERIMENTS/008-build-timestamp-attribution/first-failure.json | ce981b51a05d | 6812 |
| EXPERIMENTS/008-build-timestamp-attribution/README.md | a075f2a413d8 | 8259 |
| EXPERIMENTS/008-build-timestamp-attribution/attribute.py | c2e630217bb7 | 7570 |
| EXPERIMENTS/008-build-timestamp-attribution/builds.py | e87505d9ae66 | 10735 |
| EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py | e6e359d5c0c2 | 4056 |
| EXPERIMENTS/008-build-timestamp-attribution/results.json | f27b45130468 | 35554 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/click-8.1.7.tar.gz | ca9853ad459e | 336121 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/idna-3.3.tar.gz | 9d643ff0a55b | 286689 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/packaging-21.3.tar.gz | dd47c42927d8 | 84848 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/six-1.16.0.tar.gz | 1e61c37477a1 | 34041 |
| EXPERIMENTS/008-build-timestamp-attribution/sdists/toml-0.10.2.tar.gz | b3bda1d108d5 | 22253 |
| EXPERIMENTS/008-build-timestamp-attribution/sources.json | 1aa354bb39a9 | 1693 |
| EXPERIMENTS/008-build-timestamp-attribution/zipdiff.py | 2b188cb735d6 | 8848 |
| EXPERIMENTS/008-build-timestamp-attribution/builds.py | 225e064983fe | 11070 |
| tools/originlib/doclint.py | 80ab0f781064 | 9458 |
| tools/originlib/docfiles.py | 6d480668ccb1 | 2525 |
| tests/test_doclint.py | d39b7a5deab0 | 8420 |
| .gitignore | 4b9cd2958518 | 422 |
| FAILURES-findings-2.md | 9c0c0076ad0f | 12327 |
| FAILURES.md | ec3d421baf96 | 3834 |
| HYPOTHESES.md | f26a1b4c0695 | 10342 |
| HYPOTHESES-results.md | 6b60d23e650d | 13263 |
| ROADMAP.md | ff3050e2a3d6 | 7181 |
| STATE.md | c011d029f564 | 17352 |
| docs/process/experiment-protocol.md | 2f4e4ab7aa48 | 5650 |
| EXPERIMENTS/008-build-timestamp-attribution/README.md | 4355cd9f90ce | 14205 |
| EXPERIMENTS/008-build-timestamp-attribution/attribute.py | c2e630217bb7 | 7570 |
| EXPERIMENTS/008-build-timestamp-attribution/builds.py | 225e064983fe | 11070 |
| EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py | e6e359d5c0c2 | 4056 |
| EXPERIMENTS/008-build-timestamp-attribution/first-failure.json | ce981b51a05d | 6812 |
| EXPERIMENTS/008-build-timestamp-attribution/results.json | bc482c75c3a6 | 38138 |
| EXPERIMENTS/008-build-timestamp-attribution/sources.json | 1aa354bb39a9 | 1693 |
| EXPERIMENTS/008-build-timestamp-attribution/zipdiff.py | 2b188cb735d6 | 8848 |
| DECISIONS-GATING.md | 0f5c8a056e5b | 10940 |
| tasks/T-0017-build-one-source-twice-under-different-source-da.md | 6ed5d1403667 | 5765 |
| tasks/CLAIMS.jsonl | ba32f9be6008 | 17040 |
| tasks/T-0017-build-one-source-twice-under-different-source-da.md | ef04148c130e | 5762 |
| sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/README.md | e5bb2248d625 | 9744 |
| sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/commands.log | cacc845bece7 | 8974 |
| sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/events.jsonl | d84342e59073 | 40489 |

## Commands

8 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport setuptools, wheel, sys\nprint('python', sys.version.split()[0])\nprint('setuptools', setuptools.__version__)\nprint('wheel | 0 | 695 |
| 3 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 88498 |
| 4 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 90245 |
| 23 | ['python3', 'EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py'] | 0 | 29204 |
| 35 | ['python3', 'EXPERIMENTS/008-build-timestamp-attribution/attribute.py'] | 0 | 39409 |
| 49 | ['python3', 'EXPERIMENTS/008-build-timestamp-attribution/attribute.py'] | 1 | 38789 |
| 51 | ['python3', 'EXPERIMENTS/008-build-timestamp-attribution/attribute.py'] | 0 | 37511 |
| 53 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 93097 |

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
| 1 | 21:41:36 | session_start | Run T-0017: attribute every differing byte between repeated builds of one source under different SOURCE_DATE_EPOCH values, with the kill gate written  |
| 2 | 21:42:42 | command | $ python3 -c  import setuptools, wheel, sys print('python', sys.version.split()[0]) print('setuptools', setuptools.__version__) print('wheel', |
| 3 | 21:47:35 | command | $ python3 -m unittest discover -s tests |
| 4 | 21:49:21 | command | $ python3 -m unittest discover -s tests |
| 5 | 21:49:43 | artifact | wrote tools/originlib/paths.py |
| 6 | 21:49:43 | artifact | wrote tools/originlib/reconcile.py |
| 7 | 21:49:43 | artifact | wrote tests/test_doc_gaps.py |
| 8 | 21:49:43 | artifact | wrote DECISIONS.md |
| 9 | 21:49:43 | artifact | wrote DECISIONS-PRACTICE.md |
| 10 | 21:49:43 | artifact | wrote DECISIONS-GATING.md |
| 11 | 21:49:43 | artifact | wrote STATE.md |
| 12 | 21:49:43 | artifact | wrote docs/reference/cli-reference.md |
| 13 | 21:49:43 | artifact | wrote docs/process/session-protocol.md |
| 14 | 21:49:43 | artifact | wrote docs/process/experiment-protocol.md |
| 15 | 21:49:43 | artifact | wrote docs/reference/repo-map.md |
| 16 | 21:49:43 | artifact | wrote RELEASE-MANIFEST.md |
| 17 | 21:49:43 | artifact | wrote AGENTS.md |
| 18 | 21:49:43 | artifact | wrote .agents/skills/evidence-record/SKILL.md |
| 19 | 21:49:43 | artifact | wrote .agents/skills/session-lifecycle/SKILL.md |
| 20 | 21:49:43 | artifact | wrote HYPOTHESES-results.md |
| 21 | 21:49:43 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/README.md |
| 22 | 21:50:04 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py |
| 23 | 21:50:33 | command | $ python3 EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py |
| 24 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/README.md |
| 25 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/attribute.py |
| 26 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/builds.py |
| 27 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py |
| 28 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sdists/click-8.1.7.tar.gz |
| 29 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sdists/idna-3.3.tar.gz |
| 30 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sdists/packaging-21.3.tar.gz |
| 31 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sdists/six-1.16.0.tar.gz |
| 32 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sdists/toml-0.10.2.tar.gz |
| 33 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sources.json |
| 34 | 21:58:07 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/zipdiff.py |
| 35 | 21:58:50 | command | $ python3 EXPERIMENTS/008-build-timestamp-attribution/attribute.py |
| 36 | 22:00:58 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/first-failure.json |
| 37 | 22:00:58 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/README.md |
| 38 | 22:00:58 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/attribute.py |
| 39 | 22:00:58 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/builds.py |
| 40 | 22:00:58 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/fetch_sources.py |
| 71 | 22:14:42 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/sources.json |
| 72 | 22:14:42 | artifact | wrote EXPERIMENTS/008-build-timestamp-attribution/zipdiff.py |
| 73 | 22:15:11 | decision | Two rules from T-0017's vacuous control: a gate clause is implemented by its own noun rather than a weaker proxy (attributed to a non-timestamp cause  |
| 74 | 22:15:11 | artifact | wrote DECISIONS-GATING.md |
| 75 | 22:21:46 | artifact | wrote tasks/T-0017-build-one-source-twice-under-different-source-da.md |
| 76 | 22:22:10 | artifact | wrote tasks/CLAIMS.jsonl |
| 77 | 22:22:10 | artifact | wrote tasks/T-0017-build-one-source-twice-under-different-source-da.md |
| 78 | 22:22:10 | artifact | wrote sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/README.md |
| 79 | 22:22:10 | artifact | wrote sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/commands.log |
| 80 | 22:22:10 | artifact | wrote sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/events.jsonl |

_30 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/events.jsonl
```
