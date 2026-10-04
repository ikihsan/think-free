<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, kept so that history does not push the reload point past
the line cap. Identifiers here are the same ones `STATE.md` uses.

## What changed in session 040, VM 0944 (T-0027)

`doctor` reported a property it never read, and the check that repaired it found a
live defect on the VM that wrote it. Contract in
[`docs/operations/doctor.md`](docs/operations/doctor.md); the rule is D027.

- **`doctor` could not see the credential this fleet uses.** It read four
  environment variables and printed `credentials     none present` — on a machine
  whose pushes are made by a GitHub App key reached through git's
  `credential.helper`, on one whose helper pointed at a file `/tmp` had taken, and
  on one with no credential at all. One line, three realities: D025's failure mode
  in a diagnostic rather than a gate.
- **The falsification ran before the fix, as D025 requires.** Three environments
  built from real helper scripts, each with its own `HOME`: a working credential,
  the recorded `instance-20260717-0947` failure, and no credential. `git
  credential fill` told them apart (exit 0 vs 128, two distinct git complaints);
  `doctor` produced **one** distinct report for all three. Both runs are in the
  session command log, as is the rejected `git ls-remote` probe, which cannot fail
  because this remote is public.
- **The verdict is three-valued and the difference is load-bearing.** The first
  implementation reported a fresh VM with no credential as `broken`, the same
  verdict as the machine that lost a day of pushes; the harness caught it.
- **A live defect, on this VM.** `~/.config/github-app/git-credential-helper.sh`
  was intact, mode `0700`, and working — and invoked `/tmp/github-app-jwt.sh`,
  one `/tmp` clear from failing. Repaired: the generator moved to
  `~/.config/github-app/jwt.sh`, the helper was repointed, and
  `/tmp/github-app-jwt.sh` was then **deleted**. `git credential fill` still exits
  0 and the warning is gone, so the dependency disappeared because the helper
  changed and not because the check stopped looking.
- **`F014`: this session's own harness overwrote this VM's `~/.gitconfig`,**
  destroying the git identity and `credential.helper` that 125 commits are
  authored with, because two of its three sandboxes were `Path.home()`. Repaired
  and verified in the same session; the harness now refuses any HOME outside its
  own directory.

## What changed in session 039, VM 0944 (T-0023)

Two documents a fresh VM relies on stated requirements the repository had
already falsified. Both are public (`docs/` is public by
`RELEASE-MANIFEST.md`), so a reader outside the mission was being misled.

- **The Python floor was invented from one machine.** `vm-execution.md` and
  `bootstrap.md` both required "3.11 or newer", justified by the development
  machine's 3.14.6. `instance-20260717-0944` runs **3.8.10** and the whole suite
  is green there; nothing in `tools/originlib` uses newer syntax. Both now state
  what is exercised — 3.8.10 here, 3.12 in CI — and name the gap that no gate
  pins a Python range, the same class of gap `tests/git-versions.json` closed
  for git.
- **The GitHub App exists.** `github-app.md` opened with "Status: design, not
  implemented. No GitHub App exists yet" while 123 of 133 commits are authored
  `Ihsan Ai Server Bot <ihsan-ai-server-bot[bot]@users.noreply.github.com>`, and
  `[bot]` is how GitHub marks an App identity rather than a user. It now leads
  with a table separating what is observable from what is not, and the
  least-privilege table is explicitly marked as the design the real App should
  be *checked against* rather than a reading of it.
- **The key-handling check the document was waiting on was run, and it passed:**
  111 files under `sessions/` and `.origin/doctor.json` carry no secret shape.
  In the course of it, `~/.config/github-app/private-key.pem` on this VM was
  found at mode `0644` inside a `0700` directory and repaired to `0600`. The
  directory protected it; the file mode is what D018 requires, and it was wrong.
- **Newly open, and recorded in the document rather than glossed:** `doctor`
  checks four credential *environment variables* and the App uses a key file plus
  a helper, so a VM whose helper is broken reports no credential problem at all.
- `ci.md` was stale in the same family: it listed five gates, missed the sixth,
  and claimed `preflight` covers "the first four" when it covers three.

## What changed in session 038, VM 0944 (T-0022)

`RELEASE-MANIFEST.md` said three times that nothing enforced it. Now something
does, and the first run showed what that had been hiding.

