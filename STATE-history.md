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

## What changed in session 012, VM 0947 (T-0034)

The exercised-Python record named 3.9 to 3.11 as versions nobody had run, and its
own `why` clause gave the reason: *"CI pins a single version"*. The 3.8-or-newer
floor was two points with a gap between them. So the gap was measured instead of
described — portable CPython builds (python-build-standalone, unpacked outside the
repository, no installation step) for 3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2,
each running the full suite.

**The gap was not hypothetical, and it was not a version incompatibility.** All
five runs failed, with exactly one failure each and no errors, on
`RealRecordTest.test_the_reported_scope_names_this_suites_size` — a test written
hours earlier in T-0033 that asserts *this* interpreter appears in
`tests/python-versions.json`. 3.14.2, an interpreter newer than anything this
repository has ever named, failed exactly as 3.9.23 did. `FAILURES.md` F018,
defect 7 in [`STATE-defects.md`](STATE-defects.md).

- **The half that was nearly missed.** A sibling test asserts the same
  "this interpreter is recorded" claim from a different source: `doctor` probes
  `python3` on `PATH`. One question, two sources, agreeing only because this VM's
  `PATH` interpreter is 3.8.10 — the one recorded version available locally.
- **Why adding the matrix without the repair would have been worse than not
  adding it.** Five of seven rows red for a reason about the record invites two
  responses, weaken the assertion or drop the rows, and both reduce measurement.
- **The second machine-fact gate, one function away, and this one was invisible
  from outside.** T-0033 had also added an assertion that *this machine's* git is
  in `tests/git-versions.json`. The matrix's seven rows were all red at the
  `Tests` step, including rows whose interpreter had just been measured green on a
  VM; the run log needs admin rights and the public check-runs API returned
  `annotation_count: None` for every failing check, so the annotation route
  `docs/operations/ci.md` relies on does not work unauthenticated. Found by
  elimination (every row's minor version was green locally, so not the
  interpreter) and then by reading the runner image's own readme, which lists
  **Git 2.55.0** — a version the git record did not name. A conda-forge 2.55.0
  was unpacked outside the repository and reproduced the failure exactly.
  `FAILURES.md` F019, defect 8.
- **What was actually repaired.** Not the missing entry — the assertion. It is
  now the module's contract (four states reachable, an `exercised` verdict
  carrying its entry's scope and machine), with a control that emptying the
  record moves every version off `exercised`. Adding the 2.55.0 entry alone would
  have made CI green and left the assumption in place. The git record gained a
  2.55.0 entry, a `where` on every entry, and a `not_exercised` list — 2.26–2.54
  and 2.57+ — with test clauses, so the gap is named rather than inferred from
  two points.
- **`docs/operations/ci.md` no longer claims the annotation route works.** It
  says what is readable without rights — step conclusions and check names, which
  with a matrix is enough to localise a failure to a version — and names the fix
  that would make it enough to localise it to a test: one check per test file.
- **The other VM found the same assertion from the other end, an hour later.**
  Its CI run was red on the same test for the mirror-image reason: on a CI row the
  matched entry is `3.12`, whose scope names a run id rather than a test count.
  Its fix asserted the reported scope is the matched entry's own text unchanged —
  a different property from the one it replaced. The rebase resolved the conflict
  by keeping both clauses, because neither catches the other's failure, and the
  record's `3.12` CI entry was given a count as well as its run id.
- **Repair.** The test states the disjunction it can support: every entry's
  `scope` names a test count, the comparison returns that entry's text
  unaltered, and this interpreter either matches an entry or is reported
  `unrecorded` with its version named. The coupling is enforced on the two
  artefacts instead: `tests/test_ci_matrix.py` holds the workflow's row list and
  the record to each other in both directions, and
  `test_pythonversions.py`'s "minor version only" clause now reads its allowed
  set from the workflow so a new row cannot slip past it.
- **Falsified in four directions** — a row with no recorded scope, a guard naming
  a version that is not a row, `fail-fast` returned to its default, and the
  unmodified workflow — with the restored file green as the control. One
  non-detection is recorded rather than hidden: moving every guard to a
  *different real row* passes, because which row carries the file-reading gates is
  a decision in `docs/operations/ci.md`, not a property a gate can read without
  duplicating it. Two of the parsers were corrected first because the controls
  they failed were the parsers, not the code.
- **`doctor` now names the machine.** One record covers two environments per
  minor version — a portable build on a VM and a CI row — so a patch-level entry
  can shadow the minor-level one, and `exercised` alone would describe a runner
  the reader has never seen. The matched entry's own `where` travels with the
  verdict.
- 392 tests green on 3.8.10, on all five portable builds, and on git 2.55.0 —
  the runner's own git. D035 in
  [`DECISIONS-GATING.md`](DECISIONS-GATING.md).

## What changed in session 005, VM 0947 (T-0030)

A collision between two VMs is created by the *merge*: each branch is internally
consistent, and each VM's own `doc lint` sees nothing wrong with its own tree. So
that is where the property is now read. `tools/originlib/identifiers.py` reports an
identifier defined twice, an index row with no definition behind it, a defined
finding with no row, and a decision its own index row does not list.
`sync land` refuses to publish a tree the rule would refuse; doc lint rule 7 is
the backstop for any other route. D032 in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).

**Falsified in both directions.** Run over all 174 commits on the shared base the
rule reports **one** — `e6eb992`, which carries two different findings both headed
`## F010` to the base — and the hand repair one minute later is clean. Removing
each of the three mechanisms in turn makes the covering test fail while the
controls stay green; both runs are in this session's `commands.log`.

**The control earned its place.** A draft that compared an index row to its heading
as strings flagged 83 of 174 commits including the tip, because two rows in
`FAILURES.md` are shortened paraphrases on purpose. A second half, fixed next,
allowed no Markdown link in its filename pattern and so matched no row in any
commit — a sweep that passed while the rule did nothing. The rule also found a
real desync on its first run: **D030 was missing from its row in `DECISIONS.md`.**

## What changed in session 040, VM 0944 (T-0029)

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
