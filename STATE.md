<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Verified state

Date: 2026-10-06, Asia/Kolkata. Phase: B — the prior-art screen is measured, the recurrence
bound is refuted, and the score-tail backlog is confirmed real, unreachable and **not a
rescue**. **No product selected.**

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
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); `030-departure-recurrence` complete (H1 `not_evaluated` a third and final time, F050: the fired pair-level statistic measured comment length and rare-token coincidence, its permutation null explains the arm difference, and the length-matched sign flips; A8's held-out separation fires, 0.64 vs 0.036, so the departure-framing population is real and its ruler for recurrence was falsified); ``014-repository-signal-filter` complete (E012's strongest cluster collapses ~200× under the filter it was promised, F033); `015-incumbent-serving` complete (**gate inconclusive**; the premise behind "prior art exists" is now measured directly and **holds in mature vocabularies, fails in young ones** — 4/4 versus 1/4, F034); `016-prior-art-adjudication` complete (both arms met — 6 of 6 positive controls recovered, and 3 of 12 adjudicable judgement kills have no prior art on three corpora, F035; two web instruments refused or answered wrongly first, F036); `017-incumbent-artifact-type` complete (F037); `018-runtime-signal-selection` complete (lead 7's mechanism answered — a stock-SDK feature gap, not a candidate, F038); `019-corpus-person-diversity` complete (F039); `020-copied-config-drift` complete (**gate inconclusive**, copying instructed 687× and duplicated 4.7% of content, F040); `021-copied-artifact-serving` complete (the copy channel is 0.118× the install channel, so the screen's young-vocabulary failure is the world, F041); `022-need-outcomes` complete (gate A1 met at 100% readable, **gate A2 fires at lift 0.703** against a declared floor of 1.0; 58.0% of 1401 stated needs were answered, **0/24 built by the requester**, F042); `023-served-baseline` complete (**the `served` cell now has the control it never had** — 15/38 = 0.395 for need statements against **14/38 = 0.368** for ordinary comments in the same threads, intervals overlapping; two readers on the identical 39 rows agree at **κ = 0.923**, so F042's third number is withdrawn as a demand-side figure, F043, D055); `025-need-staters-builderhood` complete (F042's 0/24 build arm was a *disclosure floor*, so the missing channel was read: **278 of 1250 need-staters = 0.222 have publicly shipped something** against **139 of 500 = 0.278** ordinary commenters in the same stories, ratio 0.80×, intervals overlapping — need-staters are a fifth builders and build *less* than their neighbours, which **confirms** item 0d's closure rather than withdrawing it, F045, D057); `029-need-build-match` complete (**167 of 241 shipped *before* the need, so 69% of the population was never askable**; the reader arm is `not_evaluated` on κ = 0.5004 and a control separation of 0.0405 against a required 0.20, and the need-to-build link is bounded at CI95 [−0.0156, +0.1125] — consistent with zero, so F042's 0-of-24 is confirmed on a 10× larger instrument, F049, D061) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200; F035 "a tool already serves this" is materially overstated as a cause of death and a third of what it can find lives in a corpus it never read; F036 a web capture can answer HTTP 200 with results unrelated to every query; F037 the screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md`. F039 the demand-side need corpus is 1250 individual requesters rather than a sample of shared needs, so its 0-of-50 measured the corpus and not the screens; F044 "twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin over a population of 20, and 7 of the 18 died of something else; F045 the corpus's authors are a fifth builders (0.222 vs a 0.278 control) and build *less* than their neighbours, so "need-staters are not builders" is false as an absolute and the corpus closure is confirmed rather than withdrawn; F048 a prior-art verdict justified by install counts is not evidence of fit — the row with the strongest evidence of use in the record (437M downloads/month) has documentation establishing nothing about its clause;; F057 E034's per-tag spread of duplicate-closed questions is real, reproducible out of sample at both extremes, and **not attributable** — duplicate closure is a moderator act, so at 3–5 tags per site the tag and the site cannot be told apart (4/10 within-site disjoint pairs against 14/26 cross-site), and the reading it offers, *the answer existed and was not found*, cannot be separated from *a moderator closed it* (CI95 [−0.0774, +0.3075]); its a-priori stratum hypothesis is backwards, and the `Active` tab is the control it beat 4.5× |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029).  No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md`, F039 in `-15.md`, F041 in `-16.md`, F042/F043 in `-17.md`, F044 in `-18.md`, F045 in `-19.md`, F048 in `-20.md`. **The premise behind the dominant kill reason has now been measured five ways over**: coverage (F035), soundness (F034), population (F037), **what its evidence is evidence of (F048: use is not fit, so a download count cannot carry a kill)** — and **the premise itself, counted (F044: prior art is 10 of 18 = 0.556, a one-row margin, and the population is 20 rather than twelve)**. No candidate validated and no prior-art verdict falsified |

| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21). A gate's pattern for this repository's split records now reads a numbered split — `decisionindex.py` reported `DECISIONS-SCREENING-2.md` as unlisted while its row was in the table, and the pattern is held to the spellings `DECISIONS.md` uses (`tests/test_decision_row_pattern.py`, T-0063) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | **110 with an event stream, 108 closed** — counted from the tree rather than from a running total, because the two VMs had been counting different bases. An unfinished session on either VM is reported as in flight rather than as a failure (D027); VM 0947's 054 is the live one and its T-0060 claim is past the 12h lease |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 1088 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM seven times in two sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`), and in E033 four more: `tally.py` (into `descriptive.py`), `STATE-next-actions.md` (closed items into `STATE-next-actions-closed.md`), `ROADMAP.md` (the infrastructure track into `ROADMAP-infrastructure.md`) and `tests/test_allocation_measurement.py` (the per-day share into `test_allocation_world_share.py`) — and each time the repair was to move material to the file whose invariant it belongs in, never to shorten prose |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

**The fifth demand-side generator returned positives, and the next one found out where they
are — and that they were not being overlooked** (`EXPERIMENTS/035-unanswered-surface`,
F058, D065, T-0079). E035 spent **zero quota** re-reading E034's committed bytes and
changed four things. **The premise is falsified as a rescue**: within the tail arm the
duplicate rows are viewed *more* than their neighbours — **251 against 193**, at a median
age of **8.49 yr** — so this is an eight-year-old backlog, not a findability failure. **The
`Active` and `tail` arms do not intersect** for two of eight tags, so the 4.5× is about
**membership**, not density. **No Stack Overflow page offers the ordering**: 409,639 bytes
of first-party rendered HTML list `Newest / Active / Votes / Frequent / Trending /
Bounties / Unanswered` and contain **0** occurrences of `order=asc`, `oldest` or
`ascending`. **And D6's remedy was aimed at the wrong constraint** — between-tag excess
variance is **+0.0420 within `stackoverflow` alone**, equal to the pooled **+0.0417** — so
item 0e's 30-request fix, ranked the mission's top action, was not the binding one.

**Its own gates did not close it either.** `/questions/unanswered`, the surface
`tab=Unanswered` is built on, **excludes the population by definition**: **0** of E034's
224 known duplicate-closed ids appear in its 2050 rows, while **98 of 186** tail duplicates
meet its advertised `is_answered == false` criterion and are still absent. **D065**: the
overlap gate fired at 0.0283, the firing was definitional, and its declared branch is
**not taken**. **U2 is `not_evaluated`, not zero** — `closed_reason` is unreadable on that
route, so the density comparison needs an API key this host does not have. **A prototype
exists and runs offline on committed bytes.** Evidence in
[`EXPERIMENTS/035-unanswered-surface/README.md`](EXPERIMENTS/035-unanswered-surface/README.md);
readings in [`STATE-in-flight-2.md`](STATE-in-flight-2.md) and
[`STATE-in-flight-3.md`](STATE-in-flight-3.md).

**The fourth demand-side generator closed on its own premise, not on prior art**
(`EXPERIMENTS/031`, F051, D062, T-0075). Departure accounts state a missing capability
at nearly twice the base rate of ordinary same-story comments (0.347 vs 0.181, CI95
[0.0224, 0.3024]) — below the declared 0.20 margin, and **the seek stratum is
indistinguishable from the move stratum at 0.347 vs 0.347**, so "unfilled" is not a
property this population has. **0 of 100** clause pairs recur, every instrument gate
passing (κ = 0.7189, A6 20/20 and 0/10). Its declared linkage rule could not fire at all
(4 candidate pairs against a chance expectation of 4.9), the mirror image of F010; D062
governs linkage rules from here.

**And the bound those zeros built was then refuted by the platform's own judgement**
(F053, F054, **F055**; `EXPERIMENTS/032-venue-recurrence/`,
`EXPERIMENTS/033-question-recurrence/`). F053 found all **3,856** comment ids behind the
five zeros were Hacker News and four of the five experiments re-read E012's single
1401-comment file; F054 changed the venue and held the pooled bound at **0.0223**; **F055
then measured recurrence where it is decided by other people** — Stack Exchange's own
duplicate closure, 1000 questions, **0.0540 CI95 [0.0416, 0.0698]**. **The bound is
refuted, and the zeros were a stratum effect**: the top 60 by score, which is what
`sort=votes` draws, contains **0** duplicate closures against a mean of 3.37 over all 941
sliding windows, and the rate is **4.5× higher in the bottom score tertile**. Statement,
and what it does not license, in [`STATE-in-flight-2.md`](STATE-in-flight-2.md).

