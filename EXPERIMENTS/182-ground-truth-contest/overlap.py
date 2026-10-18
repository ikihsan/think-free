#!/usr/bin/env python3
"""E182 stage 4: the prescriptive-overlap instrument, calibrated on the 10
hand-read rows committed in AMENDMENT 1, then G2' on the other 50.

Reads no assistant answer and no arm label. Arm and verdict are joined only at
the reporting step, after every label is computed.

Usage: python3 overlap.py
"""
import html
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")

# The only judgement in this experiment. Committed in AMENDMENT 1 section 2
# and reproduced here verbatim so the calibration set cannot drift.
HAND_READ = {
    79824381: "differ", 79408101: "differ", 79537353: "same",
    79796450: "same",   79663905: "same",  79589468: "same",
    79791886: "differ", 79556333: "differ", 79843062: "differ",
    79600161: "same",
}

CODE_RE = re.compile(r"<code>(.*?)</code>", re.S)
CODE_TAG_RE = re.compile(r"</?code[^>]*>", re.S)
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
SNAKE_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)+$")
MIXED_RE = re.compile(r"^[A-Za-z_][a-z0-9]*[A-Z]")
DOT_RE = re.compile(r"\.")

# Words that are identifiers by shape and carry no prescription.
STOP = {
    "https", "http", "html", "python", "javascript", "typescript", "github",
    "stackoverflow", "httpsstackoverflow", "there", "which", "where", "would",
    "could", "should", "about", "using", "have", "been", "this", "that",
    "with", "from", "your", "you", "answer", "question", "example", "code",
}


def strip_html(text):
    text = CODE_TAG_RE.sub(" ", text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def prescriptive(text):
    """P(A): identifiers inside code spans, plus snake_case, mixedCase and
    dotted-path tokens elsewhere. Length >= 4."""
    body = text or ""
    in_code = set()
    for chunk in CODE_RE.findall(body):
        in_code.update(WORD_RE.findall(strip_html(chunk)))
    plain = strip_html(CODE_RE.sub(" ", body))
    out = set()
    for tok in WORD_RE.findall(plain):
        if len(tok) < 4 or tok.lower() in STOP:
            continue
        if (tok in in_code or SNAKE_RE.match(tok) or MIXED_RE.match(tok)
                or DOT_RE.search(tok)):
            out.add(tok)
    out.update(t for t in in_code if len(t) >= 4 and t.lower() not in STOP)
    return out


def fisher_exact_2x2(a, b, c, d):
    import math
    n = a + b + c + d
    if n == 0:
        return (None, None)
    r1, r2, c1 = a + b, c + d, a + c

    def logc(x, y):
        return (math.lgamma(r1 + 1) - math.lgamma(x + 1) - math.lgamma(y + 1)
                + math.lgamma(c1 + 1) - math.lgamma(a + 1) - math.lgamma(b + 1)
                + math.lgamma(c + 1) + math.lgamma(d + 1))

    def rt(x):
        return math.lgamma(x + 1) + math.lgamma(n - x + 1)

    obs = logc(a, b)
    tot = sum(math.exp(obs - rt(x) + rt(a))
              for x in range(max(0, c1 - r2), min(r1, c1) + 1))
    orr = (a * d) / float(b * c) if (b and c) else None
    return (min(1.0, tot), orr)


def wilson(k, n, z=1.959963985):
    import math
    if not n:
        return (None, None)
    p = k / float(n)
    den = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, ctr - half), min(1.0, ctr + half))