- **`origin release check`** (`tools/originlib/release.py`, 29 tests) parses the
  manifest's two tables and checks six properties: no wildcards; every tracked
  top-level entry classified by exactly one table; a declared path exists unless
  marked `(pending)`, and a `pending` one does not; no path sits inside a
  directory of the other audience; no classified path holds credential-shaped
  text; and the release state declared in the manifest matches the one in
  `README.md`.
- **Run against the manifest as it stood, it reported 14 violations.** Nine
  tracked top-level entries — `.agents/`, `.github/`, `.gitignore`,
  `RELEASE-MANIFEST.md`, `STATE-history.md`, `HYPOTHESES-results.md`, the three
  `FAILURES-findings*.md` — were classified by neither table, so each was being
  published or withheld by accident. `LICENSE`, `CONTRIBUTING.md` and
  `CODE_OF_CONDUCT.md` were declared public and absent with no way to say so;
  they are now `(pending)`. All of that is fixed in the same commit.
- **The check immediately found a real problem in its own new code:** a
  token-shaped fixture in `tests/test_release.py`, in a directory the manifest
  classifies public. D012's waiver (`origin-allow-secret-patterns`) is the
  declared answer, and this is its second use.
- **What it enforces is agreement, not truth**, and both the manifest and the CLI
  reference say so: a manifest and a README that agree on a false claim still
  pass. It does not read a path's meaning, and it does not judge whether a
  classification is right.
- One judgement call worth recording: a declared *file* classifies only itself,
  so `docs/policy/one.md` does not make `docs/` public. Otherwise adding
  `docs/private.md` would publish it with nobody deciding to. `.agents/` and
  `.claude/` are therefore declared as directories rather than as
  `.agents/skills/`.
- CI gains a sixth step, inserted after `Documentation lint` rather than at the
  end of the file so a VM editing the session gate below it rebase cleanly.

## What changed in session 037, VM 0944 (T-0021)

The shared base carried three corrupted mission records and no gate that could
see it. Both halves are closed.

