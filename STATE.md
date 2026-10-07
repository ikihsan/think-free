<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Verified state

Date: 2026-10-07, Asia/Kolkata. Phase: B — and **the one candidate this mission has
produced is now withdrawn.** `stage-lines` / `stg` (E037, E038, F060, F062–F064, D068,
D069) was the first candidate with a working artifact, and two experiments closed it.
E043 ran the candidate's stated caller — six real agents — and the packaging advantage
that was to justify adoption was not observed (F075). **E045 read the demand evidence
the candidate rests on, all 189 unique issues in E038's cached corpus, and the
population item 0a was to measure does not exist in it: 29 of 189 rows are about choosing
which lines reach the index, 28 of those carry explicit diff access and the 29th
GUI-implied, and none carries none (F081). The same reading killed the differentiator —
those 29 rows name 26 distinct repositories, two of them shipped command-line tools that
take `stg`'s coordinate, and both name `stg`'s exact hard case and target the agent
population by name (F082).** `stg` stays in the repository, unreleased, as a correct
tool: 37 of 37 tests, index byte-identical to a hand-built patch, honest exits. That is
its final standing unless the incumbents change. **The application is not closed:** 29
real issues in 26 real repositories is a real population and it is being served. The
score-tail backlog remains closed.

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
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); `030-departure-recurrence` complete (H1 `not_evaluated` a third and final time, F050: the fired pair-level statistic measured comment length and rare-token coincidence, its permutation null explains the arm difference, and the length-matched sign flips; A8's held-out separation fires, 0.64 vs 0.036, so the departure-framing population is real and its ruler for recurrence was falsified); ``036-search-backlog` complete (**the worklist is one unauthenticated `/search/advanced` query — 81 of E034's 100 sampled `git` tail ids, ascending, with the closure label in the payload; KILL-R met, F059, D066/D067, T-0080**); ``014-repository-signal-filter` complete (E012's strongest cluster collapses ~200× under the filter it was promised, F033); `015-incumbent-serving` complete (**gate inconclusive**; the premise behind "prior art exists" is now measured directly and **holds in mature vocabularies, fails in young ones** — 4/4 versus 1/4, F034); `016-prior-art-adjudication` complete (both arms met — 6 of 6 positive controls recovered, and 3 of 12 adjudicable judgement kills have no prior art on three corpora, F035; two web instruments refused or answered wrongly first, F036); `017-incumbent-artifact-type` complete (F037); `018-runtime-signal-selection` complete (lead 7's mechanism answered — a stock-SDK feature gap, not a candidate, F038); `019-corpus-person-diversity` complete (F039); `020-copied-config-drift` complete (**gate inconclusive**, copying instructed 687× and duplicated 4.7% of content, F040); `021-copied-artifact-serving` complete (the copy channel is 0.118× the install channel, so the screen's young-vocabulary failure is the world, F041); `022-need-outcomes` complete (gate A1 met at 100% readable, **gate A2 fires at lift 0.703** against a declared floor of 1.0; 58.0% of 1401 stated needs were answered, **0/24 built by the requester**, F042); `023-served-baseline` complete (**the `served` cell now has the control it never had** — 15/38 = 0.395 for need statements against **14/38 = 0.368** for ordinary comments in the same threads, intervals overlapping; two readers on the identical 39 rows agree at **κ = 0.923**, so F042's third number is withdrawn as a demand-side figure, F043, D055); `025-need-staters-builderhood` complete (F042's 0/24 build arm was a *disclosure floor*, so the missing channel was read: **278 of 1250 need-staters = 0.222 have publicly shipped something** against **139 of 500 = 0.278** ordinary commenters in the same stories, ratio 0.80×, intervals overlapping — need-staters are a fifth builders and build *less* than their neighbours, which **confirms** item 0d's closure rather than withdrawing it, F045, D057); `029-need-build-match` complete (**167 of 241 shipped *before* the need, so 69% of the population was never askable**; the reader arm is `not_evaluated` on κ = 0.5004 and a control separation of 0.0405 against a required 0.20, and the need-to-build link is bounded at CI95 [−0.0156, +0.1125] — consistent with zero, so F042's 0-of-24 is confirmed on a 10× larger instrument, F049, D061) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200; F035 "a tool already serves this" is materially overstated as a cause of death and a third of what it can find lives in a corpus it never read; F036 a web capture can answer HTTP 200 with results unrelated to every query; F037 the screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md`. F039 the demand-side need corpus is 1250 individual requesters rather than a sample of shared needs, so its 0-of-50 measured the corpus and not the screens; F044 "twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin over a population of 20, and 7 of the 18 died of something else; F045 the corpus's authors are a fifth builders (0.222 vs a 0.278 control) and build *less* than their neighbours, so "need-staters are not builders" is false as an absolute and the corpus closure is confirmed rather than withdrawn; F048 a prior-art verdict justified by install counts is not evidence of fit — the row with the strongest evidence of use in the record (437M downloads/month) has documentation establishing nothing about its clause;; F057 E034's per-tag spread of duplicate-closed questions is real, reproducible out of sample at both extremes, and **not attributable** — duplicate closure is a moderator act, so at 3–5 tags per site the tag and the site cannot be told apart (4/10 within-site disjoint pairs against 14/26 cross-site), and the reading it offers, *the answer existed and was not found*, cannot be separated from *a moderator closed it* (CI95 [−0.0774, +0.3075]); its a-priori stratum hypothesis is backwards, and the `Active` tab is the control it beat 4.5× |
| Experimental validation | **Four invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage, **E037's mechanism differentiation** via E041), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029).  No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md`, F039 in `-15.md`, F041 in `-16.md`, F042/F043 in `-17.md`, F044 in `-18.md`, F045 in `-19.md`, F048 in `-20.md`. **The premise behind the dominant kill reason has now been measured five ways over**: coverage (F035), soundness (F034), population (F037), **what its evidence is evidence of (F048: use is not fit, so a download count cannot carry a kill); **F059 the score-tail worklist is one unauthenticated `/search/advanced` query — the candidate is prior art as a URL, and F058's platform-wide reachability claim is refuted**** — and **the premise itself, counted (F044: prior art is 10 of 18 = 0.556, a one-row margin, and the population is 20 rather than twelve)**. No candidate validated and no prior-art verdict falsified |

| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21). A gate's pattern for this repository's split records now reads a numbered split — `decisionindex.py` reported `DECISIONS-SCREENING-2.md` as unlisted while its row was in the table, and the pattern is held to the spellings `DECISIONS.md` uses (`tests/test_decision_row_pattern.py`, T-0063) |
| Implemented (3) | **`stage-lines/`** — `stg`, a non-interactive `git add -p`. `list`, `list --json`, `stage`, `unstage`, `split`; addresses any change by the working-tree line it occupies, splitting adjacent modifications per line. **285 lines of library + a 297-line CLI, standard library only, no install step. 28 tests, all against real git repositories with no mocks** (`python3 -m unittest discover -s stage-lines`). Correctness is anchored to git itself: on a real file in this repository the resulting `.git/index` is **byte-identical** to the one a hand-built patch leaves. **Not released**; its header says `status: draft` |
| Users and adoption | None. No product, no release, no claims. **KILL-Q is answered for `stg`, and the answer is no.** E037 measured demand at 0.016-0.066 of matching GitHub issues through a classifier of unmeasured precision; E043 ran the candidate's stated caller and found the packaging advantage absent (F075); **E045 read that demand evidence itself, row by row, and found 0 of 189 rows is the population the last open claim rested on — all ten automated callers in the need rows name their own diff access (F081)**; and the same reading found the differentiator shipped as two installable command-line tools named inside that same corpus (F082). `stg` is withdrawn as a candidate and remains a correct tool (37/37, byte-identical index, honest exits), unreleased, `status: draft` |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | **138 with an event stream, 137 closed** — `origin session verify` reads the tree on 2026-10-06 rather than a running total; only session 2026-10-06-016 is in flight. Older note: VM 0947's 054 and its past-lease T-0060 claim have since closed |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 1088 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM seven times in two sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`), and in E033 four more: `tally.py` (into `descriptive.py`), `STATE-next-actions.md` (closed items into `STATE-next-actions-closed.md`), `ROADMAP.md` (the infrastructure track into `ROADMAP-infrastructure.md`) and `tests/test_allocation_measurement.py` (the per-day share into `test_allocation_world_share.py`) — and each time the repair was to move material to the file whose invariant it belongs in, never to shorten prose |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

**Nothing is in flight.** E046 measured the artifact against real repository
changes and fixed four defects (E046, F076–F080, D075; full reading in
[`STATE-in-flight-6.md`](STATE-in-flight-6.md)), and E045 then closed the
candidate (E045, F081, F082, D077; reading in
[`STATE-in-flight-7.md`](STATE-in-flight-7.md)). The seat for a candidate is
empty and the emptiness is measured; the one live action is named under
**Next actions**.

## What changed recently

- **Session 2026-10-07-002, VM 0947 (E045, T-0083, F081, F082, D077): the candidate is
  withdrawn, and the kill was in the record's own corpus the whole time.** E045 read all 189
  unique issues in E038's cached demand corpus, one row each, asking the two questions the
  record never asked — who is making the request, and which interface do they lack.
  **29 of 189 are about choosing which lines reach the index; 28 of those carry explicit
  diff access and the 29th GUI-implied; 0 carry none.** All ten automated callers in the
  need rows name their diff access in their own text. **Three of the four issues F064 cites
  are not evidence of what they were cited for**: `sublime_merge#465` says the feature already
  exists and asks for discoverability, `sublime_merge#976` asks for staging *within* a modified
  line (sub-line, which `stg` does not provide), `vim-gitgutter#446` is a person in vim with a
  visual selection. The rule classifier was measured before use per D069: precision 0.372,
  recall 0.552, and its `line-coordinate` class matches `file:line` source citations inside CI
  transcripts — 14 of its 43 rows are unrelated issues. **The same reading killed the
  differentiator**: the 29 rows name **26 distinct repositories**, and two are command-line
  tools taking `stg`'s coordinate that shipped before E037. `gah` (Rust, crates.io) offers
  "line range" staging, documents `stg`'s exact hard case, targets AI coding agents by name and
  ships a Claude Code plugin; `git-hunk` (Python, PyPI) has line-level control and has already
  run the two-arm agent experiment item 0a was built around. Packaging goes with it: all three
  are installable, two ship agent distribution, and `gah` addresses by a content anchor that
  survives line shift — the mechanism E041 measured as absent, arriving from outside. E038's
  prior-art check reported 2 of the 26 because it searched the web and read the corpus's titles.
  **D077** makes the demand evidence of a named population be read row by row before anything is
  built to measure that population. Evidence in
  [`EXPERIMENTS/045-demand-evidence/README.md`](EXPERIMENTS/045-demand-evidence/README.md).
