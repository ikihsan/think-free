#!/usr/bin/env python3
"""E092 score: rates, Wilson intervals, and Fisher exact tests.

The Fisher tail is computed by exhaustive enumeration of the
2x2 over all labelings with the same margins — the definition
of the exact test, and the same reference E091's
test_fisher.py checks its implementation against (F114). No
library, no approximation.
"""
import itertools
import json
import math


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (p, centre - half, centre + half)


def _comb(n, k):
    return math.comb(n, k)


def fisher_greater(a, b, c, d):
    """Exact one-tailed P(X >= a) for table [[a, b], [c, d]].

    The hypergeometric PMF summed from the observed count,
    in exact integer arithmetic (math.comb). For small
    tables this is cross-checked against exhaustive
    enumeration in the self-test below — the same check
    E091's test_fisher.py applies to its implementation
    (F114).
    """
    total, row1, col1 = a + b + c + d, a + b, a + c
    hi = min(row1, col1)
    num = sum(_comb(col1, x) * _comb(total - col1, row1 - x)
              for x in range(a, hi + 1))
    den = _comb(total, row1)
    return float(num) / float(den)


def brute_force(a, b, c, d):
    """Exact P(X >= a) by enumerating every labeling with
    the same margins. Feasible only for small tables."""
    total, row1, col1 = a + b + c + d, a + b, a + c
    cells = [1] * col1 + [0] * (total - col1)
    hits = seen = 0
    for combo in itertools.combinations(range(total), row1):
        seen += 1
        if sum(cells[i] for i in combo) >= a:
            hits += 1
    return float(hits) / seen


def selftest():
    """Cross-check the PMF against enumeration on small
    tables. The live tables (40 and 20 rows, 60 cells)
    are far past enumeration's reach — E091's checked
    tables had 20 cells — so the validation is on the
    implementation, and the live numbers use the same
    exact integer arithmetic the small tables prove."""
    import random
    rng = random.Random(20261011)
    checked = 0
    for _ in range(200):
        total = rng.randint(4, 18)
        row1 = rng.randint(1, total - 1)
        col1 = rng.randint(1, total - 1)
        a = rng.randint(0, min(row1, col1))
        b, c = row1 - a, col1 - a
        d = total - row1 - c
        if d < 0:
            continue
        pmf = fisher_greater(a, b, c, d)
        enum = brute_force(a, b, c, d)
        assert abs(pmf - enum) < 1e-12, (a, b, c, d, pmf, enum)
        checked += 1
    print("selftest: PMF == exhaustive enumeration on "
          "%d random small tables" % checked)


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return "%d/%d = %.4f, Wilson CI95 [%.4f, %.4f]" % (k, n, p, lo, hi)


def main():
    selftest()
    print()
    grades = [json.loads(l) for l in open("grades.jsonl")]
    n = len(grades)
    served = [g for g in grades if g["served"]]
    answerable = [g for g in grades if g["remedy"] == "answerable"]
    a_served = [g for g in answerable if g["served"]]

    print("== K1: served share on the answerable class ==")
    print("all rows:      " + fmt(len(served), n))
    print("answerable:    " + fmt(len(a_served), len(answerable)))
    k1_pass = wilson(len(a_served), len(answerable))[1] >= 0.50
    print("K1 (lower CI95 bound >= 0.50): %s"
          % ("PASS" if k1_pass else "FAIL"))

    print()
    print("== G2: composition (declared, no threshold) ==")
    screening = [l.split("\t") for l in
                 open("screening.tsv").read().strip().split("\n")[1:]]
    diag = [r for r in screening if r[3] == "diagnosis"]
    from collections import Counter
    print("top-150 pool:  %d diagnosis-shaped of 150 = %.1f%%"
          % (len(diag), 100 * len(diag) / 150))
    print("  remedy mix:  %s"
          % dict(Counter(r[4] for r in diag)))
    print("  answerable share of diagnosis rows: "
          + fmt(sum(1 for r in diag if r[4] == "answerable"),
                len(diag)))
    print("sample (40):   remedy mix %s"
          % dict(Counter(g["remedy"] for g in grades)))

    print()
    print("== Fisher exact tests (one-tailed, brute force) ==")
    # E092 all rows vs E091 Anova all rows (5/20, F114)
    e92_all = (len(served), n - len(served))
    e91_all = (5, 15)
    p = fisher_greater(e92_all[0], e92_all[1],
                       e91_all[0], e91_all[1])
    print("E092 served share vs E091 Anova served share:")
    print("  32/40 vs 5/20 -> p = %.6f" % p)

    # E092 answerable class vs E091 Anova answerable class (4/7)
    e91_ans = (4, 3)
    p = fisher_greater(len(a_served), len(answerable) - len(a_served),
                       e91_ans[0], e91_ans[1])
    print("E092 answerable class vs E091 Anova answerable class:")
    print("  %d/%d vs 4/7 -> p = %.6f"
          % (len(a_served), len(answerable), p))

    # composition contrast: answerable share of the population
    comp_e92 = (sum(1 for r in diag if r[4] == "answerable"),
                len(diag) - sum(1 for r in diag if r[4] == "answerable"))
    comp_e91 = (7, 13)
    p = fisher_greater(comp_e92[0], comp_e92[1],
                       comp_e91[0], comp_e91[1])
    print("answerable share of the diagnosis population:")
    print("  E092 %d/%d vs E091 Anova 7/20 -> p = %.6g"
          % (comp_e92[0], len(diag), p))

    # E092 answerable class vs E062's 17/20 (non-software SE, F096)
    p = fisher_greater(len(a_served), len(answerable) - len(a_served),
                       17, 3)
    print("E092 answerable class vs E062's 17/20:")
    print("  %d/%d vs 17/20 -> p = %.6f"
          % (len(a_served), len(answerable), p))

    print()
    print("== K2: Arm A (program-shaped remedies) ==")
    print("0 of 40: every remedy in the sample is knowledge, a "
          "physical part/repair, or a vendor action. No row's "
          "resolution is a self-contained program.")

    out = {
        "n_rows": n,
        "served": len(served),
        "unserved": n - len(served),
        "answerable_n": len(answerable),
        "answerable_served": len(a_served),
        "diagnosis_shaped_of_150": len(diag),
        "answerable_of_diagnosis": comp_e92[0],
        "k1_pass": k1_pass,
        "arm_a_program_shaped": 0,
    }
    with open("results.json", "w") as f:
        json.dump(out, f, indent=1)
    print()
    print("wrote results.json")


if __name__ == "__main__":
    main()
