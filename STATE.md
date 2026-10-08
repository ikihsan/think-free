<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Verified state

Date: 2026-10-08, Asia/Kolkata. Phase: B — **the one candidate this mission has
produced is withdrawn, and the mission has found the instrument its whole record
was missing.** `stage-lines` / `stg` (E037, E038, F060, F062–F064, D068,
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
artifacts — 0.1615, CI95 [0.134, 0.194] — so the existence bit every
installer, IDE, and checker returns is materially insufficient, and the
pre-declared metadata rule that would have repaired it failed its recall
arm (0.742 against 0.90) because the misses are healthy, popular
projects. No candidate, no prototype (F099, D086).**

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
| Experiments | `000-capabilities` complete; `044-discover-staging` complete (**6/6 exact, `nostg` 3/3 — the discovery-without-diff population does not need `stg` either; candidate closed, F083, D078**); `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); `030-departure-recurrence` complete (H1 `not_evaluated` a third and final time, F050: the fired pair-level statistic measured comment length and rare-token coincidence, its permutation null explains the arm difference, and the length-matched sign flips; A8's held-out separation fires, 0.64 vs 0.036, so the departure-framing population is real and its ruler for recurrence was falsified); ``036-search-backlog` complete (**the worklist is one unauthenticated `/search/advanced` query — 81 of E034's 100 sampled `git` tail ids, ascending, with the closure label in the payload; KILL-R met, F059, D066/D067, T-0080**); ``014-repository-signal-filter` complete (E012's strongest cluster collapses ~200× under the filter it was promised, F033); `015-incumbent-serving` complete (**gate inconclusive**; the premise behind "prior art exists" is now measured directly and **holds in mature vocabularies, fails in young ones** — 4/4 versus 1/4, F034); `016-prior-art-adjudication` complete (both arms met — 6 of 6 positive controls recovered, and 3 of 12 adjudicable judgement kills have no prior art on three corpora, F035; two web instruments refused or answered wrongly first, F036); `017-incumbent-artifact-type` complete (F037); `018-runtime-signal-selection` complete (lead 7's mechanism answered — a stock-SDK feature gap, not a candidate, F038); `019-corpus-person-diversity` complete (F039); `020-copied-config-drift` complete (**gate inconclusive**, copying instructed 687× and duplicated 4.7% of content, F040); `021-copied-artifact-serving` complete (the copy channel is 0.118× the install channel, so the screen's young-vocabulary failure is the world, F041); `022-need-outcomes` complete (gate A1 met at 100% readable, **gate A2 fires at lift 0.703** against a declared floor of 1.0; 58.0% of 1401 stated needs were answered, **0/24 built by the requester**, F042); `023-served-baseline` complete (**the `served` cell now has the control it never had** — 15/38 = 0.395 for need statements against **14/38 = 0.368** for ordinary comments in the same threads, intervals overlapping; two readers on the identical 39 rows agree at **κ = 0.923**, so F042's third number is withdrawn as a demand-side figure, F043, D055); `025-need-staters-builderhood` complete (F042's 0/24 build arm was a *disclosure floor*, so the missing channel was read: **278 of 1250 need-staters = 0.222 have publicly shipped something** against **139 of 500 = 0.278** ordinary commenters in the same stories, ratio 0.80×, intervals overlapping — need-staters are a fifth builders and build *less* than their neighbours, which **confirms** item 0d's closure rather than withdrawing it, F045, D057); `029-need-build-match` complete (**167 of 241 shipped *before* the need, so 69% of the population was never askable**; the reader arm is `not_evaluated` on κ = 0.5004 and a control separation of 0.0405 against a required 0.20, and the need-to-build link is bounded at CI95 [−0.0156, +0.1125] — consistent with zero, so F042's 0-of-24 is confirmed on a 10× larger instrument, F049, D061); `057-unserved-step` complete (**KILL, D080: G1 passes decisively — the same step, *identify an unlabelled physical object/part*, recurs in 3 of 12 sites — but G2 fails, the corpus names Brickognize/RebrickNet/Brickit/BrickLink/Brickset/LEGO Builder, all serving; the E033 score-tail rule does not transfer (51/43, 8/22, 17/5), F089**); `058-se-remaining-sites` complete (**KILL, D080: E057's exact gates on the remaining 38 SE survivors — 76 arms, 11092 rows — fire no step; every G1 cluster reads as a topic, never one step — F090**); `062-nonsw-need-shape` complete (**G4 met — still-open share by age cohort 3.0/0.8/15.2/3.5 percent; 17 of 20 arrival-ranked unremedied needs answered free today by a free assistant; G3 not run, its null branch permanently disarmed — F095–F097, D083, D084**); `061-no-run-worklist` complete (**population gate fired: 0 of 30 `coveragepy`, 0 of 1 `vulture`, 0 of 13 `pytest-cov`, 0 of 30 × 4 vocabulary arms state the need; prototype condition false, no candidate opened — F093, D082**); `056-docs-cli-drift` complete (0 of 3 observed arms drift; **verdict re-labelled as reached over 3 of 5 attempted arms, F094**); `064-remedy-existence` complete (**G5 fired: 93 of 576 near-miss mutations resolve to real, different artifacts — 0.1615, CI95 [0.134, 0.194], ground truth definitional; G6 recall arm failed, 0.742 against a 0.90 gate, because the misses are healthy, popular projects — no candidate, F099, D086**) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200; F035 "a tool already serves this" is materially overstated as a cause of death and a third of what it can find lives in a corpus it never read; F036 a web capture can answer HTTP 200 with results unrelated to every query; F037 the screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md`. F039 the demand-side need corpus is 1250 individual requesters rather than a sample of shared needs, so its 0-of-50 measured the corpus and not the screens; F044 "twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin over a population of 20, and 7 of the 18 died of something else; F045 the corpus's authors are a fifth builders (0.222 vs a 0.278 control) and build *less* than their neighbours, so "need-staters are not builders" is false as an absolute and the corpus closure is confirmed rather than withdrawn; F048 a prior-art verdict justified by install counts is not evidence of fit — the row with the strongest evidence of use in the record (437M downloads/month) has documentation establishing nothing about its clause;; F057 E034's per-tag spread of duplicate-closed questions is real, reproducible out of sample at both extremes, and **not attributable** — duplicate closure is a moderator act, so at 3–5 tags per site the tag and the site cannot be told apart (4/10 within-site disjoint pairs against 14/26 cross-site), and the reading it offers, *the answer existed and was not found*, cannot be separated from *a moderator closed it* (CI95 [−0.0774, +0.3075]); its a-priori stratum hypothesis is backwards, and the `Active` tab is the control it beat 4.5×; F089 E033's score-tail rule does not transfer to a non-developer Stack Exchange population (tail and head rates indistinguishable), and a population with a real recurring step still names four incumbents F099 the existence bit every installer and checker returns is materially insufficient — 93 of 576 plausible near-miss package names resolve to real, different artifacts (0.1615, CI95 0.134–0.194, npm 0.278 / PyPI 0.167 / crates 0.156 / RubyGems 0.063 / Packagist 0.000), and the pre-declared metadata rule that would have repaired it failed its recall arm (0.742 against 0.90) because the 24 misses are healthy, popular, maintained projects (E064-A1, D086) |
| Experimental validation | **Four invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage, **E037's mechanism differentiation** via E041), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029).  No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md`, F039 in `-15.md`, F041 in `-16.md`, F042/F043 in `-17.md`, F044 in `-18.md`, F045 in `-19.md`, F048 in `-20.md`. **Six invention claims have now been tested and none validated; the most recent closed by running it rather than screening it (E047, F084: the shipped hook runners do not sweep a partially-staged file, and one corpus row turned out to exonerate the tool the record blamed).** The premise behind the dominant kill reason has now been measured five ways over: coverage (F035), soundness (F034), population (F037), **what its evidence is evidence of (F048: use is not fit, so a download count cannot carry a kill); **F059 the score-tail worklist is one unauthenticated `/search/advanced` query — the candidate is prior art as a URL, and F058's platform-wide reachability claim is refuted**** — and **the premise itself, counted (F044: prior art is 10 of 18 = 0.556, a one-row margin, and the population is 20 rather than twelve)**. No candidate validated and no prior-art verdict falsified. **The mission's own need corpus is answered by the free alternative and has no buildable tail (F098, D085): the candidate route is retired. **E064 measured the complement of the published hallucination rate and falsified its own pre-declared repair (F099, D086): the existence bit is 16% insufficient, and the metadata rule that would have repaired it cannot separate healthy popular false accepts from the real class — so the deterministic-checker route is closed in both directions, the rate and the repair** |

| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21). A gate's pattern for this repository's split records now reads a numbered split — `decisionindex.py` reported `DECISIONS-SCREENING-2.md` as unlisted while its row was in the table, and the pattern is held to the spellings `DECISIONS.md` uses (`tests/test_decision_row_pattern.py`, T-0063). Concurrent writers of one session's event stream are serialized by an `flock` held across the seq assignment and the append (defect 24: two processes each appended the same seq into a finished session's stream, which reddened CI's `session verify --strict`; falsified as 8 of 8 duplicate-seq rounds on the pre-fix code, 0 of 8 on the repair, plus a two-process regression test) |
| Implemented (3) | **`stage-lines/`** — `stg`, a non-interactive `git add -p`. `list`, `list --json`, `stage`, `unstage`, `split`; addresses any change by the working-tree line it occupies, splitting adjacent modifications per line. **285 lines of library + a 297-line CLI, standard library only, no install step. 28 tests, all against real git repositories with no mocks** (`python3 -m unittest discover -s stage-lines`). Correctness is anchored to git itself: on a real file in this repository the resulting `.git/index` is **byte-identical** to the one a hand-built patch leaves. **Not released**; its header says `status: draft` |
| Users and adoption | None. No product, no release, no claims. **KILL-Q is answered for `stg`, and the answer is no.** E037 measured demand at 0.016-0.066 of matching GitHub issues through a classifier of unmeasured precision; E043 ran the candidate's stated caller and found the packaging advantage absent (F075); **E044 ran the discovery population E043's ceiling named — agents with no line number and no `git diff` — and it is not observed to need the tool either: 6 of 6 exact, `nostg` 3 of 3, every agent doing the discovery by hand first (F083)**; **E045 read that demand evidence itself, row by row, and found 0 of 189 rows is the population the last open claim rested on — all ten automated callers in the need rows name their own diff access (F081)**; and the same reading found the differentiator shipped as two installable command-line tools named inside that same corpus (F082). `stg` is withdrawn as a candidate and remains a correct tool (37/37, byte-identical index, honest exits), unreleased, `status: draft` | **E047 then closed the one observation E045 left behind, and it closed by being run: the hazard is byte-exact and no shipped hook runner produces it (F084, D079)** |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | **170 with an event stream** — `origin session verify` reads the tree rather than a running total; session 2026-10-08-014 finished this landing |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 1088 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM seven times in two sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`), and in E033 four more: `tally.py` (into `descriptive.py`), `STATE-next-actions.md` (closed items into `STATE-next-actions-closed.md`), `ROADMAP.md` (the infrastructure track into `ROADMAP-infrastructure.md`) and `tests/test_allocation_measurement.py` (the per-day share into `test_allocation_world_share.py`) — and each time the repair was to move material to the file whose invariant it belongs in, never to shorten prose |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. **The row went red once more, on 2026-10-07, and the cause was older still:** `37b645d` failed `release check` on the 3.12 row, four split records tracked but never classified and the manifest's three state rows duplicated from a careless merge. Repaired at `a245c34` — which itself read red only because the session committing its stream into the tree made the record-integrity gate fail on an unfinished session; its stream committed, `19c03e0` ran **green on all seven rows, `observed` 2026-10-07**. |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

**Nothing is in flight.** Session `2026-10-08-014` (this VM) ran
E064 to a recorded verdict and landed it: **G5 fired — 93 of 576
plausible near-miss package names resolve to a real, different
artifact (0.1615, CI95 0.134–0.194), so the existence bit every
installer and checker returns is materially insufficient — and G6
failed its recall arm (0.742 against a 0.90 gate), because the
false accepts the pre-declared metadata rule misses are healthy,
popular, maintained projects (`jinja2-cli`, `sqlalchemy-utils`,
`django-click`).** No candidate, no prototype (F099, D086). The
full reading is
[`EXPERIMENTS/064-remedy-existence/README.md`](EXPERIMENTS/064-remedy-existence/README.md),
and every number reproduces from the committed bytes via
`outcome.py`.

**The seat for a candidate is still empty, and E064 does not fill
it.** What E064 leaves is a *measured failure mode*, not a
direction: the separator that remains is semantic ("does this
package do what was asked"), which is the named alternative's job
— a model call — and it takes the cost and determinism advantage
that justified a deterministic checker with it.

**Task-list hygiene, recorded rather than papered over.** T-0087
(E055) is landed as F088/D081 but its row still reads `claimed`:
its verify gate (`EXPERIMENTS/055-index-postcondition/run.py
--verify`) refuses on this VM's git 2.25.1 (the git-hunk arm
needs ≥ 2.28), so it was not flipped to done from here. T-0083
(E045) and T-0085 (E054) are the same shape — landed work under
stale claims from interrupted sessions.

**The one open question E064 names, as a fresh observation and
not a build:** the installers' own guards key on names that do
*not* resolve (npm's typo protection, pip's warnings), so the 24
healthy-metadata false accepts are exactly the population those
guards cannot see. Whether that gap is observed anywhere, and
whether a "did you mean a different project" warning has a
population that wants it, is untested — and per D080 any
successor session starts from that observation, not a prototype.

The readings that bear on open items are in
[`STATE-in-flight.md`](STATE-in-flight.md) through
[`STATE-in-flight-8.md`](STATE-in-flight-8.md). One rule
survives into every session: **rebase a moving base with
`origin sync land`**, because a hand-run rebase records nothing
and its paths are then attributed to whoever holds the tree
(T-0053).

## What changed recently
- **Session 2026-10-08-014, VM 0944: E064-A1, F099, D086.**
  E064 re-aimed itself at the quantity the prior art does not
  report (AMENDMENT-1 withdrew G2/G3 as prior art — the
  hallucinated-name rate and the resolve-against-the-registry
  check are published in arXiv:2501.19012) and measured the
  false-accept rate of existence-checking: **93 of 576
  near-miss mutations of real package names resolve to real,
  different artifacts — 0.1615, CI95 [0.134, 0.194]** (npm
  0.278, PyPI 0.167, crates 0.156, RubyGems 0.063, Packagist
  0.000), ground truth definitional, zero missing observations.
  The pre-declared metadata rule failed its recall arm (69/93 =
  0.742 against a 0.90 gate; specificity 29/30 = 0.967 passed)
  because the 24 it misses are healthy, popular projects. No
  candidate, no prototype. The metadata run transiently lost all
  NuGet and all Homebrew rows; they were re-fetched, recovered,
  and the recovery is recorded in the tree.
- **Session 2026-10-08-013, VM 0944: E063, F098, D085, and defect 24 repaired.**
  E063 ran the E062 answerability instrument on the mission's own need corpora —
  E038's 189 GitHub issues, the 1401-row HN corpus — and the route is retired:
  arm A served share 0.676, arm B 0.969, `unserved-open` 0 of 103 rows, and 12
  of 71 arm A rows state nothing under a trigger phrase. Defect 24: two
  overlapping `session finish` runs grew one event stream twice (181 lines, 162
  numbers); repaired with an flocked allocator and a `.finish.lock`, session
  008's stream deduped row-by-row and the repair is recorded in its session.
- **Session 2026-10-08-009, VM 0947: E059, E060, F091, F092.** Two fresh-observation probes under D080, both killed at their gates. E059: pip-name vs import-name mismatch is real on wheels (M1 22 of 93) but served — namespace families, convention-derivable renames, and a known short unpredictable core absent from the sample, reverse mapping prior-arted; nothing built. E060: static version badges in README do not exist — 0 of 45 top-star Python/Rust/JS repos carry one; nothing to measure drift on.
- **Session 2026-10-08-006, VM 0947: E058, F090.** E057's exact
  protocol run on the 38 Stack Exchange survivors E057 skipped (same
  stratum, arms, instrument, gates, hand-read). 76 arms, 11092 rows,
  7022 requesters. G1's 42 nominal clusters all read as topics, never
  one step, so G2/G3 were never reached; KILL. The channel-level null
  now covers the whole survivor set: one class of recurring step
  (unlabelled-object identification, E057's three), and it is served.
- **Session 2026-10-08-005 landed (VM 0947): E057, F089.** Fresh observation
  per D080: 12 Stack Exchange sites, 24 arms, 3992 rows. G1 passed
  decisively (the same step recurs in 3 independent sites), G2 failed (the
  corpus's own names all serve it), pre-registered rule: KILL, nothing built.
  Corrections carried: the E033 score-tail rule does not transfer, G1 was a
  free pass in this corpus, and the first linkage instrument returned a clean
  zero until diagnosed.
- **Session 2026-10-08-006, VM 0944: a fresh observation outside software,
  and the mission's missing instrument (E062, F095–F097, D083, D084).**
  Declared to test whether the empty seat is a property of human unmet need or
  of its *software sample route*. Arm 1 retrieved **1200 rows across six
  non-software Stack Exchange sites**, all with bodies and outcome fields;
  G1 met, and `total_count` recorded as a missing observation on this route
  (D082). **G4 met**: the still-open share by age cohort is 3.0 / 0.8 / 15.2 /
  3.5 percent, a 14.4-point gap against a declared 10 — reported with its
  non-monotonicity and right-censoring, no mechanism claimed. **G3 was not run
  and its null branch is permanently disarmed** (F095, D083): the rubric's
  clause 1 disqualifies needs that consume an input the requester holds, which
  in a physical domain is nearly every row, and that protocol's null branch was
  declared to close the find-a-new-venue route **permanently**. It was caught
  by reading the whole 110-row no-remedy population before labelling any of it.
  In its place: the top 20 unremedied rows **by arrival**, each attempted
  against the strongest accessible alternative. **17 of 20 are answered in full
  by a free general assistant today** (F096). The 5% that resists is the bike
  serial nobody recorded in 2001 and the per-model spec sheets — a data
  absence, not a software problem (F097). **The candidate source does not move
  out of software, and the find-a-new-venue route is deferred with its reason
  recorded rather than closed**, because the branch that would have closed it
  was an artifact of the instrument.
- **Session 2026-10-08-005, VM 0944: a fresh observation closed on its
  own declared gate, and it closed the prototype condition (E061, F093,
  D082).** The goal was conditional — *read a project's tests statically,
  locate what a real test run reports unexercised, prototype only if a
  requester wants the substitute*. D077 puts the population first, so E061
  ran the population gate and declared it before reading a row: **0 of 30
  `coveragepy` rows, 0 of 1 `vulture`, 0 of 13 `pytest-cov`, 0 of 30 in
  each of four vocabulary arms state the declared need.** All 30
  `coveragepy` rows are coverage *when it ran* — lines executed and
  recorded missed under asyncio, `concurrency=multiprocessing`, pytest's
  assertion rewriting, dotted `--source` — plus 5x/20x/77x overhead and
  13 s start-up. The closest row (`#2211282948`, 10 comments) is answered
  by running coverage with `--source`. **No prototype was written**, the
  mechanism gate was never run, and the candidate was not opened.
  **Not closed:** coverage that under-reports lines that ran is a real,
  unsolved population, and whether a static read substitutes for the run
  is untested. Two of ten arms returned **422** (a misspelled `repo:`
  owner) and produced no observation, which is now **D082**: a missing
  observation is never a zero and never a denominator. That correction
  was applied backwards to E056's own verdict (F087), which had been
  written over 3 of 5 arms (F094).

Older per-session highlights (2026-10-07-003, the 2026-10-06 sessions, items 0b/1/2 leaving the ranked list) are in [`STATE-history.md`](STATE-history.md), and the readings that bear on open items are in [`STATE-in-flight.md`](STATE-in-flight.md), [`STATE-in-flight-2.md`](STATE-in-flight-2.md), [`STATE-in-flight-3.md`](STATE-in-flight-3.md) and [`STATE-in-flight-8.md`](STATE-in-flight-8.md). The 300-line cap has been hit fourteen times; each repair moved material to the file whose invariant owns it.

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
[`STATE-constraints.md`](STATE-constraints.md). **The seat for a candidate is empty
and every derived action from the last candidate is spent.** Item 0a is closed twice —
by the run (E044, F083, D078) and by reading the demand evidence (E045, F081, F082) —
and item 0f is closed by E047 (F084, D079), with E048 (F085) answering its follow-on:
in every configuration except lefthook without `stage_fixed` the
formatter/commit disagreement is loud or blocked, and that one silent shape ships its
remedy and trips any CI format gate. **Nothing to build.** The fresh observation the
reload point asked for is now done (E062), and it returned the instrument rather than
a candidate.

**That re-run is done, and it retired the route.** E063 ran the E062
answerability instrument on E038's 189 GitHub issues and the 1401-row HN
corpus: arm A served share **0.676** (48/71; 0.814 over the 59 rows that
state a need), arm B **0.969** (31/32), and `unserved-open` — the only label
that can open a candidate — **0 of 103 rows** (F098). Every resistant row
resists because the data was never recorded, because the remedy is human work
or an institution, or because the row states no need at all. D085 retires the
trigger-phrase harvest as a candidate source. A statement of need is now
evidence of a statement, never of a service gap. Any future exploration starts
from a fresh observation of a need this harvest cannot show (D080), and the
find-a-new-venue route stays deferred with its reason recorded (F095). **The
candidate seat stays empty, and what remains is the instrument (E062's
`view_count` + `unserved-open` labeller), the repaired record (defect 24), and
one open seat: T-0087, still unwritten.**

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified and not to be assumed:** fleet access,
unattended supervision, GPU.

*Honest limitations moved to [`STATE-history.md`](STATE-history.md).*
