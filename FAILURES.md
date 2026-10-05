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
F001-F008, [`FAILURES-findings-2.md`](FAILURES-findings-2.md) for F009-F012,
[`FAILURES-findings-3.md`](FAILURES-findings-3.md) for F013-F017,
[`FAILURES-findings-4.md`](FAILURES-findings-4.md) for F018-F021,
[`FAILURES-findings-5.md`](FAILURES-findings-5.md) for F022-F025,
[`FAILURES-findings-6.md`](FAILURES-findings-6.md) for F026 onward, and
[`FAILURES-findings-8.md`](FAILURES-findings-8.md) (F031),
[`FAILURES-findings-9.md`](FAILURES-findings-9.md) (F029) and
[`FAILURES-findings-10.md`](FAILURES-findings-10.md) (F030) and
[`FAILURES-findings-11.md`](FAILURES-findings-11.md) (F033) and
[`FAILURES-findings-12.md`](FAILURES-findings-12.md) (F034) and
[`FAILURES-findings-13.md`](FAILURES-findings-13.md) (F035, F036) and
[`FAILURES-findings-14.md`](FAILURES-findings-14.md) (F037, F038) and
[`FAILURES-findings-15.md`](FAILURES-findings-15.md) (F039, F040) and
[`FAILURES-findings-16.md`](FAILURES-findings-16.md) (F041) and
[`FAILURES-findings-17.md`](FAILURES-findings-17.md) (F042), split because
each file reached the 300-line cap and because both VMs published a part 12 on
2026-10-05; identifiers are stable across the files, so neither was renumbered. **F025 through F028 were taken by the other VM
first**, so this side's findings are F029 onward, renumbered on the unpushed
side per the rule in
[`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md):

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
| F014 | The documented VM sequence was impossible, and refusals printed tracebacks |
| F015 | The local and remote views of a task's holder disagreed after every takeover |
| F016 | A falsification harness overwrote this VM's real `~/.gitconfig` |
| F017 | A generated file's date came from the clock, so the docs gate failed at midnight |
| F018 | A gate asserted a fact about the record, so the suite failed on every interpreter nobody had run |
| F019 | The suite asserted that this machine's git is in the record, so every CI row was red and the log could not be read |
| F020 | The check-run annotations were readable all along; their silence has four causes and three are not "none" |
| F021 | The annotator's rendering was declared unmeasured on a run whose annotating steps never ran |
| F022 | The exemption that answered the wrong question hid every data-file edit from the report |
| F023 | A refusal whose remedy was the one thing an agent must not do by hand |
| F024 | A restated experiment number was false, and the obvious gate cannot see it |
| F025 | The window that made a red run explicable ended one line before the answer |
| F026 | The byproduct thesis is disconfirmed: this mission's own tooling is prior art, and so is its discipline |
| F027 | Every project in this niche has zero users, so "plausible adoption path" cannot discriminate here |
| F028 | The flat adoption tail is vocabulary age, not niche, so "adoption path" is uninformative for young candidates |
| F029 | A live corpus of 1401 unmet needs produced zero candidates that survive the screens |
| F030 | A prior-art verdict from one search query is unreliable in both directions |
| F031 | Measured from outside, the mission was spending its effort on its own record |
| F032 | Stars do not predict installs in any of five niches, so F028's flat tail was never a statement about adoption; and "prior art exists" cannot mean "served" |
| F033 | Full-text issue counts inflated E012's strongest cluster ~200× |
| F034 | The prior-art screen's premise holds in mature vocabularies and largely fails in young ones |
| F035 | "A tool already serves this" is the mission's least reliable verdict, and a third of what it can find lives in a corpus it never read |
| F036 | A web capture can answer HTTP 200 with results unrelated to every query |
| F037 | The screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact |
| F038 | Lead 7's mechanism is implementable and the stock-SDK friction is real, but the missing piece is a feature gap, not a candidate |
| F039 | The need corpus is 1250 individuals with no need-level recurrence detectable inside it, so its 0-of-50 was never interpretable (D051) |
| F040 | F037's "the reader copies the directory" is an instruction rather than an observation: 687 documented copy sites, 4.7% duplicated content, no cross-author overlap |
| F041 | The young vocabulary's copy channel is 0.12x its install channel, so the prior-art screen's young-vocabulary failure is the world and not a channel it failed to read |
| F042 | A repair walk that printed "no new ancestors" 29 times resolved 0 of 434 unreadable comments and exited 0; it never advanced the node, so no chain longer than one hop could close |

**F042's evidence lives at `EXPERIMENTS/022-need-outcomes/`,** and the defect
itself is in `need_depth_walk.py`. The reported result did not move across the
repair (odds ratio 0.701 before, 0.703 after), because the two strata the arm
uses were never affected — which could only be known after the repair.
`tests/test_need_depth_gate.py` holds the defective loop shape as a failing
assertion and reads the committed capture rather than the walk's exit code.

**F041's evidence lives at `EXPERIMENTS/021-copied-artifact-serving/`,** not at
the `020-` path some records still name: the other VM took `020-copied-config-drift`
and F040/D052 for a different experiment on the same reading, and this side
renumbered on the unpushed side per the multi-VM rule. `PROTOCOL.md` holds the
declaration, `results.json` the verdict and the lost capture, and `raw/` the 95
instrument captures.


**The invariant that makes the split sensible.** A finding is only useful if a
reader can tell a disproved claim from a still-open question, so the findings
are separated from the live list rather than interleaved with it. The files
split by line cap, not by subject: `FAILURES-findings.md` holds F001–F008,
`FAILURES-findings-2.md` takes F009–F012, `FAILURES-findings-3.md` takes F013 to
F017, `FAILURES-findings-4.md` F018–F021, and every finding after it goes in
`FAILURES-findings-5.md`. Identifiers are stable: a reference to `F013` means the
same entry whichever file it is in.

**Identifiers are allocated from each VM's own tree, so two VMs in an hour
collide by construction.** Six times on 2026-10-03, and the cost is now measured
rather than predicted: resolving a rebase restored one file's *index* row to the
renumbered form while reverting its *body* to the old identifiers, so a findings
file and its own table briefly disagreed about the same two entries — the exact
failure this paragraph exists to prevent, caught only because both were read
together before landing. Nothing in the tooling prevents a collision;
`STATE.md` records it as unfixed.

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
