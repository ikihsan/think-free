<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Verified state

Date: 2026-10-03, Asia/Kolkata. Phase: A complete, infrastructure built, B
beginning. Mission active; **no product selected**.

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
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012); `010-annotation-rendering` complete (GitHub files a check-run annotation on the workflow command's `file=`, `observed` on run `37191658964`; the run the record had quoted for that never reached the annotator, F021) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it; F021 the annotator's rendering was declared `unmeasured` on a run whose annotating steps never ran, because a red `Tests` step silently skipped all five. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 452 tests). Every file-reading CI gate now re-emits each violation as a check-run annotation naming the file (`tools/origin annotate`, T-0040, defect 17), GitHub files it on the path emitted (T-0046, F021), every such step runs whenever the job does, and `tools/origin probe` publishes one annotation per rendering shape on every run (defect 18) — measured on run `37196459285`, which filed all seven and answered the question the record had left open. A task command now also declares the task file it rewrote, with the digests of the bytes it wrote, so the tooling's own write is no longer a session's exit 4 (T-0047, D040) |
| Implemented (2) | Every diagnostic CI step runs whenever the job does, after a red `Tests` step silently skipped all five (T-0048, defect 18); `sync land` finishes a rebase it stopped on, so its own "resolve it and land again" is followable by the tool that gave it (T-0048, D039); and a task claim publishes while the session that made it is open, and refuses foreign uncommitted work *before* writing anything (T-0055, defect 21) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 74 with an event stream, 73 closed — counted from the tree, not from a running total, because the two VMs had been counting different bases. Newest: VM 0944's sessions 030 and 031 (T-0048, T-0049) and VM 0947's 030 (T-0047), all `worked`; an unfinished session on either VM is reported as in flight rather than as a failure (D027) |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 551 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, since T-0042 on a decision record's own header disagreeing with that record, since T-0051 on a link that leaves the repository, which had been judged by what the checkout's parent directory held so the same bytes passed in a worktree and failed in the main checkout (D041, defect 19), and since T-0052 on a hand-authored document repeating a table row (D043, defect 20). Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM five times in three sessions** — `identifiers.py` at 307 after a merge, `STATE-defects.md` and `STATE.md` after new findings, and in T-0050 `tasks.py` (split into `taskindex.py`) and `tests/test_task_rewrite.py` (split into `test_task_rewrite_recorded.py`) — and each time the repair was to move material to the file whose invariant it belongs in |

| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `37206580954` at `3c49642`**, the tip carrying T-0050; T-0051 and T-0052 landed after it and their runs are named in their task files. Ten runs have passed since the last time this row was written and **none was reproduced on a VM to find out why it was red** — each cause read off the run's own annotations, seven in a row (`EXPERIMENTS/010-annotation-rendering/`, arms F–J). Four were the expected case (a commit published while a session is open: runs `37196594583` and `37197942512`, each green on the next commit). **Run `37197291442` at `7790d6b` is the first red run whose cause was read off an annotation the annotator filed**, on another VM's task file at line 70 — before T-0040 that run's only failure annotation said *Process completed with exit code 2*. Every run also carries the probe's seven annotations, so a reader of any run has the rendering reference beside the failure. **What no run has exercised:** a matrix row cannot be added for a version `actions/setup-python` does not publish; the git version is still one runner's — 2.55.0, named in `git-versions.json` and measured locally, not by any row — and this VM's 2.55-first `rebase-merge` path (`landrebase.orig_head`) is therefore unrun |

Per-session detail is in [`STATE-history.md`](STATE-history.md).

## In flight

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

**Both machine-fact gates are closed, and the second was invisible from
outside** (defects 8 and 9 in [`STATE-defects.md`](STATE-defects.md)): each was
green on the VM that wrote it and red elsewhere for opposite reasons, and neither
cause was readable from outside because the run log needs admin rights. Check
`tools/origin task list --remote` before taking anything.

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

