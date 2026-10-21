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

---

## Moved from `STATE.md` on 2026-10-20, at the 300-line cap

These entries predate the money-axis narrative (E193+) and were moved here to
keep `STATE.md` focused on the active research line. Nothing was edited in the
move; every identifier here is one `STATE.md` or a findings file also uses.

**Six service closures in a row
measured a mixture and reported it as one number, and E177 has separated the two
halves: the assistant reaches 0.8667 where a question carries the fact its own
resolution depends on and 0.4000 where it does not** (F136, D118). The superseded
narrative this file used to carry in full is in [`STATE-history.md`](STATE-history.md);
what follows is only what a reader still needs.

**Four closed lines moved to [`STATE-history-2.md`](STATE-history-2.md) on
2026-10-19 at the cap, unchanged in meaning:** the `stage-lines` candidate and
its three closures (F075, F081–F083); E062's `publishable` confound (F096); the
view-count principle's withdrawal (F116, D105); and E091/E092's appliance-diagnosis
line with the Fisher-tail and registry-derivation defects (F114, F115).

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

**E162 completed (2026-10-15, local lineage, renumbered F148): the deterministic accessibility repairer is closed on mechanism, and the dominant WCAG class is plumbing.** 27 real pages, axe-core 4.14.0 in jsdom as an independent oracle, corpus hashed before any repairer existed. A repairer forbidden to invent eliminated **0 of 125** AA-tagged instances against a declared 30% gate; permitted to invent it eliminated 99 (79.2%) and **104 of its 104 repairs were fabrications**. Measured with no repairer in the loop: of the 121 instances whose defect *is* a missing name, **120 (99.2%) carry no author-written string on the node axe reported**, and **92 of 125 (73.6%) of the WCAG-tagged violations aim at machine-generated anchors** — 90 of them one syntax highlighter's line anchors. No candidate. [`162`](EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md), [`163` protocol](EXPERIMENTS/163-a11y-content-defect-composition/PROTOCOL.md).

**The value pre-pass line (local lineage, F144/F145) is measured in both directions and remains closed as a candidate.** `valueset.py` is exact on regulatory text — E142 measured 1.0 detection, 0.0 false positives on 20 Federal Register final rules — and detects **0.2826** on SQuAD v2.0's human-written answers against a declared 0.95, with 0.0113 false positives. A rate is a property of *(instrument, population)*; the general claim stays closed and the regulatory scope is recorded (D124–D126). [`140`](EXPERIMENTS/140-judge-form-invariance/RESULT.md), [`141`](EXPERIMENTS/141-valueset-second-genre/RESULT.md).

**Identifier collision, recorded not renumbered (2026-10-15).** `E140` names
two different things, both committed on 2026-10-14: the **CI/CD pipeline
failure protocol** (`EXPERIMENTS/140-github-actions-ci-failures/`, session
2026-10-14-030) and the **preflight release-readiness evaluation** (the
"E140 completed" entry below, commit `fc997da4`). Both are already pushed, so
neither is renumbered; **E140 unqualified in a sentence about CI failures means
the protocol, and in a sentence about releasing `preflight` means the
evaluation.** A later reader who takes the other reading will conclude the CI
harvest ran.

**E150 completed (2026-10-15): Hugging Face Hub view-count principle test fails — the principle does not extend to model hubs.** 1,900 models sampled via multiple sort strategies, classified by pre-declared rules into 1,151 need-related (derivatives, fine-tunes, quantized, task-adapted) and 170 general (base foundation models from major labs). Cliff's delta: likes=0.094, downloads=-0.085 (general higher), trendingScore=0.122 — all <0.147 kill gate threshold. Base models are infrastructure downloaded massively as dependencies for fine-tuning; fine-tuned models get more likes but far fewer downloads. The view-count principle works on package registries (leaf consumption) but not model hubs (infrastructure layer). Kill gate fired; principle boundary extended. See [`EXPERIMENTS/150-huggingface-viewcount/RESULT.md`](EXPERIMENTS/150-huggingface-viewcount/RESULT.md).