**Five closed readings, kept here as pointers only — each one's full text is in the file
named, and none of them changes what is next.** (i) **F037's reconciliation for the supply
question is withdrawn:** the copies are adapted, not duplicated, so near-zero install
readings are not an invisible channel (F040, `EXPERIMENTS/020`); drift is `inconclusive`.
(ii) **F049 followed the 1250 need-starters forward**: of the 241 with a public `Show HN`
item, **167 shipped before they stated the need** and only 74 after, and the reader arm is
`not_evaluated` (κ = 0.5004), so the need-to-build link bounds at **[−0.0156, +0.1125]**
— F042's 0-of-24 is confirmed on a 10× larger instrument. (iii) **The candidate generator
was refuted**: 1401 harvested need statements, 50 drawn by rule, **0 survived**, and its
strongest cluster collapsed ~200× (F029, F033). (iv) **The prior-art screen measured on
coverage**: 6 of 6 positive controls recovered, 3 of 12 adjudicable kills have no prior art,
and **corpus carriage is the result** — GitHub's index carried every verdict the code corpora
carried (F035, F036, D050). (v) **Its population came out against it**: 14 of 18 young
rows are executable code, documents carry a median 6,072 stars against 566, and the most
-starred tool there is installed 363 times a month (F037). Readings in
[`STATE-in-flight-2.md`](STATE-in-flight-2.md) and
[`STATE-in-flight.md`](STATE-in-flight.md).

**Four closed tooling findings, kept as pointers because they are the standing reasons a
session's own gate can be green and its records still false.** A restated experiment number
was false and the obvious gate is blind to it (defect 22, T-0056, D047, F024);
identifier collisions between two VMs are closed (T-0030, T-0031) but **the work-collision
case still has no detector**, so read the remote task list first
([`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md)); a
gate belongs in the one command the protocol tells every agent to run (T-0045); and a test
can read a clock the code does not (defect 15, T-0044). Accounts:
[`STATE-defects.md`](STATE-defects.md),
[`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md). **One rule survives:**
rebase a moving base with `origin sync land`, because a hand-run rebase records nothing and
its paths are then attributed to whoever holds the tree (T-0053; sessions 040 and 012 hit
that ceiling seven and twice).

## What changed recently

- **Session 004, VM 0944 (T-0079, F058, D065): four reads of committed bytes settled
  reachability, refuted the frame, and re-scoped the top item for zero quota.** Evidence in
  [`EXPERIMENTS/035-unanswered-surface/README.md`](EXPERIMENTS/035-unanswered-surface/README.md);
  reading in [`STATE-in-flight-2.md`](STATE-in-flight-2.md). **Session 003 (T-0078, F057,
  D063/D064):** E034's `tail` arm reads **4.5×** the `Active` tab's rate, per-tag rates span
  **0.0000 to 0.4300** and both extremes replicate out of sample, and **the per-tag reading
  is `not_established`**. Evidence in
  [`EXPERIMENTS/034-reask-tail/README.md`](EXPERIMENTS/034-reask-tail/README.md).
  Earlier: sessions 001–002,
  VM 0944 (T-0076, T-0077, F053–F056, `EXPERIMENTS/033-question-recurrence/`) — the
  recurrence zeros were checked for what they were a result about, one venue then one
  population, and the pooled bound was refuted.

**Earlier per-session highlights** are in [`STATE-history.md`](STATE-history.md), and the
readings that bear on open items are in [`STATE-in-flight.md`](STATE-in-flight.md) and
[`STATE-in-flight-2.md`](STATE-in-flight-2.md). Eleven readings are closed: F041's third
axis, F035's coverage, F039, F029's refutation, F042's, F043's missing control, F047's
re-read, F053/F054's venue, F055's refutation of the bound they built, and F057's two
unread halves. The 300-line cap has been hit twelve times and each repair moved material
to the file whose invariant owns it.

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

**The top item is now the one alternative this line never tested: a person's own search
box.** The screen that killed most candidates has been measured on every axis and each
measurement came out against it — F034 soundness, F035 coverage, F037 composition, F040
distribution, F048 what-its-evidence-is — and what changed is the method, not a candidate
(D050, D051). **Item 0e's declared next action is superseded** (F058): its premise is
falsified as a findability failure, its ordering is offered by no surface, and its remedy
was aimed at a constraint that was not binding. What is left is the honest question about
the population E034 found — an eight-year-old backlog, 16.5% duplicate-closed, invisible to
every ordering Stack Overflow offers — and **whether Stack Overflow's own search already
returns it.** That is reachable from this host while the site itself is not.

**The need corpus those survivors came from is 1250 individual requesters each asking
once**, and 167 of the 241 who shipped anything shipped *before* they complained (F039,
F049); the "about a third were served" figure was uncontrolled and its control reads
**0.368 against the need arm's 0.395** (F043). **Choosing what the mission selects
candidates on is still an owner decision**, narrowed to: none of the three original axes —
prior art, star-shaped adoption, harvested recurrence — can carry it, and F048 adds that
the prior-art axis's own verdict is not shown to rest on evidence of fit. E034 and E035
add a fourth that is neither an axis nor an audit: **a per-domain rate measured on
someone else's label, against the orderings that domain's own readers actually see** — and
E035's contribution is that **three of those four orderings cannot return the population at
all**, so the rate measures a surface nobody is on.

**The gaps in that pattern, both found by colliding with it, and one in the record rather
than in a red run**, are closed and carried in full by item 2 of
[`STATE-next-actions.md`](STATE-next-actions.md): rule 7 read three of the four places a
number is written, so two VMs took **defect 7** in the same hour (T-0036) and two of five
decision records were false while every gate passed (T-0042). One entry point reads the
sources now, and its residual ceiling is written down: a repeated number is detectable, a
dropped one is not.

**F055 is the ninth instance of that shape and the sharpest, because no gate was involved
at all:** a selection rule declared for one reason — `sort=votes`, because "elaborated need
statements live there" — selects for *answered* questions, and the stratum it draws is
**4.5× poorer in the thing being measured**. Full statement and the rule it generalises
to, in [`STATE-constraints.md`](STATE-constraints.md).
**The pattern in the red runs of 2026-10-04 is not "gates are missing" but gates that exist
and are never run**: a task's `verify` omits the one gate its change can break, a fixture
omits the clock the code reads, a split leaves one reader unwired. T-0045's fix is the
general one — put the gate in the command the protocol already points at, so there is
nothing to forget. A gate must also read the property it claims to check and be falsified
against the defect's own bytes (D025, F013); ten gates work that way, the two newest being
a restated experiment number held to its artifact by the number's *shape* (T-0056, F024,
defect 22) and E034's arms, whose 11 mutations are each caught. **Line caps are the
standing friction**, and each repair moved material to the file whose invariant owns it —
this session four times for E034. `STATE-defects.md` cannot be split inside its own list,
so that split is a task.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development machine:
12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy present, SciPy/pytest/Z3
absent; `gh` absent. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and pushes via
the GitHub App as `Ihsan Ai Server Bot`. **Unverified and not to be assumed:** fleet access,
unattended supervision, GPU.

