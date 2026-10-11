"""E091 composition analysis: what kind of need is in this venue at all?

The inherited harness scored assistant answerability and stopped. That answers
"did an assistant serve these 20 rows" but not the question AMENDMENT-1 §4 says
matters when K1 fails: whether the residual is a population a program could
serve. This module measures the composition of the population directly.

The classification is of the THREAD'S REMEDY - what the asker ended up being
told - and not of whether an assistant attempt matched it. That keeps it a
property of the population rather than a restatement of the grades.

Classes, assigned per row against the committed threads in full.jsonl:

  answerable  the remedy is knowledge, or an action the asker can take alone.
  repair      the remedy is a physical repair or an artifact.
  vendor      the remedy requires the vendor: a return, an account action, a
              product decision, or a software fix only they can ship.
"""
import json
import math
import os

from grades import GRADES

HERE = os.path.dirname(os.path.abspath(__file__))

# id -> (class, the reply that settles it)
CLASS = {
    "86": ("answerable", "[1] there is no PIN; pair from inside the app"),
    "12241": ("answerable", "[4]/[14] phone on the 2.4 GHz network; restart phone, cooker, router"),
    "1096": ("repair", "[18] a specific user repair, confirmed by [16]; majority advice [5]-[15] is return/exchange. BORDERLINE"),
    "5021": ("repair", "[9]/[11]-[19] replace the TM7707 ADC board"),
    "722": ("repair", "[13] an aluminium C-clamp clamped to the pot"),
    "26273": ("answerable", "[8] 'fixed by cleaning the seal and sealing surface'; [4] bag handling"),
    "717": ("answerable", "[5]/[8] the only way to stop it is unplugging; [11] the timer button stops it"),
    "12736": ("repair", "[5] a steam shield and a UPS"),
    "4261": ("vendor", "[staff] 'a feature we are planning on implementing'"),
    "9165": ("repair", "[1] staff: loose stainless skirt, contact support"),
    "9020": ("repair", "[2] support walked the user through a button press; [11] a reseated coil housing"),
    "6924": ("answerable", "[1]/[8] no PIN, pair in the app; [9] an APK sideload. BORDERLINE - the thread never converged ([7] 'I give up')"),
    "132": ("repair", "[5] jumper wire between the two sensors, after [1] called the unit defective"),
    "4681": ("answerable", "[9]/[11] Anova's own rule: 8-18 characters, no special characters"),
    "3051": ("vendor", "[14]/[17]/[19] support escalated the ticket and shipped the right SKU"),
    "8811": ("vendor", "[4] 'manual intervention by the support team'"),
    "10550": ("vendor", "[3]/[8] 'a bug, the product team knows'; still open at [17]"),
    "13044": ("vendor", "[2] 'the dev team is aware'"),
    "12987": ("vendor", "[10] confirmed vendor bug; [17] vendor had abandoned the forum"),
    "5115": ("answerable", "[1] the radio is 2.4 GHz 802.11b/g/n only"),
}
ORDER = ["answerable", "repair", "vendor"]


def fisher_greater(a, b, c, d):
    """One-tailed Fisher exact. Table is [[served,unserved]] x [[row,col]].

    P(X >= a), the observed count. The tail must run from the OBSERVED value a
    down to the maximum, not from the column total: starting at col1 silently
    dropped every term below the maximum whenever the comparison row had any
    successes, which turned p=0.0307 into p=0.0014 here.
    """
    row1, total, col1 = a + b, a + b + c + d, a + c
    lo = max(a, row1 - (total - col1))
    hi = min(row1, col1)
    return sum(float(math.comb(col1, k) * math.comb(total - col1, row1 - k))
               / math.comb(total, row1) for k in range(lo, hi + 1))


def main():
    served = {g[0]: g[1] for g in GRADES}
    missing = [g[0] for g in GRADES if g[0] not in CLASS]
    if missing:
        raise SystemExit("rows with no composition class: %s" % missing)

    cells = {c: {"served": 0, "unserved": 0} for c in ORDER}
    for gid, (klass, _why) in CLASS.items():
        cells[klass]["served" if served[gid] else "unserved"] += 1

    n = len(GRADES)
    print("COMPOSITION of the 20 highest-arrival needs in this venue")
    print("  (class is the thread's remedy, assigned without reference to the assistant grades)")
    print()
    print("  %-12s %7s %9s %8s" % ("class", "served", "unserved", "share"))
    for c in ORDER:
        s, u = cells[c]["served"], cells[c]["unserved"]
        print("  %-12s %7d %9d %8.3f" % (c, s, u, (s + u) / float(n)))
    blocked = cells["repair"]["served"] + cells["repair"]["unserved"] + \
        cells["vendor"]["served"] + cells["vendor"]["unserved"]
    print()
    print("  needs requiring a vendor or a screwdriver: %d of %d = %.4f"
          % (blocked, n, blocked / float(n)))

    a_s = cells["answerable"]["served"]
    a_u = cells["answerable"]["unserved"]
    # Served/unserved totals, NOT the population size: using n here once made the
    # comparison row read "16 served of 16" and drove p to a fabricated 0.000000.
    tot_s = sum(cells[c]["served"] for c in ORDER)
    tot_u = sum(cells[c]["unserved"] for c in ORDER)
    o_s = tot_s - a_s
    o_u = tot_u - a_u
    assert o_s + o_u == tot_s + tot_u - (a_s + a_u)
    p = fisher_greater(a_s, a_u, o_s, o_u)
    print()
    print("  assistant served answerable-class needs at %d of %d; the other classes at %d of %d"
          % (a_s, a_s + a_u, o_s, o_s + o_u))
    print("  Fisher one-tailed (answerable vs the rest): p = %.6f" % p)
    vs_vendor = fisher_greater(a_s, a_u,
                               cells["vendor"]["served"], cells["vendor"]["unserved"])
    print("  Fisher one-tailed (answerable vs vendor only): p = %.6f" % vs_vendor)

    # Same contrast restricted to the attempt-first rows, whose grades were fixed
    # before any thread was read. This is the only subset not exposed to the
    # reader who also assigned the classes.
    clean = [g for g in GRADES if g[3]]
    c_s = sum(1 for g in clean if g[1] and CLASS[g[0]][0] == "answerable")
    c_a = sum(1 for g in clean if not g[1] and CLASS[g[0]][0] == "answerable")
    c_o = sum(1 for g in clean if g[1] and CLASS[g[0]][0] != "answerable")
    c_ou = sum(1 for g in clean if not g[1] and CLASS[g[0]][0] != "answerable")
    print()
    print("  attempt-first subset only (grades fixed before any thread was read):")
    print("    answerable %d served of %d; other %d served of %d"
          % (c_s, c_s + c_a, c_o, c_o + c_ou))
    print("    Fisher one-tailed: p = %.6f" % fisher_greater(c_s, c_a, c_o, c_ou))
    print("    ^ the cleanest subset is also the smallest. It is reported, not leaned on.")

    results = {
        "cells": cells,
        "blocked_share": blocked / float(n),
        "fisher_answerable_vs_rest": p,
        "fisher_answerable_vs_vendor": vs_vendor,
        "attempt_first": {"answerable": [c_s, c_s + c_a], "other": [c_o, c_o + c_ou],
                          "fisher": fisher_greater(c_s, c_a, c_o, c_ou)},
        "class_of": {k: v[0] for k, v in CLASS.items()},
        "evidence": {k: v[1] for k, v in CLASS.items()},
    }
    with open(os.path.join(HERE, "composition.json"), "w") as handle:
        json.dump(results, handle, indent=2, sort_keys=True)
    print("\nwrote composition.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
