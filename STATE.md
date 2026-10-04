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
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030, 037–040, T-0012, T-0013, T-0017, T-0021–T-0023, T-0029) and on `instance-20260717-0947` (sessions 020–023, 027–029, 031–038, T-0011, T-0014–T-0016, T-0018–T-0020, T-0024–T-0028) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029; F018 the suite failed on every interpreter the record had never named, because a gate asserted a fact about the record instead of about the code. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). `doctor` compares this VM's git and interpreter against the exercised-version records (T-0033). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030). CI runs one row per CPython minor from 3.8 to 3.14, held to the exercised-version record by a gate that reads both (T-0034, 388 tests) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 55 recorded, 0 in flight once this one closes (session 012, T-0034, VM 0947) |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 431 files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs). Since T-0021 it also fails on an unresolved merge conflict, and since T-0030 on an identifier defined twice or indexed without a body. Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar |
| Continuous integration | **Green on all six steps on the current base** (`observed`, run `37166854486`, commit `fc9d9ed`, 2026-10-04T01:03Z; the four runs before it — `37165413909`, `37165765013`, `37166293583`, `37166485867` — also green). **Six red runs, one verified cause:** `37163434868`, `37163438950`, `37165502352`, `37165507351`, `37165802926`, `37165807196` and `37166490623` all failed the Documentation lint step with exit 2 on an orphan task file, because the commit carrying the task file did not carry the rebuilt indexes (defects 4 in `STATE-defects.md`, closed in T-0026 and T-0027). **Now exercised, once:** a rebase conflict between VMs — run `37171841544` (commit `09684f2`) failed Documentation lint, and the cause is a broken relative link in a task file this VM had just written; reproduced locally at `09684f2` and fixed in `00cd829`, which is green (run `37172039525`). A conflict-marker block committed to `tasks/CLAIMS.jsonl` in the same rebase was caught by `tests/test_conflicts.py` before the push, so it never reached a run. **Not exercised by any run:** the git 2.56.0 path — CI runs 3.12 on one runner image only |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**No task is claimed on the base.** T-0030 (the detector that refuses a commit
giving one identifier two definitions) and T-0031 (the allocator that reads
`origin/<base>`) both closed defect 5 on 2026-10-04.
`instance-20260717-0944` held T-0012, T-0013, T-0017, T-0021–T-0023, T-0029 and
T-0031–T-0033; `instance-20260717-0947` held T-0011, T-0014–T-0016,
T-0018–T-0020, T-0024–T-0028, T-0030 and T-0034. Check
`tools/origin task list --remote` before taking anything.

**Identifier collisions were allocated by reading the local tree, so two VMs in
an hour collided by construction.** Six times on 2026-10-03 and **six more in a
single hour on 2026-10-04**, all between these two machines: T-0024 through
T-0028, F014, F015, D027 and D028 were each taken on 0947 while 0944 worked. That
VM renumbered to T-0029, F016, F017 and D030, two of those rounds *during one
rebase* because the other VM pushed twice more while it resolved. **Rule
unchanged:** renumber on the side that has not been pushed, and record the
collision where the next reader looks — never by editing a closed event stream.
That rule was followed again when these two VMs' commits met in T-0032's
rebase. **The allocation cause is closed in T-0031**
(`tools/originlib/idalloc.py` reads `origin/<base>` for F, D and T and prints the
record it read); **the detector is T-0030**, because a residual race — two VMs
allocating between their own fetches — still collides and has to be caught. The
measured cost of the old behaviour, a rebase that restored a file's index row
while reverting its body so a findings file and its own table disagreed, is defect
5 in [`STATE-defects.md`](STATE-defects.md).

**All six defects there were closed on 2026-10-04.** D028 (a session that landed
a colleague's work reported it as undeclared), D029 (generated files stamped
`last-verified` with the render date), the orphan rule biting six real CI runs
because `task new` did not rebuild the indexes and `task claim` did not stage
them, **defect 5 on the detector side** (T-0030: a collision is created by the
merge, so `sync land` refuses to publish a tree where one identifier has two
definitions and `doc lint` rule 7 reports it on any route to the base — one
commit of 174 flagged, `e6eb992`), **defect 5 on the allocation side** (T-0031)
and `doctor`'s version comparison (defect 6, T-0033). The orphan defect was
found by reading pushed runs rather than by pushing something and watching, and
it took two tasks to close: T-0026's verification passed while the defect was
still live, because a lint on the author's own tree cannot see what the claim
commit published.

**The rebase that met T-0030 produced two collisions, and both are now
recorded.** This VM's `D032` and VM 0947's `D032` were different decisions, so
this side renumbered to D033 during the rebase; and the rebase resolved the
append-only `tasks/CLAIMS.jsonl` by leaving a conflict-marker block in a commit,
which `tests/test_conflicts.py` caught — the T-0021 rule doing the job it was
written for, on a recurrence of F013 in a new file. Both are repaired, the
resolution rule for a ledger conflict is now written down in
`docs/process/multi-vm-coordination.md`, and **the fix cost one red CI run**
(`37171841544`, a broken link this VM had just written, fixed in `00cd829`).

