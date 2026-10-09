<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, kept so that history does not push the reload point past
the line cap. Identifiers here are the same ones `STATE.md` uses. Older history
is in [`STATE-history-2.md`](STATE-history-2.md).


- **Session 2026-10-07-003, VM 0947 (T-0084, E047, F084, D079): the last
  observation derived from a candidate is closed, and it closed by being run.**
  E045 left one thing unpromoted and `STATE.md` named it the single most useful
  next action: establish whether a formatter hook that re-stages a whole file
  sweeps a partially-staged file's unstaged hunks into the commit. Reading both
  corpus rows verbatim first — which D077 requires, and which inverted half the
  record — showed **one row exonerates lefthook** (`nextjs-app-template#95` is a
  report that 2.x *hides* the unstaged half; the stale thing is that repository's
  own warning) **and one row's own review record names the hazard and records
  `GH-1 … Defense sustained`**, the author ruling the index-patch fix out of
  scope. So the claim to test was *about the shipped tools*, and the shipped tools
  were the thing that had to be measured. E047 ran all of them on bytes — git
  2.56.0 built from source (this VM's 2.25.1 is below lefthook's 2.31 and
  lint-staged's 2.32 minimums, and both refusing to start would have read as "no
  sweep" for arms that never ran), lefthook 2.1.17, pre-commit 4.6.2,
  lint-staged 17.6.0, husky 9.1.7, prettier 3.9.9:
  **the hazard is real and byte-exact — the naive hook's commit contains a line
  that was never staged, and the file reads as modified while its content is
  already committed — and no shipped runner produces it.** lefthook hides
  unstaged changes *with and without* `stage_fixed`; lint-staged hides them *with
  defaults and with* `--no-stash`; pre-commit hides them around the hook by
  default; `git stash push --keep-index` prevents it with no framework at all.
  **Two arms run the same hook body one layer apart** and differ only in whether
  the framework manages unstaged changes: husky sweeps, pre-commit does not. Both
  controls behaved as required, including the positive control that must sweep or
  the run is void (F010). **Three defects in the instrument itself** are recorded
  because each would have produced a wrong answer rather than an error — a hunk
  count that read `@@` occurrences where git writes two per header, hook bodies
  that called `node` from a `PATH` git replaces inside a hook, and
  `formatter_ran` read from the worktree alone. **A declared prediction also
  failed**: pre-commit was expected to sweep and did not. **D079** makes a
  candidate's stated pain be measured on bytes against the incumbents that would
  also have to fix it, before it is ranked. Evidence in
  [`EXPERIMENTS/047-hook-partial-stage/README.md`](EXPERIMENTS/047-hook-partial-stage/README.md).

Older detail continues in [`STATE-history-2.md`](STATE-history-2.md).

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

## Honest limitations of this state (moved from STATE.md 2026-10-06)

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
- **The backlog is no longer a candidate at all, and the reason is not F057's.** Its per-tag
  spread is real and reproducible and its premise as a *rescue* is **falsified** (F058: the
  duplicate rows are viewed more than their neighbours, 251 against 193, at a median age of
  8.49 yr). Then **F059 killed the mechanism**: one `/search/advanced?tagged=…&sort=votes&
  order=asc` request returns the population ascending — 81 of E034's 100 sampled `git` tail
  ids, first at rank 1 — **with `closed_reason` in the payload**, unauthenticated. So F058's
  *"no ordering Stack Overflow offers can return it"* was true of the rendered tag pages and
  false of the platform, which also corrected E035's claim that the label needs an API key.
  **The measurement stands and nothing is built.** What is left unmeasured is the only
  question that mattered: **whether anyone wants this surfaced**, and nobody has tried. Two
  gates are `not_evaluated` and should not be read as negative — R1 returned 200 with 0
  items on `travel/customs` and its cause is untested, and KILL-Q was undecidable at n=4
  against n=2 with the negative control refused by the quota window.
- The screen's own weakness: decidable from prose, so cheap and also vulnerable to
  a persuasive report. It guarantees the *next* experiment is worth running.
- **The turn outward happened, and it is uneven.** Five consecutive experiments
  audited this repository's own instruments before E020 asked about the world; since
  then E022–E029 have asked about people, and **three of E029's own findings were
  defects in its instrument**. A run can be about the world and still mostly measure
  the measurer, so the two have to be counted separately (F048, F049, D061). **E036's
  finding is the sharpest case yet and it is not about the measurer at all:** the
  population was real, the instrument worked, the positive control fired, and the run
  still produced no candidate — because the thing being looked for was already public.
- **Two items left the ranked next-action list on 2026-10-06 for a reason that is not the
  line count.** Items 0b, 1 and 2 are this repository's own gates and CI; F031's complaint
  was that maintenance was reading as research, and that was still true of a file headed
  *Ordered by information gained per unit of effort*. **The live items are now 0 and 0d,
  and only 0d is research.**
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen.
  The session-by-session account lives in the two history files named above.

## How `STATE-next-actions.md` reached its present shape

Moved here from `STATE-next-actions.md` on 2026-10-08, when that file passed the
300-line cap and this one owned the record's own structure history.

Split out of [`STATE.md`](STATE.md) on 2026-10-04, which was at 299 of the 300
permitted lines and had to grow. The reload point keeps a pointer and the top
item; the reasoning behind each item lives in
[`STATE-next-actions.md`](STATE-next-actions.md) so that a rewrite of one does
not force a rewrite of the other.
**Two siblings, by invariant rather than by size.** The standing constraints —
rules true whichever item is next — moved to
[`STATE-constraints.md`](STATE-constraints.md) on 2026-10-04. **Item 0, the owner
decision on what the mission selects candidates on, moved to
[`STATE-selection.md`](STATE-selection.md) on 2026-10-06** when it reached 168
lines: it is not work, no experiment here can settle it, and its presence in a
ranked work list invited it to be worked on.
Read the ceiling on an item before spending effort on it: a pass still leaves
prior art, usefulness and adoption untouched, and every item says which.
On 2026-10-08 the same repair ran again in the other direction: `STATE.md`
passed the cap at 307 lines because session 2026-10-08-005 recorded E057 there,
and its *Next actions* body — 99 lines that restated reasoning this file
already held — moved here. A short-form duplicate of item 0 was removed at the
same time, and the paragraphs that were not already here moved with it.


## What changed recently — body moved out of STATE.md on 2026-10-09

`STATE.md` passed the 300-line cap when E072 was recorded there. The
entries below are unchanged; only their location moved. This is the
sixteenth time this file's invariant has owned material from `STATE.md`,
and the second time the repair was to move a whole section rather than
shorten prose.

  repositories by mechanical selection (>=180d span, >=250 rows, raw
  descriptors, sha256 + Jaccard dedup, 7 exclusions recorded with reasons),
  read a hand-verified watchlist of 33 recurring-payment families covering 18
  distinct merchants, and froze it before any arm ran. It then ran E065
  unmodified against **Actual Budget's shipping `findSchedules()`, ported
  line-by-line to Python**, on the same rows. Result: **recall 0.394, F1 0.160,
  G1 and G2 did not fire, margin over the incumbent +0.0098 against a +0.05
  gate.** The instrument is non-vacuous (permutation control 0.0000) and no
  single account decides it (G5). The cause decomposition is the result:
  **6 misses from the merchant axis the action went in to measure, 14 from an
  amount-CV gate that treats a price change as non-recurrence.** E066 could not
  see the second because its own README reports CV ≈ 0.000 for standing orders.
  Nine selection and labelling defects were found and repaired on the way, all
  recorded in the experiment's code, including two privacy screens that were
  **withdrawn** for failing on ordinary merchant names and then on city names,
  and a loader that had silently read a budget app's already-cleaned `Payee`
  column instead of the raw bank `Description` beside it — the same file also
  produced the best-looking under-grouping numbers before the fix, so the defect
  inflated the finding it invalidated.
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

Older per-session highlights are in [`STATE-history.md`](STATE-history.md); the readings that
bear on open items are in [`STATE-in-flight.md`](STATE-in-flight.md),
[`STATE-in-flight-2.md`](STATE-in-flight-2.md), [`STATE-in-flight-3.md`](STATE-in-flight-3.md),
[`STATE-in-flight-8.md`](STATE-in-flight-8.md) and
[`STATE-in-flight-9.md`](STATE-in-flight-9.md). The 300-line cap has been hit fifteen
times; each repair moved material to the file whose invariant owns it.

**E046 changed what "done" means for a candidate's artifact, and D075 carries it.**
Six experiments on `stg` closed with a sentence listing the shapes they had not
tested; read as a work list, that sentence was worth four real defects. D075 makes
a candidate's limitations section a measurement plan to be executed before
release-readiness is claimed. **D077 is the same rule for populations**: a
candidate's own declared population is to be read out of the evidence before
anything is built to measure it. Both are in
[`STATE-in-flight-6.md`](STATE-in-flight-6.md) and
[`STATE-in-flight-7.md`](STATE-in-flight-7.md).