**E165 completed (2026-10-15): VS Code Marketplace view-count principle test fails — the principle does not extend to this extension marketplace with broad keyword classification.** 1,884 extensions fetched from 28 categories via the VS Code Marketplace API (v7.1-preview.1); 1,706 (90.5%) classified as "need-related" (keywords: fix, debug, lint, test, deploy, tool, utility, helper, etc.), 105 (5.6%) as "general" (theme, keymap, snippet, pack), 73 (3.9%) other. Cliff's delta (install count, need-related vs general): **-0.0266**, below 0.147 kill gate. The classifier was too broad — 90% of extensions captured as "need-related". General category (themes, keymaps, snippets) has marginally higher median installs (1,033 vs 955). Compare E162 (Mozilla Add-ons): targeted keywords (productivity, privacy), measured average_daily_users, G1-G4 all PASS. The view-count principle's domain of validity remains package registries (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos) and Mozilla Add-ons with targeted classification. Kill gate fired; principle boundary extended. See [`EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md`](EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md).

**The version-pinned line (E168 → E169 → E170, all 2026-10-16) is closed, with
its mechanism measured rather than asserted.** E168 stratified a 299-row
high-arrival Stack Overflow pool and found **85 of 299 = 0.2843** version-pinned
needs, Wilson [0.2361, 0.3379], **14× E126's 2.0% program-shaped residue**, with
the assistant serving the high-arrival end of that class at **11 of 24 = 0.4583**
against a pool-level 0.6750 (Fisher p = 0.1168 — a point estimate, not
established). E169 measured the incumbent mechanism E168 had named — *search the
project's issue tracker with the exact error string* — and **withdrew it on its
own control**: a target's own quoted title returns **17,033,706** hits, and
general web search is unavailable from this host (F130). Replaced by
**containment**, which needs no search engine: median term coverage 0.625, 9 of
13 ≥ 0.5, and **0 of 13 share a 3-word run with the fix**, while coverage against
the whole **thread** is ≥ 0.8 on 12 of 13 — the forum thread is the delivery
mechanism and the tracker link is a citation. Two record corrections ride with
it: E168's "`github.com` in 15 of 24" does not reproduce (12 by `href`, 13
counting gists), and 7 of the 85 `vp=1` rows are no longer fetchable.

**E170/E174 (2026-10-16/17), fix-reachability by ranked search: neither query form reaches the fix
globally, and repo scoping is what makes it work at all.** `in:title` returns the target at rank 1
on 11/13 by API and 10/13 on the web surface (both capability controls pass). The quoted error string
reaches the fix on 1/8 rows, component+symptom on 2/13, paired McNemar p = 1.0. **E174 recomputed all
seven arms from E170's own committed responses** and found the five it stored and did not report:
repo-scoped, **5/13 = 0.3846 each, union 6/13 = 0.4615** against the global arms' 0.1538, McNemar
p = 0.125. The best scoped point estimate clears E170's own declared 0.30 bar while its Wilson lower
bound does not, so it is a point estimate at n = 13 and **the line is `unresolved`, not closed**.
What survives is the vocabulary measurement - **a failure report names the symptom and the
environment; a fix states the cause and the change**, 0 of 13 rows share a three-word run - and
five reproducible index defects. Full entries in [`STATE-next-actions.md`](STATE-next-actions.md).
**E174 completed (2026-10-17): the whole session's work was to check whether the
record's fifteenth closure followed from its own evidence, and it did not.**
`tools/x -- python3 EXPERIMENTS/174-scoped-reach-recompute/recompute.py` reads
only files E170 committed; it prints G1/G2/G3 and writes the row-level rank table.
The rule earned: **an arm present in `summary.json` and absent from the write-up
is a defect in the write-up, and the check is a count** — declare the number of
arms in the protocol and reconcile it against the number reported *before* the
conclusion sentence is written. The same session also reconciled five sessions'
unlogged work and found **two identifiers carrying four mutually contradictory
records with no raw data behind any of them**, one of them reporting a *pass* for
a screen D105 had already withdrawn (F133); both are `untested` and add no venue
to any tally.