## Honest limitations of this state

- All six investigation roles are sealed (`RESEARCH/A.md`–`F.md`), and
  `RESEARCH/SYNTHESIS.md` compares them. The synthesis is `inferred` from prose: it
  reorders and screens existing claims and measures nothing itself.
- **E023's null is a resolution limit, not a proof of zero.** 38 rows per arm on one day
  cannot resolve a need effect below roughly 0.2, the control arm is defined by *not
  matching the trigger vocabulary*, and `served` is a label rather than a measurement —
  a reply naming an artifact is a pointer — which both arms carry equally.
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
  **F044 measured that claim: prior art is the plurality of kill reasons, not the majority
  — 10 of 18 = 0.556, a one-row margin, and every prior-art row moved to another category
  kills the majority reading** (count and sensitivity in
  [`STATE-in-flight-2.md`](STATE-in-flight-2.md)). Seven of the 18 died of something else,
  and a verdict needs more than one phrasing (F030).
- **The backlog is not a candidate yet, and the reason is now different from F057's.**
  Its per-tag spread is real and reproducible, its premise as a *rescue* is **falsified**
  (F058: the duplicate rows are viewed more than their neighbours, 251 against 193, at a
  median age of 8.49 yr), and **no ordering Stack Overflow offers can return it** — the
  `Active` arm does not intersect the tail for two of eight tags, no page carries an
  ascending-score control, and `tab=Unanswered` excludes closed questions by definition
  (0 of 224 known duplicate-closed ids; D065). **Nothing has measured whether anyone wants
  it surfaced**, which is the whole adoption question, and E035's own density gate is
  `not_evaluated` because the label is unreadable without an API key.
- The screen's own weakness: decidable from prose, so cheap and also vulnerable to
  a persuasive report. It guarantees the *next* experiment is worth running.
- **The turn outward happened, and it is uneven.** Five consecutive experiments
  audited this repository's own instruments before E020 asked about the world; since
  then E022–E029 have asked about people, and **three of E029's own findings were
  defects in its instrument**. A run can be about the world and still mostly measure
  the measurer, so the two have to be counted separately (F048, F049, D061).
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen,
  and the session-by-session account lives in the two history files named above.