- **Session 2026-10-07-001, VM 0944 (E043, F075, D074): the candidate's last
  surviving claim was three experiments old, rested on a simulation, and did not
  survive a real caller.** Six real agents on six real repositories, scored against
  a hand-written oracle no agent could read: **6 of 6 exact, 3 of 3 with no tool at
  all, and 2 of the 3 that had `stg` on `PATH` declined to use it.** Every no-tool
  agent converged independently on `git diff` → hand-write a minimal patch →
  `git apply --cached`. `stg` is no longer a candidate for release on agent
  usability; it remains a correct tool and that is now the whole claim. **D074**
  requires a candidate whose surviving claim names a caller to run that caller as an
  arm before it is called validated, and requires the arm to be *checked to have
  exercised the tool* — because the `stg` arm shipped a binary that was not on
  `PATH`, three agents reported `command not found`, and **the run still scored 6 of
  6, which reads as confirmation.** Evidence in
  [`EXPERIMENTS/043-real-agent-staging/README.md`](EXPERIMENTS/043-real-agent-staging/README.md).
- **Session 2026-10-06-015 (E041 reconcile/publish) finished: worked.** The 816-test
  suite is green (OK, 651s), doc lint exits 0, and the test-suite and release-check
  gates it had left "running in background" are captured in its command log.