**E175 completed (2026-10-17): the registry route derives the wrong repository,
and its own declared kill fires.** 200 rows drawn by a committed seed, 145 with
answers: **21 name a GitHub repository and 10 a specific tracker document — 0.1448
and 0.0690 of answered rows.** **G1 = 0 of 21 = 0.0000**, Wilson
[0.0000, 0.1546], declared kill 0.20, **20 `wrong_repo` and 1 `not_in_registry`**:
`hapijs/code` for `microsoft/vscode`, `rumpl/c` for `vs-solutionpersistence`.
**A package registry is keyed by distributable name and a failure report carries
a symptom name** — the projects that own fixes are applications, runtimes,
standards bodies and working groups, and where a name *is* a registry name it is
a common word owned by an unrelated package, so collision returns a confident
wrong answer where an abstention would have been honest. **The zero was wrong
four times**, each repair declared and committed before the next run, and G0's
later runs are withdrawn as instrument-limited (`403`, 60/hour). G2 is **not
run**: stage two of a pipeline whose stage one is wrong 20 in 21 measures
nothing. The step stays open and redirected — a *project index* is the right
source shape, those exist as prior art, so nothing is proposed to build (D117,
F135). [`E175`](EXPERIMENTS/175-repo-from-report/RESULT.md).

**E177 completed (2026-10-17): the mission's only standing constraint is now measured, and it is supported.** Six service closures in a row each reported one number for a pool containing two kinds of question. Same venue, key, treatment and blinded readers; the only difference is whether the question contained the fact its own resolution depends on: **SELF 26/30 = 0.8667 [0.7032, 0.9469]; EVID 12/30 = 0.4000 [0.2459, 0.5768]; gap +0.4667, Fisher p = 0.000368**, against a bar of `gap >= 0.25` and `p < 0.05` declared before any answer body was read; four controls green. **0.4000 is the lowest rate a free general assistant has scored on a real question population here, and it was inside all six closure pools, unmeasured** (F136, D118). The class is **46 of the 100 highest-arrival rows carrying a key answer**, its failures spread across its kinds in proportion, so no mechanical sub-kind exists to check; **abstention was 0 of 30 against 0 of 30**, so the assistant answers confidently on exactly the questions whose evidence is absent and is wrong 60% of the time. Six instrument defects were declared, four before any measurement; the last left **every control green while the p-value was wrong by 2,700×**, because a reader protocol has no control on its arithmetic. A post-hoc pass flagged **7 of the 30 EVID labels** as indefensible — one wrong answer rather than absent evidence, one untestable row with no fix in existence, one mirror URL — so **CLF's precision on this population is ~0.77–0.87, not 1.0**; the headline is not recomputed, because dropping rows after seeing which arm scored is fitting. [`RESULT.md`](EXPERIMENTS/177-evidence-gated-need/RESULT.md).

**F137 (2026-10-17, exploratory cross-tab): the round trip fails uniformly and the unserved residue is tiny.** A post-hoc cross-tab of `has_ask` against the M2 bucket (replicating E178's exact `is_ask` lexicon) shows the round trip's failure is **uniform across buckets** — 7/21 asker_only, 6/20 third_party, 2/5 none (overall 15/46 = 0.3261). It is not concentrated in asker_only, so there is no special asker-held-fact sub-population for an automated ask to uniquely serve. On the 30 scored EVID rows, the genuinely unserved residue (round trip failed AND assistant missed) is **7/30 = 0.2333**, and all 7 carry a key answer — they were served by a mechanism other than the assistant or the visible round trip. **The "automated ask" route has no buildable sub-population on Stack Overflow.**

**F138 (2026-10-17, fresh observation): the round trip is stronger, not weaker, when the missing fact is personal.** On Personal Finance SE (`money.stackexchange.com`, the largest non-software SE site where high-arrival questions routinely turn on a personal fact), the top 30 highest-vote questions with answers were scored with E178's `is_ask` lexicon. **9/30 = 0.3000 lack a specific personal fact** (the money-SE analog of E177's EVID class), and **27/30 = 0.9000 carry a round-trip ask** — against SO's 31/46 = 0.6739. The round trip is **stronger** on money SE, not weaker: the venue asks more readily when the fact is sensitive. **F137's conclusion is confirmed on a second venue.** The "unserved need" hypothesis is dead for money SE too. Raw data: `/tmp/opencode/money_analysis.json`.

