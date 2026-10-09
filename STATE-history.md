<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
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

## What changed in the 2026-10-07-001/002 sessions (moved from STATE.md, cap)

- **Session 2026-10-07-002, VM 0947 (E045, T-0083, F081, F082, D077): the candidate is
  withdrawn, and the kill was in the record's own corpus the whole time.** E045 read all 189
  unique issues in E038's cached demand corpus, one row each, asking the two questions the
  record never asked — who is making the request, and which interface do they lack.
  **29 of 189 are about choosing which lines reach the index; 28 of those carry explicit
  diff access and the 29th GUI-implied; 0 carry none.** All ten automated callers in the
  need rows name their diff access in their own text. **Three of the four issues F064 cites
  are not evidence of what they were cited for**: `sublime_merge#465` says the feature already
  exists and asks for discoverability, `sublime_merge#976` asks for staging *within* a modified
  line (sub-line, which `stg` does not provide), `vim-gitgutter#446` is a person in vim with a
  visual selection. The rule classifier was measured before use per D069: precision 0.372,
  recall 0.552, and its `line-coordinate` class matches `file:line` source citations inside CI
  transcripts — 14 of its 43 rows are unrelated issues. **The same reading killed the
  differentiator**: the 29 rows name **26 distinct repositories**, and two are command-line
  tools taking `stg`'s coordinate that shipped before E037. `gah` (Rust, crates.io) offers
  "line range" staging, documents `stg`'s exact hard case, targets AI coding agents by name and
  ships a Claude Code plugin; `git-hunk` (Python, PyPI) has line-level control and has already
  run the two-arm agent experiment item 0a was built around. Packaging goes with it: all three
  are installable, two ship agent distribution, and `gah` addresses by a content anchor that
  survives line shift — the mechanism E041 measured as absent, arriving from outside. E038's
  prior-art check reported 2 of the 26 because it searched the web and read the corpus's titles.
  **D077** makes the demand evidence of a named population be read row by row before anything is
  built to measure that population. Evidence in
  [`EXPERIMENTS/045-demand-evidence/README.md`](EXPERIMENTS/045-demand-evidence/README.md).
- **Session 2026-10-07-002, VM 0944 (E044, F083, D078): the discovery population
  doesn't need the tool either — the candidate closes.** E043's ceiling named the
  last open population: an agent that must *discover* which line changed, with no
  line number and no `git diff`. E044 reran the harness with exactly those two
  changes — semantic task descriptions, and a logging policy shim refusing
  `git diff` (passing `stg`'s own plumbing). Kill gate declared before the runs;
  oracle validated on four routes × three scenarios including a no-diff route.
  **6 of 6 exact, `nostg` 3 of 3** — every agent discovered by hand first
  (`git show HEAD:app.py` vs `cat -n app.py`, correct line on the first attempt);
  the three with `stg` describe `stg list` as *confirming* a line already
  identified. A second no-tool route appeared: `git hash-object -w` +
  `git update-index --cacheinfo`, no patch at all. **D078**: the one
  policy-relevant event — a refused agent-facing `git diff --cached --stat` —
  appears in no agent's self-report; compliance is logged at the enforcement
  point. Evidence in
  [`EXPERIMENTS/044-discover-staging/README.md`](EXPERIMENTS/044-discover-staging/README.md).
- **Session 2026-10-07-001, VM 0944 (E043, F075, D074): the candidate's last
  surviving claim was three experiments old, rested on a simulation, and did not
  survive a real caller.** Six real agents on six real repositories, scored against
  a hand-written oracle no agent could read: **6 of 6 exact, 3 of 3 with no tool at
  all, and 2 of the 3 that had `stg` on `PATH` declined to use it.** Every no-tool
  agent converged independently on `git diff` → hand-write a minimal patch →
  `git apply --cached`. `stg` is no longer a candidate for release on agent
  usability; it remains a correct tool and that is now the whole claim. **D074**
  requires a candidate whose surviving claim names a caller to run that caller as an
  arm before it is called validated, and requires the arm to be *checked to have
  exercised the tool* — because the `stg` arm shipped a binary that was not on
  `PATH`, three agents reported `command not found`, and **the run still scored 6 of
  6, which reads as confirmation.** Evidence in
  [`EXPERIMENTS/043-real-agent-staging/README.md`](EXPERIMENTS/043-real-agent-staging/README.md).

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

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, so history does not push the reload point past the line cap.
Identifiers here are the same ones `STATE.md` uses.

**This file split on 2026-10-09** when E069's record pushed it past 300 lines.
It is now a stub with the newest sessions; older and thematic sections moved to
siblings. Nothing was edited in the move.

| Sibling | Holds |
|---|---|
| [`STATE-history-2.md`](STATE-history-2.md) | the 2026-10-06 and 2026-10-07 moves out of `STATE.md`, and this file's older sections |

## The invariant behind the split

A reader asks this file one question — *what did the recent sessions actually
change?* — and the answer is a chronological list. Sections are therefore cut
between sessions, never inside one, so a session's entry and its identifiers
always travel together and a reader never has to open two files to follow one
session's finding from protocol to verdict. `STATE.md` holds the reload point,
this file holds the per-session detail behind it, and `STATE-next-actions.md`
holds the reasoning behind each open item; when one of them grows, material
moves to the file whose invariant owns it, never shortened to fit.

## Sessions in this file

## Honest limitations of this state (moved from STATE.md 2026-10-06)