- **E041 (`EXPERIMENTS/041-need-index/`, this VM's second E-number collision, F070-F074, D072/D073): the needs-index premise closes on its own arithmetic.**
  The instrument was first validated on the positive control E040 could not build
  (**77 judged duplicate pairs**, both members in a 44,669-row corpus): G1/G3 pass,
  **G2 fails** (top-1 0.390 titles, 0.143 with body, 0 of 14 no-shared-term pairs,
  median partner rank 10), and G4's separation is confirmed for the first time
  (3.9-27.2x), which is weaker than a same-need index. The scaling premise is
  arithmetically false: `alpha = 0.971`, so 20 qualifying clusters needs n ~ 3,500,
  and the matched control yields 4 of arm A's 8. Full reading in the experiment
  README.
- **Session 2026-10-06-013, VM 0944 (E041): the strongest shell baseline matches `stg`
  exactly and honestly on all tests.** A ~180-line Python script implementing the same
  pair-removes-with-adds splitting logic as `stg` achieves 5/5 on E040 agent-style cases
  and 30/30 on E038's full case matrix (10 cases × 3 diff.context). The kill gate for
  `stg`'s mechanism differentiation is **met** — the practical advantage E040 measured was
  against a naive baseline, not the strongest achievable one. The differentiator is
  packaging (a ready-to-use CLI tool), not the algorithm. KILL-Q remains `not_evaluated`.
- **Session 2026-10-06-012, VM 0944 (E040, F065, D070): the caller's loop
  pits the candidate against what a caller would write without it.** `stg` exact
  and honest **5 of 5**, one call, 10–33 bytes; plumbing silently over-staged
  2 of 5; `filterdiff` exact 2 of 5. KILL-Q still `not_evaluated`.
- **Session 010, VM 0944: session 009 committed and reconciled** — F062/F063/F064
  indexed in FAILURES.md (findings-26 added, findings-25's mislabelled header fixed),
  stagelib split into `stagelib_change`/`stagelib_split`, harvest split into
  `harvest_core`/`harvest_pools`, the third decision-file list gained
  DECISIONS-SCREENING-9.md, 816 tests green, doc lint 0.
- **Session 011, VM 0944 (E039): the honest-exit claim holds at the
  boundary.** Eight real-repository failure modes: `stg` refused loudly exactly
  when it did not stage, 8 of 8, while the naive filterdiff route exited 128 on
  five and silently staged on three. KILL-Q remains `not_evaluated`.
- **Session 009, VM 0944 (E038, F062/F063/F064, D069): the candidate survives, narrower, and
  two of its bugs die with the oracle that could not see them.** Prior art searched properly and
  **found**: `filterdiff --lines=RANGE` and VS Code's `git.stageSelectedRanges` both take the
  coordinate E037 declared absent. A stronger oracle then found `stg` staging *two* lines when
  asked for one — a bug a test had pinned with a comment asserting a false premise — and fixed
  it: **30 of 30** against 12, 12 and 6. The demand side read 195 issues and found a keyword
  classifier with **precision 0.033–0.067**, so the 0.016–0.066 rate is a range across two
  readers, not prevalence. **D069 makes an oracle read the artifact the user receives, and makes
  a classifier's precision be measured before its output is read.** Evidence in
  [`EXPERIMENTS/038-staging-prior-art/README.md`](EXPERIMENTS/038-staging-prior-art/README.md).
- **Session 006, VM 0944 (T-0081, E037, F060/F061, D068): a candidate, built and measured.**
  `git add -p` has no non-interactive equivalent, and that is the wrong thing to fix: the
  operation is available, the *interface* is not, and the difference costs a caller 133 lines.
  `stg` is **6 of 6 against the incumbent's 4 of 6**, and its index is byte-identical to a
  hand-built patch's. **Both numbers superseded by E038 above** — the 6 of 6 was scored by an
  oracle that could not detect over-staging. Evidence in [`EXPERIMENTS/037-line-staging/README.md`](EXPERIMENTS/037-line-staging/README.md)
  and [`stage-lines/`](stage-lines/README.md); the candidate record is
  [`HYPOTHESES-candidates.md`](HYPOTHESES-candidates.md). 8 requests, one of which returned 81 of E034's own harvested ids in
  ascending-score order with the closure label attached. Three corrections to the record,
  and **D067** reorders the work for the next candidate. Evidence in
  [`EXPERIMENTS/036-search-backlog/README.md`](EXPERIMENTS/036-search-backlog/README.md);
  reading in [`STATE-in-flight-3.md`](STATE-in-flight-3.md). **Session 004 (T-0079, F058,
  D065):** E034's `tail` arm reads **4.5×** the `Active` tab's rate, per-tag rates span
  **0.0000 to 0.4300** and both extremes replicate out of sample, and **the per-tag reading
  is `not_established`**. Evidence in
  [`EXPERIMENTS/034-reask-tail/README.md`](EXPERIMENTS/034-reask-tail/README.md).
  Earlier: sessions 001–002,
  VM 0944 (T-0076, T-0077, F053–F056, `EXPERIMENTS/033-question-recurrence/`) — the
  recurrence zeros were checked for what they were a result about, one venue then one
  population, and the pooled bound was refuted.
- **Items 0b, 1 and 2 left the ranked next-action list** — they are this repository's own
  gates and CI, and F031's complaint that maintenance was reading as research was still
  true of a file headed *Ordered by information gained per unit of effort*. **The live items
  are now 0 and 0d, and only 0d is research.** Derivations in
  [`STATE-next-actions-closed.md`](STATE-next-actions-closed.md).

**Earlier per-session highlights** are in [`STATE-history.md`](STATE-history.md), and the
readings that bear on open items are in [`STATE-in-flight.md`](STATE-in-flight.md),
[`STATE-in-flight-2.md`](STATE-in-flight-2.md) and
[`STATE-in-flight-3.md`](STATE-in-flight-3.md). Thirteen readings are closed: F041's third
axis, F035's coverage, F039, F029's refutation, F042's, F043's missing control, F047's
re-read, F053/F054's venue, F055's refutation of the bound they built, F057's two unread
halves, and **F059's**. The 300-line cap has been hit thirteen times and each repair moved
material to the file whose invariant owns it — **twice in this session**.

**E046 changed what "done" means for a candidate's artifact, and D075 carries it.**
Six experiments on `stg` closed with a sentence listing the shapes they had not
tested; read as a work list, that sentence was worth four real defects. D075 makes
a candidate's limitations section a measurement plan to be executed before
release-readiness is claimed. **D077 is the same rule for populations**: a
candidate's own declared population is to be read out of the evidence before
anything is built to measure it. Both are in
[`STATE-in-flight-6.md`](STATE-in-flight-6.md) and
[`STATE-in-flight-7.md`](STATE-in-flight-7.md).

## Infrastructure build (sessions 015–016, earlier)

`tools/origin`, `tools/x`, append-only per-session logs reconciled against git, multi-VM
safety with a two-clone fleet harness (T-0004), the metadata-tagged documentation graph,
and 21 skills vendored in-repo and mirrored. Standard-library Python, no installation step.
Current state: the **Implemented** rows above and
[`ROADMAP-infrastructure.md`](ROADMAP-infrastructure.md).

## Resume procedure

1. Read `MISSION.md`, then this file, then `DECISIONS.md` and `HYPOTHESES.md`.
2. `tools/origin session verify` — is any session unfinished? Finish it honestly.
3. `tools/origin preflight` — do the tooling and the documents still agree?
4. `git status` and `git log --oneline -5` before editing. Preserve anything
   unexpected; another agent or an earlier session may own it.
5. Read the raw evidence for the next experiment, not a summary of it, and continue
   the highest-information one.
## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md); the standing constraints that hold
whichever item is next are in
[`STATE-constraints.md`](STATE-constraints.md). Ordered by information gained
per unit of effort; the top item is:

**Item 0a is closed and its experiment is not run, because the population it
measures does not exist (E045, F081).** The candidate's remaining claim rested on
"an agent that must discover which line changed, with no line number and no
`git diff`", and that population came from E043's harness. Reading the demand
evidence itself — all 189 unique issues in E038's cached corpus, one row each —
gives **29 rows about choosing which lines reach the index, 28 with explicit diff
access and 1 GUI-implied, 0 with none**, and three of the four issues F064 cites
are not evidence of what they were cited for. **Do not rerun the harness.** The
same reading killed the differentiator: those 29 rows name **26 distinct
repositories**, two of them shipped command-line tools that take `stg`'s
coordinate, one of which has already run the two-arm agent experiment item 0a was
built around (F082). `stg` is withdrawn; what remains is a correct tool.

**The single most useful next action, and it is a small one: read the observation
E045 recorded and did not promote.** Two of the 29 need rows are about a
difficulty *none* of the three shipped tools addresses — a formatter or lint hook
that re-stages a whole file and sweeps a partially-staged file's unstaged hunks
into the commit. `nextjs-app-template#95` states the warning its own
`lefthook.yml` carries is **false**; `agent-orchestra#154` is the same class of bug.
That is a correctness failure with a byte-level oracle, named by two independent
repositories, and it is checkable against the real `lefthook` and `pre-commit`
sources in an afternoon. **Two rows is not evidence for a candidate**, so nothing is
promoted here — the action is to establish whether the hook behaviour is real in
the shipped tools, which is a fact that can be read or run, not a screen.

**Beneath that: three rules about the order of work, not experiments.** Stack
Overflow's own search **does** return the score-tail population from one
unauthenticated request with the closure label in the payload (F059) — **the
worklist is closed and nothing is built.** D066 requires a reachability claim to
name the interface surface it enumerated. **D067**: a mechanism-bearing candidate
is tested against its mechanism's existing source first. D074: a candidate whose
surviving claim names a *caller* runs that caller first. **D077**: a candidate
whose surviving claim names a *population* has that population read out of the
evidence — row by row, requester and missing interface per row — before anything
is built to measure it, **because the corpus already on disk named 26 incumbents
where the web search returned 2 (F082)**. Item 0 remains an owner decision. The
seat (0d) is empty and the emptiness is measured four ways (F029, F051, F039,
F059). **The generator is not the blocker; the ordering of the work is.**

**The four candidate-selection axes, and where each now stands.** Prior art,
star-shaped adoption and harvested recurrence cannot carry it (F048 adds that
the prior-art axis's own verdict is not shown to rest on evidence of fit), and
**E045 adds the sharpest instance: the prior-art axis was consulted by a search
that returned 2 of 26 implementations named by the corpus already on disk
(F082)**. The need corpus behind them is 1250 individual requesters each asking
once, 167 of whose 241 shipped *before* they complained (F039, F049). The fourth
axis E034 and E035 added is closed by F059 — three of four orderings cannot return
the population and the fourth is a first-party API route. The numbers behind all
of this are in item 0 and item 0d of
[`STATE-next-actions.md`](STATE-next-actions.md) and, in full, in
[`STATE-selection.md`](STATE-selection.md).

**The gate pattern behind this repository's own red runs is carried in full by
items 1 and 2 in [`STATE-next-actions-closed.md`](STATE-next-actions-closed.md).**
Its one rule is load-bearing enough to repeat: the problem is not gates that are
missing but **gates that exist and are never run**, so the fix is to put a gate in
the command the protocol already points at (T-0045) and to hold it to reading the
property it claims (D025, F013). F055 is the ninth instance of the same shape and
the sharpest, because no gate was involved at all. Full statement in
[`STATE-constraints.md`](STATE-constraints.md).

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified and not to be assumed:** fleet access,
unattended supervision, GPU.

*Honest limitations moved to [`STATE-history.md`](STATE-history.md).*
