#!/usr/bin/env python3
"""Fixtures for the bounded-neighbourhood comparison.  ALL SYNTHETIC.

Three groups, kept separate on purpose:

* 004's own ten cases, unchanged, so the result is comparable with T-0010.
* Cases constructed for this experiment to stress the bounded planner.
* Seeded random grids, split into a development seed and a holdout seed that was
  declared before the run and inspected once.

The last group is called `large` in spirit only: `large_cases()` are fixtures
the exhaustive oracle cannot enumerate, so only validity and cost are recorded
for them and optimality is never claimed.
"""

from __future__ import annotations

import random

from planner import MODEL, Patch

DEV_SEED = 1
DEV_COUNT = 40
HOLDOUT_SEED = 20261003
HOLDOUT_COUNT = 60
MODEL_CASES = [(n, p) for n, p in MODEL.CASES]


def constructed_cases():
    """Cases built to stress the bounded planner. SYNTHETIC, hand-built."""
    return [
        # Six errors whose closures never meet: six neighbourhoods of size 1,
        # the family where per-neighbourhood search should actually pay off.
        ("fragmented_6x4",
         Patch(6, 4, [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 2)], [])),
        # One neighbourhood of four: any chunking must split it, which is where
        # the additive cost argument stops holding.
        ("single_deep_stack_5x6", Patch(5, 6, [(2, 1), (2, 2), (2, 3), (2, 4)], [])),
        # A coupled pair plus two independent shallow errors: mixed group sizes.
        ("mixed_groups_6x5", Patch(6, 5, [(0, 2), (1, 2), (3, 2), (5, 3)],
                                   [((0, 2), (1, 2)), ((1, 3), (2, 3))])),
        # A cable chain dragging releases across four columns.
        ("cable_chain_6x5", Patch(6, 5, [(0, 1), (3, 1), (5, 1)],
                                  [((0, 1), (1, 1)), ((1, 1), (3, 1)), ((3, 1), (5, 1))])),
        # A second unsupported state with a different reason, so the refusal
        # path is tested by more than one fixture.
        ("unsupported_tension_4x4",
         Patch(4, 4, [(1, 2)], [], unsupported="yarn tension change at column 1")),
    ]


def random_cases(seed, count):
    """Seeded random grids. SYNTHETIC. Small enough for the exhaustive oracle."""
    rng = random.Random(seed)
    out = []
    for i in range(count):
        width, height = rng.randint(3, 6), rng.randint(3, 6)
        errors = set()
        for _ in range(rng.randint(1, 4)):
            errors.add((rng.randrange(width), rng.randrange(height)))
        cables = []
        for _ in range(rng.randint(0, 3)):
            a = (rng.randrange(width), rng.randrange(height))
            b = (rng.randrange(width), rng.randrange(height))
            if a != b:
                cables.append((a, b))
        out.append((f"rand_s{seed}_{i:02d}", Patch(width, height, sorted(errors), cables)))
    return out


def large_cases():
    """Fixtures beyond the random family's size. SYNTHETIC, hand-built.

    Each entry is `(name, patch, oracle_feasible)`. Two are checked against the
    oracle; the 24-error one is not by default, because the oracle enumerates all
    `2**24 = 16,777,216` patch subsets for it. `run.py --slow` enables it anyway:
    that run was measured at 334.8 s wall on this VM against 2.3 s without it, and
    the bounded planner matched the oracle on the fixture too (24 = 24).
    """
    return [
        # 24 independent one-loop releases: 2**24 subsets for the oracle, 48
        # for the bounded planner.
        ("large_fragmented_24x4",
         Patch(24, 4, [(c, 3) for c in range(24)], []), False),
        # A cable mesh over a 12x8 fabric, eight errors in four coupled groups.
        ("large_mesh_12x8",
         Patch(12, 8,
               [(c, r) for c in range(0, 12, 3) for r in (2, 5)],
               [((c, r), (c + 1, r)) for c in range(0, 11, 3) for r in (2, 5)]), True),
        # Three errors stacked in one column of a 12x8 fabric: the shape on
        # which the per-error rule of 004 is known to be suboptimal.
        ("large_column_stack_12x8", Patch(12, 8, [(5, 2), (5, 4), (5, 6)], []), True),
    ]


def compared_cases():
    """Every fixture the oracle can enumerate."""
    return (MODEL_CASES
            + constructed_cases()
            + random_cases(DEV_SEED, DEV_COUNT)
            + random_cases(HOLDOUT_SEED, HOLDOUT_COUNT))


def family(name):
    """Which group a case belongs to, for per-family reporting."""
    if any(name == n for n, _ in MODEL_CASES):
        return "from_004"
    if any(name == n for n, _ in constructed_cases()):
        return "constructed"
    if any(name == n for n, _, oracle in large_cases()):
        return "large_with_oracle" if any(
            n == name and oracle for n, _, oracle in large_cases()
        ) else "large_oracle_skipped"
    return "dev_random" if f"_s{DEV_SEED}_" in name else "holdout_random"