**A decision number is written in three places, and one of the three had no
reader at all** (defect 14, T-0042). The heading and the index row in
`DECISIONS.md` were held to each other by T-0030, the numbered defect list was
added by T-0036, and the header under each record's title had no check until
T-0042 found `DECISIONS-GATING.md` naming D013 — which lives in another file —
while omitting three of its own entries, with both index rows correct throughout.

**Collisions were allocated by reading the local tree, so two VMs in an hour
collided by construction.** Twelve times in two days; the allocation cause is
closed in T-0031 (`origin id next` reads `origin/<base>` and prints the record it
read) and the detector in T-0030 — and the twelfth happened while fixing it. **Rule
unchanged:** renumber on the side that has not been pushed, and record the
collision where the next reader looks — never by editing a closed event stream.
When two VMs' commits meet, keep both facts and let the generated indexes be
regenerated rather than merged; a ledger conflict is resolved by keeping both
lines. **A work collision is the same case with no detector at all:** T-0054 and
T-0055 were one defect found by two VMs nine minutes apart, each VM giving it a
different number, and the unpushed side yielded. Read the remote task list first.

**Defects 1–4 and 7 are closed, and each mechanism is recorded rather than quietly
repaired**: a session that landed a colleague's work reported it as undeclared
(D028), generated files stamped `last-verified` with the render date (D029), and
the orphan rule bit six real CI runs because `task new` did not rebuild the indexes
and `task claim` did not stage them — T-0026 and T-0027, and the second took two
tasks, because a lint on the author's own tree cannot see what the claim commit
published. **Rebase a moving base with `origin sync land`:** a rebase run by
hand records nothing — T-0053 recovers that arrival from `ORIG_HEAD` and the
reflog, while a pull, cherry-pick or reset run by hand still leaves its paths
reported. Sessions 040 and 012 hit the old ceiling through seven and two hand-run
rebases respectively, and the stream is closed and is not edited, as with session 029.


## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md) and
[`STATE-history-2.md`](STATE-history-2.md), which exist so that history does not
push this reload point past the line cap.

