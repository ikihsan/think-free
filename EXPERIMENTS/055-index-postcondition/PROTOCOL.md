<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# E055 — can a caller verify that a stager staged what it was asked to stage?

Task T-0087. Declared **before any arm was run**, on the byte sources of the
arms and before any row was scored.

## The question, and why this one

The line-staging application is closed as an *application*: F081 read all 189
rows of the demand corpus and found 0 for the population item 0a measured, F043
ran six real agents and found the tool unnecessary, and F082 found two shipped
incumbents. **This protocol does not reopen that.** It tests a different claim.

F082 closed it on the two incumbents' **README prose**, never having measured
either. Reading both sources instead produced three facts that no run in the
record has:

1. **Neither incumbent ever reads `.git/index` back.** `git-hunk` re-prints its
   own in-memory request (`_ui.py:199-209`); `gah` prints `selected.len()`
   (`main.rs:431-438`). The only success predicate either has is
   `git apply`'s exit status.
2. **Their coordinate spaces are unlabelled and different.** `git-hunk -l 3` is
   the 3rd line *of the hunk body, context included* (`_lines.py:26-31`); `gah
   --lines 3` is *absolute file line 3*. Same number, different thing, both
   in range, neither says which in its output.
3. **So a caller cannot tell, after exit 0, which line was staged.** This is a
   *postcondition* gap, not a staging gap. F063 already measured the shape — 78
   wrong-but-exit-0 rows across three alternatives — and had no reusable
   artefact for it; F079 records that writing the referee correctly took three
   attempts even inside this repository.

**Question.** Given a repository, a declared intent, and any stager at all, can
the resulting `.git/index` be *proved* equal to the intent — with a checker that
reads the index and never reads the stager's own output?

## The instrument: `indexcheck.py`

One job, tool-neutral by construction:

> "Does the index entry for PATH hold exactly these bytes?"

Input is an **outcome**, not a coordinate: a path and the exact expected content.
No arm-specific vocabulary, no arm's exit code, no arm's stdout. It reads
`git show :PATH` and compares byte for byte, and reports the first differing
line and both lengths on a mismatch. It cannot be right about an arm by
construction, because it has never heard of an arm.

Its wrapper form, `--intent FILE -- CMD …`, runs `CMD` and then checks, so a
caller can wrap any stager — `stg`, `git-hunk`, `gah`, `git add -p`, a human's
keystrokes — and get a non-zero exit when the post-state is not the one asked
for.

## Arms

Declared before the fetch. An arm that cannot run is recorded `not_evaluated`
and **counts neither for nor against** — F010's shape, and F084's: an arm that
never started reads as a clean result.

| Arm | What it is | Runnable here |
|---|---|---|
| `stg` | this repository's `stage-lines/stg` | yes |
| `git-hunk` | `git-hunk` 0.4.2, PyPI, MIT | yes, under a fetched CPython 3.12.15 |
| `filterdiff` | patchutils 0.3.4 `--lines=RANGE` | yes |
| `pty_driver` | E037's `git add -p` driver | yes |
| `naive` | `printf 'y\n' \| git add -p` — the route F083 observed every agent converging on | yes |
| `gah` | `gah` 0.3.0, crates.io, MIT | **no** — no release binary on any channel, no Rust toolchain |

`git-hunk` gets two selector arms, because the unlabelled coordinate space is
the claim under test:

- `git-hunk-native` — the caller converts the working-tree line to a hunk-body
  line using `git-hunk list --json`, i.e. the tool's own best case.
- `git-hunk-naive` — the caller passes the same number it would pass to `stg`,
  which is what porting a script between the two actually does.

## Oracle, and the three controls that keep it honest

The oracle is **E038's own hand-written `want_content`** in
`EXPERIMENTS/038-staging-prior-art/compare.py`: for each of 10 cases, the exact
bytes the index must hold if exactly the change at the named working-tree line is
staged, written by hand from the case's own two texts. It does not depend on any
route's idea of which lines changed — which is how E037's oracle scored a
two-line over-stage as a pass (F063).

