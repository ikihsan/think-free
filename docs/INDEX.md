# Documentation index

<!-- origin-meta
owner: docs/README.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

Every document in the repository, grouped by zone, with the index that owns it.
Regenerate with `tools/origin doc index`. Policies that govern these documents
are in [`policy/doc-standards.md`](policy/doc-standards.md).

Skill bodies under `.agents/skills/` are indexed by
[`reference/skill-inventory.md`](reference/skill-inventory.md) instead.

## Start here

| Document | Purpose |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Canonical agent contract. Read first. |
| [`../STATE.md`](../STATE.md) | Verified current state and next actions. The reload point. |
| [`../MISSION.md`](../MISSION.md) | Objective, boundaries, stopping rules. |
| [`../RELEASE-MANIFEST.md`](../RELEASE-MANIFEST.md) | What is public and what is internal. |
| [`../README.md`](../README.md) | Human front door. |

## docs/policy

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/policy/evidence-labels.md`](policy/evidence-labels.md) | `docs/INDEX.md` | active | 2026-10-03 | Every claim carries one of these labels. They are not decoration: an unlabelled |
| [`docs/policy/gate-falsification.md`](policy/gate-falsification.md) | `docs/INDEX.md` | active | 2026-10-04 | Split out of STATE-defects.md on 2026-10-04 (T-0042), when adding a defect |
| [`docs/policy/logging-standard.md`](policy/logging-standard.md) | `docs/INDEX.md` | active | 2026-10-03 | What must be recorded, in what form, and what is deliberately exempt. The |
| [`docs/policy/permissions-and-safety.md`](policy/permissions-and-safety.md) | `docs/INDEX.md` | active | 2026-10-03 | What an agent may do without asking, what needs explicit authorization, and |

## docs/process

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/process/experiment-protocol.md`](process/experiment-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | How an experiment is designed, run, and judged. Read this before writing code |
| [`docs/process/hypothesis-lifecycle.md`](process/hypothesis-lifecycle.md) | `docs/INDEX.md` | active | 2026-10-03 | How a candidate becomes a decision. The aim is that no candidate is ever |
| [`docs/process/multi-vm-coordination.md`](process/multi-vm-coordination.md) | `docs/INDEX.md` | active | 2026-10-04 | How several machines share this repository safely. The invariant: git is the |
| [`docs/process/review-protocol.md`](process/review-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | The adversarial step. Its purpose is not to confirm work but to find the reason |
| [`docs/process/session-protocol.md`](process/session-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | Every working session follows these steps. The goal is that a session's record |
| [`docs/process/task-lifecycle.md`](process/task-lifecycle.md) | `docs/INDEX.md` | active | 2026-10-03 | A task is a unit of work another machine can pick up without asking a question. |

## docs/operations

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/operations/bootstrap.md`](operations/bootstrap.md) | `docs/INDEX.md` | active | 2026-10-03 | Getting a fresh machine able to work on this repository. The design goal is that |
| [`docs/operations/ci-diagnosis.md`](operations/ci-diagnosis.md) | `docs/INDEX.md` | active | 2026-10-04 | How to find out which test failed on a pushed commit, without repository admin |
| [`docs/operations/ci.md`](operations/ci.md) | `docs/INDEX.md` | active | 2026-10-04 | Runs on every push and pull request. The gates are the same ones a session must |
| [`docs/operations/doctor.md`](operations/doctor.md) | `docs/INDEX.md` | active | 2026-10-04 | tools/origin doctor answers one question: can this machine do the work a |
| [`docs/operations/github-app.md`](operations/github-app.md) | `docs/INDEX.md` | active | 2026-10-03 | Status: one App exists and authenticates every push. The design below was |
| [`docs/operations/scheduling-and-supervision.md`](operations/scheduling-and-supervision.md) | `docs/INDEX.md` | active | 2026-10-03 | Whether agent work can run unattended, and what has actually been verified. The |
| [`docs/operations/vm-execution.md`](operations/vm-execution.md) | `docs/INDEX.md` | active | 2026-10-03 | How a task gets executed on another machine. The design constraint is that the |

## docs/reference

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/reference/cli-reference.md`](reference/cli-reference.md) | `docs/INDEX.md` | active | 2026-10-04 | Every command the repository's tooling provides. Stdlib Python only, so no |
| [`docs/reference/identifier-allocation.md`](reference/identifier-allocation.md) | `docs/INDEX.md` | active | 2026-10-04 | How an F, D or T number is chosen, and why the choice is recorded. Every number |
| [`docs/reference/skill-inventory.md`](reference/skill-inventory.md) | `docs/INDEX.md` | active | 2026-10-03 | Twenty-one skills in .agents/skills/<name>/SKILL.md, mirrored into |

## sessions

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`sessions/README.md`](../sessions/README.md) | `docs/INDEX.md` | active | 2026-10-03 | The append-only record of every working session in this repository. |

## tasks

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`tasks/README.md`](../tasks/README.md) | `docs/INDEX.md` | active | 2026-10-03 | Dispatchable units of work. One Markdown file per task, each declaring a |
| [`tasks/T-0001-write-falsification-kill-gates-for-the-three-hel.md`](../tasks/T-0001-write-falsification-kill-gates-for-the-three-hel.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0002-run-investigation-e-the-experimental-engineer-ro.md`](../tasks/T-0002-run-investigation-e-the-experimental-engineer-ro.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0003-run-investigation-f-the-adoption-researcher-role.md`](../tasks/T-0003-run-investigation-f-the-adoption-researcher-role.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md`](../tasks/T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md`](../tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md`](../tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md`](../tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md`](../tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0009-repair-the-knitting-witness-input-set-by-adding.md`](../tasks/T-0009-repair-the-knitting-witness-input-set-by-adding.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0010-run-the-knitting-stage-a-planner-comparison-loca.md`](../tasks/T-0010-run-the-knitting-stage-a-planner-comparison-loca.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md`](../tasks/T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md`](../tasks/T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0013-run-e3-s-build-timestamp-census-over-200-recent.md`](../tasks/T-0013-run-e3-s-build-timestamp-census-over-200-recent.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md`](../tasks/T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0015-run-the-knitting-candidate-s-remaining-kill-gate.md`](../tasks/T-0015-run-the-knitting-candidate-s-remaining-kill-gate.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0016-make-the-test-suite-pass-on-the-ci-runner-s-pyth.md`](../tasks/T-0016-make-the-test-suite-pass-on-the-ci-runner-s-pyth.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0017-build-one-source-twice-under-different-source-da.md`](../tasks/T-0017-build-one-source-twice-under-different-source-da.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0018-record-exercised-git-versions-machine-readably-a.md`](../tasks/T-0018-record-exercised-git-versions-machine-readably-a.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0019-snapshot-side-a-of-the-e2-dependency-closure-dri.md`](../tasks/T-0019-snapshot-side-a-of-the-e2-dependency-closure-dri.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0020-tell-an-in-flight-session-apart-from-an-abandone.md`](../tasks/T-0020-tell-an-in-flight-session-apart-from-an-abandone.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0021-resolve-the-merge-conflict-markers-committed-to.md`](../tasks/T-0021-resolve-the-merge-conflict-markers-committed-to.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0022-implement-origin-release-check-so-release-manife.md`](../tasks/T-0022-implement-origin-release-check-so-release-manife.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0023-repair-the-two-operations-documents-whose-stated.md`](../tasks/T-0023-repair-the-two-operations-documents-whose-stated.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0024-stop-session-reconciliation-and-the-documentatio.md`](../tasks/T-0024-stop-session-reconciliation-and-the-documentatio.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0025-record-the-measured-result-of-the-pushed-ci-run.md`](../tasks/T-0025-record-the-measured-result-of-the-pushed-ci-run.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0026-make-task-new-leave-no-orphan-a-new-task-file-re.md`](../tasks/T-0026-make-task-new-leave-no-orphan-a-new-task-file-re.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0027-make-the-published-claim-commit-carry-the-regene.md`](../tasks/T-0027-make-the-published-claim-commit-carry-the-regene.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0028-record-the-ci-run-history-around-the-orphan-fix.md`](../tasks/T-0028-record-the-ci-run-history-around-the-orphan-fix.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0029-make-origin-doctor-report-the-push-credential-me.md`](../tasks/T-0029-make-origin-doctor-report-the-push-credential-me.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0030-refuse-a-commit-that-gives-one-finding-decision.md`](../tasks/T-0030-refuse-a-commit-that-gives-one-finding-decision.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0031-allocate-f-d-and-t-identifiers-from-the-shared-b.md`](../tasks/T-0031-allocate-f-d-and-t-identifiers-from-the-shared-b.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0032-record-the-python-versions-the-suite-has-actuall.md`](../tasks/T-0032-record-the-python-versions-the-suite-has-actuall.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0033-make-doctor-compare-this-vm-s-git-and-interprete.md`](../tasks/T-0033-make-doctor-compare-this-vm-s-git-and-interprete.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0034-run-the-test-suite-on-the-python-versions-tests.md`](../tasks/T-0034-run-the-test-suite-on-the-python-versions-tests.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0035-stop-the-credential-sandbox-from-inheriting-a-ci.md`](../tasks/T-0035-stop-the-credential-sandbox-from-inheriting-a-ci.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0036-report-a-duplicate-defect-number-in-state-defect.md`](../tasks/T-0036-report-a-duplicate-defect-number-in-state-defect.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0037-explain-the-four-red-ci-runs-since-the-version-m.md`](../tasks/T-0037-explain-the-four-red-ci-runs-since-the-version-m.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0038-record-that-the-public-check-run-annotations-wer.md`](../tasks/T-0038-record-that-the-public-check-run-annotations-wer.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md`](../tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0040-make-a-red-doc-lint-release-check-or-skills-gate.md`](../tasks/T-0040-make-a-red-doc-lint-release-check-or-skills-gate.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0041-make-sync-land-rebuild-any-generated-file-the-re.md`](../tasks/T-0041-make-sync-land-rebuild-any-generated-file-the-re.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0042-report-a-decision-file-whose-own-header-disagree.md`](../tasks/T-0042-report-a-decision-file-whose-own-header-disagree.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0043-split-tools-originlib-identifiers-py-so-doc-lint.md`](../tasks/T-0043-split-tools-originlib-identifiers-py-so-doc-lint.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0044-date-the-lease-tests-from-the-clock-the-code-act.md`](../tasks/T-0044-date-the-lease-tests-from-the-clock-the-code-act.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0045-run-release-check-from-preflight-and-classify-de.md`](../tasks/T-0045-run-release-check-from-preflight-and-classify-de.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0046-measure-how-github-files-an-annotation-on-the-fi.md`](../tasks/T-0046-measure-how-github-files-an-annotation-on-the-fi.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0047-attribute-a-task-file-that-a-task-command-rewrot.md`](../tasks/T-0047-attribute-a-task-file-that-a-task-command-rewrot.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0048-teach-sync-land-to-finish-a-paused-rebase-whose.md`](../tasks/T-0048-teach-sync-land-to-finish-a-paused-rebase-whose.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0049-record-the-measured-ci-state-on-the-tip-and-the.md`](../tasks/T-0049-record-the-measured-ci-state-on-the-tip-and-the.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md`](../tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md`](../tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md`](../tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0053-record-a-base-advance-when-a-paused-rebase-is-co.md`](../tasks/T-0053-record-a-base-advance-when-a-paused-rebase-is-co.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0054-measure-every-commit-on-the-base-branch-that-red.md`](../tasks/T-0054-measure-every-commit-on-the-base-branch-that-red.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0055-publish-a-task-claim-from-inside-an-open-session.md`](../tasks/T-0055-publish-a-task-claim-from-inside-an-open-session.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0056-hold-a-mission-record-s-restated-experiment-numb.md`](../tasks/T-0056-hold-a-mission-record-s-restated-experiment-numb.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0057-make-the-ci-failure-annotation-carry-the-excepti.md`](../tasks/T-0057-make-the-ci-failure-annotation-carry-the-excepti.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0058-test-whether-flat-adoption-is-general-or-niche-s.md`](../tasks/T-0058-test-whether-flat-adoption-is-general-or-niche-s.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md`](../tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md`](../tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0061-test-whether-a-prior-art-screen-s-population-in.md`](../tasks/T-0061-test-whether-a-prior-art-screen-s-population-in.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md`](../tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md) | `tasks/INDEX.md` | active | 2026-10-04 | ## Goal |
| [`tasks/T-0063-test-whether-f033-s-project-level-denominator-hi.md`](../tasks/T-0063-test-whether-f033-s-project-level-denominator-hi.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |

## RESEARCH

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`RESEARCH/A.md`](../RESEARCH/A.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/B.md`](../RESEARCH/B.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/C.md`](../RESEARCH/C.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/D.md`](../RESEARCH/D.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/E.md`](../RESEARCH/E.md) | `RESEARCH.md` | sealed | 2026-10-03 | Independent report. Written 2026-10-03 after reading MISSION.md only. The |
| [`RESEARCH/EXPERIMENT-PROTOCOL.md`](../RESEARCH/EXPERIMENT-PROTOCOL.md) | `docs/process/experiment-protocol.md` | archived | 2026-10-03 | The canonical text is now |
| [`RESEARCH/F.md`](../RESEARCH/F.md) | `RESEARCH.md` | sealed | 2026-10-03 | Independent report. Written 2026-10-03 after reading MISSION.md only; |
| [`RESEARCH/PRIOR-ART-KNITTING.md`](../RESEARCH/PRIOR-ART-KNITTING.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/PRIOR-ART-ORIGIN.md`](../RESEARCH/PRIOR-ART-ORIGIN.md) | `RESEARCH.md` | sealed | 2026-10-04 | Written 2026-10-04, session 2026-10-04-045. Follows the method of |
| [`RESEARCH/README.md`](../RESEARCH/README.md) | `RESEARCH.md` | active | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/ROOT-SCOUTING.md`](../RESEARCH/ROOT-SCOUTING.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/SYNTHESIS.md`](../RESEARCH/SYNTHESIS.md) | `RESEARCH.md` | active | 2026-10-03 | owner: RESEARCH.md |