**E181 completed (2026-10-18) and superseded by E182: supplying the missing fact
does not move the assistant, and pasting the thread does not either.** Four paired
arms, one population, no arm label in any input file: question alone 7/14 = 0.5000,
+ the extracted missing fact 8/14 = 0.5714, + every comment verbatim 9/14 = 0.6429,
placebo 4/10. **Every paired comparison is null** (exact McNemar p = 1.0), and
pasting the entire discussion beat answering the question alone on **0** rows. The
comments name the deciding fact on 14/30 = 0.4667, with 10 of the 16 nulls carrying
the remedy itself — **the round trip runs to the solution, not to the fact.**
**G4 FIRED** (the same reader disagreed with itself on 4 of 10), so no absolute
level in E181 may be compared with E177's. Full entry:
[`E181`](EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md).

> **RUN as E182 (2026-10-18); the question had to be corrected first.** The draw
> is of questions that were *unanswered*, so `accepted_answer_id` is non-null on
> **0 of 60** rows and the key answer is the **top-voted** one (F141). Corrected
> and run with an instrument built for it: the ground truth on missed rows is no
> more contested (**p = 1.0**) and no more divergent (**p = 1.0000**) than on
> reached rows, on an instrument that cleared its own declared bar at **0.8000 /
> specificity 1.0000**. Vote margin was **4 of 10** against hand-read labels, so
> its earlier null was **withdrawn, not reported**. **The EVID line closes as a
> capability limit.** [Full entry.](EXPERIMENTS/182-ground-truth-contest/RESULT.md).

**Superseded by E181 and closed by E182 (2026-10-18).** The named next action
that stood here — read the rows every arm missed and ask whether the
community's chosen resolution is contestable — was run as E182, whose record is
the blockquote above, and those 11 lines were removed from this file on
2026-10-19 rather than left as a directive a cold session could re-run.

**Superseded (2026-10-18).** **Named next action: return to fresh exploration.** The EVID class is served by the venue's round trip across two venues of very different personal-fact sensitivity. The genuinely unserved residue is small and eventually answered in both. The "unserved need" hypothesis is dead for every population this mission can measure. The mission should either test a completely different kind of need (not evidence-gated questions) or pivot to a different invention axis entirely.

