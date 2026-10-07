<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — strongest shell baseline for line-addressable staging

`observed` 2026-10-06, session 2026-10-06-013, VM `instance-20260717-0944`, git 2.25.1,
Python 3.8.10. Plan, declared before the run:
[`docs/2026-10-06-strongest-shell-baseline.md`](../../docs/2026-10-06-strongest-shell-baseline.md).
Raw evidence: [`raw/comparison.jsonl`](raw/comparison.jsonl),
[`raw/e038_comparison.jsonl`](raw/e038_comparison.jsonl). Reproduce:
`python3 EXPERIMENTS/041-strongest-baseline/compare.py` and
`python3 EXPERIMENTS/041-strongest-baseline/test_e038_cases.py`.

The plan this experiment executed was written before the run and is kept at [`docs/2026-10-06-strongest-shell-baseline.md`](../../docs/2026-10-06-strongest-shell-baseline.md); it is linked from here because the generated `docs/INDEX.md` does not count as a link for the orphan rule.


**Verdict: the strongest shell baseline (a Python script implementing the same
pair-removes-with-adds splitting logic as `stg`) matches `stg` exactly and
honestly on all E040 agent-style cases (5/5) and all E038 cases (30/30 across
3 diff.context values). The kill gate for `stg`'s practical advantage over a
scripted solution is met.**

## The question

E037 hypothesized that "a ten-line `git diff -U0` filter" could be the real
competitor to `stg`. E040 compared `stg` against a naive approach (piping keys
to `git add -p`) and found a practical difference. E038 compared against
`filterdiff` and `git add -p` via pty and found `stg` superior. But neither
tested the **strongest achievable shell baseline** — a script that correctly
implements the line-pairing split logic.

This experiment builds that strongest baseline and tests it against `stg`.

## The strongest shell baseline

`shell_baseline.py` (~180 lines of Python) implements:
1. Parse `git diff -U0` into hunks
2. Split multi-line hunks by pairing removed lines with added lines line-for-line
3. Surplus adds become individual per-line hunks; surplus removes stay as one hunk
4. Select the hunk(s) covering the requested working-tree line
5. Apply via `git apply --cached --unidiff-zero`
6. Return honest exit codes (1=success, 2=error/nothing-to-do)

This is **the same algorithm as `stg`**, reimplemented independently. It is not
a strawman — it correctly handles adjacent edits, multi-line insertions,
deletions, and all E038 case classes.

## Results

### E040 agent-style cases (5 cases)

| Route | exact | honest | silent wrong |
|-------|-------|--------|--------------|
| stg | 5/5 | 5/5 | 0 |
| shell_baseline | 5/5 | 5/5 | 0 |

**KILL GATE MET**: shell baseline matches `stg` exactly and honestly on all 5 cases.

### E038 full case matrix (10 cases × 3 diff.context = 30 rows)

| Route | correct | wrong-but-exit-0 | exit-0 |
|-------|---------|------------------|--------|
| stg | 30/30 | 0 | 0 |
| shell_baseline | 30/30 | 0 | 0 |

**Every single row matches.** The shell baseline achieves parity with `stg`
across the entire E038 test matrix.

## What this means

**The mechanism is not the differentiator.** The practical advantage E040
measured was against a naive baseline, not the strongest achievable one. A
determined developer can write a ~180-line Python script that provides the same
line-addressable staging capability as `stg`.

**The differentiator is packaging and maintenance.** `stg` provides:
- A ready-to-use CLI tool (`stg stage file:line`)
- Tested correctness (30 tests against real git repos)
- Documented behavior and error messages
- No need to maintain custom git plumbing code

A scripted solution requires:
- Writing and maintaining ~180 lines of non-trivial git diff parsing
- Handling edge cases (binary files, CRLF, no trailing newline, untracked files)
- Testing against real repositories
- Keeping it working across git versions

## Ceiling

- The shell baseline is Python, not pure shell (awk/sed). A pure shell
  implementation would be significantly harder and more fragile.
- The baseline implements `stg`'s exact algorithm — it's not an independent
  invention. The "independent implementation arriving at the same mechanism"
  (VS Code's `git.stageSelectedRanges`, F062) is evidence the mechanism is
  natural, not that it's trivial to reimplement.
- Only tested on git 2.25.1. Git 2.55.0 (CI runner) may behave differently.
- Does not test renames, mode changes, `--intent-to-add`, `diff.algorithm`,
  binary files, untracked files, or conflicted merges — same ceiling as E038.
- KILL-Q (does anyone want this) remains `not_evaluated` for the fifth experiment.

## Negative control

A deliberately broken variant (don't split adjacent changes — use raw git hunks)
was tested implicitly by E038's `filterdiff` and `naive` routes, which both
failed on adjacent-change cases. The experiment can distinguish correct from
incorrect implementations.

## Next action

The candidate `stg` survives as a **useful tool** (packaging value) but not as a
**mechanism invention** (the algorithm is replicable). The open question remains
KILL-Q: does anyone want this enough to adopt it?

Options:
1. Measure adoption interest (contact `mcp-multi-root-git#3`, `sublime_merge#976`,
   `vim-gitgutter#446` — requires authorization)
2. Publish `stg` as-is and observe organic adoption
3. Pivot to a different candidate

The seat (item 0d in STATE-next-actions.md) remains empty for a mechanism
invention. `stg` is a candidate with a working artifact whose interface gap is
demonstrated but whose adoption is unmeasured.