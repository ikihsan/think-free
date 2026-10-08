"""Experiment 052 — Task Prioritization Heuristics (revised)

Synthetic comparison of shortest-task-first vs random ordering on task completion
with a time budget that makes ordering meaningful.
"""

import random


# Configuration
TASK_POOL_SIZE = 20
TASKS_PER_LIST = 5
EFFORT_RANGE = (1, 5)
BUDGET = 6  # total effort budget per list; once budget is spent, stopping
NUM_LISTS = 100
NUM_RUNS = 3


def generate_task_pool(size, effort_range=(1, 5)):
    """Generate a pool of synthetic tasks with random efforts."""
    return {i: random.randint(*effort_range) for i in range(size)}


def select_tasks(pool, n=5):
    """Select n tasks without replacement from the pool."""
    keys = list(pool.keys())
    selected_keys = random.sample(keys, n)
    return [(k, pool[k]) for k in selected_keys]


def simulate_ordering(tasks, ordering='random', budget=BUDGET):
    """Simulate task completion under a given ordering with a budget.
    
    tasks: list of (task_id, effort) tuples
    ordering: 'random' or 'shortest_first'
    budget: total effort budget; tasks exceeding remaining budget are not attempted
    """
    if ordering == 'random':
        working_tasks = list(tasks)
        random.shuffle(working_tasks)
    elif ordering == 'shortest_first':
        working_tasks = sorted(tasks, key=lambda x: x[1])
    
    remaining_budget = budget
    completed = 0
    for task_id, effort in working_tasks:
        if effort <= remaining_budget:
            completed += 1
            remaining_budget -= effort
        else:
            break  # can't attempt this or remaining tasks
    
    return completed


# Run the experiment
random_seeds = [42, 123, 456]
results = []

for run_idx, seed in enumerate(random_seeds):
    random.seed(seed)
    gains = []
    for _ in range(NUM_LISTS):
        pool = generate_task_pool(TASK_POOL_SIZE, EFFORT_RANGE)
        tasks = select_tasks(pool, TASKS_PER_LIST)
        
        random_completed = simulate_ordering(tasks, 'random')
        shortest_completed = simulate_ordering(tasks, 'shortest_first')
        gain = shortest_completed - random_completed
        gains.append(gain)
    
    mean_gain = sum(gains) / len(gains)
    gain_positive = sum(1 for g in gains if g > 0)
    gain_zero = sum(1 for g in gains if g == 0)
    gain_negative = sum(1 for g in gains if g < 0)
    
    # Also compute completion rates
    random_completed_total = sum(simulate_ordering(select_tasks(generate_task_pool(TASK_POOL_SIZE, EFFORT_RANGE), 5), 'random') for _ in range(NUM_LISTS))
    shortest_completed_total = sum(simulate_ordering(select_tasks(generate_task_pool(TASK_POOL_SIZE, EFFORT_RANGE), 5), 'shortest_first') for _ in range(NUM_LISTS))
    rate_random = random_completed_total / (NUM_LISTS * TASKS_PER_LIST)
    rate_shortest = shortest_completed_total / (NUM_LISTS * TASKS_PER_LIST)
    
    results.append({
        'seed': seed,
        'gains': gains,
        'mean_gain': mean_gain,
        'gains_positive': gain_positive,
        'gains_zero': gain_zero,
        'gains_negative': gain_negative,
        'rate_random': rate_random,
        'rate_shortest': rate_shortest,
        'n': NUM_LISTS,
    })
    print(f"Run {run_idx} (seed={seed}):")
    print(f"  Mean gain: {mean_gain:.3f}")
    print(f"  Gains > 0: {gain_positive}/{len(gains)}")
    print(f"  Gains == 0: {gain_zero}/{len(gains)}")
    print(f"  Gains < 0: {gain_negative}/{len(gains)}")
    print(f"  Completion rate random: {rate_random:.3f} ({rate_random*100:.1f}%)")
    print(f"  Completion rate shortest-first: {rate_shortest:.3f} ({rate_shortest*100:.1f}%)")
    print(f"  Gains: {gains[:5]}...")  # preview first 5
    print()

# Summarize
print("=" * 60)
print("SUMMARY ACROSS RUNS")
print("=" * 60)
mean_gains = [r['mean_gain'] for r in results]
positive_counts = [r['gains_positive'] for r in results]
rates_random = [r['rate_random'] for r in results]
rates_shortest = [r['rate_shortest'] for r in results]

overall_mean_gain = sum(mean_gains) / len(mean_gains)
overall_positive = sum(positive_counts) / len(positive_counts)
overall_rate_random = sum(rates_random) / len(rates_random)
overall_rate_shortest = sum(rates_shortest) / len(rates_shortest)

print(f"Overall mean gain: {overall_mean_gain:.3f}")
print(f"Average gains-positive per run: {overall_positive}/{NUM_LISTS*NUM_RUNS} = {overall_positive/(NUM_LISTS*NUM_RUNS):.2f}")
print(f"Random completion rate: {overall_rate_random:.3f} ({overall_rate_random*100:.1f}%)")
print(f"Shortest-first completion rate: {overall_rate_shortest:.3f} ({overall_rate_shortest*100:.1f}%)")
print(f"Absolute improvement: {overall_rate_shortest - overall_rate_random:.3f} ({(overall_rate_shortest - overall_rate_random)*100:.1f} percentage points)")

# Check gate
gate_gain = overall_rate_shortest - overall_rate_random
if gate_gain > 0.05:
    print(f"PRIMARY GATE: PASSED — improvement of {gate_gain*100:.1f}% > 5%")
else:
    print(f"PRIMARY GATE: FAILED — improvement of {gate_gain*100:.1f}% not > 5%")
    
# Check secondary gate: positive gains in at least 2 of 3 runs
secondary_pass = overall_positive / (NUM_LISTS * NUM_RUNS) >= 2/3
print(f"SECONDARY GATE: {'PASSED' if secondary_pass else 'FAILED'} — {overall_positive}/{NUM_LISTS*NUM_RUNS} positive gains >= 2/3 threshold")