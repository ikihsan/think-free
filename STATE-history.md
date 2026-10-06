<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, kept so that history does not push the reload point past
the line cap. Identifiers here are the same ones `STATE.md` uses. Older history
is in [`STATE-history-2.md`](STATE-history-2.md).

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