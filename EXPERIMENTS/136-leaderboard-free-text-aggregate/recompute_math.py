#!/usr/bin/env python3
"""E136 G3: R1-style recomputation of the published MATH aggregate.

Primary cell (protocol selection rule): `math_chain_of_thought`, the HELM lite
v1.0.0 group that is BOTH free-text (chain-of-thought generation completions,
max_tokens=400) AND a multi-run aggregate (published as the mean over the
7 subject runs of model 01-ai/yi-34b).

R1 discipline, declared before the run bytes were read: this script recomputes
every verdict from `scenario_state.json` alone. It never reads a verdict
column: `stats.json` means and `per_instance_stats.json` are loaded only after
the recomputation, for comparison and reconciliation.

Scoring rule (declared in advance, calibrated against the harness's own
per-instance verdicts, reported per-instance):
  gold  = content of the LAST \\boxed{...} in the correct reference
  pred  = content of the LAST \\boxed{...} in the completion;
          a completion with no \\boxed scores 0 (the harness's verdicts on
          such rows are checked explicitly and reported)
  verdict = 1.0 iff normalize(pred) == normalize(gold) exactly, else 0.0
"""
import glob
import json
import os
import re

D = "/tmp/opencode/e136"
HERE = os.path.dirname(os.path.abspath(__file__))

SUBJECTS = [
    "algebra", "counting_and_probability", "geometry", "intermediate_algebra",
    "number_theory", "prealgebra", "precalculus",
]

BOXED = "\\boxed{"


def boxed_all(text):
    """All \\boxed{...} contents, balanced-brace aware, in order."""
    out = []
    i = 0
    while True:
        j = text.find(BOXED, i)
        if j < 0:
            break
        k = j + len(BOXED)
        depth = 1
        start = k
        while depth > 0 and k < len(text):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        out.append(text[start:k - 1])
        i = k
    return out


def normalize(s):
    """Normalize a MATH answer to a comparable form (no sympy on this VM).

    Calibrated against the harness's own per-instance verdicts (see
    RESULT.md): the harness's operator is normalized-string equality, NOT
    numeric equivalence — 3/2 and 1.5 score 0, and 7/12 vs 35/60 scores 0.
    """
    s = s.strip()
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    s = s.replace("\\cfrac", "\\frac")
    s = s.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\[,;! ]", "", s)
    s = s.replace("~", "").replace("$", "")
    s = re.sub(r"\\(?:mbox|text)\{([^{}]*)\}", r"\1", s)
    s = s.replace("^{\\circ}", "").replace("^\\circ", "")
    s = s.replace("\\circ", "").replace("\\degree", "")
    s = s.replace("\\%", "").replace("%", "")
    s = s.replace("\\infty", "inf").replace("infinity", "inf")
    s = s.replace("\\cdot", "*").replace("\\times", "*")

    # brace-less \frac14 -> \frac{1}{4} first (single-token args)
    s = re.sub(r"\\frac([0-9A-Za-z])([0-9A-Za-z])", r"\\frac{\1}{\2}", s)

    # \frac{a}{b} -> ((a)/(b)) recursively, innermost first
    def frac_sub(m):
        return "((" + m.group(1) + ")/(" + m.group(2) + "))"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac_sub, s)

    # \sqrt[n]{a} -> ((a)**(1/(n))) ; \sqrt{a} -> sqrt(a)
    def sqrt_sub(m):
        if m.group(1):
            return "(( " + m.group(2) + " )**(1/(" + m.group(1) + ")))"
        return "sqrt(" + m.group(2) + ")"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\sqrt(?:\[([^{}]*)\])?\{([^{}]*)\}", sqrt_sub, s)

    # \begin{pmatrix}...\end{pmatrix} -> | ... |
    s = re.sub(r"\\begin\{[a-zA-Z*]+\}", "", s)
    s = re.sub(r"\\end\{[a-zA-Z*]+\}", "", s)
    s = s.replace("\\\\", "&").replace("\\\\", "&")
    s = s.replace("\\", "")
    s = s.replace("^", "**")
    s = s.replace("{,}", ",")          # thousand separator {,} in 1{,}000
    s = re.sub(r"\s+", "", s)
    s = s.strip().rstrip(".").rstrip(",")
    if s.endswith("."):
        s = s[:-1]
    return s


