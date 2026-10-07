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


## What changed in the 2026-10-06 sessions (moved from STATE.md, cap)

- **Session 2026-10-06-015 (E041 reconcile/publish) finished: worked.** The 816-test
  suite is green (OK, 651s), doc lint exits 0, and the test-suite and release-check
  gates it had left "running in background" are captured in its command log.

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