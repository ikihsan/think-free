#!/usr/bin/env python3
"""E031 gate A3 — reader agreement, computed BEFORE any rate is read.

Cohen's kappa on the three-label q1 scheme, over the 96 double-read rows and
nothing else (PROTOCOL-AMENDMENT-1.md §2). Declared floor 0.6. Below it the
verdict is `not_evaluated` and recurrence.py reports no recurrence number.

Writes raw/agreement.json. Prints the per-arm counts, the kappa, and the rows
the two readers disagree on, with both clauses, so the disagreement is
inspectable rather than summarised.
"""

import json
import os

import common as C

FLOOR = 0.6


def read_tsv(path):
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                out[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else "-")
    return out


def main():
    ids = [x.strip() for x in
           open(os.path.join(C.RAW, "doubleread_ids.txt"), encoding="utf-8")
           if x.strip()]

    per_arm = {}
    for stem, prefix in (("seek", "S"), ("move", "M"), ("ordinary", "O")):
        p1 = os.path.join(C.RAW, "e031_labels_%s__r1.tsv" % stem)
        p2 = os.path.join(C.RAW, "e031_labels_%s__r2.tsv" % stem)
        l1, l2 = read_tsv(p1), read_tsv(p2)
        rows = [(i, l1[i][0], l2[i][0], l1[i][1], l2[i][1])
                for i in ids if i.startswith(prefix)]
        kappa, n = C.cohen_kappa([(a, b) for _, a, b, _, _ in rows])
        disagree = [{"id": i, "r1": a, "r2": b, "clause_r1": c1, "clause_r2": c2}
                    for i, a, b, c1, c2 in rows if a != b]
        per_arm[stem] = {
            "n_double_read": n,
            "r1_yes": sum(1 for _, a, _, _, _ in rows if a == "1"),
            "r2_yes": sum(1 for _, _, b, _, _ in rows if b == "1"),
            "kappa": kappa,
            "agreement": sum(1 for _, a, b, _, _ in rows if a == b) / float(n) if n else None,
            "n_disagree": len(disagree),
            "disagreements": disagree,
        }

    allrows = []
    for stem in per_arm:
        prefix = {"seek": "S", "move": "M", "ordinary": "O"}[stem]
        p1 = read_tsv(os.path.join(C.RAW, "e031_labels_%s__r1.tsv" % stem))
        p2 = read_tsv(os.path.join(C.RAW, "e031_labels_%s__r2.tsv" % stem))
        allrows.extend((p1[i][0], p2[i][0]) for i in ids
                       if i.startswith(prefix) and i in p1 and i in p2)
    kappa_all, n_all = C.cohen_kappa(allrows)

    out = {
        "gate": "A3",
        "declared_floor": FLOOR,
        "kappa_overall": kappa_all,
        "n_double_read": n_all,
        "raw_agreement": sum(1 for a, b in allrows if a == b) / float(n_all),
        "verdict": "passes" if (kappa_all is not None and kappa_all >= FLOOR) else "fails",
        "per_arm": per_arm,
        "note": ("two independent sub-agent contexts, same model family; "
                 "independent context, not independent priors"),
    }
    path = os.path.join(C.RAW, "agreement.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    C.log("agreement", kappa=kappa_all, n=n_all, floor=FLOOR,
          verdict=out["verdict"],
          per_arm_kappa={k: v["kappa"] for k, v in per_arm.items()},
          disagree={k: v["n_disagree"] for k, v in per_arm.items()})


if __name__ == "__main__":
    main()