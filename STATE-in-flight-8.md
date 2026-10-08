<!-- origin-meta
owner: STATE.md
status: active
last-verified: 2026-10-08
-->

# In flight 8 — E055: the postcondition checker that F082's prose implied, and the
# gate it failed

Session 2026-10-08-003, VM `instance-20260717-0947`, task T-0087. Split out of
[`STATE.md`](STATE.md) on 2026-10-08 at the 300-line cap. Evidence:
[`EXPERIMENTS/055-index-postcondition/`](EXPERIMENTS/055-index-postcondition/README.md).
Finding **F088**, decision **D081**.

## Why this was run

F082 closed the line-staging application on two shipped incumbents (`git-hunk`,
`gah`) that had been read from **README prose and never measured**. The prose
implied a second, narrower gap than the staging one: neither tool reads
`.git/index` back, so a caller scripting one gets exit 0 without learning what
landed. E055 tested exactly that claim rather than the application, which F081,
F043 and F083 had already closed.

## What was built

`indexcheck.py` — one question, *does the index entry for PATH hold exactly these
bytes?* — answered by `git show :PATH` compared byte for byte. Its input is an
**outcome**, not a coordinate; it reads no arm's exit code and no arm's stdout, so
it cannot be right about an arm by construction. In wrapper form
(`--intent FILE -- CMD …`) it wraps any stager, including a human's keystrokes.

The oracle is E038's own hand-written `want_content`: for each of 10 cases, the
exact bytes the index must hold if exactly the change at the named working-tree
line is staged, written by hand from the case's own two texts. E037's oracle had
scored a two-line over-stage as a pass because it depended on a route's idea of
which lines changed (F063); this one does not.

## The tally

| arm | counted | holds | refused (non-zero) | silent-wrong |
|---|---|---|---|---|
| `stg` (unreleased) | 30 | **30** | 0 | 0 |
| `filterdiff` (shipped) | 30 | 12 | 12 | **6** |
| `git-hunk-native` (shipped) | 27 | 9 | 18 | 0 |
| `git-hunk-naive` | 30 | 9 | 21 | 0 |
| `pty_driver` (`git add -p`) | 30 | 13 | 0 | 17 |
| `naive` (`printf 'y\n'`) | 30 | 6 | 0 | 24 |
| `gah` (shipped) | 0 | — | — | `not_evaluated` ×30 |

**The count that must not be overstated:** the 6 silent-wrong rows are **one**
distinct index state (`678239f1620d`), not six observations — `adjacent-edits` and
`adjacent-pair-plus-far` share a base and an intent. `kill_c()` therefore counts by
digest and never by case name (F052's shape).

`gah` is `not_evaluated` on all 30 rows and counts neither for nor against: all
five of its GitHub releases carry zero assets, there is no binstall entry or
container, and building it needs a Rust edition-2024 toolchain this host lacks.
Declared, not inferred from silence (F010, F084).

## The gate

**`KILL-C` = `do_not_build`.**

- **K1** — both grader controls fired: C1 10/10 recovery, C2 23/23 injected wrong
  states flagged with 0 missed. One of the 23 injections was not actually a wrong
  state, so the flag is conservative rather than a miss.
- **K2** — a shipped arm exited 0 on a wrong index: **true** (`filterdiff`).
- **K3** — that arm's own output gives the caller no way to derive the same
  verdict: **false**.

K3 fails because `filterdiff` is self-describing. In a unified diff a carried line
is exactly a `+`/`-` body line, so the patch the caller already piped through the
tool prints `1 :A` and `2 :B` when the caller named line 2. A checker that
re-derives what the tool already printed adds no fact.

F063 had already measured "wrong but exit 0" — 78 rows across three alternatives —
and had no reusable artefact for the shape. E055 supplied the artefact and the
criterion, and the criterion is what closed it: **D081** requires that a
verifier's verdict not be derivable from the incumbent's own *primary* output.

## The ceiling, and it does not rescue the negative

Both the arm and the K3 probe ran `git diff -U0`, so the negative could have been a
property of the pipeline. `ceiling.py` re-ran the question at `-U1`, `-U3` and the
default: **12 of 12** rows over-stage at exit 0 and the arm's primary output names
a line beyond the want in **12 of 12**. C11 holds the new reader to
`git diff --cached -U0` on all 16 staged rows; C12 holds it to an exact selection
read exactly. So the negative is a property of the tool's output, not of the
context — and `-U0` remains load-bearing for *correctness* (away from it
`filterdiff` over-stages every case probed) but not for *auditability*.

## F082's premise is falsified

The gap the instrument rested on was that the incumbents take *unlabelled,
incompatible* coordinate spaces. On bytes: `man filterdiff` on this host says
`--lines` selects "lines **from the original file**", and the measured arm agrees;
`git-hunk show` prints its `-l` positions as its left column. What survives is
narrower and is a **documented property of `filterdiff`** — `--lines` selects whole
**hunks** — so a wanted line whose hunk carries another change is staged with it,
at exit 0, with the carry visible in the patch the caller already sees.

## Three instruments corrected, each adverse to building

1. The premise above was false; the gap is narrower than declared.
2. Run 2's K3 is **void**: `--as-numbered-lines=after` printed exactly the wanted
   line on a fixture whose index had *also* lost a line, because a deleted line has
   no number in the new file. Both halves are read, and C7 has its own fixture.
3. Run 2's probe ran *after* the arm had staged, so `git diff` no longer showed
   the selection, every probe returned empty, and `do_not_build` came **from an
   instrument that had seen nothing** — F010's shape. An empty probe is now
   `undecided` and the verdict follows it.

Runs 1–3 and the first ceiling probe are preserved unedited under `raw/`. The test
files exist to falsify the gates: each asserts `kill_c()`, the probe and the
verdict readers *can* return the other answers, so a green suite is evidence the
instrument is falsifiable, not that the gate fired.

## What this leaves, and the next action

**An instrument, not a direction.** The oracle, its two bounds, and a
gate-falsification suite are reusable by any future work on line-addressed
staging. Reusing it is cheap; that is not a candidate.

**The honest frame for the whole table** is F081/F043/F083: the population that
would want a line stager was measured and does not, and agents route around the
failure by doing the discovery by hand. A table showing `git add -p` driven by an
agent is silently wrong on 17 of 30 rows describes a difficulty that population
already routes around — not a market. **The single most useful next action is
unchanged and is not a measurement of something already chosen:** observe
independently until a specific testable opportunity appears (D080), and hold any
candidate to D077, D079 and D081 before it is ranked.

**Ceilings of this reading:** `gah` never measured; 10 single-file LF cases × 3
contexts, so CRLF, new files, deletions and mode changes are outside it (E046
covered those for `stg` only); one change requested per file; one host.
