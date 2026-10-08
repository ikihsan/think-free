<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

# E055 — can a caller verify that a stager staged what it was asked to stage?

Task T-0087. Protocol `PROTOCOL.md` and its three declared amendments; raw
results in `raw/`; verdict `do_not_build`, and the artifact stays an experiment.

## The question

F082 closed the line-staging application on two incumbents (`git-hunk`, `gah`)
read from **README prose, never measured**. E055 did not reopen the application —
F081, F043 and F083 had already measured that nobody in that population wants a
staging tool, and D080/KILL-D keeps any adoption claim from this experiment
`untested`. It tested a narrower claim: given a repository, a declared intent, and
*any* stager, can the resulting `.git/index` be **proved** equal to the intent by a
checker that reads the index and never reads the stager's output?

## The instrument, and why it is tool-neutral

`indexcheck.py` asks one question — *does the index entry for PATH hold exactly
these bytes?* — by running `git show :PATH` and comparing byte for byte. Its input
is an **outcome** (a path plus the exact expected content), not a coordinate. It
has never heard of an arm, reads no arm's exit code and no arm's stdout, and so
cannot be right about an arm by construction.

The **oracle** is E038's own hand-written `want_content`
(`EXPERIMENTS/038-staging-prior-art/compare.py`): for each of 10 cases, the exact
bytes the index must hold if exactly the change at the named working-tree line is
staged, written by hand from the case's own two texts. It does not depend on any
route's idea of which lines changed, which is how E037's oracle scored a two-line
over-stage as a pass (F063).

## Arms

An arm that cannot run is `not_evaluated` and counts neither for nor against — the
F010/F084 shape, where an arm that never started reads as a clean result.

| Arm | What it is | Counted | Holds | Refused (non-zero) | Silent-wrong |
|---|---|---|---|---|---|
| `stg` | this repository's `stage-lines/stg`, unreleased | 30 | **30** | 0 | 0 |
| `filterdiff` | patchutils 0.3.4 `--lines=RANGE`, shipped | 30 | 12 | 12 | **6** |
| `git-hunk-native` | `git-hunk` 0.4.2, PyPI, MIT, shipped | 27 | 9 | 18 | 0 |
| `git-hunk-naive` | the same tool, passed a *file* line | 30 | 9 | 21 | 0 |
| `pty_driver` | E037's `git add -p` driver | 30 | 13 | 0 | 17 |
| `naive` | `printf 'y\n' \| git add -p` | 30 | 6 | 0 | 24 |
| `gah` | `gah` 0.3.0, crates.io, MIT | 0 | — | — | `not_evaluated` ×30 |

`git-hunk-native`'s 3 unevaluated rows are the one case whose named line is pure
context (`deletion-among-edits`, line 3): nothing to select, and it is not scored.
`gah` has no release binary on any channel (all five GitHub releases carry zero
assets, no binstall entry, no container) and building it needs a Rust
edition-2024 toolchain this host lacks. Both absences are declared, not inferred.

## The three grader controls, and what the run measured

