# Documentation index

<!-- origin-meta
owner: docs/README.md
status: active
last-verified: 2026-10-11
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

## docs (other)

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/2026-10-06-strongest-shell-baseline.md`](2026-10-06-strongest-shell-baseline.md) | `docs/INDEX.md` | active | 2026-10-06 | > For agentic workers: This is an experiment plan, not a product implementation. It follows the  |
| [`docs/METHODOLOGY-SUMMARY.md`](METHODOLOGY-SUMMARY.md) | `docs/INDEX.md` | active | 2026-10-07 | A concise synthesis of patterns across all closed invention claims in this repository. |

## sessions

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`sessions/2026-10-07-013-land-e049-evidence-from-sessions-011-012/SESSION-SUMMARY.md`](../sessions/2026-10-07-013-land-e049-evidence-from-sessions-011-012/SESSION-SUMMARY.md) | `docs/INDEX.md` | stale | 2026-10-08 | Date: 2026-10-07 |
| [`sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/DEDUPE-008.md`](../sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/DEDUPE-008.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session 2026-10-08-013, VM instance-20260717-0944, 2026-10-08. Defect 24. |
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
| [`tasks/T-0064-measure-whether-the-young-vocabulary-s-artifacts.md`](../tasks/T-0064-measure-whether-the-young-vocabulary-s-artifacts.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0065-test-whether-agent-configuration-copied-into-rep.md`](../tasks/T-0065-test-whether-agent-configuration-copied-into-rep.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0066-measure-what-happens-to-a-publicly-stated-unmet.md`](../tasks/T-0066-measure-what-happens-to-a-publicly-stated-unmet.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0067-falsify-e022-s-38-5-served-figure-against-a-cont.md`](../tasks/T-0067-falsify-e022-s-38-5-served-figure-against-a-cont.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0068-classify-what-killed-each-candidate-from-its-p.md`](../tasks/T-0068-classify-what-killed-each-candidate-from-its-p.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0069-measure-whether-the-people-who-publicly-stated-a.md`](../tasks/T-0069-measure-whether-the-people-who-publicly-stated-a.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0070-classify-the-589-never-answered-need-statements.md`](../tasks/T-0070-classify-the-589-never-answered-need-statements.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0071-re-read-the-31-clause-killed-harvested-needs-fro.md`](../tasks/T-0071-re-read-the-31-clause-killed-harvested-needs-fro.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md`](../tasks/T-0072-test-whether-the-incumbents-a-prior-art-screen-n.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0073-test-whether-the-need-staters-who-publicly-shipp.md`](../tasks/T-0073-test-whether-the-need-staters-who-publicly-shipp.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0074-e030-test-whether-departure-accounts-people-publ.md`](../tasks/T-0074-e030-test-whether-departure-accounts-people-publ.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0075-e031-test-whether-public-accounts-of-leaving-a-n.md`](../tasks/T-0075-e031-test-whether-public-accounts-of-leaving-a-n.md) | `tasks/INDEX.md` | active | 2026-10-05 | ## Goal |
| [`tasks/T-0076-e032-test-whether-the-mission-s-three-zero-recur.md`](../tasks/T-0076-e032-test-whether-the-mission-s-three-zero-recur.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0077-e033-measure-the-rate-at-which-a-question-in-pub.md`](../tasks/T-0077-e033-measure-the-rate-at-which-a-question-in-pub.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0078-e034-test-whether-stack-exchange-questions-close.md`](../tasks/T-0078-e034-test-whether-stack-exchange-questions-close.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0079-e035-establish-whether-the-score-tail-population.md`](../tasks/T-0079-e035-establish-whether-the-score-tail-population.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md`](../tasks/T-0080-e036-test-whether-stack-overflow-s-own-search-bo.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0081-measure-what-happened-to-e012-s-1401-pub.md`](../tasks/T-0081-measure-what-happened-to-e012-s-1401-pub.md) | `tasks/INDEX.md` | active | 2026-10-06 | ## Goal |
| [`tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md`](../tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md) | `tasks/INDEX.md` | active | 2026-10-07 | # corpus needs three repositories, two of them clones, and a verify step that |
| [`tasks/T-0083-e045-read-the-demand-evidence-the-candidate.md`](../tasks/T-0083-e045-read-the-demand-evidence-the-candidate.md) | `tasks/INDEX.md` | active | 2026-10-07 | ## Goal |
| [`tasks/T-0084-test-with-a-byte-level-oracle-whether-any-shippe.md`](../tasks/T-0084-test-with-a-byte-level-oracle-whether-any-shippe.md) | `tasks/INDEX.md` | active | 2026-10-07 | ## Goal |
| [`tasks/T-0085-e2-measure-whether-dependency-lockfile-closures.md`](../tasks/T-0085-e2-measure-whether-dependency-lockfile-closures.md) | `tasks/INDEX.md` | active | 2026-10-07 | ## Goal |
| [`tasks/T-0086-e2-registry-mechanisms-a-re-run-e049-part-b-cont.md`](../tasks/T-0086-e2-registry-mechanisms-a-re-run-e049-part-b-cont.md) | `tasks/INDEX.md` | active | 2026-10-07 | ## Goal |
| [`tasks/T-0087-e055-build-a-tool-neutral-git-index-postconditio.md`](../tasks/T-0087-e055-build-a-tool-neutral-git-index-postconditio.md) | `tasks/INDEX.md` | active | 2026-10-08 | ## Goal |
| [`tasks/T-0088-e086-measure-whether-real-python-import-error-re.md`](../tasks/T-0088-e086-measure-whether-real-python-import-error-re.md) | `tasks/INDEX.md` | active | 2026-10-10 | ## Goal |
| [`tasks/T-0089-e090-measure-whether-a-module-to-distribution-re.md`](../tasks/T-0089-e090-measure-whether-a-module-to-distribution-re.md) | `tasks/INDEX.md` | active | 2026-10-10 | ## Goal |

## RESEARCH

| Directory | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| `RESEARCH/A.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/B.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/C.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/D.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/E.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/EXPERIMENT-PROTOCOL.md/` | `docs/process/experiment-protocol.md` | archived | 2026-10-03 | 1 documents |
| `RESEARCH/F.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/PRIOR-ART-E065-E066-E067.md/` | `docs/INDEX.md` | active | 2026-10-08 | 1 documents |
| `RESEARCH/PRIOR-ART-KNITTING.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/PRIOR-ART-ORIGIN.md/` | `RESEARCH.md` | sealed | 2026-10-04 | 1 documents |
| `RESEARCH/README.md/` | `RESEARCH.md` | active | 2026-10-03 | owner: RESEARCH.md |
| `RESEARCH/ROOT-SCOUTING.md/` | `RESEARCH.md` | sealed | 2026-10-03 | 1 documents |
| `RESEARCH/SYNTHESIS.md/` | `RESEARCH.md` | active | 2026-10-03 | 1 documents |

## EXPERIMENTS

| Directory | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| `EXPERIMENTS/000-capabilities/` | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/001-photo-baseline/` | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/002-a1-masking/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | Bounded A1 masking experiment over the PPNA Seattle crossings extract. |
| `EXPERIMENTS/003-information-sufficiency/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | Applies the information-sufficiency witness (the cheap pre-implementation gate in |
| `EXPERIMENTS/004-knitting-stage-a/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | The knitting repair candidate's own Stage-A test (HYPOTHESES.md): does a cheap |
| `EXPERIMENTS/005-knitting-bounded-search/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | Follow-up to EXPERIMENTS/004-knitting-stage-a (T-0010), testing the repair |
| `EXPERIMENTS/006-ventilation-measurement-design/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | RESEARCH/C.md hypothesis 2, run as its own predeclared kill gate (T-0014). |
| `EXPERIMENTS/007-build-timestamps/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | E3's build-timestamp census: RESEARCH/E.md's smallest falsifying experiment |
| `EXPERIMENTS/008-build-timestamp-attribution/` | `EXPERIMENTS/README.md` | active | 2026-10-03 | Task T-0017. The second half of E3's own falsifying experiment: build the same |
| `EXPERIMENTS/009-lockfile-drift-snapshot/` | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| `EXPERIMENTS/010-annotation-rendering/` | `EXPERIMENTS/README.md` | active | 2026-10-04 | Task T-0046. Does GitHub file a check-run annotation on the workflow command's |
| `EXPERIMENTS/011-niche-adoption-census/` | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| `EXPERIMENTS/012-candidate-harvest/` | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| `EXPERIMENTS/013-prior-art-predicts-adoption/` | `docs/INDEX.md` | active | 2026-10-04 | F027 and F028 counted stars. This counts installs, because "does prior |
| `EXPERIMENTS/014-repository-signal-filter/` | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| `EXPERIMENTS/015-incumbent-serving/` | `docs/INDEX.md` | active | 2026-10-04 | owner: docs/INDEX.md |
| `EXPERIMENTS/016-prior-art-adjudication/` | `docs/INDEX.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| `EXPERIMENTS/017-incumbent-artifact-type/` | `EXPERIMENTS/017-incumbent-artifact-type/README.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| `EXPERIMENTS/018-runtime-signal-selection/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/019-corpus-person-diversity/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/020-copied-config-drift/` | `docs/INDEX.md` | active | 2026-10-05 | Date: 2026-10-05. Verdict: inconclusive, and two figures retracted. |
| `EXPERIMENTS/021-copied-artifact-serving/` | `EXPERIMENTS/021-copied-artifact-serving/README.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| `EXPERIMENTS/022-need-outcomes/` | `docs/INDEX.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| `EXPERIMENTS/023-served-baseline/` | `docs/INDEX.md` | active | 2026-10-05 | owner: docs/INDEX.md |
| `EXPERIMENTS/024-kill-reason-causes/` | `docs/INDEX.md` | active | 2026-10-05 | Date: 2026-10-05. T-0068. The declaration was written before any row was |
| `EXPERIMENTS/025-need-staters-builderhood/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | Date: 2026-10-05. Task T-0069. Protocol written before the first fetch: |
| `EXPERIMENTS/026-unserved-need-structure/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/027-cause-of-death-reread/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/028-incumbent-fit/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | Date: 2026-10-05. Task T-0072. Protocol declared before any label and |
| `EXPERIMENTS/029-need-build-match/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | Date: 2026-10-05. Task |
| `EXPERIMENTS/030-departure-recurrence/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | Date: 2026-10-05. Task T-0074. Protocol declared in |
| `EXPERIMENTS/031-unfilled-requirement/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/032-venue-recurrence/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/033-question-recurrence/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/034-reask-tail/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/035-unanswered-surface/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-004, VM instance-20260717-0944. Protocol: |
| `EXPERIMENTS/036-search-backlog/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-005, VM instance-20260717-0944, 8 requests |
| `EXPERIMENTS/037-line-staging/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-006, VM instance-20260717-0944, git 2.25.1, |
| `EXPERIMENTS/038-staging-prior-art/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-009, VM instance-20260717-0944, git 2.25.1, |
| `EXPERIMENTS/039-honest-exit/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | Date: 2026-10-06. Status: complete. Verdict: the claim holds on all eight |
| `EXPERIMENTS/039-need-statement-response/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-05 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/040-agent-staging-loop/` | `docs/INDEX.md` | active | 2026-10-06 | E037 measured the interface cost of git add -p (a 133-line pty driver, 4 of 6); |
| `EXPERIMENTS/041-need-index/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | control terms |
| `EXPERIMENTS/041-strongest-baseline/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-013, VM instance-20260717-0944, git 2.25.1, |
| `EXPERIMENTS/042-agent-staging-e2e/` | `docs/INDEX.md` | active | 2026-10-06 | owner: docs/INDEX.md |
| `EXPERIMENTS/042-stg-end-to-end/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-06 | observed 2026-10-06, session 2026-10-06-014, VM instance-20260717-0944, git 2.25.1, |
| `EXPERIMENTS/043-real-agent-staging/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-07 | observed 2026-10-07, session 2026-10-07-001, VM instance-20260717-0944, git 2.25.1, |
| `EXPERIMENTS/044-discover-staging/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-07 | observed 2026-10-07, session 2026-10-07-002, VM instance-20260717-0944, |
| `EXPERIMENTS/045-demand-evidence/` | `docs/INDEX.md` | complete | 2026-10-07 | owner: docs/INDEX.md |
| `EXPERIMENTS/046-real-changes/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-07 | observed 2026-10-07, session 2026-10-06-016, VM instance-20260717-0947, |
| `EXPERIMENTS/047-hook-partial-stage/` | `docs/INDEX.md` | complete | 2026-10-07 | Task T-0084. Corpus for the question: two rows of the 189-row demand corpus |
| `EXPERIMENTS/048-formatter-review/` | `docs/INDEX.md` | complete | 2026-10-07 | Task T-0084's follow-on. E047 measured what the shipped hook runners do to |
| `EXPERIMENTS/049-lockfile-closure/` | `docs/INDEX.md` | complete | 2026-10-07 | T-0085. E2's claim: a lockfile is a weak witness of reproducibility because |
| `EXPERIMENTS/050-registry-mechanisms/` | `docs/INDEX.md` | complete | 2026-10-07 | T-0086. E049 measured that 10 of 11 lockfile closures |
| `EXPERIMENTS/051-claim-contradiction/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-07 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/052-task-prioritization/` | `EXPERIMENTS/052-task-prioritization` | active | 2026-10-07 | owner: EXPERIMENTS/052-task-prioritization |
| `EXPERIMENTS/053-financial-reconciliation/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-07 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/054-lockfile-artifact-fidelity/` | `docs/INDEX.md` | complete | 2026-10-08 | owner: docs/INDEX.md |
| `EXPERIMENTS/055-index-postcondition/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Task T-0087. Protocol PROTOCOL.md and its three declared amendments; raw |
| `EXPERIMENTS/056-docs-cli-drift/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | (Renumbered from E055 on 2026-10-08: the public remote had already |
| `EXPERIMENTS/057-unserved-step/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | observed 2026-10-08, session 2026-10-08-005, VM instance-20260717-0947. |
| `EXPERIMENTS/058-se-remaining-sites/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | # step appear there? |
| `EXPERIMENTS/059-install-import-mismatch/` | `EXPERIMENTS/PLAN.md` | complete | 2026-10-08 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/060-badge-release-drift/` | `EXPERIMENTS/PLAN.md` | complete | 2026-10-08 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/061-no-run-worklist/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | observed 2026-10-08, session 2026-10-08-005, VM instance-20260717-0944, |
| `EXPERIMENTS/061-supplement-drug-adulteration/` | `EXPERIMENTS/PLAN.md` | complete | 2026-10-08 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/062-nonsw-need-shape/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session 2026-10-08-006, VM instance-20260717-0944, declared 2026-10-08. |
| `EXPERIMENTS/062-package-importability/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | 1 documents |
| `EXPERIMENTS/063-own-corpus-answerability/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session 2026-10-08-013, VM instance-20260717-0944, declared 2026-10-08. |
| `EXPERIMENTS/063-text-organization/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | 1 documents |
| `EXPERIMENTS/064-remedy-existence/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session 2026-10-08-014, VM instance-20260717-0944, declared |
| `EXPERIMENTS/064-serialization-effectiveness/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | 1 documents |
| `EXPERIMENTS/065-recurring-expense-detection/` | `docs/INDEX.md` | complete | 2026-10-08 | ## Experiment Summary |
| `EXPERIMENTS/065-view-count-prototype/` | `docs/INDEX.md` | active | 2026-10-08 | 1 documents |
| `EXPERIMENTS/066-berka-real-validation/` | `docs/INDEX.md` | active | 2026-10-08 | Date: 2026-10-08 · Status: complete — all four predeclared gates PASS |
| `EXPERIMENTS/066-need-answerability/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session: 2026-10-08-021, VM instance-20260717-0944, declared 2026-10-08. |
| `EXPERIMENTS/067-arxiv-code-repro/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Status: Complete (kill gates passed, candidate viable) |
| `EXPERIMENTS/067-viewcount-framework/` | `docs/INDEX.md` | active | 2026-10-08 | Status: Prototype. Core measurement engine implemented and verified against E062's non-software  |
| `EXPERIMENTS/067b-did-you-mean-test/` | `docs/INDEX.md` | complete | 2026-10-09 | Date: 2026-10-08 · Session: 2026-10-08-021 · Status: complete — |
| `EXPERIMENTS/068-arxiv-spec-generator/` | `docs/INDEX.md` | active | 2026-10-08 | Status: Complete — 4 of 4 kill gates PASSED (after conda parsing fix and fair K4 metric) |
| `EXPERIMENTS/069-false-accept-confusion/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | Session 2026-10-08-027-explore-the-existence-checking-false-acc, VM instance-20260717-0944, decl |
| `EXPERIMENTS/069-install-test/` | `docs/INDEX.md` | active | 2026-10-09 | Verdict: the direction closes, and its own gate passes vacuously. E068's |
| `EXPERIMENTS/069-view-count-nonsoftware/` | `docs/INDEX.md` | complete | 2026-10-09 | Date: 2026-10-08 · Session: 2026-10-08-021 · Status: complete — |
| `EXPERIMENTS/070-discourse-fresh-observation/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-08 | 2 documents |
| `EXPERIMENTS/070-kill-gate-protocol/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | ## The question |
| `EXPERIMENTS/070-name-guard-gap/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/070-silent-wrong-project/` | `EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md` | active | 2026-10-09 | Status: Complete. K1a met, K2 primary ≥ 0.10 (build authorized). |
| `EXPERIMENTS/071-config-validity/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/071-did-you-mean-checker/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/071-pip-name-guard-prototype/` | `docs/INDEX.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/071-viewcount-denominator/` | `docs/INDEX.md` | complete | 2026-10-09 | Date: 2026-10-09 · Session: 2026-10-09-002 · Status: complete — |
| `EXPERIMENTS/072-fresh-observation-protocol/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | Date: 2026-10-09 · Status: complete — G1 and G2 met, G3 measured, G4 not applicable to prototype |
| `EXPERIMENTS/072-git-file-presence/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 |  |
| `EXPERIMENTS/072-merchant-noise-raw/` | `docs/INDEX.md` | active | 2026-10-09 | Date: 2026-10-09 · Status: complete — G1 and G2 did not fire. No |
| `EXPERIMENTS/072-npm-view-count-prototype/` | `docs/INDEX.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/073-piecewise-price/` | `docs/INDEX.md` | active | 2026-10-09 | Date: 2026-10-09 · Status: complete — G1 and G2 fail. The pwc repair |
| `EXPERIMENTS/074-diy-problem-taxonomy/` | `docs/INDEX.md` | active | 2026-10-09 | Fresh observation in the DIY (home improvement) Stack Exchange domain to discover whether a conc |
| `EXPERIMENTS/074-mfg-cost-estimation/` | `docs/INDEX.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/075-clinical-trial-failures/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | Session 2026-10-09-008, VM instance-20260717-0944, declared 2026-10-09. |
| `EXPERIMENTS/075-maven-view-count-prototype/` | `docs/INDEX.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/077-se-nonsoftware-viewcount/` | `docs/INDEX.md` | active | 2026-10-09 | ## Summary |
| `EXPERIMENTS/078-nec220-load-calc/` | `docs/INDEX.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/078-need-classification-prototype/` | `docs/INDEX.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/079-arxiv-reproducibility/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/079-automotive-obd2-diagnostics/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/080-flaky-test-rootcause/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/080-food-recall-matching/` | `docs/INDEX.md` | active | 2026-10-09 | 2 documents |
| `EXPERIMENTS/081-lab-instrument-error-codes/` | `docs/INDEX.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/081-medical-device-fault-codes/` | `docs/INDEX.md` | active | 2026-10-09 | ## Domain |
| `EXPERIMENTS/082-embedded-fault-codes/` | `docs/INDEX.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/082-mcu-fault-diagnostics/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/082-medical-device-alarm-codes/` | `docs/INDEX.md` | active | 2026-10-09 | 1 documents |
| `EXPERIMENTS/083-3dprint-fault-codes/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | owner: docs/INDEX.md |
| `EXPERIMENTS/083-aviation-maintenance-fault-codes/` | `docs/INDEX.md` | active | 2026-10-10 | 1 documents |
| `EXPERIMENTS/084-industrial-equipment-fault-codes/` | `docs/INDEX.md` | active | 2026-10-10 | 1 documents |
| `EXPERIMENTS/084-px4-fault-codes/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-09 | Session: 2026-10-09-026, VM instance-20260717-0947 |
| `EXPERIMENTS/085-building-automation-hvac/` | `docs/INDEX.md` | active | 2026-10-10 | 1 documents |
| `EXPERIMENTS/085-declared-not-provided/` | `EXPERIMENTS/085-declared-not-provided/PROTOCOL.md` | active | 2026-10-10 | Result: the candidate does not survive. The instrument works and the class |
| `EXPERIMENTS/086-building-code-compliance/` | `docs/INDEX.md` | active | 2026-10-11 | 1 documents |
| `EXPERIMENTS/087-environmental-monitoring/` | `docs/INDEX.md` | active | 2026-10-11 | 1 documents |
| `EXPERIMENTS/088-instrument-discrimination/` | `docs/INDEX.md` | active | 2026-10-10 | observed 2026-10-10, session 2026-10-10-004, VM instance-20260717-0944. |
| `EXPERIMENTS/089-substitute-or-neighbour/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-10 | Session 2026-10-10-005, VM instance-20260717-0944. Protocol declared in |
| `EXPERIMENTS/PLAN.md/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | 1 documents |
| `EXPERIMENTS/README.md/` | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| `EXPERIMENTS/synthesis-view-count-principle.md/` | `EXPERIMENTS/PLAN.md` | withdrawn | 2026-10-10 | 1 documents |

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
