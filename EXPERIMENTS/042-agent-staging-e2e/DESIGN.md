<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Experiment 042: Agent End-to-End Staging Test

## Goal
Test KILL-Q for `stg`: measure whether a coding agent asked to stage specific lines would use `stg` vs alternatives, by counting attempts, wrong answers, and success rates.

## Background
- E037: `stg` built and measured against naive baselines (pty driver, filterdiff) — 6 of 6 vs 4 of 6
- E038: Prior art found (`filterdiff --lines=RANGE`, VS Code's `git.stageSelectedRanges`), bugs fixed — 30 of 30 correct
- E041: Strongest shell baseline matches `stg` exactly on all 35 test rows — mechanism differentiation falsified
- KILL-Q: "Does anyone want this?" — partially evaluated (tool works, demand low at 0.016-0.066), but daily-use adoption never measured

## Experimental Design

### Test Scenarios
Create a set of realistic staging tasks that an agent might encounter:
1. Single line modification in a function
2. Multiple scattered modifications
3. Adjacent modified lines (the split case)
4. Multi-line insertion
5. Mixed modifications and insertions
6. Deletion at various positions

Each scenario is a real git repository with a specific working-tree state and a target line to stage.

### Approaches to Compare
1. **stg**: `stg stage file:line` — the candidate tool
2. **shell_baseline**: The ~180-line Python script from E041 implementing the same algorithm
3. **filterdiff**: `git diff -U0 | filterdiff --lines=N | git apply --cached --unidiff-zero`
4. **naive_git_add_p**: `git add -p` driven via pty (what E037 used)

### Agent Simulation
Since we can't run a real coding agent, we simulate the agent's decision process:
- Given a task "stage line N of file F", the agent must produce a command that achieves this
- For each approach, we measure:
  - **Attempts**: How many commands/tries before success
  - **Wrong answers**: Commands that staged wrong lines, staged too much, or failed silently
  - **Success**: Whether the final index matches exactly what was requested
  - **Time/Complexity**: Lines of code the agent must write/maintain

### Metrics
For each (scenario × approach) pair:
- `success`: boolean — final index matches request exactly
- `attempts`: integer — number of commands tried
- `wrong_staged`: boolean — staged something other than requested
- `silent_failure`: boolean — exited 0 but staged wrong thing
- `agent_code_lines`: lines of code the agent must write to use this approach

### Hypothesis
H0: Agents using `stg` achieve higher success rate with fewer attempts and less code than agents using alternatives.
H1: The shell baseline (which matches `stg` functionally) closes the gap — the differentiator is packaging, not mechanism.

### Kill Gate
If the shell baseline achieves parity with `stg` on success rate and attempts, then the mechanism is not the differentiator — confirming E041. The only remaining differentiator is packaging (ready-to-use CLI vs writing/maintaining a script).

If `stg` still outperforms the shell baseline on agent-usability metrics (fewer attempts, less code to write), then packaging matters for agents too.

## Implementation Plan
1. Create test scenarios as git repositories with known states
2. Implement the four approaches as callable functions
3. Run each approach against each scenario
4. Record metrics
5. Analyze and report

## Deliverables
- `results.json`: Raw measurements
- `README.md`: Experiment report with conclusions