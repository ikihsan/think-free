<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E055 — protocol amendment 1

Written 2026-10-08 after reading `raw/results-run1.json` and before run 2.
Base protocol: [`PROTOCOL.md`](PROTOCOL.md). Run 1 is preserved unedited at
`raw/results-run1.json`.

Two changes were made after reading that run, so both are declared here rather
than left implicit in the diff.

## Premise 2 of the base protocol is falsified, and it was the premise the
## instrument rests on

The base protocol says both incumbents' coordinate spaces are "unlabelled".
Measured on bytes and on each tool's own documentation, neither is unlabelled:

- `filterdiff --lines=RANGE`, `man filterdiff` on this host: "Only include hunks
  that contain lines **from the original file** that lie within the specified
  RANGE." The coordinate is the working-tree line, and the measured arm agrees:
  `--lines=2` on a hunk beginning at line 1 selects that hunk, and
  `--lines=4` on `modify-one-of-three` selects only line 4.
- `git-hunk show <hunk>` prints its `-l` positions as its left column
  (`  3 +A`, `  4 +B` on the fixture used here), so the body position a caller
  must pass is printed by the tool. Its `stage --help` says "Select specific
  lines **within a hunk**".

So the gap is not a mislabelled coordinate. What is left is narrower, and is
stated in run 2's result: `filterdiff` selects whole **hunks**, so a wanted line
whose hunk also carries another change is staged together with that other
change, at exit 0 and with no output.

## K3's operationalisation is replaced

Run 1's version grouped wrong rows by the arm's output text and asked for two
*different* wrong index states inside one group. That is not what K3 in the base
protocol says, and the reason recorded in that file's docstring for introducing
it was itself wrong: `adjacent-edits` and `adjacent-pair-plus-far` have
*different* edited text; what they share is the base and the intent. The
two-states rule was a strengthening added after seeing that only one wrong state
exists, which is the shape F010 records.

K3 is now a measurement of the arm's own output: for each silent-wrong row of a
shipped arm, `k3probe.py` runs the **same selector** through the tool's own
`--as-numbered-lines=after` and reads back the absolute new-file lines the tool
says it carries. K3 holds when that set is **exactly** the line the caller named
— the tool then claims a request it did not honour. K3 fails when the set is a
strict superset, because the caller can derive the post-state from the tool's own
output. Both controls for the probe were added with it:

- **C5** on a fixture that does over-stage, the probe must report more than the
  wanted line. A blind probe would make a negative K3 meaningless.
- **C6** on a fixture that stages exactly the wanted line, the probe must report
  exactly it, so C5 cannot be satisfied by a probe that reports too much.

## Direction of the change, stated because it was made after a result

It is adverse to building: a probe that can see the tool's own derivation makes
K3 fail and so forces `do_not_build`, and C5/C6 can only remove confidence.
`KILL-C` also counts index states by digest and never by case name, which is a
correction in the same direction — a count keyed on a name reads one state as
several.

## `SHIPPED` is now stated in `run.py` rather than left to a reader

K2 counts only arms that take a line coordinate in their own best case and are
shipped: `filterdiff` and `git-hunk-native`. `git-hunk-naive` passes a file line
where the tool wants a body position on purpose, `naive` never addresses a line,
`stg` is unreleased and `pty_driver` is this repository's own harness. All five
stay in the tally and are reported; none may carry a gate about an incumbent.
