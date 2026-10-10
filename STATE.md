<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Verified state

Date: 2026-10-10, Asia/Kolkata. Phase: B — **the one candidate this mission has
produced is withdrawn, and the mission has found the instrument its whole record
was missing.** E082 validated the view_count instrument's generalization to a
sixth platform type (embedded Discourse forums), with unserved-open-like
fraction 15.3% consistent with Discourse baseline 11.7%. `stage-lines` / `stg` (E037, E038, F060, F062–F064, D068,
D069) was the first candidate with a working artifact, and three experiments closed it.
E043 ran the candidate's stated caller — six real agents — and the packaging advantage
that was to justify adoption was not observed (F075). **E045 read the demand evidence
the candidate rests on, all 189 unique issues in E038's cached corpus, and the
population item 0a was to measure does not exist in it: 29 of 189 rows are about choosing
which lines reach the index, 28 of those carry explicit diff access and the 29th
GUI-implied, and none carries none (F081). The same reading killed the differentiator —
those 29 rows name 26 distinct repositories, two of them shipped command-line tools that
take `stg`'s coordinate, and both name `stg`'s exact hard case and target the agent
population by name (F082).** **E044, run concurrently with that reading, tested
that population directly — six real agents, no line number and no `git diff` — and
it is not observed to need the tool either: 6 of 6 exact, `nostg` 3 of 3
(F083, D078).** `stg` stays in the repository, unreleased, as a correct
tool: 37 of 37 tests, index byte-identical to a hand-built patch, honest exits. **E062 then took the question out of software and found the
confound the mission has been reading as data all along: F096 — "the requester never
came back" was never evidence that a need went unserved. Of the 20 highest-arrival
unremedied needs in a non-software population, a free general assistant answers
**17 of 20 in full today** (F096, D084). Unanswered on a platform is not unserved,
and every population this mission has measured counted *statements* of need while
reading them as service levels. The instrument that was missing is `view_count`:
independent arrivals at a need, on every row.** That is
its final standing unless the incumbents change. **The application is not closed:** 29
real issues in 26 real repositories is a real population and it is being served. The
score-tail backlog remains closed. **E064 then measured the failure mode
complementary to the published hallucinated-name rate (arXiv:2501.19012):
93 of 576 plausible near-miss package names resolve to real, different
artifacts (0.1615, CI95 [0.134, 0.194]). **E089 read those 93 descriptions,
which E064 had already committed and nobody opened: only 11 are
self-declared substitutes — 11 of 576 = 0.0191, an 8.5x reduction — and 13
more are parked names whose install succeeds and imports nothing. The same
rule labels 0 of 30 controls. E085's independent hand-read put the silent
rate on real declared dependencies at 0.6%, and the two agree. The existence
bit is still insufficient; it is not insufficient at the strength 0.1615
implies (F099 corrected by F110, D097).** The pre-declared metadata rule
that would have repaired it failed its recall arm (0.742 against 0.90)
because the misses are healthy, popular projects. No candidate, no
prototype (F099, F110, D086, D097).**

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
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030, 037–040, 2026-10-06-001–003, T-0012, T-0013, T-0017, T-0021–T-0023, T-0029, T-0040, T-0076–T-0078) and on `instance-20260717-0947` (sessions 020–023, 027–029, 031–038, T-0011, T-0014–T-0016, T-0018–T-0020, T-0024–T-0028, T-0042–T-0045) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `044-discover-staging` complete (**6/6 exact, `nostg` 3/3 — the discovery-without-diff population does not need `stg` either; candidate closed, F083, D078**); `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); `030-departure-recurrence` complete (H1 `not_evaluated` a third and final time, F050: the fired pair-level statistic measured comment length and rare-token coincidence, its permutation null explains the arm difference, and the length-matched sign flips; A8's held-out separation fires, 0.64 vs 0.036, so the departure-framing population is real and its ruler for recurrence was falsified); ``036-search-backlog` complete (**the worklist is one unauthenticated `/search/advanced` query — 81 of E034's 100 sampled `git` tail ids, ascending, with the closure label in the payload; KILL-R met, F059, D066/D067, T-008... |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200... |
| Experimental validation | **Four invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage, **E037's mechanism differentiation** via E041), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029).  No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md`, F039 in `-15.md`, F041 in `-16.md`, F042/F043 in `-17.md`, F044 in `-18.md`, F045 in `-19.md`, F048 in `-20.md`. **Six invention claims have now been tested and none validated; the most recent closed by running it rather than screening it (E047, F084: the shipped hook runners do not sweep a partially-staged file, and one corpus row turned out to exonerate the tool the record blamed).** The premise behind the dominant kill reason has now been measured five ways over: coverage (F035), soundness (F034), population (F037), **what its evidence is evidence of (F048: use is not fit, so a download count cannot carry a kill); **F059 the score-tail worklist is one unauthenticated `/search/advanced` query — the candidate is prior art as a URL, and F058's platform-wide reachability claim is refuted**** — and **the premise itself, counted (F044: prior art is 10 of 18 = 0.556, a one-row... |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21). A gate's pattern for this repository's split records now reads a numbered split — `decisionindex.py` reported `DECISIONS-SCREENING-2.md` as unlisted while its row was in the table, and the pattern is held to the spellings `DECISIONS.md` uses (`tests/test_decision_row_pattern.py`, T-0063). Concurrent writers of one session's event stream are serialized by an `flock` held across the seq assignment and the append (defect 24: two processes each appended the same seq into a finished session's stream, which reddened CI's `session verify --strict`; falsified as 8 of 8 duplicate-seq rounds on the pre-fix code, 0 of 8 on the repair, plus a two-process regression test) |
| Implemented (3) | **`stage-lines/`** — `stg`, a non-interactive `git add -p`. `list`, `list --json`, `stage`, `unstage`, `split`; addresses any change by the working-tree line it occupies, splitting adjacent modifications per line. **285 lines of library + a 297-line CLI, standard library only, no install step. 28 tests, all against real git repositories with no mocks** (`python3 -m unittest discover -s stage-lines`). Correctness is anchored to git itself: on a real file in this repository the resulting `.git/index` is **byte-identical** to the one a hand-built patch leaves. **Not released**; its header says `status: draft` |
| Users and adoption | None. No product, no release, no claims. **KILL-Q is answered for `stg`, and the answer is no.** E037 measured demand at 0.016-0.066 of matching GitHub issues through a classifier of unmeasured precision; E043 ran the candidate's stated caller and found the packaging advantage absent (F075); **E044 ran the discovery population E043's ceiling named — agents with no line number and no `git diff` — and it is not observed to need the tool either: 6 of 6 exact, `nostg` 3 of 3, every agent doing the discovery by hand first (F083)**; **E045 read that demand evidence itself, row by row, and found 0 of 189 rows is the population the last open claim rested on — all ten automated callers in the need rows name their own diff access (F081)**; and the same reading found the differentiator shipped as two installable command-line tools named inside that same corpus (F082). `stg` is withdrawn as a candidate and remains a correct tool (37/37, byte-identical index, honest exits), unreleased, `status: draft` | **E047 then closed the one observation E045 left behind, and it closed by being run: the hazard is byte-exact and no shipped hook runner produces it (F084, D079)** |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | **171 with an event stream** — `origin session verify` reads the tree rather than a running total; session 2026-10-08-021 finished this landing |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 1088 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM seven times in two sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`), and in E033 four more: `tally.py` (into `descriptive.py`), `STATE-next-actions.md` (closed items into `STATE-next-actions-closed.md`), `ROADMAP.md` (the infrastructure track into `ROADMAP-infrastructure.md`) and `tests/test_allocation_measurement.py` (the per-day share into `test_allocation_world_share.py`) — and each time the repair was to move material to the file whose invariant it belongs in, never to shorten prose |
| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. **The row went red once more, on 2026-10-07, and the cause was older still:** `37b645d` failed `release check` on the 3.12 row, four split records tracked but never classified and the manifest's three state rows duplicated from a careless merge. Repaired at `a245c34` — which itself read red only because the session committing its stream into the tree made the record-integrity gate fail on an unfinished session; its stream committe... |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

See [`STATE-in-flight.md`](STATE-in-flight.md) through [`STATE-in-flight-9.md`](STATE-in-flight-9.md).

## What changed recently

See [`STATE-history.md`](STATE-history.md).

## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md); the standing constraints that hold
whichever item is next are in
[`STATE-constraints.md`](STATE-constraints.md). **The seat for a candidate is empty
and every derived action from the last candidate is spent.** Item 0a is closed twice —
by the run (E044, F083, D078) and by reading the demand evidence (E045, F081, F082) —
and item 0f is closed by E047 (F084, D079), with E048 (F085) answering its follow-on:
in every configuration except lefthook without `stage_fixed` the
formatter/commit disagreement is loud or blocked, and that one silent shape ships its
remedy and trips any CI format gate. **Nothing to build.** The fresh observation the
reload point asked for is now done (E062), and it returned the instrument rather than
a candidate.

**The single most useful next action, after E088.** E069 showed a predeclared kill gate whose passing region contains only vacuous cases cannot fail (F101, D088). **E088 showed the same failure one level earlier, and this time it cost seven sessions and a committed synthesis: no run in E081-E087 ever checked that its instrument separated a known-served case from a known-unserved one.** Each of the seven wrote its own G2 'control validity' gate, and E081's asserts the labels it checks against, so it cannot fail (F109, D095).

**The package-name line is closed on measured grounds and can be dropped from the next session's reading list.** F108 measured the silent wrong-dependency rate on real declared dependencies at **0.6%** (3 true of 6 flagged, hand-read); F110 then corrected the 0.1615 that had been standing in for it, finding **11 of 576 = 0.0191** self-declared substitutes among the 93 E064 counted. Neither number is worth a candidate, and the strongest alternative (`deptry`) does not detect the class — but a class at 0.6% is a warning, not a product (D097).

**So the next work is not another domain and not another screen: it is a real need population, measured by an instrument that has first passed a discrimination test on labels known by construction.** The concrete opportunity E088 leaves open is that the seven domains it closed were closed on *instrument* grounds and never on *population* grounds. Whether structured fault/error-code domains -- aviation, industrial PLC, medical device -- hold needs that are unserved is an open question with a cheap first step: read the actual practitioner rows that exist on those venues, by hand, before any classifier is written. Reading is what ended the need-harvest route honestly (E045, F081) and it is the one step this route never took.

A protocol for that work must (a) name the instrument and call that instrument rather than a local copy, (b) pass a discrimination test before any population row is read, and (c) enumerate what its gate's passing value can be made of (D088, D095).

**Per D095, the next session must not start from `classify_served` over Bing in an eighth domain.** E088 showed that instrument classifies 40% of nonexistent entities as `served` and reads no arrival count, so the route's output was never a measurement of its own variable. Seven sessions and a committed synthesis rested on it (F109).

**Per D083, the next session must start from fresh observation in a new domain.**
The ArXiv reproducibility line (E067→E069→E079) is closed on measured grounds:
- E067: all kill gates passed on real data (problem is real)
- E069: spec generator's kill gate K1 only passes on empty specs (gate vacuous)
- E079: information-sufficiency witness FAIL (static analysis cannot resolve version ambiguity)
- E083: 3D printer fault codes on manufacturer Discourse forums show concentration (G2 PASS 73.4%) but fail cross-model coverage (G3 FAIL 1.8 models/fault) due to brand silos; view_count instrument validated (100%).
No candidate emerges. The mission's 10th measurement shows the seat is empty (F029, F051, F039, F059, F081, F084, F085, E075, E079, F106).

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified and not to be assumed:** fleet access,
unattended supervision, GPU.

*Honest limitations moved to [`STATE-history.md`](STATE-history.md).*