def main():
    bodies = json.load(open(os.path.join(HERE, "bodies.json")))
    states = {r["qid"]: r for r in json.load(
        open(os.path.join(HERE, "states.json")))["rows"]}

    labelled = []
    for q in bodies["qids"]:
        answers = bodies["rows"][str(q)]
        st = states[q]
        row = {"qid": q, "n_answers": len(answers),
               "top": st["top"], "runner_up": st["runner_up"]}
        # AMENDMENT 1 rule 4: only rows with >= 2 answers and a runner-up > 0
        if len(answers) < 2 or not answers[1].get("score") or answers[1]["score"] <= 0:
            row["eligible"] = False
            row["reason"] = ("single_answer" if len(answers) < 2
                             else "runner_up_not_positive")
            labelled.append(row)
            continue
        p0 = prescriptive(answers[0]["body"])
        p1 = prescriptive(answers[1]["body"])
        row["eligible"] = True
        row["n_p0"], row["n_p1"] = len(p0), len(p1)
        row["only_in_p1"] = sorted(p1 - p0)[:12]
        row["only_in_p0"] = sorted(p0 - p1)[:12]
        if not p1:
            row["overlap"] = None
            row["reason"] = "runner_up_no_prescriptive_tokens"
        else:
            row["overlap"] = round(len(p0 & p1) / float(len(p1)), 4)
        labelled.append(row)

    # ---- calibration: choose tau on the 10 hand-read rows only ----
    cal = [r for r in labelled if r["qid"] in HAND_READ
           and r.get("eligible") and r.get("overlap") is not None]
    for r in cal:
        r["truth"] = HAND_READ[r["qid"]]
    grid = [round(x / 100.0, 2) for x in range(5, 96)]

    def bal_acc(tau):
        tp = fp = tn = fn = 0
        for r in cal:
            pred = "differ" if r["overlap"] <= tau else "same"
            if r["truth"] == pred:
                tp += 1 if pred == "differ" else 0
                tn += 1 if pred == "same" else 0
            else:
                fp += 1 if pred == "differ" else 0
                fn += 1 if pred == "same" else 0
        pos, neg = tp + fn, tn + fp
        sens = tp / float(pos) if pos else 0.5
        spec = tn / float(neg) if neg else 0.5
        return (sens + spec) / 2.0, sens, spec, (tp, fp, tn, fn)

    scored = [(bal_acc(t)[0], t, bal_acc(t)) for t in grid]
    scored.sort(key=lambda x: (-x[0], x[1]))
    best_ba, tau, best = scored[0]
    accepted = best_ba >= 0.80
    for r in labelled:
        if r.get("eligible") and r.get("overlap") is not None:
            r["divergent"] = (r["overlap"] <= tau) if accepted else None

    # ---- G2' on the 50 non-calibration rows ----
    labels = {l["qid"]: l for l in json.load(
        open(os.path.join(E177, "labels.json")))["labels"]}
    verdicts = {}
    with open(os.path.join(E177, "score", "verdicts.jsonl")) as fh:
        for line in fh:
            if line.strip():
                v = json.loads(line)
                verdicts[v["pid"]] = v
    for r in labelled:
        q = r["qid"]
        r["arm"] = labels[q]["arm"]
        r["reached"] = verdicts["g-%d" % q]["same_resolution"] == "YES"
        r["calibration"] = q in HAND_READ

    def bucket(rs):
        return [r for r in rs if r.get("divergent") is not None
                and not r["calibration"]]

    em = bucket([r for r in labelled if r["arm"] == "EVID" and not r["reached"]])
    eh = bucket([r for r in labelled if r["arm"] == "EVID" and r["reached"]])
    sh = bucket([r for r in labelled if r["arm"] == "SELF" and r["reached"]])

    g2 = {"eligible_rows": len(bucket(labelled)), "tau": tau,
          "balanced_accuracy_on_calibration": round(best_ba, 4),
          "instrument_accepted": accepted}
    if accepted and em and eh:
        a = sum(1 for r in em if r["divergent"])
        b = len(em) - a
        c = sum(1 for r in eh if r["divergent"])
        d = len(eh) - c
        p, orr = fisher_exact_2x2(a, b, c, d)
        diff = a / float(len(em)) - c / float(len(eh))
        g2.update({"evid_missed": [a, len(em)], "evid_hit": [c, len(eh)],
                   "diff": round(diff, 4), "fisher_p": p, "odds_ratio": orr,
                   "fires": bool(p is not None and p < 0.05 and diff >= 0.20)})
        a2 = sum(1 for r in sh if r["divergent"])
        g2["self_hit"] = [a2, len(sh)]

    out = {"tau": tau, "instrument_accepted": accepted,
           "calibration": [{"qid": r["qid"], "overlap": r["overlap"],
                            "truth": HAND_READ[r["qid"]],
                            "n_p0": r["n_p0"], "n_p1": r["n_p1"]}
                           for r in cal],
           "gates": {"G5_repaired_instrument": g2},
           "rows": labelled}
    with open(os.path.join(HERE, "overlap.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")

    print("calibration on %d hand-read rows" % len(cal))
    miss = [q for q in HAND_READ if q not in {r["qid"] for r in cal}]
    if miss:
        print("  hand-read rows with no usable comparison: %s -> %s"
              % (miss, [(r.get("reason"), r["n_answers"], r["top"],
                         r["runner_up"]) for r in labelled
                        if r["qid"] in miss]))
    for r in sorted(cal, key=lambda r: r["overlap"]):
        print("  qid %d  overlap %.4f  (%d vs %d tokens)  truth %-6s -> %s"
              % (r["qid"], r["overlap"], r["n_p0"], r["n_p1"],
                 r["truth"], "differ" if r["overlap"] <= tau else "same"))
    ba, sens, spec, cm = best
    print("tau = %.2f, balanced accuracy %.4f (sens %.4f, spec %.4f, cm %s)"
          % (tau, ba, sens, spec, cm))
    print("instrument %s (bar balanced accuracy >= 0.80)"
          % ("ACCEPTED" if accepted else "REJECTED -- G2 is not_evaluated"))
    inelig = Counter(r.get("reason", "?") for r in labelled
                     if not r.get("eligible"))
    print("ineligible rows: %s" % dict(inelig))
    print()
    if g2.get("fisher_p") is not None:
        print("G2'  EVID missed %d/%d divergent vs EVID hit %d/%d"
              % (g2["evid_missed"][0], g2["evid_missed"][1],
                 g2["evid_hit"][0], g2["evid_hit"][1]))
        print("     diff %+0.4f  Fisher p %.6g  OR %s -> %s"
              % (g2["diff"], g2["fisher_p"],
                 ("%.4f" % g2["odds_ratio"]) if g2["odds_ratio"] else "n/a",
                 "FIRES" if g2["fires"] else "does not fire"))
        print("     reference SELF hit %d/%d = %.4f"
              % (g2["self_hit"][0], g2["self_hit"][1],
                 g2["self_hit"][0] / float(g2["self_hit"][1])))
    else:
        print("G2'  not evaluable: %s" % g2)
    return 0


if __name__ == "__main__":
    sys.exit(main())