- **C1, recovery.** The checker must agree with `want_content` on every row where
  the arm is known correct. Disagreement on a row `want_content` and the bytes
  agree is a checker defect, and the run is void.
- **C2, sensitivity.** The checker must reject **every** wrong index state
  injected by `git apply` directly — E046's four shapes: `nothing_staged`,
  `all_changes`, `invented_line`, `doubled_run`. A checker that accepts any of
  these makes every downstream number meaningless, because a checker that
  accepts a wrong state cannot be trusted to reject one.
- **C3, falsifiability.** C1 bounds the checker from above and C2 from below;
  a run in which both hold has a checker that both accepts correct states and
  rejects wrong ones, and the run exits non-zero if either fails. **Both
  controls are run before any arm is scored**, and an arm is not run at all if
  they have not fired.

## Gates

**KILL-C — the build decision.** The checker earns a tool only if all three hold:

- K1. C1 and C2 both fired as declared.
- K2. It rejects at least one index that a **shipped** arm left behind while
  exiting 0.
- K3. That arm's own output gives the caller no way to derive the same verdict —
  so the checker is not merely re-reporting something the tool already said.

If K2 or K3 fails, **no tool is built.** The measurement stands and the artifact
stays an experiment. This is declared now so that it cannot be argued later.

**KILL-D — the demand reading.** F081, F043 and F083 already measured that the
staging *application* is not wanted. Nothing here can revive it, and a checker
that separates arms does not become a product by being correct. Any adoption
claim from this experiment is `untested` and will be recorded as such.

## Ceiling, stated before the run

- One fixture family: E038's 10 cases × 3 `diff.context` values, all
  single-file, all small, all LF. E046's real-commit replay is **not** rerun
  here, so CRLF, new files, deletions and mode changes are outside what this
  measures — E046 covered those for `stg` only, and nothing here extends that to
  any other arm.
- One host: git 2.56.0 built from source on a 2-CPU VM, `filterdiff` from Ubuntu
  focal, CPython 3.12.15 fetched as a static build.
- `gah` is not measured. Its absence is declared, not inferred from silence.
- The checker's soundness is established on injected wrong states of four named
  shapes, not on all possible wrong states.
- Every arm is asked for **one** change per file. Multi-change requests, mixed
  file types and cross-file interactions are not exercised.
- Nothing here measures whether anybody wants a checker. KILL-D says so.

## Amendments

Three amendments were declared after results and before the next run. Each is in
its own file, and each states the failure it prevents and the direction the change
runs in — every one of them adverse or neutral to building.

1. [`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md) — **after run 1.**
   Premise 2 above is falsified: neither incumbent's coordinate space is
   unlabelled, and `man filterdiff` plus `git-hunk show`'s own left column both
   say which line is meant. What is left is narrower: `--lines` selects whole
   **hunks**. The amendment also replaces K3's operationalisation, adds the
   probe's controls C5 and C6, and states `SHIPPED` in `run.py`.
2. [`PROTOCOL-AMENDMENT-2.md`](PROTOCOL-AMENDMENT-2.md) — **after run 2**, whose
   K3 answer is void: `--as-numbered-lines=after` printed exactly the wanted line
   on a fixture whose index had *also* lost a line, because a deleted line has no
   number in the new file. Both halves are read, C7 gets its own fixture, and a
   probe that saw nothing now yields `undecided` rather than `do_not_build`.
3. [`PROTOCOL-AMENDMENT-3.md`](PROTOCOL-AMENDMENT-3.md) — **after run 3**, whose
   verdict was `partial` because `K3_away_from_U0` was `not_evaluated`. That probe
   read the tool's *optional* report, which spans context lines; `patchwalk.py`
   reads the **primary** unified diff instead, where a carried line is exactly a
   `+`/`-` body line. C11 holds it to `git diff --cached -U0` and C12 holds it to
   an exact selection read exactly.

Runs 1-3 and the first ceiling probe are preserved unedited at
`raw/results-run1.json` through `raw/ceiling-run1.json`. The verdict is reported
in [`README.md`](README.md): `do_not_build`, with `KILL-C` never `not_evaluated`
once the reader was replaced.
