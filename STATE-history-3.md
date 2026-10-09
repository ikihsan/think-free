<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Session history, part 3

The oldest per-session entries, moved out of [`STATE-history-2.md`](STATE-history-2.md)
on 2026-10-09 when E069's record pushed the history chain past its line cap.
Nothing was edited in the move; every identifier here is one `STATE.md` or a
findings file also uses.

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

## Moved from `STATE-history.md` on 2026-10-09, at the 300-line cap

These two sections sat in `STATE-history.md` and moved here when E069's record
pushed it past the cap. Nothing was changed but the file they live in.

## What changed in the 2026-10-06 sessions (moved from STATE.md, cap)

- **Session 2026-10-06-015 (E041 reconcile/publish) finished: worked.** The 816-test
  suite is green (OK, 651s), doc lint exits 0, and the test-suite and release-check
  gates it had left "running in background" are captured in its command log.

## Moved out of `STATE.md` on 2026-10-07, at the 300-line cap

These entries are about the `stg` line and are superseded by E045's withdrawal of the
candidate (F081, F082) and by E047 (F084). They are kept here, not deleted, because
the identifiers they carry are still cited by the candidate record.

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

## Moved from `STATE-history.md` on 2026-10-09, when E069's record pushed it past the cap

These three sections sat in `STATE-history.md` and moved here in that split.
Nothing was edited in the move.

Moved from `STATE.md`'s *What changed recently* on 2026-10-09, when that file
passed the 300-line cap on E069's record. The findings (F098, F099, F100) and
decisions (D085, D086, D087) stand; this is the per-session detail.

- **Session 2026-10-08-021, VM 0944: E066, F100, D087.** E066 confirmed E063's finding on the mission's own need corpora: classified all 189 E038 GitHub issues (only 34 actually about git line staging, 155 false positives on CI/CD/build stages) and 100 HN needs (top 5 triggers, 20 each; 55% not-software, 39% resolved-from-knowledge). The need-harvest route retires at the population level: GitHub corpus measures CI stages not git staging; HN corpus measures wishes/politics not tool requests. `unserved-open` 0 of sampled rows. This replicates E063's arm A served share 0.676 and arm B 0.969 with an independent classifier. E063's instrument with controls (G1/G2/G4) is the primary result; E066 is an independent confirmation. The route is closed — seven emptiness measurements (F029, F039, F051, F059, F081, F084, F085) were reading a served-statement route.
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
