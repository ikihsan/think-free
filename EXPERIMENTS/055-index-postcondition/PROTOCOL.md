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

## Amendment 1 — after run 1, before run 2

Run 1 exists and is preserved unedited at `raw/results-run1.json`. Two changes
were made after reading it, so both are declared here rather than in the diff.

**Premise 2 above is falsified, and it was the premise the instrument rests on.**
It says both incumbents' coordinate spaces are "unlabelled". Measured on bytes
and on each tool's own documentation, neither is unlabelled:

- `filterdiff --lines=RANGE`, `man filterdiff` on this host: "Only include hunks
  that contain lines **from the original file** that lie within the specified
  RANGE." The coordinate is the working-tree line, and the measured arm agrees:
  `--lines=2` on a hunk beginning at line 1 selects that hunk, and
  `--lines=4` on `modify-one-of-three` selects only line 4.
- `git-hunk show <hunk>` prints its `-l` positions as its left column
  (`  3 +A`, `  4 +B` on the fixture used here), so the body position a caller
  must pass is printed by the tool. Its `stage --help` says "Select specific
  lines **within a hunk**".

So the gap is not a mislabelled coordinate. What is left is narrower and is
stated in run 2's result: `filterdiff` selects whole **hunks**, so a wanted line
whose hunk also carries another change is staged with that other change, at exit
0 and with no output.

**K3's operationalisation was replaced.** Run 1's version grouped wrong rows by
the arm's output text and asked for two *different* wrong index states inside one
group. That is not what K3 above says, and the reason recorded in that file's
docstring for introducing it was itself wrong: `adjacent-edits` and
`adjacent-pair-plus-far` have *different* edited text; what they share is the base
and the intent. The two-states rule was a strengthening added after seeing that
only one wrong state exists, which is the shape F010 records.

K3 is now a measurement of the arm's own output: for each silent-wrong row of a
shipped arm, `k3probe.py` runs the **same selector** through the tool's own
`--as-numbered-lines=after` and reads back the absolute new-file lines the tool
says it carries. K3 holds when that set is **exactly** the line the caller named —
the tool then claims a request it did not honour. K3 fails when the set is a
strict superset, because the caller can derive the post-state from the tool's own
output. Both controls for the probe were added with it:

- **C5** on a fixture that does over-stage, the probe must report more than the
  wanted line. A blind probe would make a negative K3 meaningless.
- **C6** on a fixture that stages exactly the wanted line, the probe must report
  exactly it, so C5 cannot be satisfied by a probe that reports too much.

**Direction of the change, stated because it was made after a result.** It is
adverse to building: a probe that can see the tool's own derivation makes K3 fail
and so forces `do_not_build`, and C5/C6 can only remove confidence. `KILL-C` also
counts index states by digest and never by case name, which is a correction in
the same direction — a count keyed on a name reads one state as several.

**`SHIPPED` is now stated in `run.py` rather than left to a reader.** K2 counts
only arms that take a line coordinate in their own best case and are shipped:
`filterdiff` and `git-hunk-native`. `git-hunk-naive` passes a file line where the
tool wants a body position on purpose, `naive` never addresses a line, `stg` is
unreleased and `pty_driver` is this repository's own harness. All five stay in the
tally and are reported; none may carry a gate about an incumbent.

## Amendment 2 — the probe could not see a carried deletion, so it read K3 as failed

Run 2 was executed with the Amendment 1 probe and **its K3 answer is void**. It is
preserved unedited at `raw/results-run2.json`. The instrument defect, measured on
bytes before any re-run:

    $ printf 'a\nb\nc\nd\ne\n'  > f.txt && git add f.txt && git commit -qm i
    $ printf 'A\nc\nd\ne\n'     > f.txt        # line 1 replaced, line 2 deleted
    $ git diff -U0 | filterdiff --lines=1 | filterdiff --as-numbered-lines=after
    1	:A
    $ git diff -U0 | filterdiff --lines=1 | git apply --cached --unidiff-zero; echo $?
    0
    $ git show :f.txt
    A
    c
    d
    e

The caller named line 1. `git show :f.txt` has also lost line 2. `--as-numbered-lines
=after` printed `1 :A` — **exactly the line the caller named** — because a deleted
line has no number in the new file. The tool's own output therefore did *not* reveal
the extra change on this row, which is the case K3 exists to find, and Amendment 1's
probe reported it as a clean superset because it read `after` alone.

Three changes, each with the failure it prevents:

