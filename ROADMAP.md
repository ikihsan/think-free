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
      mechanisms. Sealed 2026-10-03 (T-0002). E1 and E2 remain `untested`; E3's
      census ran (T-0013) and its declared gate turned out not to be able to fail
      (`FAILURES.md` F010), so E3's load-bearing claim is still `untested`.
- [x] Investigation F: adoption researcher — six pre-release checkable criteria.
      Sealed 2026-10-03 (T-0003); the criteria become a gate at stage D, not a
      candidate screen.
- [ ] Consolidate the reports into competing hypotheses, preserving
      disagreements. Partly done in `HYPOTHESES.md`; the cross-report screen is
      `RESEARCH/SYNTHESIS.md` (T-0012).

## B — Experimental discovery

**Status: partial.** Eight experiments have run; three invention claims are
disproved, one declared gate was shown not to be able to fail, one mechanism was
confirmed while its candidate died of it, and no candidate is validated.

- [x] Write the experiment protocol (`docs/process/experiment-protocol.md`)
- [x] Run E001 as a baseline check; kill gate met, candidate's motivating example
      disproved (`FAILURES.md` F001)
- [x] Write kill gates for the three held candidates in `HYPOTHESES.md` (T-0001, 2026-10-03)
- [x] Apply the information-sufficiency test to the three held candidates (`003-information-sufficiency`, T-0008: W1/W3 survive, W2 spec insufficient, F007)
- [x] Run the A1 masking experiment on the PPNA sidewalk extract (`002-a1-masking`, T-0005/T-0006/T-0007: count-budget gate met, fieldwork-cost gate fails, F006)
- [x] Test the knitting candidate's Stage-A planner twice: per-error rule
      suboptimal (`004-knitting-stage-a`, T-0010), whole-neighbourhood search
      exact (`005-knitting-bounded-search`, T-0011)
- [x] Search the knitting candidate's last kill-gate condition in three
      vocabularies (`RESEARCH/PRIOR-ART-KNITTING.md`, T-0015): the algorithmic
      advantage is prior art (`FAILURES.md` F009), no tool supplies an
      intervention sequence for an existing hand-knit
- [x] Run the ventilation candidate's measurement-design kill gate
      (`006-ventilation-measurement-design`, T-0014): gate not met, formulation
      stopped (`FAILURES.md` F008)
- [x] Run E3's build-timestamp census over 200 PyPI wheels
      (`007-build-timestamps`, T-0013): declared 5% gate met at 0.965, but the
      metric measures DOS-epoch pinning rather than reproducibility and attributes
      no cause (`FAILURES.md` F010)
- [x] Attribute the byte difference (`008-build-timestamp-attribution`, T-0017):
      398 of 398 differing bytes are timestamp fields, and `SOURCE_DATE_EPOCH`
      makes builds bit-identical, so E3's mechanism is supported and its
      candidate abandoned — the remedy is one environment variable the builder
      already honours (`FAILURES.md` F011)
- [ ] Run at least two materially different falsification experiments before any
      commitment decision. Only the knitting line has had two, and both runs
      produced no product claim; with C2 stopped (F008) and the knitting
      algorithmic claim abandoned (F009), no candidate has two.
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
- [x] Standard-library test suite (176 tests), green on git 2.25.1 and 2.56.0
- [x] Machine-readable exercised-git-versions record (`tests/git-versions.json`, T-0018)
- [x] Decision log split by invariant a second time (`DECISIONS-GATING.md`, T-0018)
- [x] Environment doctor with presence-only credential checks
- [x] Continuous integration running lint, tests, and session verification.
      Five gates, Python pinned with `setup-python`, failing tests re-emitted as
      public annotations. **Measured green** for Tests, doc lint, skills check
      and vendored integrity (run `37157528596`); it had failed on **all 60**
      earlier runs because of a git-version defect in `sync land`
      (`FAILURES.md` F011, fixed in T-0016). The remaining red step is
      `session verify --strict` while any VM has a session in flight on the
      shared branch, which is D013 meeting fleet practice rather than a defect.
- [ ] `origin release check` validating `RELEASE-MANIFEST.md`
- [ ] Seed tasks from `STATE.md` next actions
- [ ] Headless task-runner script for VMs, once a VM exists
- [ ] Scheduling or supervision, once unattended execution is authorised

## Sequencing note

The infrastructure track finished ahead of stage B because stage B is blocked on
judgement rather than tooling. Kill gates now exist for the three held
candidates, eight experiments have run, and none has validated a claim. Stage B
is now blocked on the open questions in `STATE.md`: E2's time-gated drift
comparison, and the two questions no experiment here can answer — whether a
knitter follows a generated repair plan, and whether E3's builder-level finding
generalises beyond the one builder this machine has.