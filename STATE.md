<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Verified state

Date: 2026-10-03, Asia/Kolkata. Phase: A complete, infrastructure built, B
beginning. Mission active; **no product selected**.

Host note: continuation VM `instance-20260717-0944` came online 2026-10-03;
GitHub remote configured via GitHub App installation on `ikihsan/think-free`.
Commits from this VM are authored as `Ihsan Ai Server Bot` (global git
identity, 2026-10-03). This VM runs **Python 3.8.10 and git 2.25.1**, not the
3.14.6/2.55.0 recorded from the development machine, so the capability numbers
below are per machine and must be re-probed here with `tools/origin doctor`.

Push-credential note, corrected 2026-10-04. The note here used to say a durable JWT generator
had been added under `~/.config/github-app/` and "the helper now points at it". That is
true of `instance-20260717-0947` and was **not** true of `instance-20260717-0944`: its helper
still invoked `/tmp/github-app-jwt.sh`, which is how `0947` lost a day of pushes in the first
place. Repaired there in T-0029 — the generator is `~/.config/github-app/jwt.sh`, the helper
points at it, and the `/tmp` copy was deleted to prove it. `doctor` now reports such a
dependency before it fails ([`docs/operations/doctor.md`](docs/operations/doctor.md)).

This is the reload point. A cold session reads this file, then whatever it links.

## Dashboard

| Area | Verified status |
|---|---|
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030, 037–040, T-0012, T-0013, T-0017, T-0021–T-0023, T-0029, T-0040) and on `instance-20260717-0947` (sessions 020–023, 027–029, 031–038, T-0011, T-0014–T-0016, T-0018–T-0020, T-0024–T-0028, T-0042–T-0045) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code; F019 the same class one function away, so every CI row was red because the runner's git 2.55.0 was not in the record and the log could not be read; F020 the public check-runs API does publish annotations, so a red run is diagnosable without admin rights — and the claim that it does not was generalised from one shape of failure to the case that needed it. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030), and rule 7 reads every source of identifiers — findings, decisions, tasks, the defect list **and each decision record's own header** — through one entry point both publishing gates call (T-0036, T-0042). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 418 tests) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 58 recorded; four on this VM today (024, 025, 026, 027), all `worked`. VM 0944's session 020 is in flight on T-0040 and correctly reported as such rather than as a failure (D027) |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 506 files and exits 0; every authored file is under the 300-line cap, and the declared exemptions are vendored skills, raw machine-generated results, and append-only command logs. Since T-0021 it also fails on an unresolved merge conflict, since T-0030 on an identifier defined twice or indexed without a body, since T-0036 on a defect list it cannot read, and since T-0042 on a decision record's own header disagreeing with that record. Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar. **The cap bit this VM three times in two sessions** — `identifiers.py` at 307 after a merge, and `STATE-defects.md` and `STATE.md` after new findings — and each time the repair was to move material to the file whose invariant it belongs in |
| Continuous integration | **Green on all seven rows, `observed` 2026-10-04 on run `37192717297` at `cfaf4ed`** — reached after three consecutive red runs on the base, each from a different cause and all three this VM's: `37189825232` at `ea3bfb5` (the merge took `identifiers.py` over the line cap, T-0043), `37190842104` at `f566ff0` (defect 15, a lease test that expired on a schedule, T-0044) and `37191658964` at `c9e89e1` (`DECISIONS-RECORDS.md` unclassified in the release manifest, T-0045). **All three were diagnosed by reading the run's annotations, with no reproduction at all**, which is the method F020 and T-0038 pointed at and the first time it was used on three real failures in a row. Those runs are also how T-0040's annotation mechanism was exercised on a real `Documentation lint` failure: 11 per check-run, naming the failing test and the file to open. The green run's three annotations on the 3.12 row are the runner's own Node.js deprecation warning, D027's in-flight note for the other VM, and an `ubuntu-latest` migration notice. **What no run has exercised:** a matrix row cannot be added for a version `actions/setup-python` does not publish, and the git version is still one runner's — 2.55.0, named in `git-versions.json` and measured locally, not by any row |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**Both machine-fact gates are closed, and the second was invisible from
outside** (defects 8 and 9 in [`STATE-defects.md`](STATE-defects.md)). T-0033's two
assertions were each green on the VM that wrote it and red elsewhere for opposite
reasons — the interpreter one on every version the record lacked, the git one on
the CI runner, whose **git 2.55.0** the record did not name. Seven rows were red,
the run log needs admin rights, and the cause came from elimination plus a
reproduction with that git unpacked outside the repository. Check
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
lines.

**Defects 1–4 and 7 are closed, and each mechanism is recorded rather than quietly
repaired**: a session that landed a colleague's work reported it as undeclared
(D028), generated files stamped `last-verified` with the render date (D029), and
the orphan rule bit six real CI runs because `task new` did not rebuild the indexes
and `task claim` did not stage them — T-0026 and T-0027, and the second took two
tasks, because a lint on the author's own tree cannot see what the claim commit
published. **Rebase a moving base with `origin sync land`:** a hand-run rebase
records nothing, so its paths stay reported as undeclared. Sessions 040 and 012 hit
that ceiling through seven and two hand-run rebases respectively, and the stream is
closed and is not edited, as with session 029. It is D028's stated ceiling and the
intended direction of failure.


## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md), which
exists so that history does not push this reload point past the line cap.

**Corrected 2026-10-04, and it is the one correction in this record made by
reading a source rather than a tree.** The claim that "the public check-runs API
returns no annotations" is true of the red runs this VM had read — Documentation
lint failures, whose step emits no `::error::` lines, so their one failure
annotation says only "Process completed with exit code 2" — and **false of the run
F019 was about**: run `37178057818` at commit `687961f` carries 11 annotations on
`verify (3.12)`, and one of them is
`FAIL: test_this_vms_versions_are_exercised_against_the_real_records (test_doctor_versions.RealRecordTest…)`,
with `tests/test_doctor_versions.py`, line 69 in the next one up. Read from the
public endpoint on 2026-10-04; no rights required, and the same call returns the
full annotation list rather than the empty `output.text` that a first reading of
the check-run object shows. The hour was spent on a conclusion generalised from one
shape of failure to the case that needed it, and the general form is already
recorded as D025: **read the property, not the field you happened to look at.**
Now `FAILURES.md` **F020**, with the four answers that endpoint can give and the
60-requests-an-hour limit that makes three of them look like "none"; the method is
[`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md).

- **Session 017, VM 0947 (T-0036).** `doc lint` rule 7 now reads the numbered list
  in `STATE-defects.md`, where two VMs had taken **defect 7** in the same hour and
  both copies reached the base with each VM's own tree internally consistent.
  `tools/originlib/defectlist.py` reports a number defined twice, and a list it
  cannot read; `tools/originlib/idcheck.py` is the one entry point `doc lint` and
  `sync land` both call, because a rule wired into one gate is not thereby read by
  the other. Falsified against the defect's own bytes — each commit's real tree out
  of git, where the previous wiring reports **nothing** and the new rule names both
  lines — and against the repair commit and the tip, which must stay silent. The
  first control failed and found a real tension rather than a bad test: a file whose
  only numbered list is unbolded is both "not a definition" and "nothing readable",
  and the second reading is the one that fires. 418 tests green.
- **Session 012, VM 0947 (T-0034, D035, F018, F019).** Every CPython minor from
  3.8 to 3.14 has run the suite — portable builds on this VM and one CI matrix
  row each — with `tests/test_ci_matrix.py` holding the matrix to the record in
  both directions. **Neither gap was theoretical.** On the five interpreters the
  record had never named, the suite failed; so it did on the runner, because
  T-0033 had added two assertions that the machine running it is covered by the
  records. Each was green on the VM that wrote it and red elsewhere for opposite
  reasons, and neither cause was readable from outside; the log needs admin
  rights, and **the claim recorded here that the public check-runs API returns no
  annotations is false for the run that mattered** — see the correction below.
  The second was found by elimination and reproduced with the runner's own git
  2.55.0. Both assertions are now the module's contract; the portable form is in
  D035. 392 tests green on 3.8.10, five portable builds and git 2.55.0. Detail in
  [`STATE-history.md`](STATE-history.md).
- **Session 005, VM 0947 (T-0030, D032).** A colliding identifier is refused
  before publication, because a collision is created by the merge and each VM's
  own lint sees nothing wrong with its own tree. Over all 174 commits it reports
  **one**, `e6eb992`. Detail in [`STATE-history.md`](STATE-history.md).
- **Session 017, VM 0944 (T-0037).** The four red CI runs were already explained
  by VM 0947 as F019 while this VM was creating a task to explain them, so this
  session recorded the elimination table rather than redoing the diagnosis.
  **The process lesson is the durable part:** when a gate is red somewhere you
  cannot reproduce, check `task list --remote` first — the answer took a second
  and the reproduction took forty minutes.
- **Sessions 011 and 012, VM 0944 (T-0033, T-0035, D034).** `doctor` reads both
  exercised-version records, so a VM outside the exercised set is warned rather
  than undocumented — and then three CI runs went red while both VMs were green,
  because a credential fixture had inherited a CI runner's `GITHUB_TOKEN`. Both
  were machine-environment faults: a gate that reads its own environment is only
  as portable as the record of that environment (F018, F019). Detail in
  [`STATE-defects.md`](STATE-defects.md) and the two task files.
- **Session 037, VM 0944 (T-0021, F013).** Three mission records reached the
  shared base with `<<<<<<< HEAD` in them and every gate passed. Repaired by
  keeping both sides of all three regions (F011 and F012 are different findings),
  and `doc lint` rule 6 now reads every tracked text file for git's marker shape.
  The rule was falsified against the defect's own bytes and **failed first**,
  reporting 1 of 4 committed defects; D025 records the obligation this
  establishes.
- **Sessions 026–029, 033–036, VM 0947 and 0944.** T-0014 stopped the ventilation
  candidate (F008), T-0015 spent the knitting prior-art condition (F009), T-0016
  fixed the git-version defect behind 60 failed CI runs (F011), T-0018 recorded
  exercised git versions, T-0019 banked side A of the E2 closure-drift snapshot.
  Detail in [`STATE-history-2.md`](STATE-history-2.md).

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

Recently closed there: a CI matrix row per CPython minor from 3.8 to 3.14, held to
`tests/python-versions.json` in both directions (T-0034, D035, F018, F019). Run
`37180041369` is green on all seven rows; nothing from 3.15 onwards has run, and
no gate widens that.

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