1. **Both halves are read.** `--as-numbered-lines=after` numbers the new file and
   `=before` numbers the old one, so **neither alone is the selection**: `after`
   cannot see a carried deletion and `before` cannot see a carried addition. Both are
   read and the union is what K3 is asked about.
2. **C7, a carried-deletion control, with its own fixture.** No E038 case has a
   deletion adjacent to the wanted change, which is why the fixture family did not
   already contain this shape and why nothing else caught it. C7 needs
   `a,b,c,d,e → A,c,d,e` naming line 1, and a test asserts that fixture really does
   drop line 2 into the index, so C7 cannot be satisfied by a probe that is merely
   wrong.
3. **A blind probe now yields `undecided`, not a verdict.** Run 2's K3 was false
   because every probe came back empty: `run_arms` probed *after* the arm had staged,
   so `git diff` no longer showed the selected lines. `kill_c` returned `do_not_build`
   from an instrument that had seen nothing — the same failure as a parser that
   quietly stops matching. An empty probe is now recorded as undecided and the
   verdict is `undecided`; a test asserts it cannot read as a clean negative. The
   probe runs before the arm, and a test asserts the ordering.

Direction of the change, stated again because it was made after a result: all three
are adverse to closing the gate. A probe that can see a carried deletion makes K3
*more* likely to fire, and an undecided verdict is not a pass. Amendment 1's
corrections are kept; nothing here relaxes a threshold.

## Amendment 3 — the `not_evaluated` was the probe's blind spot, not the tool's

Runs 1–3 and the ceiling probe are preserved unedited at `raw/results-run1.json`
through `raw/ceiling-run1.json`. The verdict they produced is
`do_not_build` with `verdict_state: partial`, because `ceiling.py` recorded
**`K3_away_from_U0: not_evaluated`**.

**The partial came from an instrument, and the instrument is replaceable.** Both
probes so far read the tool's *optional* `--as-numbered-lines` report. That
report prints every line the selection **spans**, so away from `-U0` its line
list contains context lines as well as carried ones and cannot tell the two
apart — which is why `ceiling.py`'s C10 is falsified away from `-U0` and the
boolean was recorded as undecidable there.

The tool's **primary** output has no such ambiguity. `filterdiff --lines=N`
emits a unified diff, and in a unified diff a carried line is exactly a `+` or
`-` body line while a context line begins with a space. Measured on bytes
before this amendment was written, on `a,b,c,d,e → a,B,c,D,e` naming line 2:

| context | selected patch carries | named beyond the want |
|---|---|---|
| `-U0` | old 2, new 2 | — |
| `-U1` | old 2 and 4, new 2 and 4 | **4** |
| `-U3` | old 2 and 4, new 2 and 4 | **4** |
| default | old 2 and 4, new 2 and 4 | **4** |

So the same number the `--as-numbered-lines` reader had to guess at is
**unambiguous in the patch's own markers at every context**, and the default
context a caller actually gets is one where the tool names the carried line.

**What this may change.** Only `K3_away_from_U0`. KILL-C is already
`do_not_build` on the `-U0` evidence, and this can only confirm or strengthen
that: if the patch markers name the carried line at every context, K3 fails
everywhere and the negative is no longer context-bound. Nothing here can turn
`do_not_build` into `build`, because K3's question — *does the arm's own output
give the caller no way to derive the same verdict* — is answered by the arm's
primary output whenever that output names the carried line, and the ceiling
rows already record that it does. **The direction of this change is adverse to
building**, and that is why it is recorded here rather than folded into the
code silently.

**Controls, both required, both about the new reader and neither about KILL-C:**

- **C11, agreement with git.** The lines the patch walk reports as carried must
  equal the lines `git diff --cached -U0` says the index actually touches, on
  every probed row. This is C8's comparison, run through a second reader: it
  holds the *walk* to git's own statement of the post-state rather than to the
  other probe, so the two readers cannot agree merely by sharing a bug.
- **C12, the walk is not trivially "everything".** On a fixture where the
  selection is exact, the walk must report the wanted line and **no** other
  line. Without this, a reader that reported the whole hunk would satisfy C11
  on the over-staging rows and make K3 unfalsifiable in the direction that
  matters.

C11 and C12 are the same pair `ceiling.py` used (C9, C10), pointed at the new
reader. C10's falsification stands and is not redefined away: `--lines` really
does select whole **hunks**, which is a property of the tool and the reason
away from `-U0` it over-stages every case probed.