**Rebasing onto VM 0947's matrix cost two more collisions, both resolved by
keeping both sides.** The third rebase conflict in a day, and the rule is routine
enough to be worth stating once: keep both facts, and let the generated indexes
be regenerated rather than merged.

**Session 040 closed with 61 `unlogged_change` events that are not its own.** Nearly
all are the other VM's files — `landed.py`, `inflight.py`, `sync.py`, its task files,
its tests — which arrived through **seven hand-run `git rebase`s**. D028 attributes a
path only from a base move *the tooling performed* (`sync pull`/`sync land`), so
attribution had nothing to work from: a raw rebase is not one. That is the ceiling
D028 states on purpose, and this is the first case to hit it. The stream is closed
and is not edited, as with session 029. **Fix is procedural:** rebase a moving base
with `origin sync land`, which records what arrived.

## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md), which
exists so that history does not push this reload point past the line cap.

- **Session 012, VM 0947 (T-0034, D035, F018).** Every CPython minor from 3.8
  to 3.14 has now run the suite, on portable builds and on one CI matrix row
  each, held to the record in both directions by `tests/test_ci_matrix.py`. **The
  gap was not theoretical:** the suite failed on all five newly named
  interpreters, on a T-0033 test that asserted *this* interpreter is in the
  record — which the other VM's CI hit an hour later from the other end. Both
  clauses are kept. Detail in [`STATE-history.md`](STATE-history.md).
- **Session 005, VM 0947 (T-0030, D032).** A colliding identifier is refused
  before publication, because a collision is created by the merge and each VM's
  own lint sees nothing wrong with its own tree. Over all 174 commits it reports
  **one**, `e6eb992`. Detail in [`STATE-history.md`](STATE-history.md).
- **Session 012, VM 0944 (T-0035).** Three CI runs failed the Tests step
  (`37174050724`, `37174316639`, `37174309822`) and the suite was green on both
  VMs and locally on the same commits. The credential sandbox cleared `HOME`,
  `XDG_CONFIG_HOME` and git config but inherited `GH_TOKEN`/`GITHUB_TOKEN`, and
  `pushprobe` counts an environment token as a mechanism — correctly, it is one
  — so a test asserting `unavailable` read `broken` wherever a runner exports
  one. Found by reproducing with the variable set rather than by reading the run,
  and confirmed against `4401bd2c`, so it predates T-0033 and came in with the
  fixture in T-0025. Falsified three ways; the third was found *by* falsifying,
  because a fixture that clears but never restores leaves every test green.
  **A fixture must build the machine it claims to build, environment
  included.**
- **Session 011, VM 0944 (T-0033, D034).** `doctor` now reads both
  exercised-version records, so a VM outside the exercised set is warned rather
  than undocumented: `exercised` with the entry's own scope, `NOT exercised`,
  `record unreadable`, `no record`. Falsified four ways, one of which removed the
  single rendering line and left every module test green. **Defect 6 is closed.**
- **Sessions 006–007, VM 0944 (T-0032, D033).** The Python equivalent of
  `git-versions.json`, which `vm-execution.md` had named as unclaimed work:
  `tests/python-versions.json` records each interpreter with the scope it ran and
  names the versions nobody has run — 3.9–3.11, 3.13 and newer, any non-CPython or
  non-Linux target. CI is credited with the minor version only, because the run
  log needs admin rights. The test checks honesty clauses rather than schema, and
  was falsified four ways first. **Defect 6 is twice-partly closed:** the claim
  exists and is checked; nothing reads it at run time, so an unexercised VM is
  undocumented rather than warned. **This session's own decision was renumbered
  from D032 to D033** during the rebase that met VM 0947's D032 — the collision
  rule applied to itself.
- **Session 005, VM 0944 (T-0031, D031).** Identifier allocation reads
  `origin/<base>` instead of the local tree, for F, D and T alike, and every
  command that hands out a number prints the record it read. Twelve collisions in
  two days were the cost of not doing this; the ceiling is that two VMs
  allocating between their own fetches still collide, and T-0030 detects that.
  Falsified against the defect's own bytes before the repair, which also caught
  two defects in the implementation being tested. Two more defects surfaced from
  running the task's own verification: `session start` wrote its report before
  its first event, so `doc lint` could not pass while a session was open, and two
  modules passed the 300-line cap with the new code in them. 329 tests green.
  [`STATE-history.md`](STATE-history.md) is at its cap, so the detail lives in
  the task file and this session's own record.
