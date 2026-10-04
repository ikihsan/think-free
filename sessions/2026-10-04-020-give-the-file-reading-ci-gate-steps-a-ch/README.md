# Session 2026-10-04-020-give-the-file-reading-ci-gate-steps-a-ch

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T07:35:57+00:00
- **Duration:** 8330.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Give the file-reading CI gate steps a check-run annotation that names the violating file, and split DECISIONS-GATING.md so the decision has a home

## Summary

T-0040: every file-reading CI gate step now re-emits each violation as a check-run annotation naming the file. A violation carries the location its own rule knows (tools/originlib/finding.py) and 'origin annotate -- <gate>' publishes it; all five steps run it. Falsified against e53ca23's real bytes in both directions - the present command emits zero :: lines there and the new one emits file=STATE-defects.md, while on this tip both emit none - with the first run failing its own kill gate by dropping the location when it prefixed the message. doclint.py was split into doclint_tree.py by what a rule may read, at the 300-line cap. Two more defects came out of running the code rather than reading it: the workflow's awk escaped % wrongly, and four CLI handlers raised a Usage they had never imported; both are folded into defect 17 because STATE-defects.md has one line of room. 474 tests green, doc lint and preflight exit 0.

## Next

The gating decision for T-0040 is owed and could not be written: DECISIONS-GATING.md took its split and D036 in T-0042, so the prose lives in docs/operations/ci.md and the log entry waits for room. Whether GitHub honours the file= property is still unmeasured - run 37189825232 came back with path=.github - so the claim is that the location reaches the reader. A one-line variant of the lease-test clock fix (T-0046) was withdrawn unpublished because T-0044 solved the same defect better.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/annotate.py | e0380d394ea6 | 5757 |
| tools/originlib/finding.py | a1c8ffe6bc24 | 6779 |
| tools/originlib/doclint_tree.py | 425fedfad9b6 | 6116 |
| tools/originlib/usage.py | 3b56bb8c8f32 | 854 |
| tests/test_annotate.py | f595bfe0613e | 12906 |
| tests/test_ci_annotations.py | 0b094b72f71c | 6028 |
| tasks/T-0040-make-a-red-doc-lint-release-check-or-skills-gate.md | 0884f9d83a23 | 6229 |
| .github/workflows/ci.yml | 3a8a85f8c020 | 5318 |
| docs/operations/ci-diagnosis.md | 50b16220a2db | 6543 |
| tools/originlib/annotate.py | e0380d394ea6 | 5757 |
| tools/originlib/finding.py | a1c8ffe6bc24 | 6779 |
| tools/originlib/doclint_tree.py | 425fedfad9b6 | 6116 |
| tools/originlib/usage.py | 3b56bb8c8f32 | 854 |
| tests/test_annotate.py | f595bfe0613e | 12906 |
| tests/test_ci_annotations.py | 0b094b72f71c | 6028 |
| docs/operations/ci-diagnosis.md | fea91cbc992e | 7253 |

## Commands

