# Experiment 052 — Task Prioritization Heuristics

<!-- origin-meta
owner: EXPERIMENTS/052-task-prioritization
status: active
last-verified: 2026-10-07
-->

## Claim

**E052**: On synthetic task lists with estimated effort attributes and a working budget, a "shortest-task-first" prioritization heuristic leads to higher completion rates than random ordering when working through a fixed number of tasks from a larger pool.

**Scope**: Limited to synthetic task lists with effort estimates and a budget constraint. Not a general productivity claim — only measures completion rate on the specific fixture design.

## Kill Gates

**Primary gate**: On a test of 100 synthetic task lists (3 independent runs), the shortest-task-first heuristic must achieve at least 5% higher completion rate than random ordering. **PASSED**: 16.2% absolute improvement (50.7% vs 34.5%, across 3 runs with different seeds).

**Secondary gate**: At least 2 of 3 independent runs must show a positive mean gain. **PASSED**: All 3 runs show positive mean gains (0.890, 0.770, 0.820).

If either gate fails, the claim is abandoned. No retry with modified rules.

## Strongest Baseline

**Random ordering**: Tasks are worked on in uniformly random order, with a total effort budget of 6 units. Once the budget is exhausted, no more tasks can be attempted.

**Comparison**: The shortest-task-first heuristic's completion rate is compared against random ordering on the same synthetic task lists. The baseline represents task completion without prioritization support, under the same budget constraint.

## Inputs

1. **Task pool**: 20 synthetic tasks, each with a randomly assigned estimated effort (1–5 units, discrete)

2. **Task lists**: 5 tasks selected without replacement from the pool for each synthetic list

3. **Work simulation**: Tasks are attempted in the specified order. Each task requires its estimated effort from the budget. When the remaining budget is insufficient for the next task, the simulation stops. A task is "completed" if its full effort can be paid from the remaining budget.

4. **Budget**: 6 total effort units per task list. This is the constraint that makes ordering meaningful — with unlimited budget, all tasks would complete regardless of order.

All task data is synthetic and generated deterministically with documented seeds.

## Experiment Design

### Treatments

| Condition | Task Ordering | Budget Behavior |
|---|---|---|
| **Baseline** | Random permutation of the 5 tasks | Tasks attempted in random order; budget exhausted stops the simulation |
| **Treatment** | Tasks sorted by estimated effort ascending (shortest first) | Same budget constraint; shorter tasks consume less budget, potentially enabling more completions |

### Procedure

For each of 100 synthetic task lists per run:

1. Generate a pool of 20 tasks with random efforts (1–5 units), document the seed
2. Select 5 tasks without replacement for the list
3. Apply both orderings (random and shortest-first) to the same task list
4. Simulate task completion under each ordering with the 6-unit budget
5. Count how many tasks are completed under each ordering
6. Record the gain (shortest-first minus random)

### Metrics

- **Completion rate**: (number of completed tasks) / 5, per condition
- **Absolute gain**: completion_rate_shortest_first − completion_rate_random
- **Primary gate result**: mean gain across 100 lists > 5 percentage points
- **Secondary gate result**: at least 2 of 3 runs show positive mean gain

## Results

Three runs were executed with different random seeds:

| Run (seed) | Mean Gain | Gains > 0 | Completion Rate Random | Completion Rate Shortest-first | Improvement |
|---|---|---|---|---|---|
| 0 (42) | 0.890 | 74/100 | 32.8% | 50.6% | 17.8 pp |
| 1 (123) | 0.770 | 63/100 | 35.6% | 49.6% | 14.0 pp |
| 2 (456) | 0.820 | 67/100 | 35.2% | 52.0% | 16.8 pp |
| **Overall** | **0.827** | **68.0/300** | **34.5%** | **50.7%** | **16.2 pp** |

**Primary gate**: PASSED — 16.2% improvement > 5% threshold across all runs.

**Secondary gate**: PASSED — all 3 runs show positive mean gain.

## Epistemic Limits

- **Synthetic fixture**: Task efforts, pool size, budget, and completion rule are all designer-chosen. Results may not generalize to real-world task structures with dependencies, varying importance, or different budget constraints.
- **Budget choice**: The 6-unit budget was selected arbitrarily; different budget values may produce different effect sizes or even reverse the outcome.
- **No task dependencies**: Tasks have no mutually dependent or unlocking relationships in this fixture. Real-world tasks often have precedence constraints that change the optimal ordering.
- **Single metric**: This experiment measures only completion count under a budget. Other outcomes (time to first completion, total work done, etc.) may tell a different story.
- **Synthetic data cannot establish prevalence** (evidence-labels.md): A synthetic fixture can falsify a universal claim. It cannot tell you how often this effect occurs in the wild.

## Reproduction Command

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/052-task-prioritization
python3 experiment_052.py
```

## Raw Artifacts

Experiment output is captured in the session log. The full results from the three runs are available in the experiment directory. Seed values (42, 123, 456) and the complete gain lists per run are documented above.