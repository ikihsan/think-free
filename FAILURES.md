<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures and negative results

Disproved ideas, failed implementations, and the lessons worth keeping. An
abandoned option is progress; a silently dropped one is a repeat.

Distinguishing the kind of failure matters, because it determines the next step:

| Statement | Consequence |
|---|---|
| The implementation was wrong | The approach may still work |
| The approach does not work | Do not rebuild it |
| The measurement was inadequate | Unknown; fix the experiment |
| Access or resources blocked it | Unknown; record the blocker precisely |

Recorded findings live in [`FAILURES-findings.md`](FAILURES-findings.md) for
F001–F008 and [`FAILURES-findings-2.md`](FAILURES-findings-2.md) from F009,
split because the first file reached the 300-line cap:

| Id | Subject |
|---|---|
| F001 | Photo-migration auditor: the motivating example is not evidence |
| F002 | E001 first run: implementation failure, not hypothesis failure |
| F003 | Session 002 under-declared its artifacts; reconciliation caught it |
| F004 | The new directory sweep declared 13 build-output files |
| F005 | Claims were local-only, so two VMs could both own one task |
| F006 | Decision-directed advantage does not transfer to a fieldwork-cost budget |
| F007 | Knitting repair planner: the stated input set is information-insufficient |
| F008 | Adaptive ventilation measurement selection: prescribing one intervention beats choosing it |
| F009 | Knitting repair planner: the algorithmic advantage is prior art |

**The invariant that makes the split sensible.** A finding is only useful if a
reader can tell a disproved claim from a still-open question, so the findings
are separated from the live list rather than interleaved with it. Identifiers
are stable: a reference to `F008` means the same entry in either file.

## Open, not yet disproved

These remain live questions, not settled negatives:

- **Knitting repair planning** (`RESEARCH/C.md`): graph representation is prior
  art and so is the algorithmic core (F009). What is untested is whether a
  knitter follows a generated plan and saves real work — Stage B, unperformable
  in this repository. Stage A is settled mechanically (T-0010, T-0011).
- **Adaptive ventilation measurement selection** (`RESEARCH/C.md`): stopped as
  formulated (F008). NVAPF and NIST tools occupy uncertainty-aware estimation;
  the surviving reading-a-second-sensor robustness observation is untested
  against existing tools and may belong inside them.
- **Sidewalk survey prioritisation** (`RESEARCH/A.md`): strong value story,
  substantial prior art; the decision-value advantage is falsified in its
  motivating cost regime (F006) but not in every regime.

## Reopening

A failed idea returns when the specific evidence that killed it is invalidated —
not because effort was previously spent on it. Record that evidence here so the
next session finds it in one search.