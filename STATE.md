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
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021); `012-candidate-harvest` complete (0 of 50 needs survive the screens, F029, D049); ``014-repository-signal-filter` complete (E012's strongest cluster collapses ~200× under the filter it was promised, F033); `015-incumbent-serving` complete (**gate inconclusive**; the premise behind "prior art exists" is now measured directly and **holds in mature vocabularies, fails in young ones** — 4/4 versus 1/4, F034); `016-prior-art-adjudication` complete (both arms met — 6 of 6 positive controls recovered, and 3 of 12 adjudicable judgement kills have no prior art on three corpora, F035; two web instruments refused or answered wrongly first, F036); `017-incumbent-artifact-type` complete (F037); `018-runtime-signal-selection` complete (lead 7's mechanism answered — a stock-SDK feature gap, not a candidate, F038) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. F025 a red-run cause was made readable but never explained; F026 this mission's own tooling is prior art as a candidate; F027 every project in that niche has zero users; F028 the flat adoption tail is vocabulary age, not niche; F029 a live corpus of 1401 need statements yielded 0 of 50 candidates that survive the screens; F030 a prior-art verdict from one search query is wrong in both directions; F033 a repository count without a relevance filter overstates prevalence by ~200; F035 "a tool already serves this" is materially overstated as a cause of death and a third of what it can find lives in a corpus it never read; F036 a web capture can answer HTTP 200 with results unrelated to every query; F037 the screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). **The mission's own tooling was tested as a candidate for the first time and is prior art — mechanism six weeks old, process discipline independently reinvented (F026), and every project in the niche has zero users (F027).** **Two more candidate lines were opened and closed in one day**: this repository's own tooling as a byproduct candidate (F026) and a live need corpus as a generator (F029). **The premise behind the dominant kill reason has now been measured three ways over — its coverage (F035: 4 of 12 served verdicts were reachable only on the open web), its soundness (F034: sound in mature vocabularies, unsound in young ones), and its population (F037: that young population is real code, so the failure is not an artefact)**. No candidate validated. Findings F001-F008 in `FAILURES-findings.md`, F009-F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md`, F022-F025 in `FAILURES-findings-5.md`, F026+ in `FAILURES-findings-6.md`, F029/F030/F031 in `FAILURES-findings-9.md`, `-10.md`, `-8.md`, F033 in `-11.md`, F034 in `-12.md`, F035/F036 in `-13.md`, F037/F038 in `-14.md` |

| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 74 with an event stream, 73 closed — counted from the tree, not from a running total, because the two VMs had been counting different bases. Newest: VM 0944's sessions 030 and 031 (T-0048, T-0049) and VM 0947's 030 (T-0047), all `worked`; an unfinished session on either VM is reported as in flight rather than as a failure (D027) |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 551 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM five times in three sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, and in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`) — and each time the repair was to move material to the file whose invariant it belongs in |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `ac4a12b`'s 7 check-runs at `ac4a12b4b192`** — and the three failures of `37219755262` and `37220040091`, which were on identical bytes and read as three unrelated faults, have not recurred in six full suite runs since. **They were never explained, only made readable:** T-0057 found the `Tests` step's annotation window took the first twelve lines of a failure block, and the exception is the last line of a traceback, so every traceback past twelve frames annotated a cause-free failure (defect 23, F025). The window is now anchored on the end of the block. The cause remains `untested`, and `make_fleet` builds a bare remote plus two clones per test class — the only thing here that scales with the number of tests. **All seven rows were red again on 2026-10-05, and neither cause was new work: both were inherited.** `test_allocation_measurement` re-derived F025's two-day claim against the *first and last* day of a history that has since grown a third, so a five-commit day decided a two-day finding; and its synthetic-history fixture carried the identity in `git()` but built the commits with an env holding only the dates, so `git commit` exited 128 on a runner with no configured identity while passing on a VM that has one — F019's shape, on identical bytes, and it was the whole class erroring. Both are repaired, both are falsified against their own bytes, and **all seven rows are green again on `4d85e02`, `observed` 2026-10-05** — the first green run since `ac4a12b`. |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

**The candidate generator was tested against a live corpus and refuted, and
its strongest cluster then failed the filter it was promised** (`EXPERIMENTS/012`, `EXPERIMENTS/014`, D049, F029, F033).
1401 practitioner need statements harvested from Hacker News comments since
2024-01-01; 50 drawn by a stated rule; **0 survived** — 38% prior art, 30% no
mechanism, 24% not software, 8% needing hardware, against the prior generator's
own 3-of-16. The corpus cannot supply recurrence: term recurrence returns only
function words. E014 applied the repository-signal half of D049 and the
"5805 issues / 28 repositories" cluster collapsed to 15 issues across 9
agent-labeled repositories — a complaint inside a dozen agent-project trackers,
not a cross-project problem (F033). F030: a prior-art verdict from one search
query is wrong in both directions.

**That verdict has now been measured on coverage, and it is the mission's weakest
instrument** (`EXPERIMENTS/016`, D050, F035, F036). E016 re-adjudicated E012's 19
prior-art kills on three corpora with six positive controls, phrasings written
before the first fetch. **Both arms met: 6 of 6 controls recovered served, and 3
of 12 adjudicable judgement kills have no prior art** — and one row decides that
count, so `results.json` carries both numbers. **Corpus carriage is the
transferable result:** GitHub's index carried every verdict the code corpora
carried, the registries carried none on their own, and the open web carried 4
served verdicts two code corpora returned nothing for. Bing answered HTTP 200 with
ten well-formed results per query, all unrelated (F036). D050 puts the three
unserved needs into a mechanism step and narrows F029 rather than reversing it:
**they are need statements, not candidates, and an absence of a hit on three
corpora is the absence of a hit.**

**The third axis is now measured too, and it came out against the alternative**
(`EXPERIMENTS/017`, F037). One explanation for F034's young-vocabulary failure had
never been tested: that the screen's population is *documents*, so "prior art
exists" is satisfied by prose. **It is 14 of 18 executable code** — 13 of 18 with
every young root listing read by hand, so the verdict does not rest on the
classifier's margins. Documents are 22% of the young arm and carry a **median 6,072
stars against 566** for the code rows, while 14 of 18 young rows have no readable
use channel at all and 13 of those are tools: **the most-starred tool in the young
vocabulary is installed 363 times a month.** Supply is plentiful and measured use
is scarce, and a prior-art screen counts the first and reports the second.

**A restated experiment number was false, and the obvious gate is blind to
it** (defect 22, T-0056, D047, F024). `docs/process/experiment-protocol.md` claimed
`005-knitting-bounded-search` was exact on **113/113** checked cases; that artifact's
`results.json` says `cases_with_oracle = 115`, and the wrong number was in `318374a` —
the commit that published the artifact — so it was wrong on arrival and every gate passed.
**The load-bearing half is the rule that cannot see it:** "does this number occur anywhere
in the artifact?" answers *yes*, since `113` also sits at
`patch_cost_sensitivity/*/cases`, so the obvious gate would have been green on the defect.
`resultnumbers.py` decides the property from the number's *shape*, and
`tests/test_result_numbers_falsified.py` asserts the rejected rule's blindness.

**Identifier collisions between two VMs are closed** (T-0030, T-0031): allocate
with `origin id next`, renumber on the side that has **not** been pushed, and
record the collision where the next reader looks — never by editing a closed event
stream. Keep both lines when two VMs' commits meet and regenerate the indexes
rather than merging them. **The work-collision case still has no detector**, so
read the remote task list first. Detail in
[`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).

**A gate belongs in the one command the protocol tells every agent to run**
(T-0045). T-0042 added `DECISIONS-RECORDS.md` at the top level, classified
nothing in `RELEASE-MANIFEST.md`, and its own `verify` passed — because the
command ran the suite, `doc lint` and `preflight`, and `preflight` did not run
`release check`. Three commits carried it to the base before run `37191658964`
named it. `release check` now runs from `preflight`, and the rule is written into
[`docs/process/session-protocol.md`](docs/process/session-protocol.md) rather than
left as something to remember.

**A test can read a clock the code does not, and it expires on a schedule rather
than intermittently** (defect 15, T-0044). The three CLI tests behind the
in-flight gate dated their claim from a fixed `NOW = 2026-10-03T22:00Z` while
`session verify` reads the real one, so a 13-hour claim aged by an hour every hour
and the 24-hour-lease assertion began failing at **2026-10-04T09:00Z exactly** and
can never pass again. Run `37190842104` at `f566ff0` is red on it. This is F018 and
F019 with the environment being time, and nothing scans for the pairing of a
fixed instant in a fixture with a wall clock in the code.

**Defect 14 (a decision number written in three places with one reader) and
defects 1–4 and 7 are closed**; the full accounts are items 2(a) and 2(c) of
[`STATE-next-actions.md`](STATE-next-actions.md), and the mechanisms live in
[`STATE-defects.md`](STATE-defects.md) rather than being quietly repaired. **One
rule survives here:** rebase a moving base with `origin sync land`, because a
hand-run rebase records nothing and its paths are then attributed to whoever
holds the tree (T-0053; sessions 040 and 012 hit that ceiling seven and twice).

## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md) and
[`STATE-history-2.md`](STATE-history-2.md), which exist so that history does not
push this reload point past the line cap. That cap has now been hit by this file
five times, and each repair moved material to the file whose invariant owns it.

- **Sessions 050-051, VM 0944 (F029, F030, D049, E012).** D048's invention seat
  was **tested rather than filled**: 1401 need statements harvested from Hacker
  News since 2024-01-01, 50 drawn by a stated rule, **0 survived the screens**
  (38% prior art, 30% no mechanism, 24% not software, 8% needing hardware)
  against the prior generator's own 3-of-16. A need statement is not a candidate,
  and a need corpus cannot supply recurrence — term recurrence over 1273 clauses
  returns only function words — while an issue corpus counted **by repository**
  does (5805 issues across 28 repositories for the one cluster that recurred by
  eye). F030 is the methodological by-product: one search query decides a
  prior-art verdict wrongly in both directions. **What it changed is the
  pipeline's inputs, not a candidate's state** — and the owner decision already
  recorded above, on which axis candidates are now selected, is the binding one.
  **Two costs recorded:** a concurrent instance of session 044 closed that
  stream mid-session, so these commits predate session 050's record; and the
  renumbering from `EXPERIMENTS/011` to `012` was applied to the README while
  the rebase that renamed the directory was discarded, leaving two indexed copies
  of one experiment that no gate could see, consolidated in `c38f1b4`.
- **Session 047, VM 0947 (T-0058, F028).** The flat adoption tail is vocabulary
  age, not niche: `build provenance` / `supply chain audit` carry long-lived or
  vendor-official outliers, so a stars-based "plausible adoption path" criterion
  is uninformative for a vocabulary younger than a few years — which is where
  every candidate lives. Census in
  [`EXPERIMENTS/011-niche-adoption-census`](EXPERIMENTS/011-niche-adoption-census/README.md).
  **Which axis replaces the criterion is an owner decision**, and is recorded as such.

- **Session 047, VM 0947 (T-0059). Twelve prior-art deaths are not twelve
  pieces of evidence.** Measuring installs rather than stars in five niches:
  three young vocabularies have 88–100% of their leading implementations with
  no measurable monthly install, and stars do not predict installs in any niche,
  mature included — which retracts the reading F028 was offered as support for.
  A crowded niche is the normal state of every niche. Two instrument defects
  were found by pre-flight and would each have flattered the hypothesis: an npm
  endpoint that answers in two different shapes, and an HTTP 200 that means
  *rate limited*. A third — a package name matching a repository it does not
  belong to, 25% of the time — would have under-counted the mature arm's leader
  by three orders of magnitude. F032.

## Infrastructure build (sessions 015–016, earlier)

`tools/origin` (session logging, task dispatch, documentation lint, index
generation, skill checks, environment doctor), `tools/x` (command capture with
exit codes and secret redaction), per-session append-only logs reconciled against
git, multi-VM safety with a two-clone fleet harness (T-0004), the
metadata-tagged documentation graph, and 21 skills vendored in-repo and mirrored.
Standard-library Python, no installation step. Current state: the **Implemented**
rows above and the infrastructure track in [`ROADMAP.md`](ROADMAP.md); the
session-by-session account is in [`STATE-history.md`](STATE-history.md) and
[`STATE-history-2.md`](STATE-history-2.md), including the two record-keeping
defects that running it on itself exposed (F003, F004), both fixed under test.

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

**The screen that killed every candidate has now been measured on both axes, and
it produced the mission's first leads that did not come from its own reports.**
F034 (other VM) measures its **soundness**: on the population the screen consulted,
**4 of 4 on-topic incumbents in mature vocabularies are served and 1 of 4 in a
young one**, so the verdict is sound exactly where it is least used and unsound in
the young vocabularies every candidate here lives in — the twelve deaths are
twelve judgements whose reason was never measured. F035 (this VM) measures its
**coverage**: of 12 adjudicable kills, **3 have no prior art at all** and **4 were
served only on the open web**, which no code index can see. Both declared E016
arms met (6 of 6 controls recovered; 3 of 12 no prior art), one attribution row
decides that count, and `results.json` carries both numbers.

**What changed is the method, not a candidate.** Prior art is judged on the open
web and on the clause's attribute, never on a code index and a category (D050).
The three survivors are need statements — no mechanism, no differentiation, no
adoption path — so each goes to a mechanism question first, and F029's generator
verdict is narrowed rather than reversed. **Choosing what the mission selects
candidates on is still an owner decision**, and F037 narrows what the choice has
to fix: the screen's *population* is sound and its *coverage* is not, so a better
search does not repair it. Item 0 of [`STATE-next-actions.md`](STATE-next-actions.md)
holds the three leads, the reasoning, and the axis still on offer.

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

**Four repair rounds have missed a layer, and the layer that *merges* trees was
the one nobody covered.** A stale generated file is the same defect whichever file
it is: three commits reddened CI by carrying one and a fourth was published by
`land` itself (`e942225`). T-0026/T-0027 fixed the *task* commands, session 015
fixed the *CLI*, and only T-0041 covered the *merge* (defect 13). This session
saw the same class again — a merge carried a duplicated dashboard row past every
gate, which D043 already named.

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
- No invention claim has been validated. Three claims are **disproved**: A1 in its
  motivating regime (F006), C2's measurement design (F008), and the knitting
  planner's algorithmic advantage (F009, by prior art). Two further *lines* died
  without a candidate: this repository's own tooling read as prior art (F026) and
  live need harvesting as a generator, 0 of 50 (F029). E's mechanisms remain
  unvalidated: E1 and E2 are `untested`, E3's declared gate could not fail (F010).
- Every candidate has substantial prior art, and none has passed prior-art review:
  twelve candidates, twelve prior-art deaths. Two prior-art reviews are recorded
  and negative in their decisive halves (`RESEARCH/PRIOR-ART-KNITTING.md`,
  `RESEARCH/PRIOR-ART-ORIGIN.md`), and a verdict needs more than one phrasing (F030).
- The screen's own weakness: decidable from prose, so cheap and also vulnerable to
  a persuasive report. It guarantees the *next* experiment is worth running.
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen,
  and the session-by-session account lives in the two history files named above.
