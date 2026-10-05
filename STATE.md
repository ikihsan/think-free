<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Verified state

Date: 2026-10-05, Asia/Kolkata. Phase: B — the prior-art screen is now measured
and three unserved needs await a mechanism question. **No product selected.**

Host note: continuation VM `instance-20260717-0944` came online 2026-10-03, with the
GitHub remote configured through a GitHub App installation on `ikihsan/think-free`. It
runs **Python 3.8.10 and git 2.25.1**, not the 3.14.6/2.55.0 recorded from the development
machine, so the capability numbers below are per machine and are re-probed with
`tools/origin doctor`.

Push-credential note, corrected 2026-10-04. The note here used to say a durable JWT
generator had been added under `~/.config/github-app/` and that the helper points at
it. That was true of `instance-20260717-0947` and not of `instance-20260717-0944`, whose
helper still invoked `/tmp/github-app-jwt.sh` — which is how `0947` lost a day of pushes.
Repaired there in T-0029 and `doctor` now reports such a dependency before it fails
([`docs/operations/doctor.md`](docs/operations/doctor.md)).

This is the reload point. A cold session reads this file, then whatever it links.

## Dashboard

| Area | Verified status |
|---|---|
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030, 037–040, T-0012, T-0013, T-0017, T-0021–T-0023, T-0029, T-0040) and on `instance-20260717-0947` (sessions 020–023, 027–029, 031–038, T-0011, T-0014–T-0016, T-0018–T-0020, T-0024–T-0028, T-0042–T-0045) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); ``014-repository-signal-filter` complete (E012's strongest cluster collapses ~200× under the filter it was promised, F033); `015-incumbent-serving` complete (**gate inconclusive**; the premise behind "prior art exists" is now measured directly and **holds in mature vocabularies, fails in young ones** — 4/4 versus 1/4, F034); `016-prior-art-adjudication` complete (both arms met — 6 of 6 positive controls recovered, and 3 of 12 adjudicable judgement kills have no prior art on three corpora, F035; two web instruments refused or answered wrongly first, F036); `017-incumbent-artifact-type` complete (F037); `018-runtime-signal-selection` complete (lead 7's mechanism answered — a stock-SDK feature gap, not a candidate, F038); `019-corpus-person-diversity` complete (F039); `020-copied-config-drift` complete (**gate inconclusive**, copying instructed 687× and duplicated 4.7% of content, F040); `021-copied-artifact-serving` complete (the copy channel is 0.118× the install channel, so the screen's young-vocabulary failure is the world, F041); `022-need-outcomes` complete (gate A1 met at 100% readable, **gate A2 fires at lift 0.703** against a declared floor of 1.0; 58.0% of 1401 stated needs were answered, **0/24 built by the requester**, F042); `023-served-baseline` complete (**the `served` cell now has the control it never had** — 15/38 = 0.395 for need statements against **14/38 = 0.368** for ordinary comments in the same threads, intervals overlapping; two readers on the identical 39 rows agree at **κ = 0.923**, so F042's third number is withdrawn as a demand-side figure, F043, D055); `025-need-staters-builderhood` complete (F042's 0/24 build arm was a *disclosure floor*, so the missing channel was read: **278 of 1250 need-staters = 0.222 have publicly shipped something** against **139 of 500 = 0.278** ordinary commenters in the same stories, ratio 0.80×, intervals overlapping — need-staters are a fifth builders and build *less* than their neighbours, which **confirms** item 0d's closure rather than withdrawing it, F045, D057) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200; F035 "a tool already serves this" is materially overstated as a cause of death and a third of what it can find lives in a corpus it never read; F036 a web capture can answer HTTP 200 with results unrelated to every query; F037 the screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md`. F039 the demand-side need corpus is 1250 individual requesters rather than a sample of shared needs, so its 0-of-50 measured the corpus and not the screens; F044 "twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin over a population of 20, and 7 of the 18 died of something else; F045 the corpus's authors are a fifth builders (0.222 vs a 0.278 control) and build *less* than their neighbours, so "need-staters are not builders" is false as an absolute and the corpus closure is confirmed rather than withdrawn; |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029).  No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md`, F039 in `-15.md`, F041 in `-16.md`, F042/F043 in `-17.md`, F044 in `-18.md`, F045 in `-19.md`. **The premise behind the dominant kill reason has now been measured four ways over**: coverage (F035), soundness (F034), population (F037) — and **the premise itself, counted (F044: prior art is 10 of 18 = 0.556, a one-row margin, and the population is 20 rather than twelve)**. No candidate validated and no prior-art verdict falsified |

| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21). A gate's pattern for this repository's split records now reads a numbered split — `decisionindex.py` reported `DECISIONS-SCREENING-2.md` as unlisted while its row was in the table, and the pattern is held to the spellings `DECISIONS.md` uses (`tests/test_decision_row_pattern.py`, T-0063) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | **110 with an event stream, 108 closed** — counted from the tree rather than from a running total, because the two VMs had been counting different bases. An unfinished session on either VM is reported as in flight rather than as a failure (D027); VM 0947's 054 is the live one and its T-0060 claim is past the 12h lease |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 1088 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM five times in three sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, and in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`) — and each time the repair was to move material to the file whose invariant it belongs in |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

**F037's reconciliation for the supply question is withdrawn: the copies are
adapted, not duplicated** (`EXPERIMENTS/020`, F040, T-0065) — the first line in
five experiments about the world rather than about this repository's own
instruments. **Copying is widely instructed (`cp -r .claude`, 687 Sourcegraph
matches against a nonsense control of 0) and barely duplicated (92 of 1950
distinct contents, 4.7%; no cross-author pair overlaps by half)**, so the install
readings are not explained by an invisible channel. Drift is **`inconclusive`**,
not zero: 0 attributable pairs exist in the measurable population, so the declared
gate fires. Two instruments this session built were falsified and both retractions
are held by a test — see [`STATE-constraints.md`](STATE-constraints.md).

**The number that narrowed item 0 had no control, and the control is now run**
(`EXPERIMENTS/023`, F043, D055, T-0067): E022's hand-labelled **15/39 = 0.385**
"served" rate is **0.368** for ordinary comments in the *same stories*, drawn
from answered comments so both arms share the "a reply exists" condition. The
difference is 0.026 and the Wilson intervals overlap across nearly their whole
width. **The rubric is not the cause** — this reader and E022's labelled the
identical 39 rows at **κ = 0.923**, which turns E022's "one reader, no second
coder" caveat into a measured magnitude. **What is withdrawn is the inference,
not the measurement:** a reply naming an artifact is not distinguishable from
what an ordinary comment receives, so 0.385 was a description of Hacker News
read as a description of needs. **E022's other two numbers stand** — 58.0%
answered, and 0 of 24 unserved requesters who built it themselves. **The second
was a disclosure floor, and E025 has now read the missing channel: 22.2% of the
1250 have publicly shipped something** (F045), so they are a fifth builders who
build less than their neighbours. **The transferable bound:** a trigger vocabulary
finds people who state needs and is invisible to what happens to those needs
afterwards (lift 0.703 on answered, +0.026 on served), which bounds every outcome
read from a trigger-harvested corpus, E022's included.

**The candidate generator was refuted and its strongest cluster with it**
(`EXPERIMENTS/012`, `EXPERIMENTS/014`, D049, F029, F033): 1401 harvested need
statements, 50 drawn by a stated rule, **0 survived**; the "5805 issues / 28
repositories" cluster collapsed to 15 issues across 9 agent-labelled repositories.
F030: a prior-art verdict from one query is wrong in both directions.

**The prior-art screen was then measured on coverage** (`EXPERIMENTS/016`, D050,
F035, F036): re-adjudicated on three corpora with six positive controls, **6 of 6
controls recovered served and 3 of 12 adjudicable kills have no prior art**.
**Corpus carriage is the transferable result:** GitHub's index carried every
verdict the code corpora carried, the registries carried none on their own, and
the open web carried 4 served verdicts two code corpora returned nothing for. D050:
**an absence of a hit on three corpora is the absence of a hit.** E019 then closed
two of the three as sources (F039).

