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
| .agents/skills/brainstorming/SKILL.md | 4a54a4858b99 | 10047 |
| .agents/skills/brainstorming/scripts/frame-template.html | 6a8a4e58bd6a | 8094 |
| .agents/skills/brainstorming/scripts/helper.js | 43c6d69954a4 | 5615 |
| .agents/skills/brainstorming/scripts/server.cjs | 2d2961ea8d11 | 25693 |
| .agents/skills/brainstorming/scripts/start-server.sh | a4e5ae84275b | 6908 |
| .agents/skills/brainstorming/scripts/stop-server.sh | 0b5ccbbd57f6 | 3263 |
| .agents/skills/brainstorming/spec-document-reviewer-prompt.md | 95a0a195de9d | 1747 |
| .agents/skills/brainstorming/visual-companion.md | 60cbad29b9dd | 13298 |
| .agents/skills/dispatching-parallel-agents/SKILL.md | 1968923066f3 | 6078 |
| .agents/skills/doc-keeper/SKILL.md | bf054363f767 | 4413 |
| .agents/skills/evidence-record/SKILL.md | e48092f157eb | 5242 |
| .agents/skills/executing-plans/SKILL.md | c4c3d8b628c5 | 2305 |
| .agents/skills/falsification-design/SKILL.md | c4ae9c628d30 | 5520 |
| .agents/skills/finishing-a-development-branch/SKILL.md | d0ac8360ed9d | 7022 |
| .agents/skills/honest-reporting/SKILL.md | 3d2aeb0643a0 | 4986 |
| .agents/skills/prior-art-check/SKILL.md | b9bcb2404f4b | 5749 |
| .agents/skills/receiving-code-review/SKILL.md | 091df1629510 | 6203 |
| .agents/skills/requesting-code-review/SKILL.md | d71cc01ba56d | 2956 |
| .agents/skills/requesting-code-review/code-reviewer.md | b2f2ec759692 | 5213 |
| .agents/skills/session-lifecycle/SKILL.md | 5b0a680e4806 | 5821 |
| .agents/skills/subagent-driven-development/SKILL.md | 349a08ad8b59 | 28077 |
| .agents/skills/subagent-driven-development/implementer-prompt.md | 946601616a6f | 5717 |
| .agents/skills/subagent-driven-development/re-review-prompt.md | e1d8e0e65e58 | 4300 |
| .agents/skills/subagent-driven-development/scripts/review-package | fac3d4bd7f94 | 1469 |
| .agents/skills/subagent-driven-development/scripts/sdd-workspace | 95a09d9d3983 | 1586 |
| .agents/skills/subagent-driven-development/scripts/task-brief | d6954ef7841c | 1158 |
| .agents/skills/subagent-driven-development/task-reviewer-prompt.md | e3b4a1bfe7cd | 7816 |
| .agents/skills/systematic-debugging/CREATION-LOG.md | c24733a5b182 | 4257 |
| .agents/skills/systematic-debugging/SKILL.md | 808fc5717aa8 | 9465 |
| .agents/skills/systematic-debugging/condition-based-waiting-example.ts | 40ae5ebe497f | 5054 |
| .agents/skills/systematic-debugging/condition-based-waiting.md | e89fec8400d6 | 3516 |
| .agents/skills/systematic-debugging/defense-in-depth.md | 1e175fb86fc3 | 3650 |
| .agents/skills/systematic-debugging/find-polluter.sh | dd7b8f13c4cc | 1986 |
| .agents/skills/systematic-debugging/root-cause-tracing.md | 6b0622269e09 | 5316 |
| .agents/skills/systematic-debugging/test-academic.md | fe2ba480d78a | 653 |
| .agents/skills/systematic-debugging/test-pressure-1.md | 0b6a915db005 | 1900 |
| .agents/skills/systematic-debugging/test-pressure-2.md | b2030aeffba0 | 2283 |
| .agents/skills/systematic-debugging/test-pressure-3.md | 96b50a52e2c7 | 2692 |
| .agents/skills/task-execution/SKILL.md | f01f2f1eb5fe | 4532 |
| .agents/skills/test-driven-development/SKILL.md | bf1b8216e523 | 9015 |
| .agents/skills/test-driven-development/writing-good-tests.md | 51471c853306 | 8268 |
| .agents/skills/using-git-worktrees/SKILL.md | 8cfb86f12126 | 6813 |
| .agents/skills/using-superpowers/SKILL.md | 55379fe7c1c4 | 3063 |
| .agents/skills/using-superpowers/references/antigravity-tools.md | 4880f6de3da4 | 1495 |
| .agents/skills/using-superpowers/references/codex-tools.md | d3f113a8ebbd | 1774 |
| .agents/skills/using-superpowers/references/gemini-tools.md | 62b9157bcb0e | 4598 |
| .agents/skills/using-superpowers/references/pi-tools.md | 703dbc83d23e | 1242 |
| .agents/skills/verification-before-completion/SKILL.md | 2befe7fc55bc | 3646 |
| .agents/skills/writing-plans/SKILL.md | 72190c88b2b5 | 6907 |
| .agents/skills/writing-plans/plan-document-reviewer-prompt.md | aa728b96aad6 | 1713 |
| .agents/skills/writing-skills/SKILL.md | d34db5c8aed6 | 26360 |
| .agents/skills/writing-skills/anthropic-best-practices.md | 217629b356c0 | 46197 |
| .agents/skills/writing-skills/examples/CLAUDE_MD_TESTING.md | 0b379a3415e1 | 5423 |
| .agents/skills/writing-skills/graphviz-conventions.dot | e2890a593c91 | 5970 |
| .agents/skills/writing-skills/persuasion-principles.md | a51bc9bf7518 | 5901 |
| .agents/skills/writing-skills/render-graphs.js | ccda971a87bb | 4857 |
| .agents/skills/writing-skills/testing-skills-with-subagents.md | c711346852c9 | 12558 |
| .git/COMMIT_EDITMSG | 64cb610a9c22 | 66 |
| .git/FETCH_HEAD | c1cb63c3236c | 108 |
| .git/HEAD | 07d1ce5a2f54 | 32 |
| .git/ORIG_HEAD | 1f55b797edcd | 41 |
| .git/config | 6ee3a77a44a7 | 284 |
| .git/description | 85ab6c163d43 | 73 |
| .git/hooks/applypatch-msg.sample | 0223497a0b8b | 478 |
| .git/hooks/commit-msg.sample | 1f74d5e92929 | 896 |
| .git/hooks/fsmonitor-watchman.sample | 9c34ab652721 | 3079 |
| .git/hooks/post-update.sample | 81765af2daef | 189 |
| .git/hooks/pre-applypatch.sample | e15c5b469ea3 | 424 |
| .git/hooks/pre-commit.sample | d6d114e507a3 | 1638 |
| .git/hooks/pre-merge-commit.sample | d3825a703379 | 416 |
| .git/hooks/pre-push.sample | 4b1119e1e13a | 1348 |
| .git/hooks/pre-rebase.sample | 4febce867790 | 4898 |
| .git/hooks/pre-receive.sample | a4c3d2b9c7bb | 544 |
| .git/hooks/prepare-commit-msg.sample | e9ddcaa4189f | 1492 |
| .git/hooks/update.sample | 751c03732002 | 3610 |
| .git/index | 98613b7ec838 | 42036 |
| .git/info/exclude | 6671fe83b7a0 | 240 |

## Commands

10 captured, 1 non-zero exit.

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
| 159 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 94292 |
| 160 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 92231 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   error | refused artifact .git/logs/HEAD: secret pattern(s) assigned-credential |

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
| 151 | 22:25:33 | artifact | wrote .git/hooks/pre-push.sample |
| 152 | 22:25:33 | artifact | wrote .git/hooks/pre-rebase.sample |
| 153 | 22:25:33 | artifact | wrote .git/hooks/pre-receive.sample |
| 154 | 22:25:33 | artifact | wrote .git/hooks/prepare-commit-msg.sample |
| 155 | 22:25:33 | artifact | wrote .git/hooks/update.sample |
| 156 | 22:25:33 | artifact | wrote .git/index |
| 157 | 22:25:33 | artifact | wrote .git/info/exclude |
| 158 | 22:25:33 | integrity_error | refused artifact .git/logs/HEAD: secret pattern(s) assigned-credential |
| 159 | 22:31:48 | command | $ python3 -m unittest discover -s tests |
| 160 | 22:35:02 | command | $ python3 -m unittest discover -s tests |

_110 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-030-run-t-0017-attribute-every-differing-byt/events.jsonl
```
