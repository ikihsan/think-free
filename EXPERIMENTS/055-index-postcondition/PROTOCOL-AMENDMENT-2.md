<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E055 — protocol amendment 2: the probe could not see a carried deletion

Written 2026-10-08 **after** run 2 was executed and **before** any re-run. Base
protocol: [`PROTOCOL.md`](PROTOCOL.md); first amendment:
[`PROTOCOL-AMENDMENT-1.md`](PROTOCOL-AMENDMENT-1.md). Run 2 is preserved
unedited at `raw/results-run2.json`.

Run 2 was executed with the amendment 1 probe and **its K3 answer is void**.
The instrument defect, measured on bytes before any re-run:

```console
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
```

The caller named line 1. `git show :f.txt` has also lost line 2.
`--as-numbered-lines=after` printed `1 :A` — **exactly the line the caller
named** — because a deleted line has no number in the new file. The tool's own
output therefore did *not* reveal the extra change on this row, which is the
case K3 exists to find, and amendment 1's probe reported it as a clean superset
because it read `after` alone.

## Three changes, each with the failure it prevents

1. **Both halves are read.** `--as-numbered-lines=after` numbers the new file
   and `=before` numbers the old one, so **neither alone is the selection**:
   `after` cannot see a carried deletion and `before` cannot see a carried
   addition. Both are read and the union is what K3 is asked about.
2. **C7, a carried-deletion control, with its own fixture.** No E038 case has a
   deletion adjacent to the wanted change, which is why the fixture family did
   not already contain this shape and why nothing else caught it. C7 needs
   `a,b,c,d,e → A,c,d,e` naming line 1, and a test asserts that fixture really
   does drop line 2 into the index, so C7 cannot be satisfied by a probe that is
   merely wrong.
3. **A blind probe now yields `undecided`, not a verdict.** Run 2's K3 was false
   because every probe came back empty: `run_arms` probed *after* the arm had
   staged, so `git diff` no longer showed the selected lines. `kill_c` returned
   `do_not_build` from an instrument that had seen nothing — the same failure as
   a parser that quietly stops matching. An empty probe is now recorded as
   undecided and the verdict is `undecided`; a test asserts it cannot read as a
   clean negative. The probe runs before the arm, and a test asserts the
   ordering.

## Direction of the change, stated again because it was made after a result

All three are adverse to closing the gate. A probe that can see a carried
deletion makes K3 *more* likely to fire, and an undecided verdict is not a pass.
Amendment 1's corrections are kept; nothing here relaxes a threshold.