**The screen's population was measured too, and it came out against the
alternative** (`EXPERIMENTS/017`, F037): **14 of 18** young-vocabulary rows are
executable code, 13 of 18 with every root listing read by hand. Documents are 22%
of the young arm and carry a **median 6,072 stars against 566**, 14 of 18 rows have
no readable use channel, and **the most-starred tool there is installed 363 times
a month.** The reading that followed — the reader copies a `.claude/` directory,
so the artifact is not a package and installs read zero — **is withdrawn by F040
above.**
**Four closed tooling findings, kept as pointers because they are the standing
reasons a session's own gate can be green and its records still false.** A
restated experiment number was false and the obvious gate is blind to it (defect
22, T-0056, D047, F024) — a protocol claimed 113/113 where the artifact said 115,
and `resultnumbers.py` decides from the number's *shape*. Identifier collisions
between two VMs are closed (T-0030, T-0031), but **the work-collision case still
has no detector**, so read the remote task list first
([`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md)).
A gate belongs in the one command the protocol tells every agent to run (T-0045).
A test can read a clock the code does not (defect 15, T-0044). Accounts:
[`STATE-defects.md`](STATE-defects.md),
[`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md). **One rule
survives:** rebase a moving base with `origin sync land`, because a hand-run
rebase records nothing and its paths are then attributed to whoever holds the tree
(T-0053; sessions 040 and 012 hit that ceiling seven and twice).
## What changed recently

- **Sessions 008 and 010, VM 0944 (T-0066/T-0068, F042/F043/F044).** Two
  counts that had never been made, both about this record rather than about
  software: what became of the 1401 stated needs (58.0% answered, 0 of 24 unserved
  requesters built it themselves, the third number withdrawn by F043), and what
  actually killed the candidates (**a plurality with a one-row margin, 10 of 18 =
  0.556, over a population of 20 rather than twelve, with 7 of the 18 dying of
  something else**). Full readings in [`STATE-in-flight.md`](STATE-in-flight.md)
  and [`STATE-in-flight-2.md`](STATE-in-flight-2.md); evidence in
  [`EXPERIMENTS/022-need-outcomes`](EXPERIMENTS/022-need-outcomes/README.md),
  [`EXPERIMENTS/023-served-baseline`](EXPERIMENTS/023-served-baseline/README.md)
  and [`EXPERIMENTS/024-kill-reason-causes`](EXPERIMENTS/024-kill-reason-causes/README.md).

- **Session 053, VM 0944 (T-0063, F039, D051).** E019 counted the people in
  E012's need corpus: **1250 distinct authors**, median one comment each, so
  F029's narrow-audience explanation is disproved and no need-level recurrence is
  detectable inside the corpus. F029 is not reversed — those 50 rows are dead
  either way. Full detail in
  [`EXPERIMENTS/019-corpus-person-diversity`](EXPERIMENTS/019-corpus-person-diversity/README.md).
  **Session 008 then measured what became of those statements** — see above.

- **Session 009, VM 0944 (T-0067, F043, D055).** E022's `served` cell had no
  control, so the control was run: **0.395 for need statements against 0.368 for
  ordinary comments in the same threads**, drawn from answered comments so both
  arms share the "a reply exists" condition. **Reader agreement on the identical
  39 rows is κ = 0.923**, which converts E022's single-reader caveat into a
  measured magnitude and makes the null a fact about the population. **F042's
  third number is withdrawn as a demand-side figure**; its other two stand and
  item 0 now rests on them. Evidence in
  [`EXPERIMENTS/023-served-baseline`](EXPERIMENTS/023-served-baseline/README.md).

**The open readings are enumerated in [`STATE-in-flight.md`](STATE-in-flight.md),
so they can grow without pressing this file against the cap.** Five are closed:
F041's third axis (the copy channel is 0.118x the install channel), F035's
coverage measurement (3 of 12 adjudicable kills have no prior art on any of three
corpora), F039 and F029's refutation of the corpus as a generator (0 of 50, from
1250 individuals each asking once), **F042's** — the outcomes of those 1401
statements, measured — and now **F043's**, the missing control on the one cell
of that measurement that carried a conclusion.

