<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E042 — agent end-to-end test: stg vs alternatives for line-addressable staging

## Goal

Measure whether `stg` provides a practical advantage over the strongest achievable
baselines when used by an agent (script, CI job, editor keybinding, AI coding
agent) that needs to stage exactly one change by line number.

## Hypothesis

H1: `stg` achieves higher first-try correctness and lower silent-failure rate
than `filterdiff` and naive `git add -p` when driven by an automated caller.

H2: The shell baseline (a ~180-line Python script implementing the same logic as
`stg`) matches `stg` on correctness and honesty, demonstrating that the
mechanism is not the differentiator — packaging is.

## Method

Six test cases from E038/E040, each representing a realistic scenario an agent
might encounter. Each case is run in a fresh git repository.

Cases:
1. modify-one-of-three: single modification among unchanged lines
2. deletion-among-edits: deletion mixed with other changes
3. insertion-among-edits: insertion mixed with other changes
4. adjacent-edits: two adjacent modifications (the case that breaks `git add -p`)
5. adjacent-inserts: two adjacent insertions (the case that broke stg in E037)
6. append-at-eof: insertion at end of file

Routes under test:
- `stg`: the candidate tool
- `shell_baseline`: strongest scriptable baseline (E041's ~180-line Python)
- `filterdiff`: patchutils 0.3.4, the incumbent shell tool
- `naive`: `git add -p` with `y` answered to every hunk (not scriptable, control)

Metrics per case per route:
- `first_try_correct`: staged content exactly matches the oracle (what git would
  produce for only the requested line's change)
- `silent_failure`: exited 0 but staged content ≠ oracle (wrong thing staged
  with success code)
- `honest_failure`: exited non-zero and staged nothing (correctly refused)
- `exit_code`: raw exit code for debugging

Kill gate (pre-declared):
- If `stg` does NOT achieve strictly better (first_try_correct, silent_failure)
than `filterdiff` and `naive`, the practical advantage claim is falsified.
- If `shell_baseline` matches `stg` on both metrics, the mechanism is not the
  differentiator (already established by E041, but re-verified here end-to-end).

## Oracle

For each case, `want_content` is the exact file content that should result from
staging ONLY the requested line's change. This is written by hand from the case
definition and verified by applying the hand-built patch with `git apply
--cached --unidiff-zero`. The oracle is the staged file content, not the diff
anchors (which missed over-staging in E037).

## Reproduction

```bash
FILTERDIFF=/path/to/filterdiff python3 EXPERIMENTS/042-stg-end-to-end/run_experiment.py
```

The FILTERDIFF environment variable must point to the filterdiff binary
(patchutils 0.3.4). On this host: `/tmp/opencode/pu/x/usr/bin/filterdiff`.