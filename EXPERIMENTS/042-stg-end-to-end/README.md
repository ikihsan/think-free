<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E042 — agent end-to-end test: stg vs alternatives for line-addressable staging

`observed` 2026-10-06, session 2026-10-06-014, VM `instance-20260717-0944`, git 2.25.1,
Python 3.8.10, patchutils 0.3.4. Protocol in [`PROTOCOL.md`](PROTOCOL.md).
Raw evidence: [`raw/compare.jsonl`](raw/compare.jsonl).

**Verdict: `stg` achieves perfect first-try correctness and zero silent failures
against the incumbent tools, but the strongest shell baseline matches it exactly.
The mechanism is not the differentiator; packaging is.**

## Results

| Route | correct | silent_failure | honest_failure | other (exit≠0,1,2) |
|-------|---------|----------------|----------------|-------------------|
| **stg** | **6/6** | **0/6** | 0 | 0 |
| **shell_baseline** | **6/6** | **0/6** | 0 | 0 |
| filterdiff | 2/6 | 1/6 | 0 | 3 (exit 128) |
| naive (`git add -p`) | 2/6 | 4/6 | 0 | 0 |

### Per-case breakdown

| Case | stg | shell_baseline | filterdiff | naive |
|------|-----|----------------|------------|-------|
| modify-one-of-three | ✓ | ✓ | ✓ | ✓ |
| deletion-among-edits | ✓ | ✓ | ✓ | ✗ silent |
| insertion-among-edits | ✓ | ✓ | ✗ exit 128 | ✓ |
| adjacent-edits | ✓ | ✓ | ✗ silent | ✗ silent |
| adjacent-inserts | ✓ | ✓ | ✗ exit 128 | ✗ silent |
| append-at-eof | ✓ | ✓ | ✗ exit 128 | ✗ silent |

## Kill gates

**Kill gate 1 (stg better than filterdiff AND naive): PASSED**
- stg: 6/6 correct, 0 silent failures
- filterdiff: 2/6 correct, 1 silent failure, 3 hard errors
- naive: 2/6 correct, 4 silent failures
- stg is strictly superior on both metrics to both alternatives.

**Kill gate 2 (shell_baseline matches stg): PASSED**
- shell_baseline: 6/6 correct, 0 silent failures — identical to stg.
- The mechanism (pair-removes-with-adds line splitting) is replicable in ~180
  lines of Python. The differentiator is packaging: a ready-to-use, tested,
  documented CLI tool vs. writing and maintaining custom git plumbing code.

## What this means for the candidate

| Dimension | Status | Evidence |
|-----------|--------|----------|
| **Mechanism** | Supported, but not novel | E038: independent implementation (VS Code) uses same heuristic; E041: shell baseline matches; E042: end-to-end confirms |
| **Interface gap** | Demonstrated | No CLI tool takes `file:line`, splits adjacent changes, and exits honestly. `filterdiff` fails on adjacent changes and exits 128 on insertions. `git add -p` is interactive only. |
| **Correctness** | Verified | 30/30 against oracle (E038), 6/6 end-to-end (E042), byte-identical index to hand-built patch |
| **Honest exit codes** | Verified | E039: 8/8 real failure modes refused loudly; E042: 0 silent failures |
| **Adoption (KILL-Q)** | **not_evaluated** | Four experiments, no measurement of whether anyone *wants* this enough to adopt it |

## Ceiling

- Six synthetic cases, one git version (2.25.1), default `diff.context`.
- Does not test renames, mode changes, `--intent-to-add`, `diff.algorithm`,
  binary files, untracked files, conflicted merges, or multi-file scenarios.
- `filterdiff` tested at default settings; stronger shell pipelines exist but
  were not tried (per D067: test against mechanism's existing source first).
- The shell baseline is Python, not pure shell (awk/sed). A pure shell
  implementation would be significantly harder and more fragile.
- No adoption measurement, and none is possible from this host without authorization.

## Next action

The candidate `stg` survives as a **useful tool** (packaging value: a ready-to-use
CLI that an agent can call without writing 180 lines of git plumbing) but not as
a **mechanism invention** (the algorithm is replicable and independently
discovered).

The open question remains **KILL-Q**: does anyone want this enough to adopt it?

Options (from E041):
1. Measure adoption interest (contact `mcp-multi-root-git#3`, `sublime_merge#976`,
   `vim-gitgutter#446` — requires authorization)
2. Publish `stg` as-is and observe organic adoption
3. Pivot to a different candidate

The invention seat (item 0d in `STATE-next-actions.md`) remains empty for a
mechanism invention. `stg` is a candidate with a working artifact whose interface
gap is demonstrated but whose adoption is unmeasured.