> **E178 closed the fetch route** (`publishable` **0/46**; `has_ask` **0.6739**,
> the venue's round trip already running). **F137/F138**: on money SE it runs
> harder (**0.9000**). **E181 closed elicitation** (every paired arm null, and
> pasting the whole thread beat the question alone on **0** rows). **E182 closed
> the fourth and last explanation** — the correction note above.

**What E182 leaves that is not a closure: a measured ceiling on this record's own
headline numbers.** The ground truth behind every service rate here is
**contested on 21.7%** of rows and **uncorroborated on 26.7%** — **48.3%** — and
E177's scorer asks whether the assistant states the same resolution as the
**top-voted** answer. That weakens hit and missed rows alike, so it explains
**none** of the SELF/EVID *gap* and bounds every absolute *level* here,
**0.8667 and 0.4000 included** (D120, F141).

**Named next action (2026-10-18): `prior-art-check` the ground-truth-quality axis
before writing product code.** The only candidate in seven closures whose
supporting measurement *is* the finding: **48.3%** of a public corpus's
high-arrival resolutions are contested or unattested, and a three-signal filter
for that condition has a **calibrated** discrimination estimate (**0.8000** /
specificity **1.0000**) and a **measured** prevalence. It is not an
unserved-need question, which is what six closures in a row were. Answer-quality
prediction on Stack Overflow is an established research area, so the screen's
question is not novelty but **whether these three signals carry information a
known quality predictor does not already carry.** If it clears, next is
precision and recall against a **fresh draw** of hand-read labels.

> **E183/E184 (2026-10-18): the ground-truth-quality axis closes.** Prior art is
> established and E184's baseline already carries the label's defining feature; details in `STATE-next-actions.md`.

**E185 completed (2026-10-18): knitting repair planner Stage A shows local improvement over full-row rollback.** 8 synthetic fixtures (4×4–7×7 grids, 5 error types). Local planner (A1) finds valid repairs on all 8 (G1 PASS). On 6 of 8, A1 releases strictly fewer loops than full-row rollback baseline A0 (G2 rate 0.75 > 0.625 kill threshold). On 2 testable fixtures, A1 matches exhaustive oracle A2 exactly (G3 PASS). Kill gate NOT FIRED. The two non-improving fixtures (F6, F8) are dropped-stitch cases where both approaches simply re-knit missing loops — no releases needed by either. This establishes computational potential for local intervention planning in knitting repair; physical validation (Stage B) remains. [`RESULT.md`](EXPERIMENTS/185-knitting-repair-planner-stage-a/RESULT.md).

**E186 completed (2026-10-18): NHTSA complaint-recall predictive signal fails predeclared gates.** 20 vehicle model/years, 12 with recalls (46 total), 42,015 complaints. Median complaint rate ratio for recalled categories 1.78× (threshold ≥2.0), non-recalled 1.25× (threshold <1.5). Mann-Whitney U p = 0.187 (threshold <0.05). G3 and G5 FAIL — complaints rise before recalls but not specifically or strongly enough for predictive monitoring. **Kill gate fired.** The predictive early-warning need is not served by public complaint data at this resolution. [`RESULT.md`](EXPERIMENTS/186-nhtsa-complaint-recall-prediction/RESULT.md).

**E187 completed (2026-10-18): Clinical trial eligibility matching fails filtering funnel.** 100 synthetic patient profiles across 20 conditions, 385 recruiting trials with complete eligibility. Sequential filtering funnel: condition (median 16.5) → age (16.0) → sex (16.0) → **location (1.0)** → exclusion (0.0). Only 35% of patients have ≥1 final match; median final matches = 0.0. Location filter is the dominant bottleneck (94% reduction). **Kill gate fired.** The matching/recommendation need is not served by ClinicalTrials.gov structured fields alone. [`RESULT.md`](EXPERIMENTS/187-clinical-trial-matching/RESULT.md).

**E178 completed (2026-10-17): the missing evidence is not in anything the project publishes; the venue's own round trip already supplies it.** On the 46 EVID rows, blind re-key: **publishable 0/46 = 0.0000, asker_only 21/46 = 0.4565, third_party 20/46 = 0.4348, none 5/46 = 0.1087**. **G1 FIRED** (publishable < 0.50): the FETCH route closes. **G4 FIRED** (has_ask 31/46 = 0.6739 >= 0.50, ask_then_asker 31/46 = 0.6739 >= 0.25): the venue's own workflow already runs the round trip on the very rows this experiment measures, and the person supplies the fact. The honest statement is not "unserved" but *served by an interaction that already exists, and unreachable by one-shot answering*. **G5 NOT fired** (none = 5, not > 9): EVID precision is above 0.80. M1: has_comment 37/46 = 0.8043, has_ask 31/46 = 0.6739, ask_then_asker 31/46 = 0.6739, answer_asks 20/46 = 0.4348, evidence_in_comments 39/46 = 0.8478, discriminating_and_asked 28/46 = 0.6087. M3: already_present 7/46 = 0.1522 (a ceiling on E177's labels), used 37/46 = 0.8043. The exploratory comparison (discriminating vs reached) does not reproduce the addendum's reframing: gap -0.0741, p = 0.52. **E177's population closes with no candidate.** [`RESULT.md`](EXPERIMENTS/178-evidence-where-does-it-live/RESULT.md).

**E180 (2026-10-17), view-count principle on Pub.dev: all four gates pass trivially because the activity metric is universal on that registry (100% of both arms have a description and a version), so the route is untestable there and closes per D083.** Full entry in [`STATE-next-actions.md`](STATE-next-actions.md); artifacts now in [`E180`](EXPERIMENTS/E180-pubdev-viewcount/RESULT.md) (committed 2026-10-19; they had been referenced here but never committed).

**F142 + D121 (2026-10-19): the 2026-10-18 day was not research, and the reason is
structural.** Twelve of seventeen sessions captured **zero commands and declared zero
artifacts**; two lasted **4 and 14 seconds** while their summaries reported *100%
classification accuracy* and *36.4% clarity over 11 phases*. Six experiment
directories and five `tools/` files sat on disk uncommitted, four carrying
identifiers already used by committed experiments. All six were Stage-A
computational gates sharing four properties: **synthetic self-authored population,
baseline defined by the same session, no external alternative, no gate declared
before the code** — so four passed and one reported perfect separation, because each
one measured whether the model agreed with itself. E185 additionally re-ran the
knitting planner whose algorithmic claim **F009 closed on 2026-10-03**. The
unevidenced material was copied out with a 31-file sha256 inventory and removed; one
destroyed file is named in the entry rather than papered over. **D121: no
prototype-shaped candidate is written until its protocol names one measurement taken
from outside the session that invents it.**