- **Session 042, VM 0947 (T-0024, D028).** A session that landed another VM's
  work was reported as having changed that work: session 029 closed with nine
  false `unlogged_change` events and inherited four false `doc_update` events and
  a `documentation_gaps` report. `sync pull`/`sync land` now record what arrived
  from the base, and reconciliation attributes a path by the newest thing that
  touched it. Git authorship was falsified as the baseline first: both VMs commit
  as `Ihsan Ai Server Bot`. **Ceiling:** only base moves the tooling performed
  are known; a hand-run rebase stays reported — and session 040 then hit exactly
  that ceiling through seven hand-run rebases. 265 tests green. A second defect
  surfaced in the same session: every generated file stamped `last-verified` with
  the render date, so `doc lint` failed on 42 committed reports the day after
  they were written (D029). Both fixes were falsified against their own defect
  before being trusted. 269 tests green.
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
exit codes and secret redaction), per-session append-only logs reconciled
against git, multi-VM safety with a two-clone fleet harness (T-0004), the
metadata-tagged documentation graph, and 21 skills vendored in-repo and mirrored.
Standard-library Python, no installation step. The current state of each is the
**Implemented** row above and the infrastructure track in
[`ROADMAP.md`](ROADMAP.md); the session-by-session account is in
[`STATE-history.md`](STATE-history.md) and [`STATE-history-2.md`](STATE-history-2.md).
Two defects in that record-keeping were found by running it on itself and are
recorded rather than quietly repaired: session 002 under-declared 55 committed
files (F003), and a directory sweep recorded build output as artifacts (F004).
Both fixes are covered by tests.

## Resume procedure

1. Read `MISSION.md`, then this file, then `DECISIONS.md` and `HYPOTHESES.md`.
2. `tools/origin session verify` — is any session unfinished? Finish it honestly.
3. `tools/origin preflight` — do the tooling and the documents still agree?
4. `git status` and `git log --oneline -5` before editing. Preserve anything
   unexpected; another agent or an earlier session may own it.
5. Read the raw evidence for the next experiment, not a summary of it.
6. Continue the highest-information experiment. Update this file and make a
   focused checkpoint.
7. Do not load unrelated personal memory. Do not restart discovery from scratch;
   the evidence is in `RESEARCH/`, `EXPERIMENTS/`, and `sessions/`.

## Next actions

Full list, with the ceiling on each item and the reasoning behind it, is in
[`STATE-next-actions.md`](STATE-next-actions.md). Ordered by information gained
per unit of effort; the top item is:

**A gate must read the property it claims to check, and must be falsified
against the defect's own bytes before it is trusted** (D025, from F013). Five
gates now work that way: the conflict-marker rule, `release check`, the
landed-work attribution and generated-stamp rules (T-0024), identifier
allocation (T-0031), and the CI matrix held to the exercised-version record
(T-0034). **Ceiling:** each rule detects only the shape it was written against.
The last of those adds a second kind of falsification — run the thing on an input
the record does not name, rather than mutating the code.

Recently closed there: a CI matrix row per CPython minor from 3.8 to 3.14, held to
`tests/python-versions.json` in both directions, after running the suite on the
five interpreters the record had never heard of found the suite red on all five
(T-0034, F018, D035). Nothing from 3.15 onwards has run, and no gate widens that.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03 on the development
machine: 12 logical CPUs; ~15.3 GiB RAM; ~8.6 GiB free disk at probe (shared,
fluctuating); Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1; `git` 2.55.0.
Public GitHub API, SQLite, and arXiv HTTPS returned 200. NumPy present; SciPy,
pytest, and Z3 absent. `crontab` and `systemctl` present, `systemd --user`
running, no user units. `gh` CLI absent. A VM's own numbers come from
`tools/origin doctor`, which writes `.origin/doctor.json`; this one reports 2
CPUs, Python 3.8.10, `git` 2.25.1.

**Unverified and not to be assumed:** fleet access, unattended supervision, GPU availability. This VM pushes via the GitHub App as `Ihsan Ai Server Bot`.

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
  interrupted run recoverable, plus detection that reveals when it did not happen.- **Session 003, VM 0947 (T-0027).** T-0026's verification passed while its
  defect was still live: a lint on the author's own tree cannot see what a claim
  commit published, and the claim staged only the task file and the ledger. Four
  more red runs followed; `task claim` now stages the rebuilt indexes and the new
  test lints a *fetched* tree on a second clone. **Lesson worth more than the
  fix:** a gate that reads the tree the author is standing in cannot see the
  commit the author is about to publish.
- **Session 002, VM 0947 (T-0026).** `task new` now rebuilds the generated
  indexes, because two CI runs failed on 2026-10-03 for exactly that: a task
  file was pushed before `tasks/INDEX.md` was rebuilt and the orphan rule
  rejected the file the VM had just created. The rule is unchanged — a file no
  command wrote is still an orphan, which the new tests assert. **The task file
  for this work guessed the wrong index:** the stale one was `docs/INDEX.md`,
  which lists task files by path. 274 tests green.
- **Session 001, VM 0947 (T-0025).** The pushed CI run for T-0024 is read and
  recorded: all six steps green on `9e865a4`, including the session-integrity
  step that had been red on every push while a VM was working. The two failures
  from ten minutes earlier were **not** the date defect this session's predecessor
  assumed: their failing step was Documentation lint, and the cause was a task
  file pushed without regenerating `tasks/INDEX.md`. **Reading the run rather than
  the expectation is what caught it.**