Full detail per session is in [`STATE-history.md`](STATE-history.md) and
[`STATE-history-2.md`](STATE-history-2.md), which exist so that history does not
push this reload point past the line cap. That cap has now been hit by this file
seven times, and each repair moved material to the file whose invariant owns it.


## Infrastructure build (sessions 015–016, earlier)

`tools/origin`, `tools/x`, append-only per-session logs reconciled against git,
multi-VM safety with a two-clone fleet harness (T-0004), the metadata-tagged
documentation graph, and 21 skills vendored in-repo and mirrored. Standard-library
Python, no installation step. Current state: the **Implemented** rows above and the
infrastructure track in [`ROADMAP.md`](ROADMAP.md).

## Resume procedure

1. Read `MISSION.md`, then this file, then `DECISIONS.md` and `HYPOTHESES.md`.
2. `tools/origin session verify` — is any session unfinished? Finish it honestly.
3. `tools/origin preflight` — do the tooling and the documents still agree?
4. `git status` and `git log --oneline -5` before editing. Preserve anything
   unexpected; another agent or an earlier session may own it.
5. Read the raw evidence for the next experiment, not a summary of it.
6. Continue the highest-information experiment, and update this file with it.

## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md); the standing constraints that hold
whichever item is next are in
[`STATE-constraints.md`](STATE-constraints.md). Ordered by information gained
per unit of effort; the top item is:

**The screen that killed most candidates has been measured on every axis, and
each measurement came out against it.** F034 measures **soundness**: **4 of 4**
on-topic incumbents in mature vocabularies are served and **1 of 4** in a young one
— sound where it is least load-bearing, unsound where every candidate here lives.
F035 measures **coverage**: of 12 adjudicable kills, **3 have no prior art at all**
and **4 were served only on the open web**. F037 measures **composition**: the
young arm is **14 of 18 executable code**, not prose. F040 measures
**distribution**: that supply is lightly used rather than invisibly copied.

**What changed is the method, not a candidate — and every source the method was
drawing on has now been measured.** Prior art is judged on the open web and on the
clause's attribute, never on a code index and a category (D050); F039 then showed
the need corpus those survivors came from is **1250 individual requesters** with no
need-level recurrence inside it (D051). **Choosing what the mission selects
candidates on is still an owner decision**, now narrowed to: none of the three axes
— prior art, star-shaped adoption, harvested recurrence — can carry it. **One asset
no failure in this record has touched: 1250 named people who each wrote down,
publicly, what was missing** — and session 008 has now measured what became of
those statements, which **narrows rather than opens the asset**: 58.0% were
answered and **0 of 24** unserved requesters built the thing themselves, so it is
a population of needs the world **absorbed in conversation** rather than one
awaiting a builder. **Session 009 removed the sentence that made that read as a
demand-side discovery**: the "about a third of those were served" was an
uncontrolled rate, and the control is **0.368 against the need arm's 0.395**
(F043). Item 0 now rests on two measured numbers rather than three, and D055
states what a rate read from a trigger-harvested corpus is worth without a
control arm. Item 0 of [`STATE-next-actions.md`](STATE-next-actions.md) holds the
reasoning, and the reading is in [`STATE-in-flight.md`](STATE-in-flight.md).

**The gaps in that pattern, both found by colliding with it, and one of them in
the record rather than in a red run.** Rule 7 did not read the numbered list in
`STATE-defects.md`, so two VMs took defect 7 in the same hour and nothing said so
(T-0036). It then did not read the third place a decision number is written — the
`Decisions **...**` header under each record's title — so two of five records were
false while every gate passed, with both index rows in `DECISIONS.md` correct
throughout (T-0042, defect 14). One entry point reads all three sources now.