10 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', 'cd /tmp/opencode/e53ca23 && ./tools/origin doc lint; echo "EXIT=$?"'] | 0 | 494 |
| 3 | ['bash', '-c', 'cd /tmp/opencode/wt-e53ca23 && ./tools/origin doc lint > /tmp/opencode/baseline-e53ca23.txt 2>&1; echo "EXIT=$?"; grep -c "::error" /t | 0 | 1877 |
| 4 | ['bash', '-c', 'cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib doc  | 1 | 1814 |
| 5 | ['bash', '-c', 'cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib anno | 0 | 2415 |
| 6 | ['bash', '-c', 'cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib anno | 0 | 1786 |
| 7 | ['bash', '-c', 'cd /tmp/opencode/wt-e53ca23 && export ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools; for g in "release | 0 | 5300 |
| 8 | ['bash', '-c', 'cd /tmp/opencode/wt-plant && ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib annotate | 0 | 2304 |
| 9 | ['bash', '-c', 'cd /tmp/opencode/wt-plant && ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib annotate | 0 | 2606 |
| 10 | ['bash', '-c', 'cd /tmp/opencode/wt-plant && export ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools; echo "### doc lint on | 1 | 6720 |
| 12 | ['tools/origin', 'task', 'verify', 'T-0040'] | 0 | 217687 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 50 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .agents/skills/task-execution/SKILL.md |
|   undeclared | AGENTS.md |
|   undeclared | DECISIONS-GATING.md |
|   undeclared | DECISIONS-PRACTICE.md |
|   undeclared | DECISIONS-RECORDS.md |
|   undeclared | DECISIONS.md |
|   undeclared | README.md |
|   undeclared | RELEASE-MANIFEST.md |
|   undeclared | ROADMAP.md |
|   undeclared | STATE-defects.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 07:35:57 | session_start | Give the file-reading CI gate steps a check-run annotation that names the violating file, and split DECISIONS-GATING.md so the decision has a home |
| 2 | 07:41:06 | command | $ bash -c cd /tmp/opencode/e53ca23 && ./tools/origin doc lint; echo "EXIT=$?" |
| 3 | 07:41:23 | command | $ bash -c cd /tmp/opencode/wt-e53ca23 && ./tools/origin doc lint > /tmp/opencode/baseline-e53ca23.txt 2>&1; echo "EXIT=$?"; grep -c "::error" |
| 4 | 07:41:39 | command | $ bash -c cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib do |
| 5 | 08:01:20 | command | $ bash -c cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib an |
| 6 | 08:01:44 | command | $ bash -c cd /tmp/opencode/wt-e53ca23 && ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib an |
| 7 | 08:02:01 | command | $ bash -c cd /tmp/opencode/wt-e53ca23 && export ORIGIN_ROOT=/tmp/opencode/wt-e53ca23 PYTHONPATH=/home/ubuntu/think-free/tools; for g in "relea |
| 8 | 08:02:22 | command | $ bash -c cd /tmp/opencode/wt-plant && ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib annota |
| 9 | 08:03:06 | command | $ bash -c cd /tmp/opencode/wt-plant && ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools python3 -m originlib annota |
| 10 | 08:05:10 | command | $ bash -c cd /tmp/opencode/wt-plant && export ORIGIN_ROOT=/tmp/opencode/wt-plant PYTHONPATH=/home/ubuntu/think-free/tools; echo "### doc lint |
| 11 | 08:23:01 | base_advance | sync land: base moved c5edfe0fe8f1 -> 24f67f43944f, 13 commit(s) arrived from the shared base |
| 12 | 08:47:13 | command | $ tools/origin task verify T-0040 |
| 13 | 08:47:28 | milestone | annotations verified on the defect's own bytes; docs updated; 452 tests green |
| 14 | 08:47:29 | artifact | wrote tools/originlib/annotate.py |
| 15 | 08:47:29 | artifact | wrote tools/originlib/finding.py |
| 16 | 08:47:29 | artifact | wrote tools/originlib/doclint_tree.py |
| 17 | 08:47:29 | artifact | wrote tools/originlib/usage.py |
| 18 | 08:47:29 | artifact | wrote tests/test_annotate.py |
| 19 | 08:47:29 | artifact | wrote tests/test_ci_annotations.py |
| 20 | 08:47:29 | artifact | wrote tasks/T-0040-make-a-red-doc-lint-release-check-or-skills-gate.md |
| 21 | 08:47:30 | artifact | wrote .github/workflows/ci.yml |
| 22 | 08:47:30 | artifact | wrote docs/operations/ci-diagnosis.md |
| 23 | 09:04:41 | note | Base carries a red doc lint and 7 red tests: tools/originlib/identifiers.py is 306 lines on origin/research/origin, over the 300-line cap, so every fi |
| 24 | 09:54:09 | artifact | wrote tools/originlib/annotate.py |
| 25 | 09:54:09 | artifact | wrote tools/originlib/finding.py |
| 26 | 09:54:09 | artifact | wrote tools/originlib/doclint_tree.py |
| 27 | 09:54:09 | artifact | wrote tools/originlib/usage.py |
| 28 | 09:54:09 | artifact | wrote tests/test_annotate.py |
| 29 | 09:54:09 | artifact | wrote tests/test_ci_annotations.py |
| 30 | 09:54:09 | artifact | wrote docs/operations/ci-diagnosis.md |
| 31 | 09:54:10 | note | T-0046 was created and then cancelled unpublished: the same wall-clock time bomb was already solved on instance-20260717-0947 as defect 15 in T-0044,  |
| 32 | 09:54:46 | unlogged_change | changed but never declared as an artifact: .agents/skills/task-execution/SKILL.md |
| 33 | 09:54:46 | unlogged_change | changed but never declared as an artifact: AGENTS.md |
| 34 | 09:54:46 | unlogged_change | changed but never declared as an artifact: DECISIONS-GATING.md |
| 35 | 09:54:46 | unlogged_change | changed but never declared as an artifact: DECISIONS-PRACTICE.md |
| 36 | 09:54:46 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS.md |
| 37 | 09:54:46 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 38 | 09:54:46 | unlogged_change | changed but never declared as an artifact: README.md |
| 39 | 09:54:46 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 40 | 09:54:46 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 79 | 09:54:46 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 80 | 09:54:46 | unlogged_change | changed but never declared as an artifact: tools/originlib/release.py |
| 81 | 09:54:46 | unlogged_change | changed but never declared as an artifact: tools/originlib/skillsync.py |
| 82 | 09:54:46 | doc_update | updated DECISIONS-GATING.md |
| 83 | 09:54:46 | doc_update | updated DECISIONS-PRACTICE.md |
| 84 | 09:54:46 | doc_update | updated DECISIONS-RECORDS.md |
| 85 | 09:54:46 | doc_update | updated DECISIONS.md |
| 86 | 09:54:47 | doc_update | updated ROADMAP.md |
| 87 | 09:54:47 | doc_update | updated STATE.md |
| 88 | 09:54:47 | session_end | T-0040: every file-reading CI gate step now re-emits each violation as a check-run annotation naming the file. A violation carries the location its ow |

_38 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-020-give-the-file-reading-ci-gate-steps-a-ch/events.jsonl
```
