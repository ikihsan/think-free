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
F001–F008, [`FAILURES-findings-2.md`](FAILURES-findings-2.md) for F009–F012, and
[`FAILURES-findings-3.md`](FAILURES-findings-3.md) from F013, split because each
file reached the 300-line cap:

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
| F010 | E3's predeclared timestamp gate is near-vacuous: prevalence measured, attribution not |
| F011 | `sync land` broke on git ≥ 2.26, and every CI run failed for that reason |
| F012 | E3's ordering claim holds, and that is why there is nothing to build |
| F013 | Three mission records were committed with conflict markers, and every gate passed |

**The invariant that makes the split sensible.** A finding is only useful if a
reader can tell a disproved claim from a still-open question, so the findings
are separated from the live list rather than interleaved with it. The files
split by line cap, not by subject: `FAILURES-findings.md` holds F001–F008,
`FAILURES-findings-2.md` takes F009–F012, and `FAILURES-findings-3.md` takes
every finding after it. Identifiers are stable: a reference to `F013` means the
same entry whichever file it is in.

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
- **Reproducible Python builds** (`RESEARCH/E.md`, E3): the mechanism is
  supported and the candidate abandoned (F012) — for the one builder available
  here, timestamps are the only byte-level cause and `SOURCE_DATE_EPOCH` removes
  all of it. Still open, and not a new repository: the census's per-package
  heterogeneity, which this run does not explain, and whether compiled-extension
  builds behave the same way. E1 (retry jitter) and E2 (lockfile drift) remain
  `untested`; D020 rules E1 out of order.

## Reopening

A failed idea returns when the specific evidence that killed it is invalidated —
not because effort was previously spent on it. Record that evidence here so the
next session finds it in one search.