- **Session 040, VM 0947 (T-0054, cancelled).** **Two VMs found defect 21 nine
  minutes apart.** This VM hit `task claim`'s refusal at 15:08Z and created T-0054 to
  fix it; the other hit the same refusal at 15:17Z, created T-0055 and landed the fix
  (`0522052`). Different numbers, so neither allocator nor detector had anything to
  say — and that was right: no identifier collided, the *finding* did. **T-0054 was
  cancelled and its unpushed commits dropped whole**, two modules publishing a claim's
  paths being worse than one. What survived is the gap the landed fix left: a claim
  under an open session is proved to publish and a published claim to exclude, but not
  composed, which is the order the fleet runs. Full account and the rule:
  [`multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).
- **Session 038, VM 0947 (T-0053).** A base move performed with raw git recorded
  nothing, so its paths were attributed to the session that happened to hold the
  tree: session 034's nine `unlogged_change` events were exactly that. Now
  `landrebase.recover` records a hand-completed rebase's arrival from
  `ORIG_HEAD` plus the `rebase …: checkout` reflog entry, and a merge, a
  fast-forward, or an arrival the tooling already recorded is refused. Both
  directions are falsified: with the `recover` call removed, the arrival is
  reported undeclared again, and a merge or fast-forward never matches.
- **Session 034, VM 0947 (T-0050, D042, F022).** Defect 12's entry named its own false
  negative in a clause and no gate read it: `reconcile` reused the *line cap's* exemption
  predicate, which answers yes for every `.json`, `.jsonl` and `.log`, so
  `tests/python-versions.json` — the record that decides whether a VM can run the work —
  changed with nothing declared and nothing reported. **Priced before the repair, by a
  committed script:** 72 (session, path) pairs over 17 paths across 77 closed sessions,
  50 of them the ledger, so 50 closed sessions now report a file they cannot declare; a
  closed stream is not edited, so the residual is written down rather than discovered.
  Falsified both ways, and the first mutation passed all 16 because the patch did not
  land — the second time this repository has been caught by it. In
  [`FAILURES-findings-5.md`](FAILURES-findings-5.md).
- **Session 036, VM 0944 (T-0052, D043, defect 20).** Commit `eff1126` — a rebase of one
  VM's branch onto a base the other had already extended — carried `STATE.md` with a
  byte-identical second copy of its `Implemented (2)` dashboard row, one per VM, and
  every gate passed: the reload point a cold session reads first showed two rows that
  are one fact, and the next session removed one by hand. Measured: 47 documents repeat
  a table row, **all 47 generated reports**, where an artifact listed once per event is
  the truth. **A hand-authored document may not say a thing twice**, with the exemption
  read from the `generated-by` marker rather than from a path. Falsified both ways — the
  rule removed reports nothing, the exemption removed reports 47 on a clean tree.

## Infrastructure build (sessions 015–016, earlier)

`tools/origin` (session logging, task dispatch, documentation lint, index
generation, skill checks, environment doctor), `tools/x` (command capture with
exit codes and secret redaction), per-session append-only logs reconciled against
git, multi-VM safety with a two-clone fleet harness (T-0004), the
metadata-tagged documentation graph, and 21 skills vendored in-repo and mirrored.
Standard-library Python, no installation step. Current state: the **Implemented**
row above and the infrastructure track in [`ROADMAP.md`](ROADMAP.md); the
session-by-session account is in [`STATE-history.md`](STATE-history.md) and
[`STATE-history-2.md`](STATE-history-2.md). Two defects in that record-keeping
were found by running it on itself and are recorded rather than quietly repaired:
session 002 under-declared 55 committed files (F003), and a directory sweep
recorded build output as artifacts (F004). Both fixes are covered by tests.

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
[`STATE-next-actions.md`](STATE-next-actions.md). Ordered by information gained
per unit of effort; the top item is:

**A gate must read the property it claims to check, and must be falsified
against the defect's own bytes before it is trusted** (D025, from F013). Six
gates now work that way, and the newest adds a third kind of falsification —
run the thing on an input the record does not name, rather than mutating the
code. **Ceiling:** each rule detects only the shape it was written against.

**The gap in that pattern, found twice by colliding with it — closed, and the
second collision was in the record rather than in a red run.** Rule 7 did not
read the numbered list in `STATE-defects.md`, so two VMs took defect 7 in the same
hour and nothing said so (T-0036). It then did not read the third place a
decision number is written — the `Decisions **…**` header under each record's
title — so two of the five records were false while every gate passed, with both
index rows in `DECISIONS.md` correct throughout (T-0042, defect 14). One entry
point reads all three sources now, and the CI annotations confirm it reaches
`doc lint`.

**What the three red runs on 2026-10-04 say about the general rule.** Each was
diagnosed by reading annotations rather than by reproducing anything, and two of
the three were this VM's own omissions — a merge that crossed a line cap, and a
root document nothing classified. The pattern is not "gates are missing" but
**gates that exist and are never run**: a task's `verify` omits the one gate its
change can break, a fixture omits the clock the code reads, a split leaves one
reader unwired. T-0045's fix is the general one: put the gate in the command the
protocol already points at, so there is nothing left to forget.

**The decision log could not record its own next decision, and that is now
paid off.** `DECISIONS-GATING.md` stood at 297 of 300 permitted lines and its own
header said so, so T-0036's decision — one entry point for every source of an
identifier, and a rule that cannot read its input must report that — lived in code
and in the state file instead of the log, which is the opposite of what a decision
log is for. D036 is recorded there, in the file its own invariant names, and
D029/D032/D035 moved verbatim to `DECISIONS-RECORDS.md`.

**A stale generated file is the same defect whichever file it is, and four
repairs have now missed a layer.** Three commits have reddened CI by carrying one
and a fourth was published by `land` itself (`e942225`, session 022's
`4c5349d`). T-0026/T-0027 fixed the *task* commands, session 015 fixed the *CLI*,
and only now has the layer that *merges* trees been covered: after every rebase
`sync land` asks `doc lint`'s question — is each generated file equal to its
renderer — and commits the answer before the push (T-0041, defect 13).

**A gate step that says nothing is read by elimination, and a step that never runs is
read as one that passed** (T-0046, defect 18, F021). Each of the five file-reading steps
carried an `if:` with no status function, so GitHub's implicit `success()` skipped all
five on a red `Tests` step: runs `37189825232` and `37190842104` carry no annotation the
annotator emitted, and four gates did not run at all with nothing to say so. Each such
step says `always() &&` now, held by a test falsified against the workflow as it was,
and `tools/origin probe` publishes one annotation per rendering shape on every run, so
the reference and the failure come from the same place. **What it cost:** the record had
declared the annotator's rendering `unmeasured` and quoted a run that never reached it.

**Line caps are the standing friction, and each repair moved material to the file whose
invariant owns it.** `STATE.md` and `STATE-defects.md` were both at 300 of 300; T-0046
landed its entries by deleting a section that restated a rule the preamble already gave
and by moving five older session entries to `STATE-history-2.md`; T-0047 cut duplication
out of four entries whose detail already lives in `tests/README.md` and
`docs/reference/identifier-allocation.md`. Both bought a few entries and no headroom.
`syncland.py` reached 310 with the rebase resume and is now split by the division
`doclint_tree.py` used. `DECISIONS-GATING.md` is at 296 after T-0048's relocation,
`FAILURES-findings-4.md` is at 297, `tasks.py` is the next code file to reach the cap at
295, and `STATE-defects.md` cannot be split inside its own numbered list without
`defectlist.py` reading more than one file. The gating decision T-0040 owed is written,
as D037 and D038, in the file its invariant names.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development
machine: 12 logical CPUs; ~15.3 GiB RAM; Python 3.14.6; Node 22.23.1; Rust 1.96.0;
GCC 16.1.1; `git` 2.55.0. GitHub API, SQLite and arXiv HTTPS all 200; NumPy
present, SciPy/pytest/Z3 absent; `gh` absent; `systemd --user` running with no
user units. A VM's own numbers come from `tools/origin doctor`, which writes
`.origin/doctor.json`; this one reports 2 CPUs, Python 3.8.10, `git` 2.25.1, and
pushes via the GitHub App as `Ihsan Ai Server Bot`.

**Unverified and not to be assumed:** fleet access, unattended supervision, GPU availability.

## Honest limitations of this state

- All six investigation roles are sealed (`RESEARCH/A.md`–`F.md`), and
  `RESEARCH/SYNTHESIS.md` compares them. The synthesis is `inferred` from prose:
  it reorders and screens existing claims and measures nothing itself.
- No invention claim has been validated. Three claims have been **disproved**: A1
  in its motivating regime (F006), C2's measurement-design advantage (F008), and
  the knitting planner's algorithmic advantage (F009, by prior art rather than by
  measurement). E's mechanisms remain unvalidated: E1 and E2 are `untested`, and
  E3's declared gate could not fail (F010).
- Every candidate has substantial prior art; none has passed prior-art review.
  One prior-art review is now recorded and negative in its decisive half
  (`RESEARCH/PRIOR-ART-KNITTING.md`).
- The screen's own weakness: it is decidable from prose, which makes it cheap and
  also vulnerable to a persuasive report. What it guarantees is that the *next*
  experiment is worth running, not that a rejected candidate is worthless.
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen.

Three earlier sessions are recorded in [`STATE-history.md`](STATE-history.md)
rather than here, as are all three red runs this VM published on 2026-10-04.
