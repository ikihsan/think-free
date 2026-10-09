#!/usr/bin/env python3
"""
Fire E072's five predeclared gates and write the verdict into results.json.

Kept separate from eval_arms.py so that the gates cannot be edited in the same
edit as the numbers. `eval_arms.py` writes measurements; this file reads them
and compares against PROTOCOL.md's table. Nothing here computes a metric.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

G1_PRECISION, G1_RECALL = 0.60, 0.50
G2_F1_MARGIN = 0.05
G3_PERMUTATION_MAX = 0.10
G4_MIN_ACCOUNTS, G4_MIN_TXNS, G4_MIN_MERCHANTS = 8, 3000, 12

ARMS = ["e065_raw", "actual_raw", "e065_normalized", "actual_shared", "naive"]


def main():
    r = json.load(open(os.path.join(HERE, "results.json")))
    prec_labels = json.load(open(os.path.join(HERE, "precision_labels.json")))
    wl = json.load(open(os.path.join(HERE, "watchlist.json")))
    gates = []

    # ---- G4 first: it decides whether any other gate may be read ---------
    g4_ok = (r["corpus"]["accounts"] >= G4_MIN_ACCOUNTS
             and r["corpus"]["transactions"] >= G4_MIN_TXNS
             and r["watchlist"]["distinct_merchants"] >= G4_MIN_MERCHANTS)
    gates.append({
        "gate": "G4", "name": "population is real and big enough",
        "requirement": ">= %d accounts, >= %d transactions, >= %d hand-verified merchants"
                       % (G4_MIN_ACCOUNTS, G4_MIN_TXNS, G4_MIN_MERCHANTS),
        "observed": "%d accounts, %d transactions, %d distinct merchants"
                    % (r["corpus"]["accounts"], r["corpus"]["transactions"],
                       r["watchlist"]["distinct_merchants"]),
        "fired": bool(g4_ok),
        "consequence": "verdict is measurable" if g4_ok else "verdict is 'untested', never 'pass'",
    })
    if not g4_ok:
        json.dump({"gates": gates, "verdict": "untested"}, open(os.path.join(HERE, "verdict.json"), "w"), indent=1)
        print(json.dumps(gates, indent=1))
        return 1

    primary = "e065_raw"

    # ---- G1: does the mechanism survive merchant strings ------------------
    a = r["arms"][primary]
    g1_ok = a["precision"] >= G1_PRECISION and a["recall"] >= G1_RECALL
    gates.append({
        "gate": "G1", "name": "the mechanism survives merchant strings",
        "requirement": "precision >= %.2f AND recall >= %.2f on real modern exports" % (G1_PRECISION, G1_RECALL),
        "observed": "precision %.4f (watchlist-scored, a LOWER BOUND), recall %.4f"
                    % (a["precision"], a["recall"]),
        "fired": bool(g1_ok),
        "consequence": "line continues" if g1_ok else "the merchant axis destroyed E066's result -- LINE CLOSED",
    })

    # stratified precision from the hand read
    labels = [l for l in prec_labels["labels"] if l["label"] != "ambiguous"]
    n_rec = sum(1 for l in labels if l["label"] == "recurring")
    r["stratified_precision"] = {
        "sampled": len(labels),
        "ambiguous_excluded": sum(1 for l in prec_labels["labels"] if l["label"] == "ambiguous"),
        "recurring": n_rec,
        "precision": round(n_rec / len(labels), 4) if labels else None,
        "note": "95%% interval is not computed: %d labels is a sample, not a census, and "
                "the watchlist-scored 0.088 is the other end of the range." % len(labels),
    }

    # ---- G2: does it beat the incumbent on the incumbent's own ground -----
    base = r["arms"]["actual_raw"]
    margin = a["f1"] - base["f1"]
    g2_ok = margin >= G2_F1_MARGIN
    gates.append({
        "gate": "G2", "name": "beats the strongest accessible alternative",
        "requirement": "F1 margin over Actual Budget findSchedules on the same raw strings >= +%.2f" % G2_F1_MARGIN,
        "observed": "e065_raw F1 %.4f, actual_raw F1 %.4f, margin %+.4f"
                    % (a["f1"], base["f1"], margin),
        "fired": bool(g2_ok),
        "consequence": "candidate survives" if g2_ok else "no differentiation against the strongest alternative -- NOTHING IS BUILT",
        "handicap_note": "actual_raw is a LOWER BOUND on the incumbent: in production Actual matches on a "
                         "payee its importer has already cleaned, and this arm gives it the same dirty strings "
                         "E065 gets. A negative margin here is therefore not evidence that E065 is better.",
    })

    # ---- G3: can the instrument say no ------------------------------------
    perm = r["permutation_control"][primary]
    g3_ok = perm["rate"] <= G3_PERMUTATION_MAX
    gates.append({
        "gate": "G3", "name": "the instrument can say no",
        "requirement": "permutation control <= %.2f" % G3_PERMUTATION_MAX,
        "observed": "%d of %d positives survive within-account date shuffling = %.4f"
                    % (perm["survived"], perm["trials_positives"], perm["rate"]),
        "fired": bool(g3_ok),
        "consequence": "results are not an artifact of date structure",
    })

    # ---- G5: no single account decides it --------------------------------
    lo = r["leave_one_out"]
    flips = [arm for arm in ARMS
             if (lo["arms"][arm]["precision"] >= G1_PRECISION) != (r["arms"][arm]["precision"] >= G1_PRECISION)]
    g5_ok = not flips
    gates.append({
        "gate": "G5", "name": "no single account decides it",
        "requirement": "the G1 direction is unchanged when the largest account is dropped",
        "observed": "dropped %s; arms whose precision verdict flips: %s"
                    % (lo["dropped"], flips or "none"),
        "fired": bool(g5_ok),
        "consequence": "the result is not one person's spending",
    })

    fired = [g["gate"] for g in gates if g["fired"]]
    failed = [g["gate"] for g in gates if not g["fired"]]
    if failed:
        verdict = ("CLOSED on the E065 detector as shipped: %s did not fire. "
                   "No candidate, no prototype." % ", ".join(failed))
    else:
        verdict = "all gates fired; the mechanism survives and earns the right to be tested further"

    out = {"gates": gates, "verdict": verdict, "fired": fired, "failed": failed,
           "primary_arm": primary,
           "arms_ranked_by_f1": sorted(ARMS, key=lambda x: -r["arms"][x]["f1"])}
    json.dump(out, open(os.path.join(HERE, "verdict.json"), "w"), indent=1)
    json.dump(r, open(os.path.join(HERE, "results.json"), "w"), indent=1)

    for g in gates:
        print("[%s] %-46s %s" % (g["gate"], g["name"], "FIRED" if g["fired"] else "DID NOT FIRE"))
        print("        needs: %s" % g["requirement"])
        print("        saw:   %s" % g["observed"])
        print("        so:    %s" % g["consequence"])
    print()
    print("VERDICT: %s" % verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)