| Control | What it bounds | Result |
|---|---|---|
| **C1** recovery | the checker must agree with `want_content` wherever the index is known correct | fired, 10/10 |
| **C2** sensitivity | must reject **every** injected wrong state (E046's four shapes) | fired, 23 injected / 23 flagged / 0 missed |
| **C3** | C1 + C2 both fire, or no arm is run at all | held — the arms ran only after both |

Two further readings, C4 (the selector mapping agrees with the tool's own printed
positions, 9/9 decidable) and C8 (the probe describes the whole selection, 6/6),
are recorded in the artifact. One **instrument note**: C2's 23 injections include
one that was *not* a wrong state (`injection_was_not_wrong: 1`), so the 22 real
wrong states are all rejected and the twenty-third flag is the control being
conservative rather than a miss.

## KILL-C, the declared build decision

- **K1** — C1 and C2 both fired: **true**.
- **K2** — a *shipped* arm exited 0 on a wrong index: **true** (`filterdiff`, 6
  rows). K2 counts only `filterdiff` and `git-hunk-native`, the arms that take a
  line coordinate in their own best case and ship; `git-hunk-naive` misuses the
  coordinate on purpose, `naive` never addresses a line, `stg` is unreleased and
  `pty_driver` is this repository's own harness.
- **K3** — that arm's own output gives the caller no way to derive the same
  verdict: **false**.

**Verdict: `do_not_build`.** The checker earns no tool.

K3 fails because `filterdiff` *is* self-describing: in a unified diff a carried
line is exactly a `+`/`-` body line, so a caller reading the selected patch sees
`1 :A` and `2 :B` when it asked for line 2. On all 6 silent-wrong rows the arm's
own output named the carried line. A checker that only re-derives what the tool
already said adds nothing there.

**One count that must not be overstated:** the 6 silent-wrong rows are **1 distinct
index state**, not 6 observations — `silent_wrong_distinct_index_states: 1`, with
all six members listed in the artifact. That is F052's shape: cases with identical
base and identical intent (`adjacent-edits`, `adjacent-pair-plus-far`) count once.
So the "silent wrong" evidence for the shipped incumbent is **one** observation,
reproduced across three `diff.context` values.

## The ceiling: was the negative an artefact of `-U0`?

Both the arm and the K3 probe run `git diff -U0`, so a negative earned there could
have been a property of the pipeline rather than of the tool. `ceiling.py` re-ran
the question at four contexts (`-U0`, `-U1`, `-U3`, default):

- **C11** — the patch walk's footprint must equal what `git diff --cached -U0`
  says the index touches, on every probed row: **16/16 agree**.
- **C12** — on an exact selection the walk must report the wanted line and no
  other: **held**.
- **K3_away_from_U0: holds.** Away from `-U0`, 12 of 12 rows over-stage at exit 0
  and the arm's own primary output names a line beyond the want in 12 of 12.

So the negative is **not context-bound**: it is a property of the tool's output.
`-U0` remains load-bearing for *correctness* — away from it `filterdiff`
over-stages every case probed, which is a real property of `--lines` selecting
whole **hunks** — but not for *auditability*.

## What this closes, and what it does not

**Closed, and the transferable part is the falsification.** The gap F082 inferred
from README prose — that the incumbents take *unlabelled, incompatible*
coordinate spaces and print nothing about what they did — **is false on bytes**.
`man filterdiff` on this host says `--lines` selects "lines from the original
file"; the measured arm agrees. `git-hunk show` prints its `-l` positions as its
left column. The only gap left is much narrower and is a property of
`filterdiff`: it selects whole **hunks**, so a wanted line whose hunk carries
another change is staged with it — at exit 0 and with output the caller must
already be reading to notice. **No tool is built, and none should be**: the
caller's fix is `git diff | <stager>`, keeping the patch in view.

**Closed as a build decision.** KILL-C is `do_not_build` and KILL-D forbids
reaching for adoption. `indexcheck.py` stays inside this experiment. It remains a
legitimate *oracle* — and that is how it was used here: C1/C2 bound it, and it
scored 210 arm-rows without ever reading an arm's output.

**Not closed, and stated rather than buried.** `gah` was never measured. The
fixture family is 10 single-file LF cases × 3 contexts; CRLF, new files,
deletions and mode changes are outside it (E046 covered those for `stg` only, and
nothing here extends that to another arm). One change per file is asked of each
arm. And the honest frame for the whole table is F081/F043/F083: the population
that has to want a line stager was measured and **does not**. A table showing that
`git add -p` driven by an agent is silently wrong on 17 of 30 rows describes a
difficulty those agents route around by doing the discovery by hand, not a
market.

## Three instruments this experiment had to correct, and a falsified premise

All three are preserved rather than rewritten: runs 1–3 and the first ceiling probe
are at `raw/results-run1.json` … `raw/ceiling-run1.json`, unedited.

1. **The premise the instrument rested on was false.** PROTOCOL.md's premise 2 —
   that both incumbents' coordinate spaces are unlabelled — was falsified by
   reading each tool's own documentation and bytes (Amendment 1). What survived
   is narrower.
2. **A probe that could not see a carried deletion read K3 as failed.** Run 2's
   K3 is `void`: `--as-numbered-lines=after` printed exactly the line the caller
   named on a fixture where the index had *also* lost a line, because a deleted
   line has no number in the new file. Amendment 2 reads both halves and adds C7,
   a fixture whose own test asserts the deletion really reaches the index.
3. **A blind probe returned `do_not_build` from having seen nothing.** Run 2's
   probe ran *after* the arm had staged, so `git diff` no longer showed the
   selection and every probe came back empty. An empty probe is now `undecided`,
   and `test_probe_order_falsified.py` pins the ordering.

Each correction was declared *before* the next run, and each was adverse or
neutral to building: the probes were made able to see more, and `undecided` is not
a pass.

## Reproducing

```bash
python3 EXPERIMENTS/055-index-postcondition/run.py            # 210 rows + KILL-C
python3 EXPERIMENTS/055-index-postcondition/run.py --verify   # controls only
python3 EXPERIMENTS/055-index-postcondition/ceiling.py        # C11, C12, K3 away from -U0
python3 -m unittest discover -s EXPERIMENTS/055-index-postcondition \
        -t EXPERIMENTS/055-index-postcondition -p 'test_*.py'
```

Needs git ≥ 2.28 (`gitenv.py` builds 2.56.0 into `/tmp/opencode/gitenv`), Ubuntu
`patchutils`, and a CPython ≥ 3.10 for `git-hunk` (`/tmp/opencode/py312`). Every
`raw/*.json` carries the sha256 of each script that wrote it, and `run.py
--verify` recomputes them — because `ceiling.py` was once edited ten seconds after
it wrote `raw/ceiling.json` and the mismatch was invisible from the artifact
alone. **The test files exist to falsify the gates, not to pass**: each asserts
that `kill_c()`, the probe and the verdict readers *can* return the other answers,
so a green suite is evidence the instrument is falsifiable, not that KILL-C fired.