def safe_eval(s):
    """Numeric value of a normalized answer, or None if not evaluable."""
    if not s:
        return None
    s = s.replace("inf", "float('inf')")
    allowed = set("0123456789+-*/().,& ")
    if not set(s) <= allowed:
        return None
    s2 = s.replace("&", ",")           # matrix row separator -> tuple-ish; give up
    if "," in s2:
        return None
    s2 = s2.replace("sqrt", "SQRT")    # sqrt not numeric-evaluable here
    if "SQRT" in s2:
        return None
    try:
        v = eval(s2, {"__builtins__": {}}, {})
        return float(v)
    except Exception:
        return None


def equiv(pred, gold):
    """1.0 iff normalize(pred) == normalize(gold) exactly.

    The harness's operator is normalized-string equality, not numeric
    equivalence: its own verdicts score 3/2 vs 1.5 and 7/12 vs 35/60 as
    NOT equivalent (RESULT.md calibration table)."""
    return normalize(pred) == normalize(gold)


def load_run(subject):
    tag = ("math__math:subject=%s,level=1,use_official_examples=False,"
           "use_chain_of_thought=True" % subject)
    ss = json.load(open(os.path.join(D, tag + "__scenario_state.json")))
    stats = json.load(open(os.path.join(D, tag + "__stats.json")))
    pis = json.load(open(os.path.join(D, "pis_math_%s.json" % subject)))
    return ss, stats, pis


def main():
    per_subject = {}
    total_rows = 0
    total_recomputed_hits = 0
    total_verdict_agree = 0
    nobox_verdicts = []

    for subj in SUBJECTS:
        ss, stats, pis = load_run(subj)
        states = ss["request_states"]

        # harness's own per-instance verdicts (loaded only for reconciliation)
        harness_verdicts = {}
        for p in pis:
            for st in p["stats"]:
                nm = st["name"]
                if nm["name"] == "math_equiv_chain_of_thought":
                    harness_verdicts[p["instance_id"]] = st["mean"]

        # harness's own printed run mean (the run's verdict column aggregate)
        printed = None
        for st in stats:
            nm = st["name"]
            if nm["name"] == "math_equiv_chain_of_thought" and nm.get("split") == "test" \
               and "perturbation" not in nm:
                printed = st["mean"]

        n = 0
        hits = 0
        agree = 0
        for rs in states:
            inst = rs["instance"]
            refs = [r for r in inst["references"] if "correct" in r.get("tags", [])]
            gold_b = boxed_all(refs[0]["output"]["text"]) if refs else []
            comp = rs["result"]["completions"][0]["text"]
            pred_b = boxed_all(comp)

            gold = gold_b[-1] if gold_b else None
            pred = pred_b[-1] if pred_b else None
            if pred is None:
                nobox_verdicts.append((subj, inst["id"], harness_verdicts.get(inst["id"])))
            v = equiv(pred, gold) if gold is not None and pred is not None else False
            hv = harness_verdicts.get(inst["id"])
            if hv is not None and (hv == 1.0) == v:
                agree += 1
            n += 1
            hits += 1 if v else 0

        mean = hits / n
        per_subject[subj] = mean
        total_rows += n
        total_recomputed_hits += hits
        total_verdict_agree += agree
        print(f"{subj:<22} recomputed {hits:>3}/{n:<3} = {mean!r:<20} "
              f"printed {printed!r:<20} match={mean == printed!r} "
              f"row-agree {agree}/{n}")

    macro = sum(per_subject.values()) / len(per_subject)
    micro = total_recomputed_hits / total_rows
    published = 0.37478395850488877

    print()
    print(f"rows recomputed            : {total_rows}")
    print(f"row-level verdict agreement: {total_verdict_agree}/{total_rows}")
    print(f"RECOMPUTED macro (mean of 7 subject means): {macro!r}")
    print(f"RECOMPUTED micro (pooled {total_rows} rows)        : {micro!r}")
    print(f"PUBLISHED group value                      : {published!r}")
    print(f"macro == published (full precision)        : {macro == published}")
    print(f"diff macro-published                       : {abs(macro-published)}")

    nb = nobox_verdicts
    nb_harness1 = sum(1 for _, _, hv in nb if hv == 1.0)
    print()
    print(f"no-boxed completions       : {len(nb)} "
          f"(harness scored {nb_harness1} of them 1.0)")

    out = {
        "per_subject_recomputed": per_subject,
        "rows": total_rows,
        "hits": total_recomputed_hits,
        "row_verdict_agreement": total_verdict_agree,
        "macro": macro,
        "micro": micro,
        "published": published,
        "nobox_count": len(nb),
        "nobox_harness_scored_1": nb_harness1,
    }
    with open(os.path.join(HERE, "recompute_math_out.json"), "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