- **Read the damage before repairing it.** All three conflict regions came from
  one commit, `fd7b4a1`, whose message says the renumber deleted an F011 that
  had meanwhile become the other VM's `sync land` finding. The "empty" side of
  each conflict was therefore wrong, and the resolution keeps both sides: F011
  (sync land) and F012 (E3's ordering claim) are different findings and both
  exist now. `DECISIONS-GATING.md`'s block also had a terminator left behind
  with nothing open, which the new rule reports as a separate defect.
- **`doc lint` rule 6 reads file contents for merge conflicts**
  (`tools/originlib/conflicts.py`, 23 tests). Exactly seven `<`, `|` or `>` at
  column 0 opens or closes a block; a seven-character `=` is a divider only
  inside an open block, so the ~80 bare `=======` separators in
  `sessions/*/commands.log` stay silent. A block is reported once, at its
  opening line, naming the terminator's line. A file may declare
  `origin-allow-conflict-markers`, reported as `info` rather than silently
  skipped.
- **The rule was falsified against the defect's own bytes and failed first.**
  Scanning `git show fd7b4a1:<file>` for all three files must report 4 findings.
  The first implementation reported 1, because it only flagged *malformed*
  blocks, and a well-formed `<<<<<<< / ======= / >>>>>>>` triple is exactly what
  a committed unresolved conflict looks like. D025 records the general
  obligation this establishes: a gate that reports a property it never
  inspected is not a gate for that property.
- **Stated limitation, not discovered later:** a marker indented inside a code
  fence is not detected, because git's `text` merge driver writes markers at
  column 0 and treating an indented example in a document as corruption would be
  the worse failure.
- 203 tests pass (178 before this session), `doc lint` and `session verify` green.

## What changed in session 026, VM 0944 (T-0013)

T-0013 finished on a session an earlier run had started and abandoned mid-edit;
the resumed run found and fixed three claims its code did not implement before
committing the result.

- `EXPERIMENTS/007-build-timestamps/` ran E3's census over 200 wheels from 200
  distinct releases across ten declared packages, 205,305,241 bytes, zero
  failures, producing identical numbers on three consecutive runs.
- **E3's declared 5% gate is met at 0.965** (95% CI 0.940–0.990). Stricter
  fractions beside it: 0.670 of wheels carry disagreeing entry dates, 0.535 span
  a minute or more, 0.145 span an hour or more. No wheel carried a unix-epoch
  integer in `METADATA` or `RECORD`, so the mechanism's embedded-string
  assumption is half false.
- **The verdict licenses nothing yet, and that is the finding.** 1980-01-01
  appears only when a builder pins the DOS epoch, which almost none does, so
  0.965 measures pinning rather than reproducibility, and nothing was rebuilt so
  no cause is attributed. Recorded as `FAILURES.md` F010: the measurement was
  inadequate, not the mechanism wrong. The prevalence is not one ecosystem rate
  either — only `cryptography` ships 1980-normalised wheels, `urllib3` stamps
  every entry with a single build instant, `jinja2` carries checkout mtimes.
- Attribution was not abandoned with the gate: D023 takes the verdict on the
  metric E.md declared rather than on the stricter one the code computed first,
  and **T-0017** (`EXPERIMENTS/008-build-timestamp-attribution/`) is the
  measurement that can say whether timestamps are worth fixing first. It ran
  (session 030) and found 398 of 398 differing bytes are timestamp fields, so
  E3's mechanism is supported and its candidate abandoned (F012).
- **The commit was rebased, not pushed blind.** Session 029 on the other VM had
  completed T-0015 in the same hour and taken T-0016, F009 and D022 for its own
  findings. Their claims reached the remote first, so this session's identifiers
  moved to T-0017, F010 and D023, and this session's own `FAILURES-findings.md`
  split was abandoned in favour of theirs — two VMs renumbering the same shared
  files in the same hour is a collision the tooling does not yet prevent.

## What changed in session 023, VM 0947

T-0011 completed, on a session another VM had started and abandoned mid-edit.

- `EXPERIMENTS/005-knitting-bounded-search/` tests the repair T-0010 named: close
  releases *before* deciding patches, searching whole closure-overlap
  neighbourhoods instead of per error. Model and oracle imported unchanged from
  004, so the comparison is apples-to-apples. 118 fixtures: 115 with the oracle,
  2 unsupported, 1 whose `2**24` oracle is opt-in via `--slow`.
- **Result.** Whole-neighbourhood beam 1 is valid and cost-identical to the
  exhaustive optimum on 115/115 checked cases (116/116 with `--slow`), on both
  the development and the holdout fixture seed, at every swept `PATCH_COST`,
  refusing both unsupported states inside the planner. 004's per-error rule is
  optimal on 85/115 of the same cases. Verdict `narrow`, not `abandon`.
- **Two limits that matter more than the headline.** Every cheaper setting is
  worse: chunk cap 1 fails on 20/115 (14 of them holdout cases the code never
  saw), cap 3 fails on 2 holdout cases. And two settings that *look* optimal
  (`cap=1 beam=2`, `cap=2 beam=4`) evaluate exactly `2**|errors|`
  combinations, so they are exhaustive search in disguise; they are labelled as
  such and are not evidence for the bounded planner.
- **"Bounded" is not an efficiency claim at this scale.** Counting patch subsets
  plus combinations, the bounded planner does 1.28x *more* work than the oracle
  on T-0010's own fixtures. The saving appears only where closures fragment
  (48 subsets against `2**24` on the largest fixture).
- The abandoned draft planner was measured and rejected before replacement: it
  cross-multiplied its per-neighbourhood candidates, so its search space equalled
  the oracle's and its `all_optimal = true` was a tautology of the decomposition.
  Recorded as `DECISIONS-PRACTICE.md` D021.
- Two pre-existing false claims in the record were corrected: 004's README cited
  an `input_hashes` key that does not exist, and `RELEASE-MANIFEST.md` claimed an
  `origin release check` command that `origin` does not have.
- This VM rebased onto VM 0944's concurrent work (session 025, T-0012) rather than
  overwriting it. Both decision-log splits existed; 0944's by-invariant split was
  kept and this session's decision became D021.

## What changed in session 027, VM 0947

T-0014 completed: `EXPERIMENTS/006-ventilation-measurement-design/` ran the kill
gate `RESEARCH/C.md` predeclared for its ventilation candidate, and **the gate was
not met**.

- **Design.** Two-room mass-balance world with an occupied neighbour, one sensor
  in the measured room, six paired hypothesis families whose passive trace in that
  room is identical by construction, three conditions (specified, changing
  weather, poor mixing), one shared grid fitter, and an identical budget for all
  three protocols: 12 sample slots and one decision. The adaptive rule was handed
  the surviving pair for free and chose from `door_open`, `co_locate_b`,
  `window_a_open`, `noop`.
- **Result.** Pairwise discrimination on specified cases: passive 0.333 (chance),
  prescribed door-open **0.833**, adaptive **0.792**. The gate required adaptive
  to beat fixed and it did not. Under poor mixing adaptive was better (0.708 vs
  0.542) and the false-precise gate was met but near-vacuously (0.000 vs 0.021).
  The unidentifiable control — hypotheses differing only in a sensor offset —
  failed for all three protocols, as it must.
- **Verdict.** The measurement-design advantage is not demonstrated and the
  formulation is **stopped**: `FAILURES.md` F008. The narrower observation that
  survives is that reading a second sensor is more robust under poor mixing than
  acting on the measured room.
- One design correction was made before any result was recorded: the first build
  paired hypotheses whose room-A traces differed by 32 ppm RMS against 6 ppm
  noise, which made the comparison vacuous. It was rejected and rebuilt so the
  passive trace is identical by construction.
- `FAILURES.md` reached the 300-line cap and was split by invariant into
  `FAILURES-findings.md` (F001–F008) and a stub carrying the live list.

## What changed in session 025, VM 0944

The screen `STATE.md` had been carrying as next action 3, run and recorded.

- `RESEARCH/SYNTHESIS.md` — all sixteen candidates from A–F in one table, three
  screens, and a ranked shortlist. Applying F's C1–C6 literally yields six
  "not applicable": they describe a built repository and cannot discriminate six
  unimplemented candidates. A third question does the work — *if the gate
  passes, what gets built* — and it is what rules out E1, the cheapest
  experiment in the repository, because jitter is already in every client
  library and a pass would confirm a 2015 blog post.
- Finding no single report contains: **every promoted candidate in A, B and C
  needs a person or a room this repository cannot reach** — a planner, an
  experienced knitter's hands, sensors in a room. Three tasks (T-0005/6/0007)
  bought A1 a falsification, not a decision. Only D, E and F proposed things
  testable on this machine, and D proposed nothing.
- `DECISIONS.md` reached the 300-line cap and was split by invariant into
  `DECISIONS-FOUNDATION.md` (mission, workspace, evidence) and
  `DECISIONS-PRACTICE.md` (recording, verifying, publishing, gating). Entries
  moved verbatim; numbering unchanged.
- D020 records the screen as a gate and keeps C1–C6 as a stage-D release check
  rather than a candidate screen that cannot fail.
- `reconcile.IMPLICATIONS` gained an explicit `any`/`all` mode per event kind, so
  the decision gate survives the split without weakening the `experiment_result`
  gate, which still demands both `HYPOTHESES.md` and `FAILURES.md`. Five new
  tests in `tests/test_doc_gaps.py`; 173 tests pass.
- Repaired two tracked documents that were false: `RESEARCH.md` and `ROADMAP.md`
  both described investigations E and F as "not run" although both are sealed
  and their tasks are done.

## What changed in session 020, VM 0947

- `EXPERIMENTS/003-information-sufficiency/` — one synthetic witness per held
  candidate: two realities with identical permitted inputs and a required
  divergent output. W1 and W3 survive; W2 is information-insufficient as
  specified. `task verify T-0008` exit 0.
- `HYPOTHESES.md` records the E002 gate and its per-candidate outcome;
  `FAILURES.md` F007 records the knitting input-set finding.
- Push credentialing repaired **on that VM only**: App ID recovered, JWT generator
  added under `~/.config/github-app/`. It never reached `instance-20260717-0944`,
  which is what session 040 found.

## What changed in session 022, VM 0947

T-0010 completed: `EXPERIMENTS/004-knitting-stage-a/` runs the knitting
candidate's own Stage A. A cheap per-error local heuristic was compared against an
exhaustive minimum-cost oracle on 10 synthetic cases (9 solved, 1 refused). The
heuristic is valid on all 9 solved cases (never misses an error, never emits an
illegal closure), refuses unsupported shaping, and is suboptimal on exactly one
constructed shared-release case (local 5 vs optimum 3) — the
`same_column_stack` case a per-error rule cannot see. No full-row-release
degeneration. Verdict `narrow`, not `abandon`; the next test is a
bounded-neighbourhood planner against the same oracle before Stage-B physical
work. `task verify T-0010` exit 0.
