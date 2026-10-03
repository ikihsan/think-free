<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Evidence-driven roadmap

Stages are ordered by dependency, not by date. Evidence can send work back to an
earlier stage; there is no calendar here and none is promised.

Status legend: **done**, **partial**, **not started**, **blocked**.

## A — Independent exploration

**Status: partial.** All six roles sealed; the consolidation below is partial.

- [x] Verify the environment and record actual limits (`EXPERIMENTS/000-capabilities`)
- [x] Preserve the mission and boundaries (`MISSION.md`)
- [x] Sealed reports A–D (`RESEARCH/A.md`–`D.md`)
- [x] Investigation E: experimental engineer — three cheap falsifiable
      mechanisms. Sealed 2026-10-03 (T-0002); all three remain `untested`.
- [x] Investigation F: adoption researcher — six pre-release checkable criteria.
      Sealed 2026-10-03 (T-0003); the criteria become a gate at stage D, not a
      candidate screen.
- [ ] Consolidate the reports into competing hypotheses, preserving
      disagreements. Partly done in `HYPOTHESES.md`; the cross-report screen is
      `RESEARCH/SYNTHESIS.md` (T-0012).

## B — Experimental discovery

**Status: not started.**

- [x] Write the experiment protocol (`docs/process/experiment-protocol.md`)
- [x] Run E001 as a baseline check; kill gate met, candidate's motivating example
      disproved (`FAILURES.md` F001)
- [x] Write kill gates for the three held candidates in `HYPOTHESES.md` (T-0001, 2026-10-03)
- [x] Apply the information-sufficiency test to the three held candidates (`003-information-sufficiency`, T-0008: W1/W3 survive, W2 spec insufficient, F007)
- [x] Run the A1 masking experiment on the PPNA sidewalk extract (`002-a1-masking`, T-0005/T-0006/T-0007: count-budget gate met, fieldwork-cost gate fails, F006)
- [ ] Run at least two materially different falsification experiments before any
      commitment decision. One run: `002-a1-masking` (a masked-real-data
      decision-policy experiment). `004-knitting-stage-a` is a second mechanism
      but a third domain; `RESEARCH/SYNTHESIS.md` names the ventilation protocol
      as the next materially different one.
- [ ] Independently reproduce or review each result, checking oracle and baseline
      fairness

## C — Commitment

**Status: not started. Nothing may be selected yet.**

Select only when evidence demonstrates technical possibility, meaningful
differentiation against the strongest existing approach, practical value, and a
plausible adoption path. Otherwise continue or pivot. Criteria in
`docs/process/hypothesis-lifecycle.md`.

## D — Engineering

**Status: not started. No product exists.**

- [ ] Build the smallest independently usable implementation
- [ ] Behavioural tests that can fail on a meaningful defect
- [ ] Honest limits documented alongside capabilities
- [ ] Reproducible build and installation, security review
- [ ] Real examples, minimal learning curve

## E — Public release

**Status: not started. Blocked on C and D, and on the user's push authorization.**

- [ ] Licence, install path, demo, honest comparison, contributor guide
- [ ] `origin release check` implemented against `RELEASE-MANIFEST.md`
- [ ] Push with explicit user authorization
- [ ] No unreleased behaviour described as shipped

## F — Real-world validation

**Status: not started.**

- [ ] Observe actual use and adoption friction
- [ ] No fabricated feedback, no unsolicited outreach

## G — Expansion

**Status: not started.** Improve reliability, capability, accessibility, and
interoperability in response to observed problems.

## H — Sustained reassessment

**Status: ongoing.** Reassess whether continuing is justified. Reopen a rejected
candidate only when the evidence that killed it is invalidated, not because effort
was previously spent.

## Infrastructure track

Separate from the invention stages, because the mission cannot be run without it.

- [x] Session logging with append-only events and git reconciliation
- [x] Command capture with exit codes and secret redaction
- [x] Task dispatch with an append-only claim ledger
- [x] Documentation lint: line cap, metadata, links, orphans, generated freshness
- [x] Generated indexes for documents, sessions, and tasks
- [x] 21 skills vendored in-repo and mirrored for every supported agent
- [x] Standard-library test suite (116 tests)
- [x] Environment doctor with presence-only credential checks
- [ ] Continuous integration running lint, tests, and session verification
- [ ] `origin release check` validating `RELEASE-MANIFEST.md`
- [ ] Seed tasks from `STATE.md` next actions
- [ ] Headless task-runner script for VMs, once a VM exists
- [ ] Scheduling or supervision, once unattended execution is authorised

## Sequencing note

The infrastructure track finished ahead of stage B because stage B is blocked on
judgement rather than tooling: no candidate has a kill gate yet. Writing those
gates is the next action in `STATE.md`.