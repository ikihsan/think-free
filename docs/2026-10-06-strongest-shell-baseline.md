<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Strongest Shell Baseline Experiment Plan

> **For agentic workers:** This is an experiment plan, not a product implementation. It follows the falsification-design protocol.

**Goal:** Test whether `stg` provides meaningful value over the strongest achievable shell pipeline for line-addressable staging, in the agent/caller setting.

**Architecture:** Build the strongest shell baseline (a `git diff -U0` filter that correctly splits adjacent changes per-line) and run it against `stg` on the same cases from E040 (agent-staging-loop). The baseline must be a genuine competitor, not a strawman.

**Tech Stack:** Python 3.8+, git, patchutils (filterdiff), standard library only.

## Global Constraints

- No external dependencies beyond git, patchutils (Debian 0.3.4), Python stdlib
- All tests against real git repositories, no mocks
- Cases from E040's CASES table (5 cases: adjacent-modifications, two-line-insertion, single-line-insertion, tail-modification, unchanged-line)
- Measure: exactness, honest exit codes, tool calls, bytes read, silent over-staging
- Kill gate: if strongest shell baseline achieves ≥4/5 exact AND honest on all 5 cases, the `stg` interface claim is falsified

## Falsification Design

**Claim:** No command-line tool takes `file:line`, splits adjacent changes correctly, and exits non-zero when it staged something else.

**Strongest Baseline:** A shell pipeline that:
1. Runs `git diff -U0` 
2. Parses hunks and splits multi-line changes into per-line hunks (pairing removed with added line-for-line)
3. Selects only the hunk(s) covering the requested working-tree line
4. Applies via `git apply --cached --unidiff-zero`
5. Returns honest exit codes (0 = nothing done, 1 = success, 2 = error)

**Kill Gate:** If the shell baseline matches `stg` on exactness (5/5) AND honesty (no silent wrong staging), `stg`'s practical value is falsified.

**Negative Control:** A deliberately broken variant (e.g., don't split adjacent changes) must perform worse, or the experiment cannot distinguish.

---

### Task 1: Build the strongest shell baseline library

**Files:**
- Create: `EXPERIMENTS/041-strongest-baseline/shell_baseline.py`

**Interfaces:**
- Consumes: None (standalone)
- Produces: `ShellBaseline` class with `stage(repo, path, line)` -> (exit_code, stdout, stderr, staged_blob)

- [ ] **Step 1: Write the failing test** (see `test_shell_baseline.py`)
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation** (see `shell_baseline.py`)
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Test all 5 E040 cases**
- [ ] **Step 6: Commit**

### Task 2: Run comparison against stg

**Files:**
- Create: `EXPERIMENTS/041-strongest-baseline/compare.py`
- Test: `EXPERIMENTS/041-strongest-baseline/test_shell_baseline.py`

**Interfaces:**
- Consumes: `shell_baseline.py`, `stage-lines/stg`
- Produces: `raw/comparison.jsonl` with per-case, per-route results

- [ ] **Step 1: Write comparison runner** (see `compare.py`)
- [ ] **Step 2: Run comparison**
- [ ] **Step 3: Record results and update hypothesis**
- [ ] **Step 4: Commit results**

### Task 3: Document findings

**Files:**
- Modify: `EXPERIMENTS/041-strongest-baseline/README.md`

**Interfaces:**
- Consumes: `raw/comparison.jsonl`, `run.log`
- Produces: Updated experiment record

- [ ] **Step 1: Write experiment README**
- [ ] **Step 2: Update HYPOTHESES-candidates.md if kill gate met**
- [ ] **Step 3: Commit**

---

## Execution

This plan was executed in session 2026-10-06-013. The experiment is complete.

**Results:** Kill gate met. The strongest shell baseline (a ~180-line Python script implementing `stg`'s exact splitting algorithm) matches `stg` on all 35 test rows (5 E040 + 30 E038). The mechanism is not the differentiator — the differentiator is packaging.

**After completion:**
- Updated STATE.md with the new experiment result
- Updated HYPOTHESES-candidates.md with E041 finding