**The pattern in the red runs of 2026-10-04 is not "gates are missing" but gates
that exist and are never run**: a task's `verify` omits the one gate its change can
break, a fixture omits the clock the code reads, a split leaves one reader unwired.
T-0045's fix is the general one — put the gate in the command the protocol already
points at, so there is nothing to forget. A gate must also read the property it
claims to check and be falsified against the defect's own bytes (D025, F013); nine
gates work that way, the newest holding a restated experiment number to its
artifact by the number's *shape* (T-0056, F024, defect 22).

**Line caps are the standing friction, and each repair moved material to the file
whose invariant owns it.** `STATE.md`, `STATE-defects.md`,
`FAILURES-findings-4.md` and `tests/README.md` have each hit 300 of 300 and been
split. `STATE-defects.md` cannot be split inside its own numbered list without
`defectlist.py` reading more than one file, so that split is a task.

**The decision log could not record its own next decision, and that is now paid
off.** `DECISIONS-GATING.md` stood at 297 of 300 permitted lines, so T-0036's
decision lived in code and in this file instead of the log. D036 is recorded there,
in the file its own invariant names.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development
machine: 12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0;
GCC 16.1.1; `git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy
present, SciPy/pytest/Z3 absent; `gh` absent; `systemd --user` running with no
user units. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and
pushes via the GitHub App as `Ihsan Ai Server Bot`.
**Unverified and not to be assumed:** fleet access, unattended supervision, GPU.

## Honest limitations of this state

- All six investigation roles are sealed (`RESEARCH/A.md`–`F.md`), and
  `RESEARCH/SYNTHESIS.md` compares them. The synthesis is `inferred` from prose:
  it reorders and screens existing claims and measures nothing itself.
- **E023's null is a resolution limit, not a proof of zero.** 38 rows per arm on
  one day cannot resolve a need effect below roughly 0.2, and the control arm is
  defined by *not matching the trigger vocabulary*, so a need phrased unusually
  could sit in it. `served` is a label, not a measurement — a reply naming an
  artifact is a pointer — which both arms carry equally.
- No invention claim has been validated. Three claims are **disproved**: A1 in its
  motivating regime (F006), C2's measurement design (F008), and the knitting
  planner's algorithmic advantage (F009, by prior art). Two further *lines* died
  without a candidate: this repository's own tooling read as prior art (F026) and
  live need harvesting as a generator, 0 of 50 (F029). E's mechanisms remain
  unvalidated: E1 and E2 are `untested`, E3's declared gate could not fail (F010).
- **The prior-art screen is now supported, not merely unrefuted, in the region
  every candidate lives in** (F041), and nothing reopens the twelve deaths. What
  has *not* been shown is that any need is served by the incumbents a screen names
  — "no prior art found" remains the absence of a hit (F035), and E020's own H2 is
  `not evaluable` because the instrument could not answer it.
- Every candidate has substantial prior art, and none has passed prior-art review.
  **F044 measured that claim for the first time: prior art is the plurality of
  kill reasons, not the majority — 10 of 18 = 0.556, a one-row margin, over a
  population of 20 rather than the twelve this file previously carried, and every
  prior-art row moved to another category kills the majority reading.** Seven of
  the 18 died of something else. Two prior-art reviews are recorded
  and negative in their decisive halves (`RESEARCH/PRIOR-ART-KNITTING.md`,
  `RESEARCH/PRIOR-ART-ORIGIN.md`), and a verdict needs more than one phrasing (F030).
- The screen's own weakness: decidable from prose, so cheap and also vulnerable to
  a persuasive report. It guarantees the *next* experiment is worth running.
- **Three of the last four experiments answered questions about this repository's
  own instruments rather than about software in the world**, and E020 is the first
  to turn outward. Its own measurement was still bounded by a population a search
  engine chooses (F040).
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen,
  and the session-by-session account lives in the two history files named above.
