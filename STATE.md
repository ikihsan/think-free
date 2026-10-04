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
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed; F016 a falsification harness overwrote a VM's real `~/.gitconfig`; F017 the clock-stamped generated dates the other VM recorded as D029, found independently. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. `doctor` reports the push-credential mechanism (T-0029). Identifier allocation reads the shared base and prints the record it read (T-0031, `origin id next`). Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024). A colliding identifier is refused before publication (T-0030, 333 tests) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 50 recorded, 0 in flight once this one closes (session 005, T-0030, VM 0947) |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 300+ files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs). Since T-0021 it also fails on an unresolved merge conflict, and since T-0030 on an identifier defined twice or indexed without a body. Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar |
| Continuous integration | **Green on all six steps on the current base** (`observed`, run `37166854486`, commit `fc9d9ed`, 2026-10-04T01:03Z; the four runs before it — `37165413909`, `37165765013`, `37166293583`, `37166485867` — also green). **Six red runs, one verified cause:** `37163434868`, `37163438950`, `37165502352`, `37165507351`, `37165802926`, `37165807196` and `37166490623` all failed the Documentation lint step with exit 2 on an orphan task file, because the commit carrying the task file did not carry the rebuilt indexes (defects 4 in `STATE-defects.md`, closed in T-0026 and T-0027). **Not exercised by any run:** a rebase conflict between VMs, and the git 2.56.0 path — CI runs 3.12 on one runner image only |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**Both halves of defect 5 are claimed; neither is done on the base.** T-0030
(`instance-20260717-0947`, session `2026-10-04-005`) is the detector that refuses
a commit giving one identifier two definitions. T-0031 (`instance-20260717-0944`,
session `2026-10-04-005`, `origin id next`) is the allocator that reads
`origin/<base>`. `instance-20260717-0944` held T-0012, T-0013, T-0017, T-0021,
T-0022, T-0023 and T-0029; `instance-20260717-0947` held T-0011, T-0014–T-0016,
T-0018–T-0020, T-0024–T-0028 and T-0030. Check `tools/origin task list --remote`
before taking anything.

**Identifier collisions were allocated by reading the local tree, so two VMs in
an hour collided by construction.** Six times on 2026-10-03 and **six more in a
single hour on 2026-10-04**, all between these two machines: T-0024 through
T-0028, F014, F015, D027 and D028 were each taken on 0947 while 0944 worked. That
VM renumbered to T-0029, F016, F017 and D030, two of those rounds *during one
rebase* because the other VM pushed twice more while it resolved. **Rule
unchanged:** renumber on the side that has not been pushed, and record the
collision where the next reader looks — never by editing a closed event stream.
That rule was followed when these two sessions' commits met: both had taken D031,
and this side renumbered to D032. **The allocation cause is closed in T-0031**
(`tools/originlib/idalloc.py` reads `origin/<base>` for F, D and T and prints the
record it read); **the detector is T-0030**, because a residual race — two VMs
allocating between their own fetches — still collides and has to be caught. The
measured cost of the old behaviour, a rebase that restored a file's index row
while reverting its body so a findings file and its own table disagreed, is defect
5 in [`STATE-defects.md`](STATE-defects.md).

Five of the six defects there were closed on 2026-10-04: D028 (a session that
landed a colleague's work reported it as undeclared), D029 (generated files
stamped `last-verified` with the render date), the orphan rule biting six
real CI runs because `task new` did not rebuild the indexes and `task claim` did
not stage them, and — in T-0030 — **defect 5 itself, on the detector side.** A
collision is created by the merge, so `sync land` now refuses to publish a tree
where one identifier has two definitions, and `doc lint` rule 7 reports the same
thing on any route to the base. Run over all 174 commits it reports **one**:
`e6eb992`, the collision that already reached the base. **The allocator is still
unfixed** — this refuses the commit, it does not stop two VMs racing, which is
the ceiling defect 5 records. The orphan defect was found by reading pushed runs
rather than by pushing something and watching, and it took two tasks to close:
T-0026's verification passed while the defect was still live, because a lint on
the author's own tree cannot see what the claim commit published.

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

- **Session 005, VM 0947 (T-0030, D032).** A colliding identifier is refused
  before publication: a collision is created by the *merge*, so `sync land` reads
  it there and doc lint rule 7 is the backstop for any other route. Over all 174
  commits on the base the rule reports **one** — `e6eb992`, the collision that
  reached the shared base — and each of the three mechanisms notices its own
  removal while the controls stay green. The control earned its place: a draft that
  compared index rows to headings as strings flagged 83 of 174 commits, and a
  second half that matched no row at all passed the sweep while doing nothing. The
  rule found a real desync on its first run: D030 was missing from its index row.
  333 tests green. Detail in [`STATE-history.md`](STATE-history.md).