## EXPERIMENTS

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`EXPERIMENTS/000-capabilities/README.md`](../EXPERIMENTS/000-capabilities/README.md) | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/001-photo-baseline/README.md`](../EXPERIMENTS/001-photo-baseline/README.md) | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/002-a1-masking/README.md`](../EXPERIMENTS/002-a1-masking/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Bounded A1 masking experiment over the PPNA Seattle crossings extract. |
| [`EXPERIMENTS/003-information-sufficiency/README.md`](../EXPERIMENTS/003-information-sufficiency/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Applies the information-sufficiency witness (the cheap pre-implementation gate in |
| [`EXPERIMENTS/004-knitting-stage-a/README.md`](../EXPERIMENTS/004-knitting-stage-a/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | The knitting repair candidate's own Stage-A test (HYPOTHESES.md): does a cheap |
| [`EXPERIMENTS/005-knitting-bounded-search/README.md`](../EXPERIMENTS/005-knitting-bounded-search/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Follow-up to EXPERIMENTS/004-knitting-stage-a (T-0010), testing the repair |
| [`EXPERIMENTS/006-ventilation-measurement-design/README.md`](../EXPERIMENTS/006-ventilation-measurement-design/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | RESEARCH/C.md hypothesis 2, run as its own predeclared kill gate (T-0014). |
| [`EXPERIMENTS/007-build-timestamps/README.md`](../EXPERIMENTS/007-build-timestamps/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | E3's build-timestamp census: RESEARCH/E.md's smallest falsifying experiment |
| [`EXPERIMENTS/008-build-timestamp-attribution/README.md`](../EXPERIMENTS/008-build-timestamp-attribution/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Task T-0017. The second half of E3's own falsifying experiment: build the same |
| [`EXPERIMENTS/009-lockfile-drift-snapshot/README.md`](../EXPERIMENTS/009-lockfile-drift-snapshot/README.md) | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| [`EXPERIMENTS/010-annotation-rendering/README.md`](../EXPERIMENTS/010-annotation-rendering/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-04 | Task T-0046. Does GitHub file a check-run annotation on the workflow command's |
| [`EXPERIMENTS/011-niche-adoption-census/README.md`](../EXPERIMENTS/011-niche-adoption-census/README.md) | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| [`EXPERIMENTS/012-candidate-harvest/README.md`](../EXPERIMENTS/012-candidate-harvest/README.md) | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| [`EXPERIMENTS/013-prior-art-predicts-adoption/README.md`](../EXPERIMENTS/013-prior-art-predicts-adoption/README.md) | `docs/INDEX.md` | active | 2026-10-04 | F027 and F028 counted stars. This counts installs, because "does prior |
| [`EXPERIMENTS/014-repository-signal-filter/README.md`](../EXPERIMENTS/014-repository-signal-filter/README.md) | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| [`EXPERIMENTS/015-incumbent-serving/README.md`](../EXPERIMENTS/015-incumbent-serving/README.md) | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| [`EXPERIMENTS/016-prior-art-adjudication/README.md`](../EXPERIMENTS/016-prior-art-adjudication/README.md) | `docs/INDEX.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| [`EXPERIMENTS/017-incumbent-artifact-type/PROTOCOL.md`](../EXPERIMENTS/017-incumbent-artifact-type/PROTOCOL.md) | `EXPERIMENTS/017-incumbent-artifact-type/README.md` | active | 2026-10-05 | owner: EXPERIMENTS/017-incumbent-artifact-type/README.md |
| [`EXPERIMENTS/017-incumbent-artifact-type/README.md`](../EXPERIMENTS/017-incumbent-artifact-type/README.md) | `docs/INDEX.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| [`EXPERIMENTS/018-runtime-signal-selection/README.md`](../EXPERIMENTS/018-runtime-signal-selection/README.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/PLAN.md`](../EXPERIMENTS/PLAN.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/README.md`](../EXPERIMENTS/README.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |

## Generated maps

| Map | Purpose |
|---|---|
| `docs/INDEX.md` | This map. |
| `sessions/INDEX.md` | Every recorded session and its outcome. |
| `tasks/INDEX.md` | Dispatchable tasks and their claims. |

## Adding a document

1. Give it an `origin-meta` block with its owning index.
2. Link it from exactly one index; orphans fail `doc lint`.
3. Keep it under 300 lines. Split at 250.
