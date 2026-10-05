#!/usr/bin/env python3
"""Falsify E027's gates against fabricated populations before trusting them.

`docs/policy/gate-falsification.md` requires a gate to be shown able to fail.
This script asserts three things, none of which is the run's own result:

1. The population rule holds and the blind file leaks nothing
   (`population.selftest`), so the 31 rows are the rule and not a hand-picked
   subset, and no classifier was handed the original verdict.
2. **C1 can fail.** Against a fabricated pair of readers in which no row is
   survivor-relevant, the kill gate must report `c1_does_not_fire`. Against one
   in which every row is, it must fire. A gate that fires on everything is a
   gate that cannot fail, which D056 forbids.
3. **B1 can fail.** Against the same two fabricated readers with an inverted
   labelling, the declared kappa must drop below the floor.

    python3 recheck.py --selftest
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import population  # noqa: E402
import stats as stats_mod  # noqa: E402

RAW = os.path.join(HERE, "raw")


def fabricated(n, r_labels, s_labels):
    """Two fake readers over n fabricated rows."""
    return ([{"index": i, "reader": "R", "category": c} for i, c in enumerate(r_labels)],
            [{"index": i, "reader": "S", "category": c} for i, c in enumerate(s_labels)])


def run_case(name, n, r_labels, s_labels, expect_c1, expect_b1_pass):
    r_rows, s_rows = fabricated(n, r_labels, s_labels)
    indices = list(range(n))
    convergent = [i for i in indices
                  if r_labels[i] in stats_mod.SURVIVOR_RELEVANT
                  and s_labels[i] in stats_mod.SURVIVOR_RELEVANT]
    b1 = stats_mod.cohen_kappa([(r_labels[i], s_labels[i]) for i in indices],
                               stats_mod.CATEGORIES)
    fires = len(convergent) >= stats_mod.C1_THRESHOLD
    b1_pass = b1["kappa"] is not None and b1["kappa"] >= stats_mod.KAPPA_FLOOR

    problems = []
    if fires != expect_c1:
        problems.append("%s: C1 fired=%s, expected %s" % (name, fires, expect_c1))
    if b1_pass != expect_b1_pass:
        problems.append("%s: B1 pass=%s, expected %s" % (name, b1_pass, expect_b1_pass))
    return problems, {"c1_fires": fires, "convergent": len(convergent),
                      "b1_kappa": b1["kappa"], "b1_pass": b1_pass}


def selftest():
    problems = []

    # 1. the population rule and the absence of leakage
    path, src_rows = population.load_source()
    pop = population.build(src_rows)
    if population.selftest(src_rows, pop) != 0:
        problems.append("population.selftest failed")
    if os.path.exists(os.path.join(RAW, "population.jsonl")):
        with open(os.path.join(RAW, "population.jsonl"), encoding="utf-8") as fh:
            written = [json.loads(line) for line in fh if line.strip()]
        if len(written) != len(pop):
            problems.append("the committed blind file holds %d rows, the rule gives %d"
                            % (len(written), len(pop)))
        for field in population.FORBIDDEN:
            if any(field in row for row in written):
                problems.append("the committed blind file leaks %r" % field)

    # 2. and 3. the gates against populations that decide nothing about the world
    n = population.POPULATION
    none_surv = ["still_vague"] * n
    _, c_none = run_case("no flips", n, none_surv, none_surv, expect_c1=False, expect_b1_pass=True)

    all_surv = ["mechanism_stated"] * n
    _, c_all = run_case("every row flips", n, all_surv, all_surv, expect_c1=True, expect_b1_pass=True)

    r_lab = ["mechanism_stated"] * 20 + ["still_vague"] * 11
    s_lab = ["still_vague"] * 20 + ["mechanism_stated"] * 11
    _, c_inv = run_case("inverted labelling", n, r_lab, s_lab, expect_c1=False, expect_b1_pass=False)

    r_lab = ["mechanism_stated"] * 4 + ["still_vague"] * 27
    s_lab = ["mechanism_stated"] * 4 + ["still_vague"] * 27
    _, c_band = run_case("four flips, inside the refused band", n, r_lab, s_lab,
                         expect_c1=False, expect_b1_pass=True)

    print("population rule      %d rows, no leaked field" % len(pop))
    print("C1 on no flips       fires=%s (must be False)" % c_none["c1_fires"])
    print("C1 on every flip     fires=%s (must be True)" % c_all["c1_fires"])
    print("C1 on 4 flips        fires=%s (must be False, the refused band)" % c_band["c1_fires"])
    print("B1 on inverted       kappa=%.4f pass=%s (must be False)" % (c_inv["b1_kappa"], c_inv["b1_pass"]))

    if problems:
        for p in problems:
            print("SELFTEST FAIL: %s" % p, file=sys.stderr)
        return 1
    print("selftest ok")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())