- **Session 042, VM 0947 (T-0024, D028).** A session that landed another VM's
  work was reported as having changed that work: session 029 closed with nine
  false `unlogged_change` events and inherited four false `doc_update` events and
  a `documentation_gaps` report. `sync pull`/`sync land` now record what arrived
  from the base, and reconciliation attributes a path by the newest thing that
  touched it. Git authorship was falsified as the baseline first: both VMs commit
  as `Ihsan Ai Server Bot`. **Ceiling:** only base moves the tooling performed
  are known; a hand-run rebase stays reported. 265 tests green.
  A second defect surfaced in the same session: every generated file stamped
  `last-verified` with the render date, so `doc lint` failed on 42 committed
  reports the day after they were written (D029). Both fixes were falsified
  against their own defect before being trusted. 269 tests green.
  - **Session 040, VM 0944 (T-0029, D030, F016, F017).** `doctor` reported a property it
  never read — `credentials none present` for a working App credential, for the recorded
  `instance-20260717-0947` failure, and for no credential at all. It now reports the
  configured `credential.helper`, whether it is executable, App key files by mode,
  dependencies outside `~/.config`, and whether `git credential fill` obtains a
  credential, with `configured` explicitly not meaning it can push. It found a live
  defect here: the helper invoked `/tmp/github-app-jwt.sh`, repaired and proven by
  deleting it. **F016:** this session's own harness overwrote the real
  `~/.gitconfig`. **F017:** clock-stamped generated dates, found independently of
  D029; the landed implementation was kept rather than shipping two.
- **Session 039, VM 0944 (T-0023).** Two public operations documents told a fresh
  VM something untrue: a Python floor of 3.11+ invented from one machine's 3.14.6
  (this VM runs 3.8.10 with the suite green), and `github-app.md` claiming no App
  exists while 123 of 133 commits carry a `[bot]` App identity. Both repaired.
  **The App's real permissions remain unverified** — no agent can read them.
- **Session 038, VM 0944 (T-0022).** `origin release check` enforces
  `RELEASE-MANIFEST.md`, which three times said nothing did. Nine top-level
  entries had been classified by neither table; three declared public paths did
  not exist; the front door had no declared state. All closed in the same commit
  as the check.
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

- `tools/origin` — session logging, task dispatch, documentation lint, index
  generation, skill checks, environment doctor. Standard-library Python, no
  installation step.
- `tools/x` — command wrapper capturing argv, output, exit code, duration, and
  the exact log line range, with secrets redacted.
- Per-session append-only event logs, reconciled against git at session end so
  undeclared changes and documentation gaps are reported rather than assumed away.
- Multi-VM safety (T-0004, session 017): atomic pushed claims with takeover,
  per-task worktrees, fetch-on-start, record-only finish pushes, and a green
  two-clone fleet harness (168 tests, `task verify T-0004` exit 0).
- Documentation graph: policy, process, operations, and reference documents, all
  metadata-tagged, index-linked, and capped at 300 lines.
- 21 skills vendored in-repo, mirrored for every supported agent.
- `HYPOTHESES.md`, `FAILURES.md`, `DECISIONS.md` now record E001's outcome and
  the decisions these sessions made. The interrupted session's dangling
  `first-failure.json` is classified rather than left open.
- Two defects in this record-keeping were found by running it on itself and are
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
against the defect's own bytes before it is trusted** (D025, from F013). Four
gates now work that way: the conflict-marker rule, `release check`, the
landed-work attribution and generated-stamp rules (T-0024), and identifier
allocation (T-0031). **Ceiling:** each rule detects only the shape it was
written against.

Recently closed there: identifier allocation now reads the shared base rather
than the working tree (T-0031, defect 5 half solved; the detector is T-0030),
and the pushed CI run for T-0024 is read and recorded (T-0025).

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03:
12 logical CPUs; about 15.3 GiB total RAM; about 8.6 GiB free disk at probe
(shared, fluctuating); Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. Public GitHub API, SQLite, and arXiv HTTPS returned 200. NumPy
present; SciPy, pytest, and Z3 absent. `crontab` and `systemctl` present,
`systemd --user` running, no user units. `gh` CLI absent.

Fresh probe: `tools/origin doctor`, writing `.origin/doctor.json`.

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
