#!/usr/bin/env python3
"""E091 scoring: Arm A (tool-shapedness) and Arm B (assistant answerability).

Arm B grades each ATTEMPTS.md entry against the thread, per AMENDMENT-1 §4. The
grade is not the instrument's confidence; it is whether the attempt contains the
fix the thread actually converged on, or - for unresolved threads - whether it
is a specific, correct, actionable remedy.

The per-row judgements live in `grades.py`, not here, so the arithmetic cannot
edit its own inputs. Wilson CI95 is computed here rather than by hand.
"""
import json
import math
import os

from grades import ARM_A_NOTES, GRADES

HERE = os.path.dirname(os.path.abspath(__file__))


def wilson(successes, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    phat = successes / float(n)
    denom = 1 + z * z / n
    centre = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def main():
    population = [str(json.loads(l)["id"])
                  for l in open(os.path.join(HERE, "population.jsonl"))]
    graded = {g[0] for g in GRADES}
    missing = [p for p in population if p not in graded]
    if missing:
        raise SystemExit("population rows with no grade: %s" % missing)
    extra = [g[0] for g in GRADES if g[0] not in population]
    if extra:
        raise SystemExit("graded rows not in the population: %s" % extra)

    # Exposure is the explicit per-row flag, never a string match on the prose.
    # The inherited harness searched the reason text for 'PRIOR EXPOSED' and so
    # counted ten thread-exposed rows as attempt-first.
    first_rows = [g for g in GRADES if g[3]]
    exposed = [g for g in GRADES if not g[3]]

    def share(rows):
        s = sum(1 for g in rows if g[1])
        n = len(rows)
        lo, hi = wilson(s, n)
        return s, n, (s / float(n) if n else 0.0), lo, hi

    s_all, n_all, p_all, lo_all, hi_all = share(GRADES)
    s_cl, n_cl, p_cl, lo_cl, hi_cl = share(first_rows)

    # K2 comparator from E062, the population this replicates.
    e_lo, e_hi = wilson(17, 20)

    unassessed = [g[0] for g in GRADES if g[0] not in ARM_A_NOTES]
    if unassessed:
        raise SystemExit("Arm A unassessed rows: %s" % unassessed)
    tool_shaped = sum(1 for g in GRADES if g[4])

    print("population rows            : %d" % len(population))
    print("attempt-first discipline   : %d rows  %s"
          % (n_cl, sorted((g[0] for g in first_rows), key=int)))
    print("thread-exposed before write: %d rows  %s"
          % (len(exposed), sorted((g[0] for g in exposed), key=int)))
    print()
    print("ARM B  served share")
    print("  all rows graded      : %2d of %2d = %.4f  Wilson CI95 [%.4f, %.4f]"
          % (s_all, n_all, p_all, lo_all, hi_all))
    print("  attempt-first subset : %2d of %2d = %.4f  Wilson CI95 [%.4f, %.4f]"
          % (s_cl, n_cl, p_cl, lo_cl, hi_cl))
    print()
    print("K1  served share CI95 lower bound >= 0.50")
    print("    all rows  : %s (%.4f)" % ("PASS" if lo_all >= 0.50 else "FAIL", lo_all))
    print("    subset    : %s (%.4f)" % ("PASS" if lo_cl >= 0.50 else "FAIL", lo_cl))
    reject_low = hi_all < e_lo
    reject_high = lo_all > e_hi
    print("K2  cannot reject E062's 17/20 = 0.8500 CI95 [%.4f, %.4f]" % (e_lo, e_hi))
    print("    this venue strictly lower  (upper < %.4f): %s" % (e_lo, reject_low))
    print("    this venue strictly higher (lower > %.4f): %s" % (e_hi, reject_high))
    print("    verdict: %s" % ("GENERALIZATION REJECTED" if (reject_low or reject_high)
                                else "cannot reject same population"))
    print()
    print("ARM A  tool-shaped remedies: %d of %d rows assessed"
          % (tool_shaped, len(GRADES)))
    for gid, klass in [(g[0], g[4]) for g in GRADES]:
        print("    %-6s %s" % (gid, ARM_A_NOTES.get(gid, "")))

    results = {
        "population_rows": len(population),
        "attempt_first_rows": n_cl,
        "thread_exposed_rows": sorted((g[0] for g in exposed), key=int),
        "arm_b_all": {"served": s_all, "n": n_all, "share": p_all,
                      "ci95": [lo_all, hi_all]},
        "arm_b_attempt_first": {"served": s_cl, "n": n_cl, "share": p_cl,
                                "ci95": [lo_cl, hi_cl]},
        "e062_comparator": {"served": 17, "n": 20, "ci95": [e_lo, e_hi]},
        "k1_pass_all": lo_all >= 0.50,
        "k1_pass_attempt_first": lo_cl >= 0.50,
        "k2_reject_low": reject_low,
        "k2_reject_high": reject_high,
        "arm_a_tool_shaped": tool_shaped,
        "arm_a_assessed": len(GRADES),
        "grades": [{"id": g[0], "served": g[1], "reason": g[2],
                    "attempt_first": g[3], "tool_shaped": g[4]} for g in GRADES],
    }
    with open(os.path.join(HERE, "results.json"), "w") as handle:
        json.dump(results, handle, indent=2, sort_keys=True)
    print("\nwrote results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
